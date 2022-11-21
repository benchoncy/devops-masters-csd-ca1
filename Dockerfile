FROM python:3.10.8-slim as base

ENV PORT=8080

# poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME="/opt/poetry"
ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN adduser --system --no-create-home app

# Build initial dependancies
FROM base as builder

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl build-essential

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-ansi --only main


# Development setup
FROM base as development
WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install
RUN playwright install
WORKDIR /app

EXPOSE 5000
CMD [ "flask", "--app", "bpcalc", "--debug", "run", "--host", "0.0.0.0" ]


# Production setup
FROM base as production

ENV OTEL_RESOURCE_ATTRIBUTES='service.name=bpcalc'

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY ./bpcalc /app/bpcalc
WORKDIR /app

USER app

EXPOSE $PORT
CMD [ "opentelemetry-instrument", "gunicorn", "-w", "3", "bpcalc:app" ]