# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import pytest

from manager_terminator.helper_functions import (
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit,
)
from manager_terminator.process_events import process_engagement_events
from tests.test_data import EMPLOYEE_OBJECTS
from tests.test_data import ENGAGEMENT_OBJECTS
from tests.test_data import (
    ENGAGEMENT_OBJECTS_MANAGER_AND_ENGAGEMENT_NOT_IN_SAME_ORG_UNIT,
)
from tests.test_data import (
    ENGAGEMENT_OBJECTS_MANAGER_WITH_EARLIER_END_DATE_THAN_ENGAGEMENT_END_DATE,
)
from tests.test_data import ENGAGEMENT_OBJECTS_NO_END_DATE_IN_ENGAGEMENT
from tests.test_data import ENGAGEMENT_OBJECTS_PERSON_IS_NOT_MANAGER
from tests.test_data import ENGAGEMENT_ORG_UNIT_OBJECTS
from tests.test_data import NO_ENGAGEMENT_OBJECTS_FOUND


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_events_when_no_objects_found_successfully(mock_event_logger):
    """
    Tests if the manager terminates successfully as part of the event.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = NO_ENGAGEMENT_OBJECTS_FOUND
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")
    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_event_logger.info.assert_any_call(
        "No engagement objects found - event might be a termination. End process."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_latest_end_date_from_engagement_objects")
async def test_process_engagements_event_terminate_managers_successfully(
    mock_get_latest_end_date_from_engagement_objects: MagicMock,
):
    """
    Tests if the manager terminates successfully as part of the event.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = ENGAGEMENT_OBJECTS
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")
    manager_uuid = UUID("29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101")
    termination_date = (
        mock_get_latest_end_date_from_engagement_objects.return_value
    ) = datetime(
        2023,
        9,
        20,
        0,
        0,
        tzinfo=timezone(timedelta(seconds=7200)),
    )
    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)

    mocked_mo_client.terminate_manager.assert_awaited_once_with(
        termination_date, manager_uuid
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_employee_not_a_manager(mock_events_logger):
    """
    Tests if function ends when employee is not a manager.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_PERSON_IS_NOT_MANAGER
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_events_logger.info.assert_any_call(
        "The person is not a manager. Event exited."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_has_no_end_date(mock_events_logger):
    """
    Tests if function ends when no engagement end date has been found.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_NO_END_DATE_IN_ENGAGEMENT
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)

    mock_events_logger.info.assert_any_call(
        "No end dates found on the persons engagement(s). End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_returns_none_when_terminate_managers_not_successful(
    mock_events_logger,
):
    """
    Tests if the process_engagement_events returns None when termination does not succeed.

    Tests if logging message gets properly logged with correct error level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_MANAGER_WITH_EARLIER_END_DATE_THAN_ENGAGEMENT_END_DATE
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_events_logger.info.assert_any_call(
        "Manager will be terminated before farthest engagement. End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_get_manager_uuid_if_eng_in_same_org_returns_none(
    mock_events_logger,
):
    """
    Tests if function returns None when manager and engagement is not in same org unit.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_MANAGER_AND_ENGAGEMENT_NOT_IN_SAME_ORG_UNIT
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit(
        EMPLOYEE_OBJECTS, ENGAGEMENT_ORG_UNIT_OBJECTS
    )
    mock_events_logger.error.assert_any_call(
        "The manager role might not exist in the same org unit as the engagement being"
        "created/updated/terminated."
    )
