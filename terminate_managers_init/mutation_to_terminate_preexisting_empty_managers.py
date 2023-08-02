# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime

from raclients.graph.client import GraphQLClient

from manager_terminator.mutations_made_to_mo import MUTATION_TERMINATE_MANAGER


async def terminate_existing_empty_manager_roles(
    gql_client: GraphQLClient, empty_manager_uuids: list
):
    """
    Terminate a manager.

    Args:
        gql_client: The GraphQL client to perform the mutation.
        empty_manager_uuids: List of UUIDs for managers being terminated.

    Returns:
        A successful termination of a manager.
    """
    for manager_uuid in empty_manager_uuids:
        terminate_variables = {
            "input": {
                "uuid": str(manager_uuid),
                "to": datetime.date.today().isoformat(),
            }
        }

        await gql_client.execute(
            MUTATION_TERMINATE_MANAGER, variable_values=terminate_variables
        )
