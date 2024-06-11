from typing import Any

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from libs.supabse import Supabase
from supabase import Client
from gotrue import User
from utils.logger_utils import get_logger
from schemas.auth_response import LoginResponse, UserResponse

logger = get_logger()


class AuthService:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        pass

    async def login(self, email: str, password: str) -> Response:
        user = self.supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        logger.info("User login with email: %s" % email)
        if user.session is None or user.user is None:
            raise Exception("Login failed")
        data = LoginResponse(
            access_token=user.session.access_token,
            refresh_token=user.session.refresh_token,
            user=UserResponse(
                id=user.user.id,
                email=user.user.email if user.user.email is not None else "",
                first_name=user.user.user_metadata.get("first_name", ""),
                last_name=user.user.user_metadata.get("last_name", ""),
            ),
        )

        logger.info("User login with resp:\n%s" % data)

        # Encode response to json compatible
        response = jsonable_encoder(data)
        return response

    async def signup(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> User:
        user = self.supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": {"first_name": first_name, "last_name": last_name}},
            },
        )

        logger.info("User signup with email: %s" % email)
        if user.user is None:
            raise Exception("Login failed")
        # convert to json
        data = user.user.model_dump_json(indent=2)
        logger.info("User signup with resp:\n%s" % data)
        return user.user
