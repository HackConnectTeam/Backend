ARG PYTHON_VERSION=3.12
ARG DEBIAN_CODENAME=bookworm
FROM python:${PYTHON_VERSION}-${DEBIAN_CODENAME} AS dev

ARG APP_HOME=/opt/project
ARG VIRTUAL_ENV=/opt/.venv
ARG UV_VERSION=0.5.14
ARG HOME=/home/root

ENV PATH="$HOME/.local/bin:${VIRTUAL_ENV}/bin:$PATH" \
    UV_PROJECT_ENVIRONMENT=${VIRTUAL_ENV} \
    UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_REQUEST_TIMEOUT=1000

# Crete folder for the project
WORKDIR ${APP_HOME}

# Install apt dependencies if needed
RUN apt-get update && \
    apt-get install -y curl git postgresql-client build-essential libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Installl uv
RUN wget -qO- https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Create virtual environment and install dependencies
RUN uv venv ${VIRTUAL_ENV} && \
    uv sync --frozen