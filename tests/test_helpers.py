# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import pytest

from manager_terminator.helper_functions import check_for_end_date
from manager_terminator.helper_functions import (
    get_latest_end_date_and_ensure_same_org_unit,
)
from manager_terminator.helper_functions import (
    get_manager_uuid_if_engagement_is_in_same_org_unit,
)

engagement_no_end_date_and_same_org_unit = {
    "org_unit": [
        {"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539", "name": "IT-Support"}
    ],
    "validity": {"from": "2023-07-18T00:00:00+02:00", "to": None},
    "employee": [
        {
            "uuid": "a224d057-b6b1-467b-bac5-558923330bc7",
            "engagements": [
                {
                    "uuid": "2944d5c1-054d-419b-a86b-a7127bbc22f5",
                    "org_unit": [{"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539"}],
                    "validity": {"from": "2023-07-18T00:00:00+02:00", "to": None},
                }
            ],
            "manager_roles": [
                {
                    "uuid": "fda755b6-565c-4b59-ab90-a4c4527ed405",
                    "org_unit": [{"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539"}],
                    "validity": {"from": "2023-07-18T00:00:00+02:00", "to": None},
                }
            ],
        }
    ],
}

engagement_with_end_date_and_same_org_unit = {
    "org_unit": [
        {"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539", "name": "IT-Support"}
    ],
    "validity": {
        "from": "2023-07-18T00:00:00+02:00",
        "to": "2023-07-19T00:00:00+02:00",
    },
    "employee": [
        {
            "uuid": "a224d057-b6b1-467b-bac5-558923330bc7",
            "engagements": [
                {
                    "uuid": "2944d5c1-054d-419b-a86b-a7127bbc22f5",
                    "org_unit": [{"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539"}],
                    "validity": {
                        "from": "2023-07-18T00:00:00+02:00",
                        "to": "2023-07-19T00:00:00+02:00",
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": "fda755b6-565c-4b59-ab90-a4c4527ed405",
                    "org_unit": [{"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539"}],
                    "validity": {"from": "2023-07-18T00:00:00+02:00", "to": None},
                }
            ],
        }
    ],
}

engagement_with_end_date_but_not_in_same_org_unit = {
    "org_unit": [
        {"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539", "name": "IT-Support"}
    ],
    "validity": {
        "from": "2023-07-18T00:00:00+02:00",
        "to": "2023-07-19T00:00:00+02:00",
    },
    "employee": [
        {
            "uuid": "a224d057-b6b1-467b-bac5-558923330bc7",
            "engagements": [
                {
                    "uuid": "2944d5c1-054d-419b-a86b-a7127bbc22f5",
                    "org_unit": [{"uuid": "cff6ef44-f91a-5b02-9e25-8d8f652c2c33"}],
                    "validity": {
                        "from": "2023-07-18T00:00:00+02:00",
                        "to": "2023-07-19T00:00:00+02:00",
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": "fda755b6-565c-4b59-ab90-a4c4527ed405",
                    "org_unit": [{"uuid": "cff6ef44-f91a-5b02-9e25-8d8f652c2c33"}],
                    "validity": {"from": "2023-07-18T00:00:00+02:00", "to": None},
                }
            ],
        }
    ],
}

multiple_manager_roles_and_earlier_engagement_end_date = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2024-10-20T00:00:00+02:00",
    },
    "employee": [
        {
            "uuid": "86906fc1-beb0-4f9f-b2d4-84eea8d4f7d2",
            "engagements": [
                {
                    "uuid": "d3da8387-cd27-4fb7-a491-2f6ec992d4db",
                    "org_unit": [{"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"}],
                    "validity": {
                        "from": "2023-07-19T00:00:00+02:00",
                        "to": "2023-08-23T00:00:00+02:00",
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": "21926ae9-5479-469a-97ae-3a996a7b3a01",
                    "org_unit": [{"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"}],
                    "validity": {
                        "from": "2023-07-19T00:00:00+02:00",
                        "to": "2024-10-23T00:00:00+02:00",
                    },
                },
                {
                    "uuid": "50aa9f61-6faa-4e5c-92a6-34f259bc9043",
                    "org_unit": [{"uuid": "c9d51723-b777-5878-af66-30626e2f9d66"}],
                    "validity": {"from": "2023-07-19T00:00:00+02:00", "to": None},
                },
                {
                    "uuid": "e2cdab1e-9406-4939-a3f3-ad08d7f58fe4",
                    "org_unit": [{"uuid": "32865a87-3475-5dbd-accb-d7659603f0b7"}],
                    "validity": {"from": "2023-07-19T00:00:00+02:00", "to": None},
                },
            ],
        }
    ],
}


@pytest.mark.parametrize(
    "test_data, expected_result",
    [  # Engagement does not have an end date, and is in same org unit.
        (engagement_no_end_date_and_same_org_unit, False),
        # Engagement does have an end date, and is in same org unit.
        (engagement_with_end_date_and_same_org_unit, True),
        # Engagement does have an end date, but is not in same org unit.
        (engagement_with_end_date_but_not_in_same_org_unit, False),
    ],
)
def test_check_for_end_date(test_data, expected_result):
    """
    Tests if the check for engagement end date returns the correct boolean.
    True if the engagement has an end.
    False if the engagement has no end date.
    """
    result = check_for_end_date(test_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        (
            engagement_no_end_date_and_same_org_unit,
            "fda755b6-565c-4b59-ab90-a4c4527ed405",
        ),
        (
            multiple_manager_roles_and_earlier_engagement_end_date,
            "21926ae9-5479-469a-97ae-3a996a7b3a01",
        ),
        (engagement_with_end_date_but_not_in_same_org_unit, None),
    ],
)
def test_end_date_in_manager_object(test_data, expected_result):
    """
    Tests to retrieve the managers uuid, if the manager role exists in
    the same org unit as the engagement being created/updated/terminated.
    Returns the managers uuid, if it exists in the same org unit.
    """
    result = get_manager_uuid_if_engagement_is_in_same_org_unit(test_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        (engagement_with_end_date_and_same_org_unit, "2023-07-19"),
        (multiple_manager_roles_and_earlier_engagement_end_date, "2024-10-20"),
        (engagement_with_end_date_but_not_in_same_org_unit, None),
    ],
)
def test_set_latest_end_date_and_ensure_same_org_unit(test_data, expected_result):
    """
    Tests whether the manager roles end date arrives before the engagements end date.
    Will return a datetime string, if the engagement has an earlier end date.
    Will return None, if the manager roles end date arrives before the engagements.
    """
    result = get_latest_end_date_and_ensure_same_org_unit(test_data)
    assert result == expected_result
