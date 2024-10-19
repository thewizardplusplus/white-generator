PROJECT_NAME := white-generator

.PHONY: help lint test install uninstall build upload upload-test

help:
	@echo "Usage:"
	@echo "  make [options] <target>"
	@echo
	@echo "Options: see for the details \"man make\"."
	@echo
	@echo "Targets:"
	@echo "  help         Show this help message."
	@echo "  lint         Run the linter."
	@echo "  test         Run the unit tests."
	@echo "  install      Install the project package."
	@echo "  uninstall    Uninstall the project package."
	@echo "  build        Generate distribution archives."
	@echo "  upload       Upload the distribution archives to https://pypi.org/."
	@echo "  upload-test  Upload the distribution archives to https://test.pypi.org/."

lint:
	mypy "$$(echo "$(PROJECT_NAME)" | tr "-" "_")"

test:
	python3 -m unittest discover --pattern '*_test.py'

install:
	python3 -m pip install .

uninstall:
	python3 -m pip uninstall --yes "$(PROJECT_NAME)"

build:
	python3 -m build
	python3 -m twine check dist/*

upload: uninstall
	python3 -m twine upload dist/*
	python3 -m pip install --no-deps "$(PROJECT_NAME)"

upload-test: uninstall
	python3 -m twine upload --repository testpypi dist/*
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps "$(PROJECT_NAME)"
