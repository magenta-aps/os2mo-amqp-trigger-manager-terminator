# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from gql import gql
from raclients.graph.client import GraphQLClient

logger = structlog.get_logger(__name__)

MUTATION_TERMINATE_MANAGER = gql(
    """
    mutation ($input: ManagerTerminateInput!) {
      manager_terminate(input: $input) {
        uuid
      }
    }
    """
)


async def terminate_manager(
    gql_client: GraphQLClient, manager_uuid: UUID, termination_date: str
):
    """
    Terminate a manager.

    Args:
        gql_client: The GraphQL client to perform the mutation.
        manager_uuid: UUID of the manager being terminated.
        termination_date: The last date of the manager validity.

    Returns:
        A successful termination of a manager.
    """

    termination_variables = {
        "input": {
            "uuid": str(manager_uuid),
            "to": termination_date,
        }
    }
    await gql_client.execute(
        MUTATION_TERMINATE_MANAGER, variable_values=termination_variables
    )
