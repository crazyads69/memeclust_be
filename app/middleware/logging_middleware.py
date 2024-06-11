from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger_utils import get_logger

logger = get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request headers
        headers = {key: value for key, value in request.headers.items()}

        # Log client
        client = request.client
        # Check if client is not None
        if client is not None:
            logger.info(f"Client: {client.host}:{client.port}")
        else:
            logger.info("Client information is not available")

        # Log user agent
        user_agent = request.headers.get("user-agent")
        logger.info(f"User Agent: {user_agent}")

        # Log the request and headers
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request Headers: {headers}")

        # Pass the request to the next middleware or route handler
        response = await call_next(request)

        # Log the response
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Headers: {response.headers}")

        return response
