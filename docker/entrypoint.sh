#!/bin/bash

PYTHONPATH="/tdp" python3 /tdp/tdp_server/pre_start.py
PYTHONPATH="/tdp" python3 /tdp/tdp_server/initialize_database.py

exec "$@"
