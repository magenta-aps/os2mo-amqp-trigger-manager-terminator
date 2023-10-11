# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION="1.5.1" \
    POETRY_HOME=/opt/poetry \
    VIRTUAL_ENV="/venv" \
    FASTRAMQPI__MO_GRAPHQL_VERSION="17"
ENV PATH="$VIRTUAL_ENV/bin:$POETRY_HOME/bin:$PATH"

# Install poetry in an isolated environment
RUN python -m venv $POETRY_HOME \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

# Install project in another isolated environment
RUN python -m venv $VIRTUAL_ENV
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . ./

CMD ["uvicorn", "--factory", "manager_terminator.main:create_app", "--host", "0.0.0.0"]
