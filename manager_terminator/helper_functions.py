# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

from more_itertools import one

from manager_terminator.autogenerated_graphql_client import (
    GetEngagementObjectsEngagementsObjectsObjectsEmployee,
)
from manager_terminator.autogenerated_graphql_client import (
    GetEngagementObjectsEngagementsObjectsObjectsOrgUnit,
)


def check_for_end_date(
    org_unit_from_engagement_objects: list[
        GetEngagementObjectsEngagementsObjectsObjectsOrgUnit
    ],
    employee_from_engagement_objects: list[
        GetEngagementObjectsEngagementsObjectsObjectsEmployee
    ],
) -> bool:
    """
    Helper function for checking whether the persons engagement(s) has an end date.

    Args:
        org_unit_from_engagement_objects: A list of the engagement objects organisation unit models.
        employee_from_engagement_objects: A list of the engagement objects employee models.


    Returns:
        True if at least one of the persons engagements has an end date.
        False if none of the persons engagements does not have an end date.

    Example:
        "True"
    """
    engagements_org_unit_uuid = one(org_unit_from_engagement_objects).uuid
    engagements = one(employee_from_engagement_objects).engagements

    return any(
        engagement.validity.to
        for engagement in engagements
        if engagement.validity.to is not None
        and one(engagement.org_unit).uuid == engagements_org_unit_uuid
    )


def get_manager_uuid_and_manager_end_date_if_in_same_org_unit(
    employee_from_engagement_objects: list[
        GetEngagementObjectsEngagementsObjectsObjectsEmployee
    ],
    org_unit_from_engagement_objects: list[
        GetEngagementObjectsEngagementsObjectsObjectsOrgUnit
    ],
) -> tuple[UUID, datetime | None] | None:
    """
    Helper function for checking whether the manager role is in the
    same org unit as the engagement exists. Will retrieve the manager
    uuid and the managers end date if the manager role and engagement
    exists in the same org unit.

    Args:
        employee_from_engagement_objects: A list of the engagement objects employee models.
        org_unit_from_engagement_objects: A list of the engagement objects organisation unit models.

    Returns:
        The managers uuid, and the managers end date:
         If the manager role is in the same org unit as the engagement
         being created/updated/terminated.

         Or None, if the manager role is not in the same org unit as
         the engagement being created/updated/terminated.

    Example:
        ("02be2d6a-e540-4f53-8b09-1fc2589ea98b", "2015-07-11T00:00:00+02:00")
    """
    manager_roles = one(employee_from_engagement_objects).manager_roles
    engagement_org_unit_uuid = one(org_unit_from_engagement_objects).uuid

    for manager in manager_roles:
        # Checking for a match on engagements org unit uuid and the manager roles org unit uuid.
        manager_org_unit_uuid = one(manager.org_unit).uuid
        manager_end_date = manager.validity.to

        # If this is the correct org unit, and the manager role either does not have an end date,
        # or the manager role end date exceeds the engagements end date.
        if manager_org_unit_uuid == engagement_org_unit_uuid:
            return manager.uuid, manager_end_date

    # Manager role may not be in same org unit as the engagement.
    return None


def get_latest_end_date_from_engagement_objects(
    employee_from_engagement_objects: list[
        GetEngagementObjectsEngagementsObjectsObjectsEmployee
    ],
    manager_end_date: datetime,
) -> datetime | None:
    """
    Helper function for setting the farthest date to the end date of the
    engagement if the manager roles end date exceeds that of the engagement.

    If the manager roles end date arrives before the engagement end date, return None.

    Args:
        employee_from_engagement_objects: A list of the engagement objects employee models.
        manager_end_date: The managers end date.

    Returns:
        An engagement end date in string format, if the manager role either
        does not have an end date, or the manager roles end date exceeds that
        of the engagement.

        None, if the manager roles end date arrives before the engagements
        end date.

    Example:
        "2023-09-07 00:00:00+02:00"
    """
    list_of_engagements = one(employee_from_engagement_objects).engagements

    for engagement in list_of_engagements:
        engagement_end_date = engagement.validity.to

        # We may assume this is always present, or we would have hit an earlier exit of the event.
        farthest_date = None

        # If the manager role end date does not exist or exceeds the engagements end date.
        if manager_end_date is None or engagement_end_date < manager_end_date:
            # Set the farthest date to the engagements end date.
            farthest_date = engagement_end_date

        return farthest_date or None

    return None
