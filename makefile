start:
	bash ./scripts/start.sh

seed:
	uv run python -m app.seed.seed

test:
	bash scripts/check-coverage.sh

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