#!/bin/bash

PYTHONPATH="/tdp" python3 /tdp/tdp_server/initialize_database.py

exec "$@"
