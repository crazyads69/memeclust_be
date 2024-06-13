import json
from fastapi import APIRouter, Depends
from supabase import Client
from schemas.response import APIResponse
from utils.logger_utils import get_logger
from services.auth.auth_svc import AuthService
from .auth_schemas import LoginRequestBody, SignUpRequestBody
from libs.supabse import Supabase
from deps.deps import init_supabase_client

logger = get_logger()

router = APIRouter()


@router.post("/login")
async def login(
    req: LoginRequestBody, supabase_client: Client = Depends(init_supabase_client)
) -> APIResponse:
    logger.info(
        "User login with request:\n%s" % req.model_dump_json(indent=2),
    )
    # Call service
    resp = await AuthService(supabase=supabase_client).login(
        email=req.email, password=req.password
    )
    logger.info(
        "User login with response:\n%s" % json.dumps(resp, indent=2),
    )

    if resp is None:
        return APIResponse(
            status=401,
            message="Login failed",
            message_vi="Đăng nhập thất bại",
            data=None,
        )

    return APIResponse(
        status=200,
        message="Login successfully",
        message_vi="Đăng nhập thành công",
        data=resp,
    )


@router.post("/signup")
async def signup(
    req: SignUpRequestBody, supabase_client: Client = Depends(init_supabase_client)
) -> APIResponse:
    logger.info(
        "User signup with request:\n%s" % req.model_dump_json(indent=2),
    )

    # Call service
    resp = await AuthService(supabase=supabase_client).signup(
        email=req.email,
        password=req.password,
        first_name=req.first_name,
        last_name=req.last_name,
    )

    logger.info(
        "User signup with response:\n%s" % json.dumps(resp, indent=2),
    )

    if resp is None:
        return APIResponse(
            status=401,
            message="Signup failed",
            message_vi="Đăng ký thất bại",
            data=None,
        )

    return APIResponse(
        status=200,
        message="Signup successfully",
        message_vi="Đăng ký thành công",
        data=resp,
    )
