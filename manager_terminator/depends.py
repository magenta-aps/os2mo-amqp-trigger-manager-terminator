# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Annotated

from fastapi import Depends
from ramqp.depends import from_context

from autogenerated_graphql_client import GraphQLClient as _GraphQLClient

GraphQLClient = Annotated[_GraphQLClient, Depends(from_context("graphql_client"))]