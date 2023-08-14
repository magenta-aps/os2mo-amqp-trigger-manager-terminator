# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime

import pytest

from terminate_managers_init.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)


@pytest.mark.parametrize(
    "manager_role_end_date,  employee_objects_data, expected_result",
    [
        (  # There is no employee data. Set termination date to today.
            "2030-12-30T00:00:00+02:00",
            None,
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": datetime.date.today().isoformat(),
                }
            ],
        ),
        (  # There are no engagements associated with the manager. Set termination date to today.
            "2023-07-18T00:00:00+02:00",
            [{"engagements": []}],
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": datetime.date.today().isoformat(),
                }
            ],
        ),
        (  # Manager has no end date, set the end date to the engagement.
            # Set termination to engagements end date.
            None,
            [
                {
                    "engagements": [
                        {
                            "uuid": "ef9f76fd-1840-4d94-961a-1140c86efd00",
                            "org_unit": [
                                {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                            ],
                            "validity": {
                                "from": "1975-12-08T00:00:00" "+01:00",
                                "to": "2023-07-18T00:00:00+02:00",
                            },
                        }
                    ]
                },
            ],
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": "2023-07-18",
                }
            ],
        ),
        (  # Engagement end date is farther than the managers end date.
            # Set termination to engagements end date.
            "2023-08-18T00:00:00+02:00",
            [
                {
                    "engagements": [
                        {
                            "uuid": "e6d1b0a8-df82-4397-b9e5-dfcf680ba7d2",
                            "org_unit": [
                                {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2024-06-01T00:00:00+02:00",
                            },
                        }
                    ]
                }
            ],
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": "2024-06-01",
                }
            ],
        ),
        (  # Manager end date is farther than engagements.
            # Set the termination to the farthest engagement date.
            "2345-01-01T00:00:00+02:00",
            [
                {
                    "engagements": [
                        {
                            "uuid": "e6d1b0a8-df82-4397-b9e5-dfcf680ba7d2",
                            "org_unit": [
                                {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2023-06-01T00:00:00+02:00",
                            },
                        }
                    ]
                }
            ],
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": "2023-06-01",
                }
            ],
        ),
        (  # Manager end date is farther than several engagements.
            # Set the termination to the farthest engagement date from same org unit.
            "2121-12-21T00:00:00+02:00",
            [
                {
                    "engagements": [
                        {
                            "uuid": "e6d1b0a8-df82-4397-b9e5-dfcf680ba7d2",
                            "org_unit": [
                                {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2025-05-05T00:00:00+02:00",
                            },
                        },
                        {
                            "uuid": "2944d5c1-054d-419b-a86b-a7127bbc22f5",
                            "org_unit": [
                                {"uuid": "f582e76e-3276-5c83-a48d-ef1fd7a58ce7"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2026-06-01T00:00:00+02:00",
                            },
                        },
                        {
                            "uuid": "c8522e20-0a38-40e3-a84b-bcc0ce5f6341",
                            "org_unit": [
                                {"uuid": "ddc5c715-d63f-59a7-9f26-b4b2588a8152"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2027-06-01T00:00:00+02:00",
                            },
                        },
                        {
                            "uuid": "0959f658-1216-467e-b47b-90ec3e16d733",
                            "org_unit": [
                                {"uuid": "ed3f6666-2a0b-5449-b388-3df81c082539"}
                            ],
                            "validity": {
                                "from": "2023-07-18T00:00:00+02:00",
                                "to": "2028-06-01T00:00:00+02:00",
                            },
                        },
                    ]
                }
            ],
            [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "termination_date": "2025-05-05",
                }
            ],
        ),
    ],
)
def test_extract_managers_with_no_persons_or_engagements(
    manager_role_end_date, employee_objects_data, expected_result
):
    test_objects = [
        {
            "objects": [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "org_unit": [{"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}],
                    "employee": employee_objects_data,
                    "validity": {
                        "from": "1975-12-08T00:00:00+01:00",
                        "to": manager_role_end_date,
                    },
                }
            ]
        }
    ]
    result = extract_managers_with_no_persons_or_engagements(test_objects)
    assert result == expected_result
