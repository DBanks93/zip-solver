lint:
	poetry run black --check --target-version py313 .
	poetry run ruff check .

format:
	poetry run black --target-version py313 .
	poetry run ruff check . --fix

run:
	poetry run zipsolver

install:
	poetry install
	poetry run playwright install chromium

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
