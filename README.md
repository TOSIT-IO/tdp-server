# TDP Server

`tdp-server` provides a server to interact with [`tdp-lib`](https://github.com/tOSIT-IO/tdp-lib).

## Requirements

The server is made with Python. The following is required:

- [Python](https://www.python.org/) `3.9.5`
- [Poetry](https://python-poetry.org/) `1.7.1`

## Installation

Install the `tdp-server` dependencies in the pyproject.toml as follows:

```bash
poetry install
```

## Usage

Start the server as follows:

```bash
uvicorn tdp_server.main:app --reload
```

Swagger is on the following [url](http://localhost:8000/docs#/)
