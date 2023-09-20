# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from fastapi import APIRouter
from fastapi import FastAPI
from fastramqpi.main import FastRAMQPI
from ramqp.depends import RateLimit
from ramqp.mo import MORouter
from ramqp.mo import PayloadUUID
from starlette.status import HTTP_204_NO_CONTENT

from manager_terminator import depends
from manager_terminator.autogenerated_graphql_client import GraphQLClient
from manager_terminator.config import get_settings
from manager_terminator.log import setup_logging
from manager_terminator.process_events import process_engagement_events
from manager_terminator.terminate_managers_init.init_manager_terminator import (
    terminator_initialiser,
)


amqp_router = MORouter()
fastapi_router = APIRouter()

logger = structlog.get_logger(__name__)


@fastapi_router.post("/initiate/terminator/", status_code=HTTP_204_NO_CONTENT)
async def initiate_terminator(mo: depends.GraphQLClient):
    """
    This function serves as an initiator to be run first upon initiating the main
    application - the listener.
    When this functions endpoint has been called, any current manager roles
    without an active engagement or a person attached to the role, will be terminated.

    Args:
        mo: A MO client used to perform various queries and mutations in MO.
    """
    await terminator_initialiser(mo)


@amqp_router.register("engagement")
async def listener(
    mo: depends.GraphQLClient,
    engagement_uuid: PayloadUUID,
    _: RateLimit,
):
    """
    This function listens on changes made to:
    ServiceType - engagements

    We receive a payload, of type PayloadUUID, with content of:
    engagement_uuid - UUID of the engagement.

    Args:
        mo: A MO client used to perform various queries in MO.
        engagement_uuid: UUID of the engagement
        _: Ratelimit, does not need to be set
    """
    await process_engagement_events(mo, engagement_uuid)


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
