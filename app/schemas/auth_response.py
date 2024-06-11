from typing import Any
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse
