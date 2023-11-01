# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
import json
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder

from manager_terminator.autogenerated_graphql_client.client import GraphQLClient
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjects,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjects,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsPersonEngagementsValidity,
)
from manager_terminator.models import InvalidManagerPeriod
from manager_terminator.utils import POSITIVE_INFINITY


logger = structlog.get_logger(__name__)


async def get(mo: GraphQLClient) -> list[GetManagersManagersObjects]:
    """Fetches all manager objects from MO using GraphQL.

    Note: The GraphQL query fetches "objects" and not "current", since we want to examine
    all manager objects, even if they are not currently active.
    """

    gql_response = await mo.get_managers()
    return gql_response.objects


async def get_by_employee_uuids(
    mo: GraphQLClient, employee_uuids: list[UUID]
) -> list[GetManagersManagersObjects]:
    gql_response = await mo.get_employee_managers(employee_uuids)
    return gql_response.objects


async def invalid_manager_periods(
    managers: list[GetManagersManagersObjects],
) -> list[InvalidManagerPeriod]:
    """Goes through a list of managers and returns periods, if any, where the manager is invalid.

    An invalid manager period, is a period where the manager validity is ACTIVE,
    but the related manager-employee does not have an ACTIVE engagement for
    the manager org_unit in the same period.

    ```
    Initial:
                ===================================================
    -----   ----------                ------------------         --------           ------------
                -----------
    Invalid periods:

                            |INVALID|                  |INVALID|
                ============         ==================         ===
    -----   ----------               ------------------         --------           ------------
                 -----------
    ```
    """

    def engagement_belongs_to_manager_org_unit(engagement, manager_obj):
        """Checks if an engagement belongs to the same org_unit as the manager.

        Args:
            engagement: An engagement object.
            manager_obj: A manager object.

        Returns:
            True if the engagement belongs to the same org_unit as the manager.
        """
        eng_org_unit_uuids = {ou.uuid for ou in engagement.org_unit}
        manager_org_unit_uuids = {ou.uuid for ou in manager_obj.org_unit}
        return bool(
            eng_org_unit_uuids & manager_org_unit_uuids
        )  # returns True if there's an intersection

    all_invalid_periods = []
    for manager in managers:
        for manager_obj in manager.objects:
            valid_manager_employee_engagements = filter(
                lambda engagement: engagement_belongs_to_manager_org_unit(
                    engagement, manager_obj
                ),
                [
                    engagement
                    for manager_employee in manager_obj.person or []
                    for engagement in manager_employee.engagements or []
                ],
            )

            valid_engagement_validities = [
                engagement.validity for engagement in valid_manager_employee_engagements
            ]

            all_invalid_periods.extend(
                _find_gaps(manager_obj, valid_engagement_validities)
            )

    return all_invalid_periods


async def terminate_manager_periods(
    mo: GraphQLClient, periods: list[InvalidManagerPeriod]
) -> list[InvalidManagerPeriod]:
    terminated_manager_periods = []
    for period in periods:
        terminate_args = {
            "uuid": period.uuid,
            "terminate_from": period.from_.date(),
            "terminate_to": period.to.date(),
        }

        if period.to is POSITIVE_INFINITY:
            terminate_args["terminate_from"] = None
            terminate_args["terminate_to"] = (
                period.from_ - datetime.timedelta(days=1)
            ).date()

        try:
            terminated_manager_periods.append(
                await mo.terminate_manager(**terminate_args)
            )
        except Exception as e:
            logger.error(
                "Failed to terminate invalid manager period: %s"
                % json.dumps(jsonable_encoder(period))
            )
            raise e

    return terminated_manager_periods


# Helper methods for this module


def _find_gaps(
    manager: GetManagersManagersObjectsObjects,
    engagement_validities: list[
        GetManagersManagersObjectsObjectsPersonEngagementsValidity
    ],
) -> list[InvalidManagerPeriod]:
    engagement_validities = sorted(engagement_validities, key=lambda x: x.from_)
    manager_end_date = manager.validity.to or POSITIVE_INFINITY

    # If there are no engagement_validities for the manager, then the entire manager validity is invalid
    if len(engagement_validities) < 1:
        return [
            InvalidManagerPeriod(
                uuid=manager.uuid,
                from_=manager.validity.from_,
                to=manager_end_date,
            )
        ]

    gaps = []

    # Check for the gap before the first period
    if manager.validity.from_ < engagement_validities[0].from_:
        gap_end_date = engagement_validities[0].from_ - datetime.timedelta(days=1)
        gaps.append(
            InvalidManagerPeriod(
                uuid=manager.uuid,
                from_=manager.validity.from_,
                to=min(
                    gap_end_date, manager_end_date
                ),  # Ensure the gap doesn't exceed the object's end date
            )
        )

    # Check for gaps between periods
    for i in range(len(engagement_validities) - 1):
        # If current period has no end date, then there won't be any more gaps
        if engagement_validities[i].to is None:
            continue

        next_start_date = engagement_validities[i + 1].from_
        current_end_date = engagement_validities[i].to

        # Check for a gap
        if current_end_date < next_start_date:
            invalid_from = current_end_date + datetime.timedelta(days=1)
            invalid_to = next_start_date - datetime.timedelta(days=1)
            if invalid_to < invalid_from:
                # OBS: This occures on tailing-engagements, where the next engagement starts the same day as the previous ends
                continue

            gaps.append(
                InvalidManagerPeriod(
                    uuid=manager.uuid,
                    from_=invalid_from,
                    to=invalid_to,
                )
            )

    # Check for the gap after the last period, only if last period has an end date
    last_period_end_date = engagement_validities[-1].to
    if last_period_end_date and last_period_end_date < manager_end_date:
        gaps.append(
            InvalidManagerPeriod(
                uuid=manager.uuid,
                from_=last_period_end_date + datetime.timedelta(days=1),
                to=manager_end_date,
            )
        )

    # Only return gaps that are within the manager's validity
    invalid_manager_gaps = [
        gap
        for gap in gaps
        if gap.from_ <= manager_end_date
        and (gap.to is None or gap.to >= manager.validity.from_)
    ]

    return invalid_manager_gaps
