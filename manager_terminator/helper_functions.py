# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

from more_itertools import one


def check_for_end_date(engagement_objects: dict) -> bool:
    """
    Helper function for checking whether the persons engagement(s) has an end date.

    Args:
        engagement_objects: A dict of engagement objects.


    Returns:
        True if at least one of the persons engagements has an end date.
        False if none of the persons engagements does not have an end date.

    Example:
        "True"
    """
    engagements_org_unit_uuid = one(engagement_objects["org_unit"])["uuid"]
    engagements = one(engagement_objects.get("employee")).get("engagements")

    return any(
        engagement.get("validity").get("to")
        for engagement in engagements
        if engagement.get("validity").get("to") is not None
        and one(engagement.get("org_unit")).get("uuid") == engagements_org_unit_uuid
    )


def get_manager_uuid_if_engagement_is_in_same_org_unit(
    engagement_objects: dict,
) -> UUID | None:
    """
    Helper function for checking whether the manager role is in the
    same org unit as the engagement exists.

    Args:
        engagement_objects: A dict of engagement objects.

    Returns:
        The managers uuid, either:
         If the manager role is in the same org unit as the engagement
         being created/updated/terminated.

         Or None, if the manager role is not in the same org unit as
         the engagement being created/updated/terminated.

    Example:
        "02be2d6a-e540-4f53-8b09-1fc2589ea98b"
    """
    manager_roles = one(engagement_objects.get("employee")).get("manager_roles")
    engagement_org_unit_uuid = one(engagement_objects.get("org_unit")).get("uuid")

    for manager in manager_roles:
        manager_org_unit_uuid = one(manager.get("org_unit")).get("uuid")

        # Checking for a match on engagements org unit uuid and the manager roles org unit uuid.
        if manager_org_unit_uuid == engagement_org_unit_uuid:
            return manager.get("uuid")

    # Manager role may not be in same org unit as the engagement.
    return None


def get_latest_end_date_and_ensure_same_org_unit(
    engagement_objects: dict,
) -> str | None:
    """
    Helper function for setting the farthest date to the end date of the
    engagement, if the manager role and the engagement exists in the same
    org unit, and if the manager roles end date exceeds that of the engagement.

    If the manager roles end date arrives before the engagement end date, return None.

    Args:
        engagement_objects: A dict of engagement objects.

    Returns:
        An engagement end date in string format, if the manager role either
        does not have an end date, or the manager roles end date exceeds that
        of the engagement.

        None, if the manager roles end date arrives before the engagements
        end date.

    Example:
        "2023-10-23"
    """
    engagement_org_unit_uuid = one(engagement_objects.get("org_unit")).get("uuid")
    manager_roles = one(engagement_objects.get("employee")).get("manager_roles")
    engagement_end_date = engagement_objects.get("validity").get("to")

    assert engagement_org_unit_uuid and manager_roles is not None

    # We may assume this is always present, or we would have hit an earlier exit of the event.
    engagement_end_date_parsed = datetime.strptime(
        engagement_end_date, "%Y-%m-%dT%H:%M:%S%z"
    ).date()

    farthest_date = None

    for manager in manager_roles:
        # To ensure we are retrieving the correct manager role in the correct org unit.
        manager_org_unit_uuid = one(manager.get("org_unit")).get("uuid")
        manager_end_date = manager.get("validity").get("to")

        # If this is the correct org unit, and the manager role either does not have an end date,
        # or the manager role end date exceeds the engagements end date.
        if manager_org_unit_uuid == engagement_org_unit_uuid and (
            manager_end_date is None
            or engagement_end_date_parsed
            < datetime.strptime(manager_end_date, "%Y-%m-%dT%H:%M:%S%z").date()
        ):  # Set the farthest date to the engagements end date.
            farthest_date = engagement_end_date_parsed

    return farthest_date.strftime("%Y-%m-%d") if farthest_date else None
