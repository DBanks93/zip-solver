lint:
	poetry run black --check --target-version py313 .
	poetry run ruff check .

format:
	poetry run black --target-version py313 .
	poetry run ruff check . --fix

run_zip:
	poetry run linkedin_solvers zip

install:
	poetry install
	poetry run playwright install chromium

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
