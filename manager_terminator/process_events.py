# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from raclients.graph.client import GraphQLClient

from manager_terminator.config import get_settings
from manager_terminator.helper_functions import check_for_end_date
from manager_terminator.helper_functions import get_end_date_in_manager_object
from manager_terminator.helper_functions import (
    get_latest_engagement_date_and_check_for_same_org_unit,
)
from manager_terminator.mutations_made_to_mo import terminate_manager
from manager_terminator.queries_made_to_mo import get_engagement_objects

logger = structlog.get_logger(__name__)
settings = get_settings()


async def process_engagement_events(
    gql_client: GraphQLClient, engagement_uuid: UUID
) -> None:
    """
    A function for handling the various events made involving a manager.
    This includes checking whether the persons engagement is active or
    has been ended, and whether the person assigned as the organisational
    manager, also has an end date that matches the persons engagements end date.

    Args:
        gql_client: A GraphQL client to perform the various queries

        engagement_uuid: UUID of the engagement

    Returns:
        A successful termination of a manager position or None.
    """
    print("LISTENING ON AN EVENT")
    logger.info(
        "Listening on an engagement event with uuid:",
        engagement_uuid=engagement_uuid,
    )
    engagement_objects = None
    try:  # Make a Graphql query to pull the engagement and its possible objects from MO.
        engagement_objects = await get_engagement_objects(gql_client, engagement_uuid)

    except ValueError as exc:
        print(exc.args[0])
        logger.error("Engagement object not found:", exc.args[0])

    # Make Mypy happy.
    assert engagement_objects is not None

    # Person is not a manager, end the process.
    if len(engagement_objects["employee"][0]["manager_roles"]) == 0:
        print("Person is not a manager. Exit event.")
        logger.info("The person is not a manager. Event exited.")
        return

    # The engagement does not have an end date, exit event.
    if not check_for_end_date(engagement_objects["employee"][0]):
        print("No end dates found on the persons engagement(s). End event.")
        return

    # Check for the managers end date. If the manager is in the same org unit as the engagement,
    # get the managers UUID.
    manager_uuid = get_end_date_in_manager_object(engagement_objects["employee"][0])

    # If manager role exists in same org unit as the engagement.
    if manager_uuid:
        # Get the farthest engagement end date, to terminate manager role on.
        farthest_engagement_date_retrieved = (
            get_latest_engagement_date_and_check_for_same_org_unit(
                engagement_objects["employee"][0],
            )
        )

        # If None, the manager role will be terminated before the engagement end date.
        if farthest_engagement_date_retrieved is None:
            print("Manager will be terminated before farthest engagement. End event.")
            return

        try:
            await terminate_manager(
                gql_client, UUID(manager_uuid), farthest_engagement_date_retrieved
            )
            return

        except ValueError as exc:
            print(exc.args)
            logger.error(
                "Engagement end date, manager end date or common org unit uuid not found:",
                exc.args,
            )

    # Manager is supposedly being terminated before an active engagement ends - do nothing.
    else:
        print(
            "The manager role might not exist in the same org unit as the engagement being"
            "created/updated/terminated."
        )
        logger.error("An error occurred.")
