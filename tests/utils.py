import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Todos, Users
from app.routers.users import bcrypt_context

# uv run pytest -vv

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "M1oir", "id": 1, "user_role": "admin"}


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo",
        description="This is a test todo",
        priority=5,
        completed=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="M1oir",
        email="faktor.milos@gmail.com",
        first_name="Milos",
        last_name="Faktor",
        hashed_password=bcrypt_context.hash("test123"),
        role="admin",
        is_active=True,
        phone_number="26262626",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
