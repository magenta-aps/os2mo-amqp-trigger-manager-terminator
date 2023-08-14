# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from manager_terminator.helper_functions import check_for_end_date
from manager_terminator.helper_functions import (
    get_latest_end_date_from_engagement_objects,
)
from manager_terminator.helper_functions import (
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit,
)
from manager_terminator.process_events import process_engagement_events
from tests.test_queries_and_mutations import ENGAGEMENT_OBJECTS
from tests.test_queries_and_mutations import ENGAGEMENT_OBJECTS_EMPLOYEE_NOT_A_MANAGER
from tests.test_queries_and_mutations import ENGAGEMENT_OBJECTS_NO_END_DATE
from tests.test_queries_and_mutations import (
    ENGAGEMENT_OBJECTS_NO_MANAGER_ROLE_IN_SAME_ORG_UNIT,
)
from tests.test_queries_and_mutations import (
    MANAGER_ROLE_END_DATE_BEFORE_ENGAGEMENT_END_DATE,
)


@pytest.mark.asyncio
@patch("manager_terminator.process_events.terminate_manager")
@patch("manager_terminator.process_events.get_latest_end_date_from_engagement_objects")
@patch("manager_terminator.process_events.get_engagement_objects")
async def test_process_engagements_event_terminate_managers_successfully(
    mock_get_engagement_objects: AsyncMock,
    mock_get_latest_end_date_from_engagement_objects: MagicMock,
    mock_terminate_manager_function: AsyncMock,
):
    """
    Tests if the manager terminates successfully as part of the event.
    """
    mocked_gql_client = AsyncMock()
    engagement_uuid = ENGAGEMENT_OBJECTS.get("employee")[0].get("uuid")  # type: ignore
    manager_uuid = (
        ENGAGEMENT_OBJECTS.get("employee")[0].get("manager_roles")[0].get("uuid")  # type: ignore
    )
    termination_date = (
        mock_get_latest_end_date_from_engagement_objects.return_value
    ) = "2023-08-23"
    mock_get_engagement_objects.return_value = ENGAGEMENT_OBJECTS

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=engagement_uuid
    )
    mock_terminate_manager_function.assert_awaited_once_with(
        mocked_gql_client, manager_uuid, termination_date
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_employee_not_a_manager(
    mock_events_logger, mock_get_engagement_objects: AsyncMock
):
    """
    Tests if function ends when employee is not a manager.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_gql_client = AsyncMock()
    eng_uuid = ENGAGEMENT_OBJECTS_EMPLOYEE_NOT_A_MANAGER["employee"][0]["uuid"]  # type: ignore

    mock_get_engagement_objects.return_value = ENGAGEMENT_OBJECTS_EMPLOYEE_NOT_A_MANAGER

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=eng_uuid
    )

    mock_events_logger.info.assert_any_call(
        "The person is not a manager. Event exited."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_has_no_end_date(
    mock_events_logger, mock_get_engagement_objects: AsyncMock
):
    """
    Tests if function ends when no engagement end date has been found.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_gql_client = AsyncMock()
    eng_uuid = ENGAGEMENT_OBJECTS_NO_END_DATE.get("employee")[0].get(  # type: ignore
        "uuid"
    )

    mock_get_engagement_objects.return_value = ENGAGEMENT_OBJECTS_NO_END_DATE

    check_for_end_date(ENGAGEMENT_OBJECTS_NO_END_DATE)
    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=eng_uuid
    )

    mock_events_logger.info.assert_any_call(
        "No end dates found on the persons engagement(s). End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_returns_none_when_terminate_managers_not_successful(
    mock_events_logger,
    mock_get_engagement_objects: AsyncMock,
):
    """
    Tests if the process_engagement_events returns None when termination does not succeed.

    Tests if logging message gets properly logged with correct error level.
    """
    mocked_gql_client = AsyncMock()
    eng_uuid = MANAGER_ROLE_END_DATE_BEFORE_ENGAGEMENT_END_DATE.get("employee")[  # type: ignore
        0
    ].get(
        "uuid"
    )

    end_date_for_manager = "2023-08-23T00:00:00+02:00"

    mock_get_engagement_objects.return_value = (
        MANAGER_ROLE_END_DATE_BEFORE_ENGAGEMENT_END_DATE
    )
    get_latest_end_date_from_engagement_objects(
        MANAGER_ROLE_END_DATE_BEFORE_ENGAGEMENT_END_DATE, end_date_for_manager
    )

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=eng_uuid
    )
    mock_events_logger.info.assert_any_call(
        "Manager will be terminated before farthest engagement. End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_get_manager_uuid_if_eng_in_same_org_returns_none(
    mock_events_logger, mock_get_engagement_objects: AsyncMock
):
    """
    Tests if function returns None when manager and engagement is not in same org unit.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_gql_client = AsyncMock()
    eng_uuid = ENGAGEMENT_OBJECTS_NO_MANAGER_ROLE_IN_SAME_ORG_UNIT.get("employee")[  # type: ignore
        0
    ].get(
        "uuid"
    )

    mock_get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_NO_MANAGER_ROLE_IN_SAME_ORG_UNIT
    )

    get_manager_uuid_and_manager_end_date_if_in_same_org_unit(
        ENGAGEMENT_OBJECTS_NO_MANAGER_ROLE_IN_SAME_ORG_UNIT
    )

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=eng_uuid
    )
    mock_events_logger.error.assert_any_call(
        "The manager role might not exist in the same org unit as the engagement being"
        "created/updated/terminated."
    )
