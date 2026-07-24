from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.routers.users import get_current_user, get_db

from .utils import (
    override_get_current_user,
    override_get_db,
    test_user,
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_get_user_me(test_user):
    response = client.get("/user/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": "faktor.milos@gmail.com",
        "first_name": "Milos",
        "is_active": True,
        "role": "admin",
        "username": "M1oir",
        "id": 1,
        "last_name": "Faktor",
        "hashed_password": test_user.hashed_password,
        "phone_number": "26262626",
    }


def test_change_password_success(test_user):
    response = client.put(
        "/user/me/password",
        json={"old_password": "test123", "new_password": "new_test_password"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/me/password",
        json={"old_password": "wrong_password", "new_password": "new_test_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Old password is incorrect"}


def test_change_phone_number_success(test_user):
    response = client.put(
        "/user/me/phonenumber/1234567890",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
