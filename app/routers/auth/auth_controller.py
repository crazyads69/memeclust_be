import json

from fastapi import APIRouter
from schemas.response import APIResponse
from utils.logger_utils import get_logger

from .auth_schemas import LoginRequestBody

logger = get_logger()

router = APIRouter()


@router.post("/login")
async def login(req: LoginRequestBody) -> APIResponse:
    logger.info(
        "User login with req:\n%s" % req.model_dump_json(indent=2),
    )

    resp = {
        "message": "Login successfully!",
    }

    logger.info(
        "User login with resp:\n%s" % json.dumps(resp, indent=2),
    )
    return APIResponse(result=resp)
