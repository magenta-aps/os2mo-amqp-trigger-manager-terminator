# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
import unittest.mock
import uuid
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from manager_terminator.mutations_made_to_mo import MUTATION_TERMINATE_MANAGER
from manager_terminator.mutations_made_to_mo import terminate_manager
from manager_terminator.queries_made_to_mo import get_engagement_objects
from manager_terminator.queries_made_to_mo import QUERY_GET_ENGAGEMENT_OBJECTS
from terminate_managers_init.mutation_to_terminate_preexisting_empty_managers import (
    terminate_existing_empty_manager_roles,
)
from terminate_managers_init.query_to_find_empty_managers import (
    get_managers,
)
from terminate_managers_init.query_to_find_empty_managers import (
    QUERY_GET_MANAGERS,
)

ENGAGEMENT_OBJECTS = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2023-08-23T00:00:00+02:00",
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
                    "validity": {"from": "2023-07-19T00:00:00+02:00", "to": None},
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

ENGAGEMENT_OBJECTS_NO_MANAGER_ROLE_IN_SAME_ORG_UNIT = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2023-08-23T00:00:00+02:00",
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
                    "uuid": "e2cdab1e-9406-4939-a3f3-ad08d7f58fe4",
                    "org_unit": [{"uuid": "32865a87-3475-5dbd-accb-d7659603f0b7"}],
                    "validity": {"from": "2023-07-19T00:00:00+02:00", "to": None},
                },
            ],
        }
    ],
}


ENGAGEMENT_OBJECTS_EMPLOYEE_NOT_A_MANAGER = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2023-08-23T00:00:00+02:00",
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
            "manager_roles": [],
        }
    ],
}

ENGAGEMENT_OBJECTS_NO_END_DATE = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2023-08-23T00:00:00+02:00",
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
                        "to": None,
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": "21926ae9-5479-469a-97ae-3a996a7b3a01",
                    "org_unit": [{"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"}],
                    "validity": {"from": "2023-07-19T00:00:00+02:00", "to": None},
                },
            ],
        }
    ],
}


MANAGER_ROLE_END_DATE_BEFORE_ENGAGEMENT_END_DATE = {
    "org_unit": [
        {"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd", "name": "Social og sundhed"}
    ],
    "validity": {
        "from": "2023-07-19T00:00:00+02:00",
        "to": "2023-08-23T00:00:00+02:00",
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
                        "to": "2025-08-23T00:00:00+02:00",
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": "21926ae9-5479-469a-97ae-3a996a7b3a01",
                    "org_unit": [{"uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"}],
                    "validity": {
                        "from": "2023-07-19T00:00:00+02:00",
                        "to": "2023-08-23T00:00:00+02:00",
                    },
                },
            ],
        }
    ],
}

ENGAGEMENT_RESPONSE = {
    "engagements": {
        "objects": [
            {
                "objects": [
                    {
                        "org_unit": [
                            {
                                "uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd",
                                "name": "Social og sundhed",
                            }
                        ],
                        "validity": {
                            "from": "2023-07-19T00:00:00+02:00",
                            "to": "2023-08-23T00:00:00+02:00",
                        },
                        "employee": [
                            {
                                "uuid": "86906fc1-beb0-4f9f-b2d4-84eea8d4f7d2",
                                "engagements": [
                                    {
                                        "uuid": "d3da8387-cd27-4fb7-a491-2f6ec992d4db",
                                        "org_unit": [
                                            {
                                                "uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"
                                            }
                                        ],
                                        "validity": {
                                            "from": "2023-07-19T00:00:00+02:00",
                                            "to": "2023-08-23T00:00:00+02:00",
                                        },
                                    }
                                ],
                                "manager_roles": [
                                    {
                                        "uuid": "21926ae9-5479-469a-97ae-3a996a7b3a01",
                                        "org_unit": [
                                            {
                                                "uuid": "25abf6f4-fa38-5bd8-b217-7130ce3552cd"
                                            }
                                        ],
                                        "validity": {
                                            "from": "2023-07-19T00:00:00+02:00",
                                            "to": None,
                                        },
                                    },
                                    {
                                        "uuid": "50aa9f61-6faa-4e5c-92a6-34f259bc9043",
                                        "org_unit": [
                                            {
                                                "uuid": "c9d51723-b777-5878-af66-30626e2f9d66"
                                            }
                                        ],
                                        "validity": {
                                            "from": "2023-07-19T00:00:00+02:00",
                                            "to": None,
                                        },
                                    },
                                    {
                                        "uuid": "e2cdab1e-9406-4939-a3f3-ad08d7f58fe4",
                                        "org_unit": [
                                            {
                                                "uuid": "32865a87-3475-5dbd-accb-d7659603f0b7"
                                            }
                                        ],
                                        "validity": {
                                            "from": "2023-07-19T00:00:00+02:00",
                                            "to": None,
                                        },
                                    },
                                ],
                            }
                        ],
                    }
                ]
            }
        ]
    }
}

