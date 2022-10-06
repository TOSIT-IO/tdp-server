# Quick-start

This guide walks you through the deployment of a TDP server, based on [`tdp-collection`](https://github.com/TOSIT-IO/tdp-collection/). For testing purpose, we'll use [SQLite](https://www.sqlite.org/index.html), a single-file database, and no authentication.

For a more feature-rich testing environment, please use the provided [`docker-compose.yml`](../dev/).

## Requirements

- Installing [Python 3.7](https://www.python.org/downloads/release/python-3714/), using [pyenv](https://github.com/pyenv/pyenv) for example.
- Installing [Poetry](https://python-poetry.org/) to manage Python dependencies.
- Installing [SQLite3](https://www.sqlite.org/index.html).

## Installation

1. Clone the `tdp-server`, `tdp-collection` and `tdp-getting-started` repositories:
   ```bash
   git clone https://github.com/TOSIT-IO/tdp-server.git
   git clone https://github.com/TOSIT-IO/tdp-collection.git
   git clone https://github.com/TOSIT-IO/tdp-getting-started.git
   ```
1. Create the following directories:

   - `server-deploy`, to hold the `tdp_vars` and the SQLite database.
   - `tdp_vars`, to configure and track the history of the `tdp_vars`

   ```bash
   mkdir -p server-deploy/tdp_vars
   ```
1. Add the path of the `tdp_vars` directory in the `Inventory` of the `tdp-getting-started/ansible.cfg` file.

   For example, using `vim tdp-getting-started/ansible.cfg`:

   ```toml
   # tdp-getting-started/ansible.cfg
   [defaults]
   # ...
   inventory = inventory/hosts,inventory/tdp_vars,../server-deploy/tdp_vars
   # ...
   ```
1. Move in the `tdp-server` directory:
   ```bash
   cd tdp-server
   ```
1. Tell Poetry to use Python 3.7:
   ```bash
   poetry env use python3.7
   ```
1. Install the required Python dependencies using Poetry:
   ```bash
   poetry install
   ```
1. Create the `.env` file from the provided example which can be found in the `dev` directory:
   ```bash
   cp dev/.env-dev .env
   ```
1. Set the following environment variable in the `.env` file.

   For example, using `vim .env`:

   ```txt
   # Database
   DATABASE_DSN=sqlite:///../server-deploy/tdp.db

   # TDP
   TDP_COLLECTION_PATH=../tdp-collection/
   TDP_RUN_DIRECTORY=../tdp-getting-started/
   TDP_VARS=../server-deploy/tdp_vars/

   # Dev
   DO_NOT_USE_IN_PRODUCTION_DISABLE_TOKEN_CHECK=True
   MOCK_DEPLOY=True
   ```
1. Initialize the SQLite database and the `tdp_vars` directory:
   ```bash
   python3.7 tdp_server/initialize_database.py
   python3.7 tdp_server/initialize_tdp_vars.py
   ```

These steps are only required the first time.

## Server launch

1. Open a terminal in the `tdp-server` directory.
1. Launch a Python 3.7 shell:
   ```bash
   poetry shell
   ```
1. Launch the server:
   ```bash
   uvicorn tdp_server.main:app --reload
   ```

## Usage

API is available at <http://localhost:8000/api/v1/service/>

API documentation pages can be found at:

- OpenAPI UI <http://localhost:8000/docs>
- ReDoc UI <http://localhost:8000/redoc>
