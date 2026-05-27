<!--
SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->
# Project: Manager Terminator

## Context
- This is an integration for the OS2mo application (https://github.com/OS2mo) that runs as a separate docker-compose service.
- This integration ensures that managers always have at least one engagement at all times, and terminates managers in the periods where they don't have any engagements.
- This integration is event-driven, it listens to events from OS2mo and triggers its validation logic

## Running Tests
- Unit tests are in `tests/`, except for any sub-directories, like `tests/integration/`, which is for integration tests
- Integration tests are in `tests/integration/`
- Integration tests require the MO stack to be running, you can clone it from: https://github.com/OS2mo
- Tests can be run using `just`
  - `just test` runs all tests
  - `just test-integration` runs only integration tests

## Boundaries
- If there are uncommitted changes, do not add them to commits you make. Either commit your changes separately, or if it isn't possible, ask me for permission to commit the existing changes.
