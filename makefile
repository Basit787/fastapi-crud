start:
	bash ./start.sh

seed:
	uv run python -m app.seed.seed

fix:
	uv run ruff check . --fix