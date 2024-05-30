## Globals
PROJECT_NAME = varimax_interventions
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python


## Commands
.PHONY: app
app:
	streamlit run app/app.py

.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip freeze > env/requirements.txt

.PHONY: test
test:
	$(PYTHON_INTERPRETER) -m unittest discover

.PHONY: venv
venv:
	$(PYTHON_INTERPRETER)$(PYTHON_VERSION) -m venv ".venv"
	. .venv/bin/activate
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r env/requirements.txt

.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: update_readmes
update_readme:
	$(PYTHON_INTERPRETER) workflows/update_readmes.py

## Help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
