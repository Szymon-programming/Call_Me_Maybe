UV = uv

all: install

ARGS ?= --functions_definition data/input/functions_definition.json \
--input data/input/function_calling_tests.json

install:
	$(UV) sync

run:
	$(UV) run python -m src $(ARGS)

debug:
	$(UV) run python -m pdb -m src $(ARGS)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	$(UV) run flake8 src
	$(UV) run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) run flake8 src
	$(UV) run mypy src --strict

.PHONY: all install run debug clean lint lint-strict