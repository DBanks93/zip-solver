lint:
	poetry run black --check --target-version py313 .
	poetry run ruff check .

format:
	poetry run black --target-version py313 .
	poetry run ruff check . --fix

run:
	poetry run python run.py