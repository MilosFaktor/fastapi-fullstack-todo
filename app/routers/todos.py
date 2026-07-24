from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from ..database import get_db
from ..models import Todos
from ..schemas import TodoRequest
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="templates")


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()

        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse(
            request,
            "todo.html",
            {"todos": todos, "user": user},
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()

        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            request,
            "add-todo.html",
            {"user": user},
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(
    request: Request,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()

        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        todo = (
            db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == user.get("id"))
            .first()
        )
        return templates.TemplateResponse(
            request,
            "edit-todo.html",
            {"todo": todo, "user": user},
        )
    except HTTPException:
        return redirect_to_login()


### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    user: user_dependency,
    db: db_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")
    ).delete()

    db.commit()