MANAGER_OBJECTS = [
    {
        "objects": [
            {
                "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                "org_unit": [{"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}],
                "employee": [
                    {
                        "engagements": [
                            {
                                "uuid": "ef9f76fd-1840-4d94-961a-1140c86efd00",
                                "org_unit": [
                                    {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                                ],
                                "validity": {
                                    "from": "1975-12-08T00:00:00+01:00",
                                    "to": None,
                                },
                            }
                        ]
                    }
                ],
                "validity": {"from": "1975-12-08T00:00:00+01:00", "to": None},
            }
        ]
    },
    {
        "objects": [
            {
                "uuid": "083de7f8-d52f-456d-a351-44075cbc0ca5",
                "org_unit": [{"uuid": "c9d51723-b777-5878-af66-30626e2f9d66"}],
                "employee": None,
                "validity": {
                    "from": "2023-07-18T00:00:00+02:00",
                    "to": "2023-07-18T00:00:00+02:00",
                },
            }
        ]
    },
]

NO_EMPTY_MANAGER_OBJECTS = [
    {
        "objects": [
            {
                "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                "org_unit": [{"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}],
                "employee": [
                    {
                        "engagements": [
                            {
                                "uuid": "ef9f76fd-1840-4d94-961a-1140c86efd00",
                                "org_unit": [
                                    {"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}
                                ],
                                "validity": {
                                    "from": "1975-12-08T00:00:00+01:00",
                                    "to": None,
                                },
                            }
                        ]
                    }
                ],
                "validity": {"from": "1975-12-08T00:00:00+01:00", "to": None},
            }
        ]
    },
    {
        "objects": [
            {
                "uuid": "106c048f-cfdc-42b4-a418-d5e40b070451",
                "org_unit": [{"uuid": "7764d0c7-e776-5f07-8a9d-5ee6f5b717b0"}],
                "employee": [
                    {
                        "engagements": [
                            {
                                "uuid": "8f1d1aac-285b-4284-ae58-35aaf944b974",
                                "org_unit": [
                                    {"uuid": "7764d0c7-e776-5f07-8a9d-5ee6f5b717b0"}
                                ],
                                "validity": {
                                    "from": "1985-11-15T00:00:00+01:00",
                                    "to": None,
                                },
                            }
                        ]
                    }
                ],
                "validity": {"from": "1985-11-15T00:00:00+01:00", "to": None},
            }
        ]
    },
    {
        "objects": [
            {
                "uuid": "220c2015-1da8-4850-9c0e-78ed4947f540",
                "org_unit": [{"uuid": "2665d8e0-435b-5bb6-a550-f275692984ef"}],
                "employee": [
                    {
                        "engagements": [
                            {
                                "uuid": "5224902e-eca4-42a8-b379-ca55a7a1fceb",
                                "org_unit": [
                                    {"uuid": "2665d8e0-435b-5bb6-a550-f275692984ef"}
                                ],
                                "validity": {
                                    "from": "1986-01-14T00:00:00+01:00",
                                    "to": None,
                                },
                            }
                        ]
                    }
                ],
                "validity": {"from": "1986-01-14T00:00:00+01:00", "to": None},
            }
        ]
    },
]


MANAGER_RESPONSE = {
    "managers": {
        "objects": [
            {
                "objects": [
                    {
                        "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                        "org_unit": [{"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}],
                        "employee": [
                            {
                                "engagements": [
                                    {
                                        "uuid": "ef9f76fd-1840-4d94-961a-1140c86efd00",
                                        "org_unit": [
                                            {
                                                "uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"
                                            }
                                        ],
                                        "validity": {
                                            "from": "1975-12-08T00:00:00+01:00",
                                            "to": None,
                                        },
                                    }
                                ]
                            }
                        ],
                        "validity": {"from": "1975-12-08T00:00:00+01:00", "to": None},
                    }
                ]
            },
            {
                "objects": [
                    {
                        "uuid": "083de7f8-d52f-456d-a351-44075cbc0ca5",
                        "org_unit": [{"uuid": "c9d51723-b777-5878-af66-30626e2f9d66"}],
                        "employee": None,
                        "validity": {
                            "from": "2023-07-18T00:00:00+02:00",
                            "to": "2023-07-18T00:00:00+02:00",
                        },
                    }
                ]
            },
        ]
    }
}


