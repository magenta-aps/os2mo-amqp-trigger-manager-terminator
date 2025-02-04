# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from fastramqpi.config import Settings as FastRAMQPISettings  # type: ignore
from pydantic import BaseSettings
from pydantic import BaseModel
from pydantic import Field


class ManagerTerminatorSettings(BaseModel):
    """Settings for the manager terminator AMQP trigger."""

    log_level: str = "INFO"
    # set_to_vacant: bool = False


class Settings(BaseSettings):
    class Config:
        frozen = True
        env_nested_delimiter = "__"

    fastramqpi: FastRAMQPISettings
    manager_terminator: ManagerTerminatorSettings
