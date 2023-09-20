# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import httpx
import pytest
import respx
from httpx import Response

from manager_terminator.main import initiate_terminator
from manager_terminator.terminate_managers_init.init_manager_terminator import (
    terminator_initialiser,
)
from tests.test_data import MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS


@pytest.mark.asyncio
@respx.mock
async def test_post_to_listener():
    async with httpx.AsyncClient() as client:
        route = respx.post("https://fakeapi/initiate/terminator/").mock(
            return_value=Response(204)
        )
        response = await client.post("https://fakeapi/initiate/terminator/")
        assert route.called
        assert response.status_code == 204


@pytest.mark.asyncio
@patch("manager_terminator.main.terminator_initialiser")
async def test_initiate_terminator(mock_terminator_initialiser: AsyncMock):
    """
    Tests if the initiate_terminator functions terminator_initialiser
    is called and is awaited once.
    """
    await initiate_terminator(AsyncMock())
    mock_terminator_initialiser.assert_awaited_once()


@pytest.mark.asyncio
@patch(
    "manager_terminator.terminate_managers_init.init_manager_terminator.extract_managers_with_no_persons_or_engagements"
)
@patch("manager_terminator.terminate_managers_init.init_manager_terminator.logger")
async def test_init_when_no_managers_found(
    mock_events_logger, mock_extract_managers_with_no_persons_or_engagements: MagicMock
):
    """
    Tests if function exits correctly, when no manager uuids are found.

    Tests for correct log message and log level.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_managers.return_value = (
        MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS
    )
    mock_extract_managers_with_no_persons_or_engagements.return_value = None

    # ACT
    await terminator_initialiser(mocked_mo_client)

    # ASSERT
    mocked_mo_client.terminate_manager.assert_not_awaited()

    mock_events_logger.info.assert_any_call(
        "No manager roles without a person or engagements associated found."
    )


@pytest.mark.asyncio
@patch(
    "manager_terminator.terminate_managers_init.init_manager_terminator.extract_managers_with_no_persons_or_engagements"
)
@patch("manager_terminator.terminate_managers_init.init_manager_terminator.logger")
async def test_terminator_initialiser(
    mock_events_logger,
    mock_extract_managers_uuid_and_end_date: MagicMock,
):
    """
    Tests if the terminate function is awaited.

    Tests for correct log message and log level.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    manager_uuid = UUID("0b51953c-537b-4bf9-a872-2710b0ddd9e3")
    list_of_terminations = [
        {
            "uuid": manager_uuid,
            "termination_date": "2023-09-19",
        }
    ]
    mock_extract_managers_uuid_and_end_date.return_value = list_of_terminations

    # ACT
    await terminator_initialiser(mocked_mo_client)
    for termination_data in list_of_terminations:
        manager_uuid = termination_data.get("uuid")  # type: ignore
        termination_date = termination_data.get("termination_date")
        await mocked_mo_client.terminate_manager(termination_date, manager_uuid)

        # ASSERT
        mocked_mo_client.terminate_manager.assert_awaited_with(
            termination_date, manager_uuid
        )

    # ASSERT
    mock_events_logger.info.assert_any_call(
        "Terminated empty manager(s) with uuid(s):",
        manager_uuids=list_of_terminations,
    )
