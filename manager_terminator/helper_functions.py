# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime


def check_for_end_date(engagement_objects: dict) -> bool:
    """
    Helper function for checking whether the persons engagement(s) has an end date.

    Args:
        engagement_objects: A dict of engagement objects.


    Returns:
        True if the persons engagement has an end date.
        False if the persons engagement does not have an end date.

    Example:
        "True"
    """
    return any(
        engagement.get("validity").get("to")
        for engagement in engagement_objects.get("engagements")  # type: ignore
        if engagement.get("validity").get("to") is not None
        and engagement.get("org_unit")[0].get("uuid")
        == engagement_objects.get("manager_roles")[0]  # type: ignore
        .get("org_unit")[0]
        .get("uuid")
    )


def get_end_date_in_manager_object(engagement_objects: dict) -> str | None:
    """
    Helper function for checking whether the manager role has an end date or no end date
    in the same org unit as the engagement exists.

    Args:
        engagement_objects: A dict of engagement objects.

    Returns:
        The managers uuid, either:
         If the manager role does not have an end date, and
         is in the same org unit as the engagement that was created/updated/terminated.

         If the manager role does have an end date, and is in
         the same org unit as the engagement that was created/updated/terminated.

        Or None, if conditions are not met.

    Example:
        "02be2d6a-e540-4f53-8b09-1fc2589ea98b"
    """
    manager_roles = engagement_objects.get("manager_roles")
    engagements = engagement_objects.get("engagements")
    assert manager_roles and engagements is not None
    for manager in manager_roles:
        # Manager has no end date. Get the manager uuid.
        manager_org_unit_uuid = manager.get("org_unit")[0].get("uuid")
        if manager.get("validity").get("to") is None and any(
            engagement.get("org_unit")[0].get("uuid") == manager_org_unit_uuid
            for engagement in engagements
        ):
            return manager.get("uuid")

        # Manager has an end date. Get the manager uuid.
        if manager.get("validity").get("to") is not None and any(
            engagement.get("org_unit")[0].get("uuid") == manager_org_unit_uuid
            for engagement in engagements
        ):
            return manager.get("uuid")

    return None


def get_latest_engagement_date_and_check_for_same_org_unit(
    engagement_objects: dict,
) -> str | None:
    """
    Helper function for retrieving the farthest end date of an engagement
    if there is an end date for the engagement, and if the manager role
    and the engagement exists in the same org unit.

    If the manager roles end date arrives before the farthest engagement
    end date, return None.

    Args:
        engagement_objects: A dict of engagement objects.

    Returns:
        An engagement end date in string format, if the manager role either
        does not have an end date, or the manager roles end date exceeds the
        farthest engagement end date.

        None, if the manager roles end date arrives before the engagements
        end date.

    Example:
        "2023-10-23"
    """
    engagements = engagement_objects["engagements"]
    manager_roles = engagement_objects["manager_roles"]

    farthest_date = None

    for engagement in engagements:
        # To ensure we are retrieving the correct engagement in the correct org unit.
        engagement_org_unit_uuid = engagement.get("org_unit")[0].get("uuid")

        # We may assume this is always present, or we would have hit an earlier exit of the event.
        engagement_to_date = datetime.strptime(
            engagement.get("validity").get("to"), "%Y-%m-%dT%H:%M:%S%z"
        ).date()

        for manager in manager_roles:
            # To ensure we are retrieving the correct manager role in the correct org unit.
            manager_org_unit_uuid = manager.get("org_unit")[0].get("uuid")
            manager_to_date = manager.get("validity").get("to")

            # If this is the correct org unit, and the manager role either does not have an end date,
            # or the manager role end date exceeds the engagements end date.
            if manager_org_unit_uuid == engagement_org_unit_uuid and (
                manager_to_date is None
                or engagement_to_date
                < datetime.strptime(manager_to_date, "%Y-%m-%dT%H:%M:%S%z").date()
            ):  # Set the farthest date to the engagements end date.
                farthest_date = engagement_to_date

    return farthest_date.strftime("%Y-%m-%d") if farthest_date else None
