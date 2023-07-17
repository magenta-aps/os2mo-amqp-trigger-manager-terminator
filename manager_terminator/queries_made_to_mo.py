# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from gql import gql
from raclients.graph.client import GraphQLClient

logger = structlog.get_logger(__name__)


async def get_engagement_objects(gql_client: GraphQLClient, engagement_uuid: UUID):
    """
    Get the engagement from the event listener and all relevant objects within.

    Args:
        gql_client: The GraphQL client to perform the query.
        engagement_uuid: UUID of the engagement being edited or created.

    Returns:
        Engagement object consisting of all relevant information thereof.
    """
    query = gql(
        """
        query GetEngagementObjects($engagement_uuids: [UUID!]) {
          engagements(uuids: $engagement_uuids) {
            objects {
              objects {
                org_unit {
                  uuid
                  name
                }
                validity {
                  from
                  to
                }
                employee {
                  uuid
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
                  manager_roles {
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
              }
            }
          }
        }
        """
    )
    response = await gql_client.execute(
        query, variable_values={"engagement_uuids": str(engagement_uuid)}
    )

    return response["engagements"]["objects"][0]["objects"][0]
