#!/bin/bash

python tdp_server/pre_start.py

alembic upgrade head
