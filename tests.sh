#!/bin/bash

flake8 . --count  --statistics
pytest --cov-report=xml --cov=src/grpc_requests
