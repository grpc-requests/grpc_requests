#!/bin/bash

# Run this script before commits to count the number of flake8 errors and
# and ensure tests are passing.

ruff check src/grpc_requests/*.py src/tests/*.py --statistics --config ruff.toml

ruff format src/grpc_requests/*.py src/tests/*.py --check --config ruff.toml

pytest --cov-report=xml --cov=src/grpc_requests

# Wily Metrics - file by file for now
wily report src/grpc_requests/client.py -n 1 difficulty effort complexity volume
wily report src/grpc_requests/aio.py -n 1 difficulty effort complexity volume
wily report src/grpc_requests/utils.py -n 1 difficulty effort complexity volume
