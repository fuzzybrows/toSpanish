VENV=.venv
.PHONY: requirements.txt .venv pip_sync clean

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