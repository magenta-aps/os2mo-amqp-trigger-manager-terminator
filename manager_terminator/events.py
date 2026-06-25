# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import json
from uuid import UUID

import structlog
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastramqpi.events import Event

from manager_terminator import depends
from manager_terminator import engagements
from manager_terminator import managers

logger = structlog.stdlib.get_logger()

events_router = APIRouter()


@events_router.post("/events/engagement")
async def _engagement_event(
    gql_client: depends.GraphQLClient, settings: depends.Settings, event: Event[UUID]
) -> None:
    logger.info("Received engagement event", engagement_event=event.dict())

    engagement_uuid = event.subject

    # Get all engagement objects related to the engagement-event
    engagement_objects = await engagements.get_by_uuid(gql_client, engagement_uuid)
    if len(engagement_objects) < 1:  # pragma: no cover
        logger.error("No engagement objects found for", engagement_uuid=engagement_uuid)
        return

    # Go through engagments and collect all unique engagement employee-uuids
    employee_uuids = {
        employee.uuid
        for engagement in engagement_objects
        for employee in engagement.person_response.validities
    }

    # Fetch all manager objects related to the engagement employee-uuids
    employee_manager_objects = await managers.get_by_employee_uuids(
        gql_client, list(employee_uuids)
    )
    if len(employee_manager_objects) < 1:  # pragma: no cover
        logger.error(
            "No manager objects found for employees", employee_uuids=employee_uuids
        )
        return

    # Find invalid manager periods
    manager_invalid_periods = managers.invalid_manager_periods(employee_manager_objects)
    if len(manager_invalid_periods) < 1:
        logger.info("No invalid manager periods found.")
        return

    logger.info(
        "Found invalid manager periods:",
        manager_invalid_periods=json.dumps(jsonable_encoder(manager_invalid_periods)),
    )

    # Terminate invalid manager periods
    if settings.manager_terminator.set_to_vacant:
        updated_invalid_manager_periods = await managers.update_manager_to_vacant(
            gql_client, manager_invalid_periods
        )

        logger.info(
            "Updated invalid periods for manager(s) to vacant:",
            updated_invalid_manager_periods=json.dumps(
                jsonable_encoder(updated_invalid_manager_periods)
            ),
        )

    else:
        terminated_invalid_manager_periods = await managers.terminate_manager_periods(
            gql_client, manager_invalid_periods
        )

        logger.info(
            "Terminated invalid periods for manager(s):",
            terminated_invalid_manager_periods=json.dumps(
                jsonable_encoder(terminated_invalid_manager_periods)
            ),
        )
