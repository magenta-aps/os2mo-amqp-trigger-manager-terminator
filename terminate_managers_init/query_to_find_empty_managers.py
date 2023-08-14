# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from gql import gql
from raclients.graph.client import GraphQLClient

logger = structlog.get_logger(__name__)

QUERY_GET_MANAGERS = gql(
    """
    query GetManagers {
      managers(from_date: null, to_date: null) {
        objects {
          objects {
            uuid
            org_unit {
              uuid
            }
            employee {
              engagements {
                uuid
                org_unit {
                  uuid
                }
                validity {
                  from
                  to
                }
              }
            }
            validity {
              from
              to
            }
          }
        }
      }
    }
    """
)


async def get_managers(gql_client: GraphQLClient) -> list:
    """
    Get manager roles.

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
        {'uuid': '0b51953c-537b-4bf9-a872-2710b0ddd9e3', 'org_unit': [
        {'uuid': '13f3cebf-2625-564a-bcfc-31272eb9bce2'}] 'employee': [
        {'engagements': [
        {'uuid': 'ef9f76fd-1840-4d94-961a-1140c86efd00', , 'org_unit': [
        {'uuid': '13f3cebf-2625-564a-bcfc-31272eb9bce2'}], 'validity': {
        'from': '1975-12-08T00:00:00+01:00', 'to': None}}]}
        ],
        'validity': {
        'from': '1975-12-08T00:00:00+01:00', 'to': None}}]}
        ,

        {'objects': [
        {'uuid': 'e4c99547-4a5b-4423-a1dc-2fc5b3b68c35', 'org_unit': [
        {'uuid': 'c9d51723-b777-5878-af66-30626e2f9d66'}], 'employee': None,
        'validity': {
        'from': '2023-07-18T00:00:00+02:00',
        'to': '2023-07-18T00:00:00+02:00'}}]}
        ]

    """
    response = await gql_client.execute(QUERY_GET_MANAGERS)
    return response["managers"]["objects"]
