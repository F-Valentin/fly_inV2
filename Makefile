PYTHON = python3
MAIN = srcs/fly_in.py

.PHONY: install run debug clean lint lint-strict

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	flake8 srcs/
	mypy srcs/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 srcs/*.py
	mypy srcs/ --strict
