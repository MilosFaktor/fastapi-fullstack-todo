from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
                "priority": 5,
                "completed": False,
            }
        }
    }


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "exampleuser",
                "email": "example.user@email.com",
                "first_name": "example",
                "last_name": "user",
                "password": "test123",
                "role": "admin",
                "phone_number": "(+22)26-62626",
            }
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "test123",
                "new_password": "newpassword123",
            }
        }
    }
