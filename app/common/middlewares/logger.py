import json
from time import time

from fastapi import Request

# from loguru import Logger
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.utils.logger import mask_sensitive_data

IGNORE_PATHS = ["/openapi.json", "/docs", "/redoc"]


class LogRequestsMiddleware(BaseHTTPMiddleware):
    """Log requests and responses."""

    def __init__(self, app, logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        if request.url.path in IGNORE_PATHS:
            return await call_next(request)

        start_time = time()
        body = await request.body()
        request._body = body
        body_content = None

        if request.method == "POST":
            try:
                body_content = json.loads(body.decode("utf-8"))
                body_content = mask_sensitive_data(body_content)
            except json.JSONDecodeError:
                body_content = body.decode("utf-8")  # Use raw body if not JSON

        # Log request information
        self.logger.info(
            f"Request: {request.method} {request.url} - Headers: {dict(request.headers)} - Body: {body_content}"
        )

        response = await call_next(request)

        process_time = time() - start_time
        self.logger.info(
            f"Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.3f}s"
        )

        return response
