# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from fastramqpi.config import Settings as FastRAMQPISettings  # type: ignore
from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import Field


class ManagerTerminatorSettings(BaseModel):
    """Settings for the manager terminator AMQP trigger."""

    set_to_vacant: bool = False


class Settings(BaseSettings):
    log_level: str = "INFO"

    class Config:
        frozen = True
        env_nested_delimiter = "__"

    fastramqpi: FastRAMQPISettings
    manager_terminator: ManagerTerminatorSettings = ManagerTerminatorSettings()
    listen_to_changes_in_mo: bool = Field(
        default=True,
        description=(
            "Declare GraphQL event listeners and process MO changes as they "
            "happen. On by default; the integration is event-driven and does "
            "nothing useful without it. Disabled in tests that drive the "
            "event endpoints directly so background fetchers don't race them."
        ),
    )
