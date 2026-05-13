# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

"""
These are integration tests that exercise the time logic of this integration.
"""

import pytest


# TODO(@lorenzo, #68625): re-write this to use the event API directly, as this
#   is not a smoke test.
@pytest.mark.integration
async def test_double_engagement():
    """
    Tests the scenario where the same manager has multiple overlapping engagements,
    in this case we expect the manager validity to span the union of the engagements.
    """
    pass
