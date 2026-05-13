# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
test:
    docker compose down
    docker compose build --no-cache
    docker compose up -d
    docker compose stop terminator
    docker compose run --rm terminator pytest
test-integration:
    docker compose down
    docker compose build --no-cache
    docker compose up -d
    docker compose stop terminator
    docker compose run --rm terminator pytest tests/integration
