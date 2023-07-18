# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime


from gql import gql
from raclients.graph.client import GraphQLClient


async def terminate_existing_empty_manager_roles(gql_client: GraphQLClient, empty_manager_uuids: list):
    mutation = gql(
        """
        mutation ($input: ManagerTerminateInput!) {
          manager_terminate(input: $input) {
            uuid
          }
        }
        """
    )

    for manager_uuid in empty_manager_uuids:
        terminate_variables = {
            "input": {
                "uuid": str(manager_uuid),
                "to": datetime.date.today().isoformat(),
            }
        }

        await gql_client.execute(mutation, variable_values=terminate_variables)
