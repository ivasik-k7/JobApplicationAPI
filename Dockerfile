ARG PYTHON_VERSION=3.11.3

FROM python:${PYTHON_VERSION}-slim as base

ARG SERVER_ENV="development"

LABEL maintainer="ivan.kovtun@capgemini.com"

ENV SERVER_ENV=${SERVER_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    tree \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN pip install "poetry==$POETRY_VERSION" && poetry --version

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock 



RUN poetry config virtualenvs.create false && \
    if [ "${SERVER_ENV}" = "development" ]; then \
    poetry install; \
    else \
    poetry install --no-dev; \
    fi && \
    rm -rf $POETRY_CACHE_DIR


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]