test:
	uv run run_tests.py
lint:
	uv run ruff format
	uv run ruff check --fix