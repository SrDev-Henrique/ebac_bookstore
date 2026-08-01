# `python-base` sets up all our shared environment variables
FROM python:3.13-alpine AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.4.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder

RUN apk add --no-cache \
        curl \
        build-base \
        libpq-dev \
        musl-dev

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --only main \
    && pip install --upgrade setuptools \
    && pip install psycopg2

FROM python-base AS runtime

ENV PATH="$VENV_PATH/bin:$PATH"

RUN apk add --no-cache libpq

COPY --from=builder $VENV_PATH $VENV_PATH

WORKDIR /app
COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
