# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from raclients.graph.client import PersistentGraphQLClient

from .config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


async def process_engagement_events(
    gql_client: PersistentGraphQLClient, engagement_uuid: UUID
) -> None:
    """
    A function for handling the various events made involving an engagement.
    This involves checking whether the engagement has an active manager role
    assigned to it, and whether the manager role includes an end date that
    matches the engagements' end date.
    Once the managers end date satisfies our quota, we handle it accordingly.

    Args:
        gql_client: A GraphQL client to perform the various queries

        engagement_uuid: UUID of the engagement

    Returns:
        A successful termination of a manager position or None.
    """
    print("STARTING AN EVENT")
    logger.info(
        "Starting event for the engagement with uuid:",
        engagement_uuid=engagement_uuid,
    )
