import time
from contextlib import asynccontextmanager

import dotenv
from constants.global_const import MODE
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from middleware.logging_middleware import LoggingMiddleware
from pydantic import ValidationError
from routers.auth import auth_controller
from utils.config_utils import get_config
from utils.logger_utils import get_logger, log_request


config = get_config()
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up")
    logger.info("Start application in %s mode" % config.app.mode)

    yield
    # Shutdown
    logger.info("Shutting down")


app = FastAPI(
    docs_url=config.app.docs_url if config.app.mode == MODE.DEVELOPMENT else None,
    redoc_url=config.app.redoc_url if config.app.mode == MODE.DEVELOPMENT else None,
    lifespan=lifespan,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(LoggingMiddleware)

if config.app.cors.enable:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.app.cors.origins,
        allow_credentials=config.app.cors.allow_credentials,
        allow_methods=config.app.cors.methods,
        allow_headers=config.app.cors.headers,
    )


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_exception_handler(request: Request, exc: Exception):
    # Handle 500 exception
    log_request(request, logger)
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": True, "message": "Internal Server Error"},
    )


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def pydantic_request_validation_error(
    request: Request,
    err: RequestValidationError,
):
    log_request(request, logger)

    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    err_msg = "Invalid request"

    return JSONResponse(
        status_code=code,
        content={
            "success": False,
            "message": err_msg,
            "detailed_error": err.errors(),
        },
    )


app.include_router(
    auth_controller.router,
    prefix="/auth",
    tags=["Authentication"],
)


@app.get("/")
async def root():
    return {
        "message": "Application is running",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.app.host,
        port=config.app.port,
        workers=config.app.workers if config.app.mode == MODE.PRODUCTION else 1,
        reload=config.app.reload if config.app.mode == MODE.DEVELOPMENT else False,
    )
