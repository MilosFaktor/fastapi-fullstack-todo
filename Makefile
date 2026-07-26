DOCKER_COMPOSE ?= docker compose
COMPOSE_FILE ?= docker-compose.postgres.yaml
COMPOSE_ENV_FILE ?= .env.docker.postgres.example

.PHONY: db-init run-app run-with-dbinit test run-with-alembic db-init-alembic compose-up-build compose-up compose-up-d compose-down-v compose-down compose-db-shell

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

compose-up-build:
	@echo "Building and starting Docker Compose services..."
	$(DOCKER_COMPOSE) --env-file $(COMPOSE_ENV_FILE) -f $(COMPOSE_FILE) up --build

compose-up:
	@echo "Starting Docker Compose services..."
	$(DOCKER_COMPOSE) --env-file $(COMPOSE_ENV_FILE) -f $(COMPOSE_FILE) up

compose-up-d:
	@echo "Starting Docker Compose services in detached mode..."
	$(DOCKER_COMPOSE) --env-file $(COMPOSE_ENV_FILE) -f $(COMPOSE_FILE) up -d

compose-down:
	@echo "Stopping Docker Compose services..."
	$(DOCKER_COMPOSE) --env-file $(COMPOSE_ENV_FILE) -f $(COMPOSE_FILE) down

compose-down-v:
	@echo "Stopping Docker Compose services and removing volumes..."
	$(DOCKER_COMPOSE) --env-file $(COMPOSE_ENV_FILE) -f $(COMPOSE_FILE) down -v

compose-db-shell:
	@echo "Opening PostgreSQL shell..."
	docker exec -it fastapi-todo-db psql -U postgres -d TodoApplicationDatabase

test:
	@echo "Running tests..."
	uv run pytest -vv