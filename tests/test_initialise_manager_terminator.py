# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from unittest.mock import AsyncMock
from unittest.mock import call
from unittest.mock import patch
from uuid import uuid4

import httpx
import pytest
import respx
from httpx import Response

from .test_data import MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagers,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjects,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsValiditiesPersonEngagementsValidity,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsValiditiesValidity,
)
from manager_terminator.autogenerated_graphql_client.terminate_manager import (
    TerminateManagerManagerTerminate,
)
from manager_terminator.autogenerated_graphql_client.update_manager import (
    UpdateManagerManagerUpdate,
)
from manager_terminator.config import Settings
from manager_terminator.main import initiate_terminator
from manager_terminator.utils import validity_timezone_aware


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
async def test_initiate_terminator():
    """
    Tests if the initiate_terminator functions terminator_initialiser
    is called as expected
    """
    settings = Settings()
    # Mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers.parse_obj({"objects": TEST_DATA_MANAGERS})
    )
    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # Invoke & assert
    await initiate_terminator(mo_mock, settings)
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_has_calls(
        [
            # First manager
            call(
                uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 3, 2),
                terminate_to=datetime.date(2023, 4, 30),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 6, 2),
                terminate_to=datetime.date(2023, 9, 30),
            ),
            # Second manager
            call(
                uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 1, 1),
                terminate_to=datetime.date(2023, 1, 31),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 5, 1),
                terminate_to=datetime.date(2023, 5, 31),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 9, 1),
                terminate_to=datetime.date(2023, 9, 30),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                terminate_from=datetime.date(2023, 12, 1),
                terminate_to=datetime.date(2023, 12, 31),
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
async def test_initiate_update_vacant(monkeypatch: pytest.MonkeyPatch):
    """
    Tests if the initiate_terminator function sets roles to vacant as expected.
    """

    with monkeypatch.context() as con:
        con.setenv("MANAGER_TERMINATOR__SET_TO_VACANT", "True")
        settings = Settings()
        # Mock dependencies
        mo_get_managers_mock = AsyncMock(
            return_value=GetManagersManagers.parse_obj({"objects": TEST_DATA_MANAGERS})
        )
        mo_update_manager_mock = AsyncMock(
            return_value=UpdateManagerManagerUpdate(
                uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"]
            )
        )

        mo_mock = AsyncMock(
            get_managers=mo_get_managers_mock,
            update_manager=mo_update_manager_mock,
        )

        # Invoke & assert
        await initiate_terminator(mo_mock, settings)
        mo_get_managers_mock.assert_called_once()
        mo_update_manager_mock.assert_has_calls(
            [
                # First manager
                call(
                    uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 4, 30),
                ),
                call(
                    uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 9, 30),
                ),
                # Second manager
                call(
                    uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 1, 31),
                ),
                call(
                    uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 5, 31),
                ),
                call(
                    uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 9, 30),
                ),
                call(
                    uuid=TEST_DATA_MANAGERS[1]["validities"][0]["uuid"],
                    vacant_from=datetime.date(2023, 12, 31),
                ),
            ]
        )


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
async def test_initiate_terminator_dry_run():
    settings = Settings()
    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers.parse_obj({"objects": TEST_DATA_MANAGERS})
    )
    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=TEST_DATA_MANAGERS[0]["validities"][0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock, settings, dryrun=True)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
async def test_initiate_terminator_tailing_engagements():
    """Verifies a manager which engagements tail eachother.

    ex:
    - manger validity: 2023-05-15 -> infinity
    - engagement 1 validity: 2023-01-01 -> 2023-05-14
    - engagement 2 validity: 2023-05-15 -> 2023-07-31
    - engagement 3 validity: 2023-08-01 -> infinity

    this should not result in a termination of the manager.
    """
    settings = Settings()
    test_data = [
        _create_test_data_manager_with_employee_engagements(
            manager_validity=GetManagersManagersObjectsValiditiesValidity(
                from_=datetime.datetime(2023, 5, 15, 0, 0), to=None
            ),
            engagement_validities=[
                GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                    from_=datetime.datetime(2023, 1, 1, 0, 0),
                    to=datetime.datetime(2023, 5, 14, 0, 0),
                ),
                GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                    from_=datetime.datetime(2023, 5, 15, 0, 0),
                    to=datetime.datetime(2023, 7, 31, 0, 0),
                ),
                GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                    from_=datetime.datetime(2023, 8, 1, 0, 0),
                    to=None,
                ),
            ],
        ),
    ]

    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers.parse_obj({"objects": test_data})
    )

    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data[0]["validities"][0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock, settings)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
