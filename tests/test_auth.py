from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from app.main import app
from app.models import Users
from app.routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_db,
)

from .utils import (
    TestingSessionLocal,
    override_get_db,
    test_user,
)

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    with TestingSessionLocal() as db:
        authenticated_user = authenticate_user(
            username="M1oir", password="test123", db=db
        )
        assert authenticated_user is not None
        assert isinstance(authenticated_user, Users)
        assert authenticated_user.username == test_user.username

        non_existent_user = authenticate_user(
            username="Wrong username", password="test123", db=db
        )
        assert non_existent_user is False

        wrong_password_user = authenticate_user(
            test_user.username,
            "wrong_password",
            db=db,
        )
        assert wrong_password_user is False


def test_create_access_token(test_user):
    username = "M1oir"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False},
    )
    assert token is not None
    assert isinstance(token, str)
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "M1oir", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "M1oir", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user."
