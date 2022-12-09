# source: https://github.com/python-poetry/poetry/discussions/1879
FROM python:3.6.15-slim-bullseye as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.15 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    # Change ansible local temp
    ANSIBLE_LOCAL_TEMP=/tmp


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `base` stage is used as base for every steps
FROM python-base as base
RUN apt-get update \
    # deps for building tdp-lib (pyproject.tml dependency is a git dependency), and used at runtime
    && apt-get install --no-install-recommends -y git


# `builder-base` stage is used to build deps + create our virtual environment
FROM base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev --extras pg

# `production` image used for runtime
FROM base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN pip install uvicorn[standard]
COPY ./tdp_server /tdp/tdp_server/
COPY ./alembic.ini /tdp/alembic.ini
COPY docker/.env-container /tdp/.env
COPY docker/entrypoint.sh /entrypoint.sh
WORKDIR /tdp
ENTRYPOINT ["bash", "/entrypoint.sh"]
CMD ["uvicorn", "--host", "0.0.0.0", "tdp_server.main:app"]