@pytest.mark.asyncio
async def test_get_engagement_objects():
    """
    Tests if the GraphQL execute coroutine was awaited and that the response data
    is retrieved with the engagement uuid, that was found from the AMQP listener.
    """
    engagement_uuid = uuid4()
    mocked_gql_client = AsyncMock()
    expected_engagement_objects = ENGAGEMENT_OBJECTS

    mock_execute = AsyncMock(return_value=ENGAGEMENT_RESPONSE)
    mocked_gql_client.execute = mock_execute

    actual_engagement_response = await get_engagement_objects(
        gql_client=mocked_gql_client, engagement_uuid=engagement_uuid
    )

    assert actual_engagement_response == expected_engagement_objects
    mock_execute.assert_awaited_once_with(
        QUERY_GET_ENGAGEMENT_OBJECTS,
        variable_values={"engagement_uuids": str(engagement_uuid)},
    )


@pytest.mark.asyncio
async def test_get_empty_managers():
    """
    Tests if the GraphQL execute coroutine was awaited and that the response data
    is retrieved as we expect it.
    """
    gql_client_mocked = AsyncMock()
    expected_manager_response = MANAGER_OBJECTS

    mock_execute = AsyncMock(return_value=MANAGER_RESPONSE)
    gql_client_mocked.execute = mock_execute

    actual_manager_response = await get_managers(gql_client=gql_client_mocked)

    assert actual_manager_response == expected_manager_response
    mock_execute.assert_awaited_once_with(QUERY_GET_MANAGERS)


@pytest.mark.asyncio
async def test_one_terminate_manager():
    """
    Test to verify the GraphQL execute coroutine is awaited and that the mutation
    was executed with only 1 manager uuid.
    """
    # ARRANGE
    manager_uuid = uuid4()
    termination_date = datetime.date.today().isoformat()
    mocked_gql_client = AsyncMock()

    mock_execute = AsyncMock()
    mocked_gql_client.execute = mock_execute

    # ACT
    await terminate_manager(mocked_gql_client, manager_uuid, termination_date)
    assert mock_execute.call_args_list[0] == unittest.mock.call(
        MUTATION_TERMINATE_MANAGER,
        variable_values={
            "input": {
                "uuid": str(manager_uuid),
                "to": termination_date,
            }
        },
    )

    # ASSERT
    mock_execute.assert_awaited_once_with(
        MUTATION_TERMINATE_MANAGER,
        variable_values={
            "input": {
                "uuid": str(manager_uuid),
                "to": termination_date,
            }
        },
    )


@pytest.mark.asyncio
async def test_initial_terminate_existing_empty_manager_roles():
    """
    Test to verify the GraphQL execute coroutine is awaited and that the mutation
    was executed with however many uuids found in the manager_uuids list.
    """
    manager_uuids = [uuid.uuid4() for _ in range(3)]
    termination_date = datetime.date.today().isoformat()
    mocked_gql_client = AsyncMock()

    mock_execute = AsyncMock()
    mocked_gql_client.execute = mock_execute
    for manager_uuid in manager_uuids:
        await terminate_existing_empty_manager_roles(
            mocked_gql_client, manager_uuid, termination_date
        )
    assert len(mock_execute.call_args_list) == len(manager_uuids)

    assert mock_execute.call_args_list[0] == unittest.mock.call(
        MUTATION_TERMINATE_MANAGER,
        variable_values={
            "input": {
                "uuid": str(manager_uuids[0]),
                "to": termination_date,
            }
        },
    )

    assert mock_execute.call_args_list[1] == unittest.mock.call(
        MUTATION_TERMINATE_MANAGER,
        variable_values={
            "input": {
                "uuid": str(manager_uuids[1]),
                "to": termination_date,
            }
        },
    )

    assert mock_execute.call_args_list[2] == unittest.mock.call(
        MUTATION_TERMINATE_MANAGER,
        variable_values={
            "input": {
                "uuid": str(manager_uuids[2]),
                "to": termination_date,
            }
        },
    )

    mock_execute.assert_awaited()
