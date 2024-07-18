#!/bin/bash

# This script generated a simplified complexity report for a given series of
# Python files, or for non-__init__.py files in the src/grpc_requests directory
# if no arguments are provided.

# Radon is used to generate the average Cyclomatic Complexity, Maintainability
# Index, and Halstead difficulty and effort metrics for the given files.

# This report is meant as a quick guide to possible weaknesses in the codebase
# and not meant as a make or break test for work being undertaken.

# Cyclomatic Complexity - Lower is better
# Maintainability Index - Higher is better
# Halstead difficulty - Lower is better
# Halstead effort - Lower is better

if ! command -v radon &> /dev/null; then
    echo "radon is not installed. Please make sure you have installed the requirements-dev.txt."
    exit 1
fi

if [ "$#" -eq 0 ]; then
    TARGETS=$(find src/grpc_requests/ -name "*.py" ! -name "__init__.py")
else
    TARGETS="${*}"
fi

for TARGET in $TARGETS; do
    echo "Report for $TARGET"
    echo "===================="
    radon cc "$TARGET" -n F -s --total-average | grep "Average" | sed "s|Average complexity|Cyclomatic Complexity|"
    radon mi "$TARGET" -s | sed "s|$TARGET|Maintainability Index|"
    radon hal "$TARGET" | grep -E "difficulty|effort" | sed "s/^[ \t]*//"
    echo "===================="
    echo
done