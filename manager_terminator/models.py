# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from uuid import UUID

from pydantic import BaseModel


class InvalidManagerPeriod(BaseModel):
    uuid: UUID
    from_: datetime.datetime
    to: datetime.datetime
