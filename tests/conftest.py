# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import logging

# httpcore spams the logs making them useless for debugging
logging.getLogger("httpcore").setLevel(logging.WARNING)
