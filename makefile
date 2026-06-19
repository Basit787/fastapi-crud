start:
	bash ./start.sh

seed:
	uv run python -m app.seed.seed

lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check . --fix