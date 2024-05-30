## Globals
PROJECT_NAME = varimax_interventions
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

## Commands
# Locally host app
.PHONY: app
app:
	streamlit run tools/distributions/gui/app/main.py

## Help
# Display all rules
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n# (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
