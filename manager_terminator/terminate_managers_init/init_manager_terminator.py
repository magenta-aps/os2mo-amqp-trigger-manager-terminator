# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog

from manager_terminator.autogenerated_graphql_client import GraphQLClient
from manager_terminator.terminate_managers_init.find_no_engagement_managers import (
    extract_managers_with_no_persons_or_engagements,
)

logger = structlog.get_logger(__name__)


async def terminator_initialiser(mo: GraphQLClient) -> None:
    """
    Function that will look for any empty manager roles - if any are found,
    they will be terminated.

    Args:
        mo: A MO client to perform queries and mutations.

    Returns:
        Successful termination, if empty manager roles are found, or None.
    """
    logger.info(
        "Initialising search for managers with no engagements or persons associated with the role."
    )
    manager_objects_as_models = await mo.get_managers()

    manager_objects = manager_objects_as_models.objects

    # Get the manager roles uuids and the termination dates, if no person or
    # engagements are associated with the manager.
    list_of_manager_uuids_and_termination_dates = (
        extract_managers_with_no_persons_or_engagements(manager_objects)
    )

    # No manager roles without engagements or persons associated found. Exit.
    if not list_of_manager_uuids_and_termination_dates:
        logger.info(
            "No manager roles without a person or engagements associated found."
        )
        return

    # Found empty managers.
    for manager_to_terminate in list_of_manager_uuids_and_termination_dates:
        manager_uuid = manager_to_terminate.get("uuid")
        termination_date = manager_to_terminate.get("termination_date")

        await mo.terminate_manager(termination_date, manager_uuid)  # type: ignore

    logger.info(
        "Terminated empty manager(s) with uuid(s):",
        manager_uuids=list_of_manager_uuids_and_termination_dates,
    )
