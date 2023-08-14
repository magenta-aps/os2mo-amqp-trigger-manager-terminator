# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from fastapi import APIRouter
from fastapi import FastAPI
from fastramqpi.main import FastRAMQPI
from ramqp.depends import Context
from ramqp.depends import RateLimit
from ramqp.mo import MORouter
from ramqp.mo import PayloadUUID
from starlette.requests import Request
from starlette.status import HTTP_204_NO_CONTENT

from manager_terminator.config import get_settings
from manager_terminator.log import setup_logging
from manager_terminator.process_events import process_engagement_events
from terminate_managers_init.init_manager_terminator import (
    terminator_initialiser,
)


amqp_router = MORouter()
fastapi_router = APIRouter()

logger = structlog.get_logger(__name__)


@fastapi_router.post("/initiate/terminator/", status_code=HTTP_204_NO_CONTENT)
async def initiate_terminator(request: Request):
    context = request.app.state.context
    graphql_session = context["graphql_session"]
    await terminator_initialiser(graphql_session)


@amqp_router.register("engagement")
async def listener(context: Context, engagement_uuid: PayloadUUID, _: RateLimit):
    """
    This function listens on changes made to:
    ServiceType - engagements

    We receive a payload, of type PayloadUUID, with content of:
    engagement_uuid - UUID of the engagement.

    Args:
        context: A GraphQL client to perform the various queries

        engagement_uuid: UUID of the engagement
    """
    graphql_session = context["graphql_session"]
    await process_engagement_events(graphql_session, engagement_uuid)


def create_fastramqpi(**kwargs) -> FastRAMQPI:
    settings = get_settings(**kwargs)
    setup_logging(settings.log_level)

    fastramqpi = FastRAMQPI(
        application_name="os2mo-manager-terminator", settings=settings
    )

    amqpsystem = fastramqpi.get_amqpsystem()
    amqpsystem.router.registry.update(amqp_router.registry)

    app = fastramqpi.get_app()
    app.include_router(fastapi_router)

    return fastramqpi


def create_app(**kwargs) -> FastAPI:
    fastramqpi = create_fastramqpi(**kwargs)
    return fastramqpi.get_app()
