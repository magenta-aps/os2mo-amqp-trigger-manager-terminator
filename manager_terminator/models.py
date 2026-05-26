# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from datetime import tzinfo
from enum import IntEnum
from itertools import pairwise
from typing import Any
from typing import Generic
from typing import TypeVar
from uuid import UUID

import structlog
from more_itertools import collapse
from more_itertools import first
from more_itertools import last
from more_itertools import only
from more_itertools import split_when
from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator
from pydantic.generics import GenericModel

from manager_terminator.exceptions import NoValueError

logger = structlog.stdlib.get_logger()

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f (%Z)"

V = TypeVar("V")


class InvalidManagerPeriod(BaseModel):
    uuid: UUID
    from_: datetime
    to: datetime


# Copied from: https://git.magenta.dk/rammearkitektur/os2mo-sdtool-plus/-/blob/918492e69de0a093bb96c5e825235c4017cc7aa7/sdtoolplus/models.py#L184
class Interval(GenericModel, Generic[V]):
    """
    Interval conventions:
    1) 'start' is included in the interval, but 'end' is not
    2) Infinity will correspond to datetime.max and minus infinity will
       correspond to datetime.min
    3) Timezones must be included
    """

    start: datetime
    end: datetime
    value: V

    class Config:
        allow_mutation = False

    @root_validator
    def ensure_timezones(cls, values: dict[str, Any]) -> dict[str, Any]:
        start = values["start"]
        end = values["end"]
        # both datetime.UTC and zoneinfo.ZoneInfo are different types (because
        # of Python jank) but they both inherit from tzinfo, so this should find
        # both kinds of timezones
        if not (isinstance(start.tzinfo, tzinfo) and isinstance(end.tzinfo, tzinfo)):
            logger.error("invalid timezone", start=start, end=end)
            raise ValueError("Timezone must be provided")
        return values

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"start={self.start.strftime(DATETIME_FORMAT)}, "
            f"end={self.end.strftime(DATETIME_FORMAT)}, "
            f"value={str(self.value)})"
        )


T = TypeVar("T", bound=Interval)


class Active(Interval[bool]):
    pass


class ManagerStatus(IntEnum):
    VACANT = 1
    ACTIVE = 2


class ManagerValue(BaseModel):
    uuid: UUID
    status: ManagerStatus


class Manager(Interval[ManagerValue]):
    pass


# Copied from: https://git.magenta.dk/rammearkitektur/os2mo-sdtool-plus/-/blob/918492e69de0a093bb96c5e825235c4017cc7aa7/sdtoolplus/models.py#L301
class Timeline(GenericModel, Generic[T]):
    intervals: tuple[T, ...] = tuple()

    class Config:
        allow_mutation = False

    @validator("intervals")
    def entities_must_be_same_type(cls, v):
        if len(v) == 0:
            return v
        if not all(isinstance(entity, type(first(v))) for entity in v):
            raise ValueError("Entities must be of the same type")
        return v

    @validator("intervals")
    def entities_must_be_intervals(cls, v):
        if not all(isinstance(e, Interval) for e in v):
            raise ValueError("Entities must be intervals")
        return v

    @validator("intervals")
    def intervals_must_be_sorted(cls, v):
        starts = [i.start for i in v]
        starts_sorted = sorted(starts)
        if not starts == starts_sorted:
            raise ValueError("Entities must be sorted")
        return v

    @validator("intervals")
    def intervals_cannot_overlap(cls, v):
        if not all(i1.end <= i2.start for i1, i2 in pairwise(v)):
            raise ValueError("Intervals cannot overlap")
        return v

    @validator("intervals")
    def successively_repeated_interval_values_not_allowed(cls, v):
        non_hole_interval_pairs = (
            (i1, i2) for i1, i2 in pairwise(v) if i1.end == i2.start
        )
        if not all(i1.value != i2.value for i1, i2 in non_hole_interval_pairs):
            raise ValueError("Successively repeated interval values are not allowed")
        return v

    def entity_at(self, timestamp: datetime) -> T:
        entity = only(e for e in self.intervals if e.start <= timestamp < e.end)
        if entity is None:
            raise NoValueError(
                f"No value found at {timestamp.strftime(DATETIME_FORMAT)}"
            )
        return entity

    def get_interval_endpoints(self) -> set[datetime]:
        return set(collapse((i.start, i.end) for i in self.intervals))

    def has_holes(self) -> bool:
        """
        Check if there are holes in the timeline.

        Returns:
            True if there are holes in the timeline and False if not.
        """
        return not all(i1.end == i2.start for i1, i2 in pairwise(self.intervals))


# Copied from: https://git.magenta.dk/rammearkitektur/os2mo-sdtool-plus/-/blob/918492e69de0a093bb96c5e825235c4017cc7aa7/sdtoolplus/models.py#L279
def combine_intervals(intervals: tuple[T, ...]) -> tuple[T, ...]:
    """
    Combine adjacent interval entities with same values.

    Example:
        |-------- v1 --------|----- v1 ------|------ v2 ------|
        |---------------- v1 ----------------|------ v2 ------|

    Args:
        intervals: The interval entities to combine.

    Returns:
        Tuple of combined interval entities.
    """
    interval_groups = split_when(
        intervals, lambda i1, i2: i1.end < i2.start or i1.value != i2.value
    )
    return tuple(
        first(group).copy(update={"end": last(group).end}) for group in interval_groups
    )


def merge_overlapping_intervals(intervals: tuple[T, ...]) -> tuple[T, ...]:
    """
    Merge intervals with overlapping timestamps, by picking one of them arbitrarily.

    Intervals must be sorted by start time. For each overlap, the
    earlier-starting interval keeps its range, and the later interval's start
    is moved forward to the earlier interval's end. Intervals that become
    fully consumed (zero or negative length) are dropped.

    Example:
    ```
        |---v1---|
             |------v2----|

        |---v1---|---v2---|
    ```
    """
    if not all(i1.start <= i2.start for i1, i2 in pairwise(intervals)):
        raise ValueError("intervals must be sorted by start time")

    merged: list[T] = []
    for interval in intervals:
        if not merged:
            merged.append(interval)
            continue
        previous = last(merged)
        # `previous` has the latest end of anything in `merged`, since `merged`
        # is non-overlapping and sorted by start. So it's the only entry the
        # current `interval` can overlap with.
        if interval.end <= previous.end:
            # fully consumed by `previous` (zero/negative length after trimming)
            continue
        new_start = max(interval.start, previous.end)
        if new_start == interval.start:
            merged.append(interval)
        else:
            merged.append(interval.copy(update={"start": new_start}))

    # after merging, there might now be adjacent identical intervals that have
    # to be combined
    return combine_intervals(tuple(merged))
