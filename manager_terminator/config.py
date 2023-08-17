# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from fastramqpi.config import Settings as FastRAMQPISettings  # type: ignore
from pydantic import BaseSettings
from pydantic import Field


class ManagerTerminatorSettings(BaseSettings):
    """Settings for the manager terminator AMQP trigger."""

    log_level: str = "INFO"

    class Config:
        """Settings are frozen."""

        frozen = True
        env_nested_delimiter = "__"

    fastramqpi: FastRAMQPISettings = Field(
        default_factory=FastRAMQPISettings, description="FastRAMQPI settings."
    )


def get_settings(*args, **kwargs) -> ManagerTerminatorSettings:
    return ManagerTerminatorSettings(*args, **kwargs)
