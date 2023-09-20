# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

import pytest

from manager_terminator.main import listener


@pytest.mark.asyncio
@patch("manager_terminator.main.process_engagement_events")
async def test_listener(mock_process_engagement_events: AsyncMock):
    """
    Tests if the listeners process_engagement_events is called and
    that it is awaited once.
    """
    engagement_uuid = uuid4()
    mock_graphql_session = MagicMock()

    await listener(mock_graphql_session, engagement_uuid, MagicMock())

    mock_process_engagement_events.assert_awaited_once_with(
        mock_graphql_session, engagement_uuid
    )
