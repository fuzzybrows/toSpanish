VENV=.venv
.PHONY: requirements.txt .venv pip_sync clean test test-verbose test-coverage test-with-coverage

requirements.txt:
		source $(VENV)/bin/activate && pip-compile --no-emit-index-url --output-file requirements.txt requirements.in

clean:
	rm -rf $(VENV)

setup: clean .venv pip_sync
	pip install -r requirements.txt && \
	source $(VENV)/bin/activate


pip_sync: requirements.txt
	source $(VENV)/bin/activate && pip-sync requirements.txt

.venv:
	command -v deactivate && deactivate || true
	python -m venv $(VENV)

run:
	source $(VENV)/bin/activate && uvicorn app.server:app --port 8000


migration:
	@if test -z "$(filter-out migration,$(MAKECMDGOALS))"; then \
		echo "no migration message provided: make migration \"migration message\""; \
		exit 1; \
	fi
	source .venv/bin/activate && alembic revision --autogenerate -m "$(filter-out migration,$(MAKECMDGOALS))"

migrate:
	source .venv/bin/activate && alembic upgrade head

test:
	source $(VENV)/bin/activate && pytest

test-verbose:
	source $(VENV)/bin/activate && pytest -v

test-coverage:
	source $(VENV)/bin/activate && pytest --cov=app

test-with-coverage:
	./scripts/run_tests.sh
