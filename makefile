start:
	bash ./src/scripts/start.sh

seed:
	PYTHONPATH=src uv run python -m lib.seed

test:
	bash src/scripts/check-coverage.sh

precommit-install:
	uv run pre-commit install
	uv run pre-commit install --hook-type pre-push

precommit:
	uv run pre-commit run --all-files

lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check . --fix