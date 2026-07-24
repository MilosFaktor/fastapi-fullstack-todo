.PHONY: db-init run-app run-with-dbinit test run-with-alembic db-init-alembic

db-init:
	@echo "Initializing database..."
	uv run python -m scripts.init_db

db-init-alembic:
	@echo "Running Alembic migrations..."
	DB_MODE=sqlite_example uv run alembic upgrade head

run-app:
	@echo "Running application..."
	uv run uvicorn app.main:app --reload

run-with-dbinit:
	@echo "Initializing database..."
	uv run python -m scripts.init_db
	@echo "Running application..."
	uv run uvicorn app.main:app --reload

run-with-alembic:
	@echo "Running Alembic migrations..."
	DB_MODE=sqlite_example uv run alembic upgrade head
	@echo "Running application..."
	uv run uvicorn app.main:app --reload

test:
	@echo "Running tests..."
	uv run pytest -vv