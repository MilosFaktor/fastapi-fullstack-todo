from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Users
from ..schemas import ChangePasswordRequest
from .auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(
    user: user_dependency,
    db: db_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user.get('id')} not found"
        )
    return user_model


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    change_password_request: ChangePasswordRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user.get('id')} not found"
        )

    if not bcrypt_context.verify(
        change_password_request.old_password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    user_model.hashed_password = bcrypt_context.hash(
        change_password_request.new_password
    )

    db.add(user_model)
    db.commit()


@router.put("/me/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    phone_number: str,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user.get('id')} not found"
        )
    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()
