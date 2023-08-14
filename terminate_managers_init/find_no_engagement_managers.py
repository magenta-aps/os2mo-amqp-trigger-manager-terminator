# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime

from more_itertools import one


def extract_managers_with_no_persons_or_engagements(
    manager_objects: list,
) -> list[dict[str, str]]:
    """
    Function for pulling UUID(s) out on all manager roles, that does
    not have a person, or an engagement associated to it.

    Args:
        manager_objects: A current list of manager objects

    Returns:
        A list of dict with:
         UUID(s) on all manager roles with no person or engagement.
         Dates on the managers farthest engagement end date.
    Example:
        "[{'uuid': '083de7f8-d52f-456d-a351-44075cbc0ca5', 'termination_date': '2023-08-11'},
        {'uuid': '21926ae9-5479-469a-97ae-3a996a7b3a01', 'termination_date': '2023-07-26'}]"
    """
    termination_objects = []

    for manager in manager_objects:
        # TODO use with "one" when graphql models are made.
        manager_org_unit_uuid = manager["objects"][0].get("org_unit")[0].get("uuid")
        manager_uuid = manager["objects"][0].get("uuid")

        # Managers engagement details
        employee_data = manager["objects"][0].get("employee")

        # If "employee": None or the "employee": [{"engagements": []}]
        if employee_data is None or all(
            len(e.get("engagements")) == 0 for e in employee_data
        ):
            # Use today, if no person or engagements are found.
            termination_objects.append(
                {
                    "uuid": manager_uuid,
                    "termination_date": datetime.date.today().isoformat(),
                }
            )

        farthest_to_date = None

        if employee_data:
            for employee in employee_data:
                engagements = employee.get("engagements")
                for engagement in engagements:
                    engagement_org_unit_uuid = one(engagement.get("org_unit")).get(
                        "uuid"
                    )
                    engagement_validity_to = engagement.get("validity").get("to")
                    if (  # If there's a match and engagement has an end date.
                        engagement_org_unit_uuid == manager_org_unit_uuid
                    ) and engagement_validity_to:
                        if (
                            farthest_to_date is None
                            or datetime.datetime.strptime(
                                engagement_validity_to, "%Y-%m-%dT%H:%M:%S%z"
                            ).date()
                            > datetime.datetime.strptime(
                                farthest_to_date, "%Y-%m-%dT%H:%M:%S%z"
                            ).date()
                        ):
                            # Assign the engagements end date to the farthest date.
                            farthest_to_date = engagement_validity_to

                        termination_objects.append(
                            {
                                "uuid": manager_uuid,
                                "termination_date": datetime.datetime.fromisoformat(
                                    farthest_to_date
                                ).strftime("%Y-%m-%d"),
                            }
                        )

    return termination_objects
