import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Simple request/response logger. In production you would replace this
    with a structured logger (e.g., loguru or structlog).
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger = logging.getLogger("uvicorn.access")
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            "%s %s - %s %sms",
            request.method,
            request.url.path,
            response.status_code,
            f"{process_time:.2f}",
        )
        return response
---