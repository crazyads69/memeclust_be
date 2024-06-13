from pydantic import BaseModel, EmailStr, Field, constr


class LoginRequestBody(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=20)  # type: ignore


class SignUpRequestBody(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=20)  # type: ignore
    first_name: constr(min_length=1, max_length=255)  # type: ignore
    last_name: constr(min_length=1, max_length=255)  # type: ignore


class RefreshTokenBody(BaseModel):
    refresh_token: constr(min_length=1, max_length=255)  # type: ignore
