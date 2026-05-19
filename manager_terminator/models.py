# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel


class InvalidManagerPeriod(BaseModel):
    uuid: UUID
    from_: datetime.datetime
    to: datetime.datetime


class ManagerState(IntEnum):
    """Represents what state the manager is in at a specific point in time."""

    NOT_SET = 0
    VACANT = 1
    SET = 2
