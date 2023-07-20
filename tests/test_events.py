# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

import pytest

from manager_terminator.process_events import process_engagement_events
from tests.test_queries_and_mutations import ENGAGEMENT_OBJECTS


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_when_no_no_objects_found_in_engagements(
    mock_events_logger, mock_get_engagement_objects_function
):
    """
    Tests if the process_engagement_events returns None when no engagement found in
    engagements object.

    Tests if logging message gets properly logged with correct error level.
    """
    engagement_uuid = uuid4()
    mocked_gql_client = AsyncMock()
    mock_get_engagement_objects_function.side_effect = ValueError()

    result = await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=engagement_uuid
    )

    assert result is None

    mock_events_logger.error.assert_any_call("Engagement object not found.")


# @patch("manager_terminator.process_events.logger")
@pytest.mark.asyncio
@patch("manager_terminator.process_events.terminate_manager")
@patch("manager_terminator.process_events.get_engagement_objects")
async def test_process_engagements_event_terminate_managers_successfully(
    mock_get_engagement_objects: AsyncMock, mock_terminate_manager_function: AsyncMock
):
    """
    Tests if the manager terminates successfully as part of the event.
    """
    mocked_gql_client = AsyncMock()
    engagement_uuid = ENGAGEMENT_OBJECTS.get("employee")[0].get("uuid")  # type: ignore
    manager_uuid = (
        ENGAGEMENT_OBJECTS.get("employee")[0].get("manager_roles")[0].get("uuid")  # type: ignore
    )
    termiation_date = "2023-08-23"
    mock_get_engagement_objects.return_value = ENGAGEMENT_OBJECTS

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=UUID(engagement_uuid)
    )
    mock_terminate_manager_function.assert_awaited_once_with(
        mocked_gql_client, UUID(manager_uuid), termiation_date
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.terminate_manager")
@patch("manager_terminator.process_events.get_engagement_objects")
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_returns_none_when_terminate_managers_not_successful(
    mock_events_logger,
    mock_get_engagement_objects: AsyncMock,
    mock_terminate_manager_function,
):
    """
    Tests if the process_engagement_events returns None when termination does not succeed.

    Tests if logging message gets properly logged with correct error level.
    """
    mocked_gql_client = AsyncMock()

    mock_get_engagement_objects.return_value = ENGAGEMENT_OBJECTS
    mock_terminate_manager_function.side_effect = ValueError()

    await process_engagement_events(
        gql_client=mocked_gql_client, engagement_uuid=uuid4()
    )

    mock_events_logger.error.assert_any_call(
        "Engagement end date, manager end date or common org unit uuid not found."
    )
