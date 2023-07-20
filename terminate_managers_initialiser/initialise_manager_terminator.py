# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from raclients.graph.client import GraphQLClient

from terminate_managers_initialiser.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)
from terminate_managers_initialiser.mutation_to_terminate_preexisting_empty_managers import (
    terminate_existing_empty_manager_roles,
)
from terminate_managers_initialiser.query_to_find_empty_managers import (
    get_empty_managers,
)

logger = structlog.get_logger(__name__)


async def terminator_initialiser(gql_client: GraphQLClient):
    """
    Function that will look for any empty manager roles - if any are found,
    they will be terminated.

    Args:
        gql_client: A GraphQL client to perform queries and mutations.

    Returns:
        Successful termination, if empty manager roles are found, or None.
    """
    print(
        "Initialising search for managers with no engagements or persons associated with the role."
    )
    try:
        manager_objects = await get_empty_managers(gql_client)

        # Get the manager roles uuids, if no person og engagements are associated with the manager.
        manager_uuids_with_no_engagements = (
            extract_managers_with_no_persons_or_engagements(manager_objects)
        )

        # No manager roles without engagements or persons associated found. Exit.
        if not manager_uuids_with_no_engagements:
            print("No manager roles without a person or engagements associated found.")
            return None

        # Found empty managers, if list is not None.
        if manager_uuids_with_no_engagements:
            await terminate_existing_empty_manager_roles(
                gql_client, manager_uuids_with_no_engagements
            )
            print("Successfully terminated empty managers.")
            logger.info(
                "Terminated empty manager(s) with uuid(s):",
                manager_uuids=manager_uuids_with_no_engagements,
            )
            return None

    except ValueError as exc:
        print("Something went wrong:", exc.args)
    print("Done.")
    return None
