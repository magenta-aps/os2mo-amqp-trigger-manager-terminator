# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from raclients.graph.client import GraphQLClient

from manager_terminator.mutations_made_to_mo import MUTATION_TERMINATE_MANAGER


async def terminate_existing_empty_manager_roles(
    gql_client: GraphQLClient, manager_uuid: UUID, termination_date: str
):
    """
    Terminate a manager.

    Args:
        gql_client: The GraphQL client to perform the mutation.
        manager_uuid: UUID for manager being terminated.
        termination_date: Date for manager roles termination.

    Returns:
        A successful termination of a manager.
    """
    terminate_variables = {
        "input": {
            "uuid": str(manager_uuid),
            "to": termination_date,
        }
    }

    await gql_client.execute(
        MUTATION_TERMINATE_MANAGER, variable_values=terminate_variables
    )
