# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from raclients.graph.client import GraphQLClient

from terminate_managers_init.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)
from terminate_managers_init.mutation_to_terminate_preexisting_empty_managers import (
    terminate_existing_empty_manager_roles,
)
from terminate_managers_init.query_to_find_empty_managers import (
    get_managers,
)

logger = structlog.get_logger(__name__)


async def terminator_initialiser(gql_client: GraphQLClient) -> None:
    """
    Function that will look for any empty manager roles - if any are found,
    they will be terminated.

    Args:
        gql_client: A GraphQL client to perform queries and mutations.

    Returns:
        Successful termination, if empty manager roles are found, or None.
    """
    logger.info(
        "Initialising search for managers with no engagements or persons associated with the role."
    )
    manager_objects = await get_managers(gql_client)

    # Get the manager roles uuids, if no person og engagements are associated with the manager.
    manager_uuids_with_no_engagements = extract_managers_with_no_persons_or_engagements(
        manager_objects
    )

    # No manager roles without engagements or persons associated found. Exit.
    if not manager_uuids_with_no_engagements:
        logger.info(
            "No manager roles without a person or engagements associated found."
        )
        return

    # Found empty managers.
    await terminate_existing_empty_manager_roles(
        gql_client, manager_uuids_with_no_engagements
    )
    logger.info(
        "Terminated empty manager(s) with uuid(s):",
        manager_uuids=manager_uuids_with_no_engagements,
    )
