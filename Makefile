PROJECT_NAME := white-generator

.PHONY: help lint test install

help:
	@echo "Usage:"
	@echo "  make [options] <target>"
	@echo
	@echo "Options: see for the details \"man make\"."
	@echo
	@echo "Targets:"
	@echo "  help     Show this help message."
	@echo "  lint     Run the linter."
	@echo "  test     Run the unit tests."
	@echo "  install  Install the project package."

lint:
	mypy "$$(echo "$(PROJECT_NAME)" | tr "-" "_")"

test:
	python3 -m unittest discover --pattern '*_test.py'

install:
	python3 -m pip install .
