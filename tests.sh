#!/bin/bash

# Run this script before commits to count the number of flake8 errors and
# and ensure tests are passing.

ruff check src/grpc_requests/*.py src/tests/*.py --statistics

ruff format src/grpc_requests/*.py src/tests/*.py --check

pytest --cov-report=xml --cov=src/grpc_requests