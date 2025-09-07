# Tests for toSpanish

This directory contains tests for the toSpanish application.

## Structure

The tests are organized as follows:

- `conftest.py`: Contains pytest fixtures used across multiple test files
- `unit/`: Contains unit tests
  - `models/`: Tests for data models
  - `api/`: Tests for API endpoints
  - `service/`: Tests for service functions
  - `test_database.py`: Tests for database functions
  - `test_settings.py`: Tests for application settings
  - `test_server.py`: Tests for the FastAPI application setup
- `integration/`: Contains integration tests
  - `test_app_integration.py`: Tests that verify the application works as a whole

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/unit/models/test_songs.py
```

To run tests with verbose output:

```bash
pytest -v
```

To run tests with coverage report:

```bash
pytest --cov=app
```

## Writing New Tests

When writing new tests:

1. Place them in the appropriate directory based on what they're testing
2. Follow the naming convention: `test_*.py` for test files and `test_*` for test functions
3. Use fixtures from `conftest.py` where appropriate
4. Mock external dependencies to avoid making actual API calls or file operations during testing
