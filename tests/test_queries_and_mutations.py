# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import unittest.mock
import uuid
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID
from uuid import uuid4

import pytest

from tests.test_data import ALL_MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL
from tests.test_data import ENGAGEMENT_OBJECTS


@pytest.mark.asyncio
async def test_get_engagement_objects():
    """
    Tests if the GraphQL execute coroutine was awaited and that the response data
    is retrieved with the engagement uuid, that was found from the AMQP listener.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = ENGAGEMENT_OBJECTS
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await mocked_mo_client.get_engagement_objects(engagement_uuid)
    # ASSERT
    mocked_mo_client.get_engagement_objects.assert_awaited_once_with(engagement_uuid)


@pytest.mark.asyncio
async def test_get_managers():
    """
    Tests if the GraphQL execute coroutine was awaited and that the response data
    is retrieved as we expect it.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_managers.return_value = (
        ALL_MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL
    )
    await mocked_mo_client.get_managers()
    # ASSERT
    mocked_mo_client.get_managers.assert_awaited_once()


@pytest.mark.asyncio
async def test_one_terminate_manager():
    """
    Test to verify the GraphQL execute coroutine is awaited and that the mutation
    was executed with only 1 manager uuid.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    manager_uuid = uuid4()
    termination_date = datetime.today()

    await mocked_mo_client.terminate_manager(termination_date, manager_uuid)

    # ASSERT
    mocked_mo_client.terminate_manager.assert_awaited_once_with(
        termination_date, manager_uuid
    )


@pytest.mark.asyncio
async def test_initial_terminate_existing_empty_manager_roles():
    """
    Test to verify the GraphQL execute coroutine is awaited and that the mutation
    was executed with however many uuids found in the manager_uuids list.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    manager_uuids = [uuid.uuid4() for _ in range(3)]
    termination_date = datetime.today()
    # ACT
    for manager_uuid in manager_uuids:
        await mocked_mo_client.terminate_manager(termination_date, manager_uuid)

        mocked_mo_client.terminate_manager.assert_awaited()

    # ASSERT
    assert mocked_mo_client.terminate_manager.call_args_list[0] == unittest.mock.call(
        termination_date, manager_uuids[0]
    )

    assert mocked_mo_client.terminate_manager.call_args_list[1] == unittest.mock.call(
        termination_date, manager_uuids[1]
    )

    assert mocked_mo_client.terminate_manager.call_args_list[2] == unittest.mock.call(
        termination_date, manager_uuids[2]
    )
