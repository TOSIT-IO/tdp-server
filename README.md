# TDP SERVER

`tdp-server` provides a server to interact with [`tdp-lib`](https://github.com/tOSIT-IO/tdp-lib).

A full beginers guide to launch a testing server is provided at [`docs/quick-start.md`](./docs/quick-start.md).

## Requirements

The server is made with Python. The following is required:

- [Python](https://www.python.org/) `^3.9`
- [Poetry](https://python-poetry.org/) `1.1.15`
- A RDBMS, to store deployment history (e.g. [PostgresQL](https://www.postgresql.org/))
- An identity management system, for authentication purposes (e.g. [Keycloak](https://www.keycloak.org/))

### Dev environment

A dev/testing environment using Keycloak and PostgreSQL is provided through `docker-compose`:

```bash
docker-compose -f dev/docker-compose.yml up -d
```

## Installation

1. Use Poetry to download and install the required Python dependencies:
   ```bash
   poetry install
   ```
1. Define the required environment variables in an `.env` file. An example file is provided in `dev/.env-dev`:
   ```bash
   cp dev/.env-dev .env
   ```

   In particular:

   - `DATABASE_DSN`: the data source name of the RDBMS.
   - `TDP_COLLECTION_PATH`: the path to one or more TDP collection, separated by `:` (as [`tdp-collection`](https://github.com/TOSIT-IO/tdp-collection) and [`tdp-collection-extras`](https://github.com/TOSIT-IO/tdp-collection-extras)).
   - `TDP_VARS`: the path to an empty directory where the `tdp_vars` will be stored and versioned.
   - `TDP_RUN_DIRECTORY`: the path to the directory where the Ansible command will be launched (as [`tdp-getting-started`](https://github.com/tOSIT-IO/tdp-getting-started) for example).
   _Note: the `ansible.cfg` file of the working directory must contain the path of the `tdp_vars` directory defined previously._
1. Initialize the database and the `tdp_vars` directory:
   ```bash
   python tdp_server/initialize_database.py
   python tdp_server/initialize_tdp_vars.py
   ```

## Usage

Start the server using:

```bash
uvicorn tdp_server.main:app --reload
```

## Build Docker Container

```bash
docker build -t tdp_server -f docker/Dockerfile .
```

## Run Docker Container

Executing the container with the minimal configuration variables:

```bash
docker run \
  -e TDP_COLLECTION_PATH="/tdp/ops/tdp/ansible/ansible_collections/tosit/tdp" \
  -e TDP_RUN_DIRECTORY="/tdp/ops" \
  -e TDP_VARS="/tdp/ops/inventory/tdp_vars" \
  -e DATABASE_DSN=sqlite:////tdp/sqlite.db \
  -e OPENID_CONNECT_DISCOVERY_URL="http://host.docker.internal:8080/auth/realms/tdp_server/.well-known/openid-configuration" \
  -e OPENID_CLIENT_ID=tdp_server \
  -e OPENID_CLIENT_SECRET=secret \
  -v "..../sqlite.db:/tdp/sqlite.db" \
  -v"..../tdp-ops:/tdp/ops" \
  -p 8000:8000 \
  tdp_server
```

N.B.: Mounting a sqlite database is not the recommended way to persist the server's data.

### Accessing the REST API

A token must be provided to access the API. Tokens can be obtained using the `get_token.py` script.

For example, using `curl`:

```bash
token=$(python get_token.py)
curl -H "Authorization: Bearer $token" http://localhost:8000/api/v1/service/
```

### Accessing the API documentation pages

Documentation pages of the API are available at:

- OpenAPI UI <http://localhost:8000/docs>
- ReDoc UI <http://localhost:8000/redoc>

## Contributing

`tdp-server` uses [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to enforce consistency in the code and commit messages.

Use Poetry to install the hooks:

```bash
poetry run pre-commit install --hook-type pre-commit
poetry run pre-commit install --hook-type commit-msg
```

The following environment variables can be used to ease development:

- `DO_NOT_USE_IN_PRODUCTION_DISABLE_TOKEN_CHECK`
- `MOCK_DEPLOY`
