# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import json

import structlog
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastramqpi.main import FastRAMQPI
from ramqp.depends import RateLimit
from ramqp.mo import MORouter
from ramqp.mo import PayloadUUID
from starlette.status import HTTP_200_OK

import manager_terminator.engagements as engagements
import manager_terminator.managers as managers
from manager_terminator import depends
from manager_terminator.autogenerated_graphql_client import GraphQLClient
from manager_terminator.config import get_settings
from manager_terminator.log import setup_logging

# from manager_terminator.process_events import process_engagement_events


amqp_router = MORouter()
fastapi_router = APIRouter()

logger = structlog.get_logger(__name__)


@fastapi_router.post("/initiate/terminator/", status_code=HTTP_200_OK)
async def initiate_terminator(mo: depends.GraphQLClient, dryrun: bool = False):
    """
    This function serves as an initiator to be run first upon initiating the main
    application - the listener.
    When this functions endpoint has been called, any current manager roles
    without an active engagement or a person attached to the role, will be terminated.

    Args:
        mo: A MO client used to perform various queries and mutations in MO.
    """

    manager_objects = await managers.get(mo)
    manager_invalid_periods = await managers.invalid_manager_periods(manager_objects)
    if len(manager_invalid_periods) < 1:
        logger.info("No invalid manager periods found.")
        return

    logger.info(
        "Found invalid manager periods:",
        manager_invalid_periods=json.dumps(jsonable_encoder(manager_invalid_periods)),
    )

    if dryrun:
        return

    terminated_invalid_manager_periods = await managers.terminate_manager_periods(
        mo, manager_invalid_periods
    )

    logger.info(
        "Terminated invalid periods for manager(s): %s"
        % json.dumps(jsonable_encoder(terminated_invalid_manager_periods))
    )


@amqp_router.register("engagement")
async def engagement_event_handler(
    mo: depends.GraphQLClient,
    engagement_uuid: PayloadUUID,
    _: RateLimit,
):
    # Get all engagement objects related to the engagement-event
    engagement_objects = await engagements.get_by_uuid(mo, engagement_uuid)
    if len(engagement_objects) < 1:
        logger.error("No engagement objects found for", engagement_uuid)
        return

    # Go through engagments and collect all unique engagement employee-uuids
    employee_uuids = {
        employee.uuid
        for engagement in engagement_objects
        for employee in engagement.person
    }

    # Fetch all manager objects related to the engagement employee-uuids
    employee_manager_objects = await managers.get_by_employee_uuids(
        mo, list(employee_uuids)
    )
    if len(employee_manager_objects) < 1:
        logger.error(
            "No manager objects found for employees", employee_uuids=employee_uuids
        )
        return

    # Find invalid manager periods
    manager_invalid_periods = await managers.invalid_manager_periods(
        employee_manager_objects
    )
    if len(manager_invalid_periods) < 1:
        logger.info("No invalid manager periods found.")
        return

    logger.info(
        "Found invalid manager periods:",
        manager_invalid_periods=json.dumps(jsonable_encoder(manager_invalid_periods)),
    )

    # Terminate invalid manager periods
    terminated_invalid_manager_periods = await managers.terminate_manager_periods(
        mo, manager_invalid_periods
    )

    logger.info(
        "Terminated invalid periods for manager(s): %s"
        % json.dumps(jsonable_encoder(terminated_invalid_manager_periods))
    )


def create_fastramqpi(**kwargs) -> FastRAMQPI:
    settings = get_settings(**kwargs)
    setup_logging(settings.log_level)

    fastramqpi = FastRAMQPI(
        application_name="os2mo-manager-terminator",
        settings=settings.fastramqpi,
        graphql_client_cls=GraphQLClient,
    )

    amqpsystem = fastramqpi.get_amqpsystem()
    amqpsystem.router.registry.update(amqp_router.registry)

    app = fastramqpi.get_app()
    app.include_router(fastapi_router)

    return fastramqpi


def create_app(**kwargs) -> FastAPI:
    fastramqpi = create_fastramqpi(**kwargs)
    return fastramqpi.get_app()
