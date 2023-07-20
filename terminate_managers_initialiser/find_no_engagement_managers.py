# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
def extract_managers_with_no_persons_or_engagements(
    manager_objects: list,
) -> list | None:
    """
    Function for pulling UUID(s) out on all manager roles, that either does
    not have a person, or an engagement associated to it.

    Args:
        manager_objects: A current list of manager objects

    Returns:
        A list of UUID(s) on all manager roles with no person or engagement.
        Or None, if no empty manager roles are found.

    Example:
        "['411c1d60-131e-4adb-b268-c1f1b8bcd275',
        '592e3fe1-5ef4-4044-924c-032df2be2ec5',
        'b969cc12-c45c-41b3-8043-e5181eb40617']"
    """
    manager_uuids = [
        manager["objects"][0]["uuid"]
        for manager in manager_objects
        if manager["objects"][0]["employee"] is None
        or len(manager["objects"][0]["employee"][0]["engagements"]) == 0
    ]
    return manager_uuids or None
