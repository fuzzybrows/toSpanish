#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run the tests with coverage report
pytest --cov=app --cov-report=term-missing

# Return the exit code of the tests
exit $?