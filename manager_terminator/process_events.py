# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from raclients.graph.client import GraphQLClient

from manager_terminator.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


async def process_engagement_events(
    gql_client: GraphQLClient, engagement_uuid: UUID
) -> None:
    """
    A function for handling the various events made involving a manager.
    This includes checking whether the persons engagement is active or
    has been ended, and whether the person assigned as the organisational
    manager, also has an end date that matches the persons engagements end date.

    Args:
        gql_client: A GraphQL client to perform the various queries

        engagement_uuid: UUID of the engagement

    Returns:
        A successful termination of a manager position or None.
    """
    print("LISTENING ON AN EVENT")
    logger.info(
        "Listening on an engagement event with uuid:",
        engagement_uuid=engagement_uuid,
    )
