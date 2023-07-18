# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from gql import gql
from raclients.graph.client import GraphQLClient

logger = structlog.get_logger(__name__)


async def get_empty_managers(gql_client: GraphQLClient) -> list:
    """
    Get empty manager roles.

    Args:
        gql_client: The GraphQL client to perform the query

    Returns:
        A list of current manager objects consisting of:
        The managers UUID.
        The persons UUID associated with the manager role.
        The persons engagement UUID associated with the manager role.

    Example:
        [
        {'objects': [
        {'uuid': '0b51953c-537b-4bf9-a872-2710b0ddd9e3', 'employee': [
        {'engagements': [
        {'uuid': 'ef9f76fd-1840-4d94-961a-1140c86efd00'}]}]}]},

        {'objects': [
        {'uuid': 'e4c99547-4a5b-4423-a1dc-2fc5b3b68c35', 'employee': None}]}
        ]

    """
    query = gql(
        """
        query GetEmptyManagers {
          managers {
            objects {
              objects {
                uuid
                employee {
                  engagements{
                    uuid
                  }
                }
                validity {
                  to
                }
              }
            }
          }
        }
        """
    )
    response = await gql_client.execute(query)

    return response["managers"]["objects"]
