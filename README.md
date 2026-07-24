# FastAPI Todo App

A full-stack Todo application built with FastAPI, SQLAlchemy, Jinja2 templates, Bootstrap 4, JavaScript `fetch()`, JWT authentication, and Alembic migrations.

This project started as a course-based FastAPI application and was then cleaned up with environment-based configuration, separated SQLAlchemy models and Pydantic schemas, centralized database dependencies, Alembic schema creation, and a focused test suite.

## Features

- User registration and login
- JWT access tokens stored in browser cookies
- Protected todo pages
- Create, read, update, and delete todos
- Mark todos as completed
- User profile endpoints
- Change password and phone number
- Admin endpoints for reading users/todos and deleting todos
- Server-rendered HTML with Jinja2
- Bootstrap 4 UI styling
- JavaScript form handling with `fetch()`
- SQLite/PostgreSQL/MySQL-ready configuration
- Alembic migrations
- Pytest test suite

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic / pydantic-settings
- Jinja2
- Bootstrap 4
- JavaScript
- pytest
- uv

## Project Structure

```text
app/
  config.py        # Environment-based settings
  database.py      # SQLAlchemy engine, SessionLocal, Base, get_db
  main.py          # FastAPI app setup
  models.py        # SQLAlchemy database models
  schemas.py       # Pydantic request/response schemas
  routers/         # Auth, todo, user, admin routes
alembic/           # Database migrations
scripts/
  init_db.py       # Manual create_all() DB initializer
templates/         # Jinja2 HTML templates
static/            # CSS and JavaScript
tests/             # Pytest tests
```

## Environment

The app chooses an env file using `DB_MODE`.

Supported modes:

```text
sqlite_example -> .env.sqlite.example
sqlite         -> .env.sqlite
postgres       -> .env.postgres
mysql          -> .env.mysql
```

Only `.env.sqlite.example` is committed. Real `.env*` files are ignored by Git.

Example `.env.sqlite.example`:

```env
ENVIRONMENT="sqlite_example"
SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.example.db"
SECRET_KEY="replace-with-openssl-rand-hex-32"
ALGORITHM="HS256"
```

Generate a local secret key with:

```bash
openssl rand -hex 32
```

For private local development, create your own ignored env file, for example:

```bash
cp .env.sqlite.example .env.sqlite
```

Then update `SECRET_KEY` and run with:

```bash
DB_MODE=sqlite uv run uvicorn app.main:app --reload
```

## Install

Install dependencies with `uv`:

```bash
uv sync
```

## Database Setup

### Recommended: Alembic

Run migrations against the default example SQLite database:

```bash
DB_MODE=sqlite_example uv run alembic upgrade head
```

Or use the Makefile:

```bash
make db-init-alembic
```

To create a new migration after changing SQLAlchemy models:

```bash
DB_MODE=sqlite_example uv run alembic revision --autogenerate -m "describe your change"
DB_MODE=sqlite_example uv run alembic upgrade head
```

### Simple Learning Option

This project also includes a manual SQLAlchemy initializer:

```bash
uv run python -m scripts.init_db
```

Or:

```bash
make db-init
```

Alembic is preferred for schema history. The manual initializer is kept as a simple learning/development helper.

## Run

Start the app:

```bash
uv run uvicorn app.main:app --reload
```

Or:

```bash
make run-app
```

Initialize with Alembic and run:

```bash
make run-with-alembic
```

Initialize with the simple SQLAlchemy script and run:

```bash
make run-with-dbinit
```

Then open:

```text
http://127.0.0.1:8000
```

## Makefile Commands

```bash
make db-init          # Create tables using scripts/init_db.py
make db-init-alembic  # Apply Alembic migrations
make run-app          # Run FastAPI app
make run-with-dbinit  # Initialize DB with script, then run app
make run-with-alembic # Apply migrations, then run app
make test             # Run pytest in verbose mode
```

## Tests

Run tests:

```bash
uv run pytest -q
```

Or:

```bash
make test
```

Current test coverage includes auth helpers, todo CRUD endpoints, user endpoints, admin endpoints, and health/main route behavior.

## Notes

- The app uses browser cookies to store the JWT access token.
- JavaScript in `static/js/base.js` intercepts form submissions and sends API requests with `fetch()`.
- Bootstrap 4 is stored locally under `static/`.
- Database files (`*.db`), private env files.

## Future Improvements

- Add Docker / Docker Compose for easier local startup
- Add screenshots to this README
