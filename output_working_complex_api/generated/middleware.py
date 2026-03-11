import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("app.middleware")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            "%s %s - %s - %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        return response