async def test_initiate_terminator_terminate_entire_infinity_manager():
    """Verfies a manager with no engagements and no end-date, is terminated correctly

    A manager with an end-date of infinity, is treated differently since our GraphQL
    termination-mutation does not accept infinity as a valid to-date.

    So instead we need to set from=None and to=manager_validity.from, which the
    mutator then treats as a termination of the entire manager from the
    manager_validity.from to infinity.

    NOTE: This is due to how the termination-mutators have been implemented.
    Ideally the mutator should be fixed so we can set to=None
    and then always require "from"-date instead of "to"-date.
    """

    settings = Settings()
    test_data = [
        _create_test_data_manager_with_employee_engagements(
            manager_validity=GetManagersManagersObjectsValiditiesValidity(
                from_=datetime.datetime(2023, 1, 1, 0, 0), to=None
            ),
            engagement_validities=[],
        ),
    ]

    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers.parse_obj({"objects": test_data})
    )

    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data[0]["validities"][0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock, settings)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data[0]["validities"][0]["uuid"],
                terminate_from=None,
                terminate_to=datetime.date(2022, 12, 31),
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures("minimal_valid_settings")
@patch("manager_terminator.main.logger")
async def test_init_when_no_managers_found(mock_events_logger):
    """
    Tests if function exits correctly, when no manager uuids are found.

    Tests for correct log message and log level.
    """
    settings = Settings()
    # ARRANGE
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers.parse_obj(
            MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS
        )
    )

    # ACT
    await initiate_terminator(mo_get_managers_mock, settings)

    # ASSERT
    mo_get_managers_mock.terminate_manager.assert_not_awaited()
    # print(mo_get_managers_mock.terminate_manager.call_args_list)

    mock_events_logger.info.assert_any_call("No invalid manager periods found.")


@pytest.mark.asyncio
@respx.mock
async def test_post_to_listener():
    async with httpx.AsyncClient() as client:
        route = respx.post("https://fakeapi/initiate/terminator/").mock(
            return_value=Response(200)
        )
        response = await client.post("https://fakeapi/initiate/terminator/")
        assert route.called
        assert response.status_code == 200


def _create_test_data_manager_with_employee_engagements(
    manager_validity: GetManagersManagersObjectsValiditiesValidity,
    engagement_validities: list[
        GetManagersManagersObjectsValiditiesPersonEngagementsValidity
    ],
) -> GetManagersManagersObjects:
    org_units = [
        {
            "uuid": uuid4(),
        }
    ]

    return {
        "validities": [
            {
                "uuid": uuid4(),
                "person": [
                    {
                        "uuid": uuid4(),
                        "engagements": [
                            {
                                "uuid": uuid4(),
                                "org_unit": org_units,
                                "validity": validity_timezone_aware(eng_validity),
                            }
                            for eng_validity in engagement_validities
                        ],
                    }
                ],
                "org_unit": org_units,
                "validity": validity_timezone_aware(manager_validity),
            }
        ]
    }


TEST_DATA_MANAGERS = [
    _create_test_data_manager_with_employee_engagements(
        manager_validity=GetManagersManagersObjectsValiditiesValidity(
            from_=datetime.datetime(2023, 1, 1, 0, 0),
            to=datetime.datetime(2023, 12, 31, 0, 0),
        ),
        engagement_validities=[
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2022, 1, 1, 0, 0),
                to=datetime.datetime(2022, 9, 29, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2022, 12, 1, 0, 0),
                to=datetime.datetime(2023, 3, 1, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2023, 5, 1, 0, 0),
                to=datetime.datetime(2023, 6, 1, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2023, 10, 1, 0, 0),
                to=datetime.datetime(2024, 3, 1, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2024, 6, 1, 0, 0),
                to=None,
            ),
        ],
    ),
    # Test cut of manager validity, if manager validity-from is before engagement validity-from
    # same goes for manager validity-to and engagement validity-to
    _create_test_data_manager_with_employee_engagements(
        manager_validity=GetManagersManagersObjectsValiditiesValidity(
            from_=datetime.datetime(2023, 1, 1, 0, 0),
            to=datetime.datetime(2023, 12, 31, 0, 0),
        ),
        engagement_validities=[
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2023, 2, 1, 0, 0),
                to=datetime.datetime(2023, 4, 30, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2023, 6, 1, 0, 0),
                to=datetime.datetime(2023, 8, 31, 0, 0),
            ),
            GetManagersManagersObjectsValiditiesPersonEngagementsValidity(
                from_=datetime.datetime(2023, 10, 1, 0, 0),
                to=datetime.datetime(2023, 11, 30, 0, 0),
            ),
        ],
    ),
]
