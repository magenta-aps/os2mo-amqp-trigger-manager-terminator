# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = ZoneInfo("Europe/Copenhagen")
POSITIVE_INFINITY = datetime.datetime.max.replace(tzinfo=datetime.UTC)
