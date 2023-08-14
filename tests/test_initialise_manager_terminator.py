# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from manager_terminator.main import create_app
from manager_terminator.main import initiate_terminator
from terminate_managers_init.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)
from terminate_managers_init.init_manager_terminator import (
    terminator_initialiser,
)
from tests.test_queries_and_mutations import MANAGER_OBJECTS
from tests.test_queries_and_mutations import NO_EMPTY_MANAGER_OBJECTS


mock_settings = MagicMock(
    return_value={"CLIENT_ID": "Foo", "CLIENT_SECRET": "Bar", "AMQP": "Baz"}
)

CLIENT = TestClient(
    create_app(
        client_id="foo",
        client_secret="bar",
        amqp={"url": "amqp://guest:guest@msg_broker:5672/"},
    )
)


@pytest.mark.asyncio
async def test_post_to_listener():
    CLIENT.app.state.context = {"graphql_session": AsyncMock()}
    response = CLIENT.post("/initiate/terminator/")
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
    "terminate_managers_init.init_manager_terminator.terminate_existing_empty_manager_roles"
)
@patch("terminate_managers_init.init_manager_terminator.get_managers")
@patch("terminate_managers_init.init_manager_terminator.logger")
async def test_init_when_no_managers_found(
    mock_events_logger,
    mock_managers_object: AsyncMock,
    mock_terminate_existing_empty_manager_roles: AsyncMock,
):
    """
    Tests if function exits correctly, when no manager uuids are found.

    Tests for correct log message and log level.
    """
    mocked_gql_client = AsyncMock()
    mock_managers_object.return_value = NO_EMPTY_MANAGER_OBJECTS

    await terminator_initialiser(mocked_gql_client)

    mock_terminate_existing_empty_manager_roles.assert_not_awaited()

    mock_events_logger.info.assert_any_call(
        "No manager roles without a person or engagements associated found."
    )


@pytest.mark.asyncio
@patch(
    "terminate_managers_init.init_manager_terminator.terminate_existing_empty_manager_roles"
)
@patch("terminate_managers_init.init_manager_terminator.get_managers")
@patch("terminate_managers_init.init_manager_terminator.logger")
async def test_terminator_initialiser(
    mock_events_logger,
    mock_managers_object: AsyncMock,
    mock_terminate_existing_empty_manager_roles: AsyncMock,
):
    """
    Tests if the terminate function is awaited.

    Tests for correct log message and log level.
    """
    mocked_gql_client = AsyncMock()
    mock_managers_object.return_value = MANAGER_OBJECTS
    list_of_terminations = extract_managers_with_no_persons_or_engagements(
        MANAGER_OBJECTS
    )

    await terminator_initialiser(mocked_gql_client)
    for termination_data in list_of_terminations:
        manager_uuid = termination_data.get("uuid")
        termination_date = termination_data.get("termination_date")
        mock_terminate_existing_empty_manager_roles.assert_awaited_once_with(
            mocked_gql_client, UUID(manager_uuid), termination_date
        )

    mock_events_logger.info.assert_any_call(
        "Terminated empty manager(s) with uuid(s):",
        manager_uuids=list_of_terminations,
    )
