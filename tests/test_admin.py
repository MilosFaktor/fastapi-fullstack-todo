from fastapi.testclient import TestClient

from app.main import app
from app.models import Todos
from app.routers.admin import get_current_user, get_db

from .utils import (
    TestingSessionLocal,
    override_get_current_user,
    override_get_db,
    test_todo,
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [
        {
            "completed": False,
            "title": "Test Todo",
            "description": "This is a test todo",
            "priority": 5,
            "id": 1,
            "owner_id": 1,
        }
    ]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    with TestingSessionLocal() as db:
        todo = db.query(Todos).filter(Todos.id == 1).first()
        assert todo is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo with id 999 not found"}
