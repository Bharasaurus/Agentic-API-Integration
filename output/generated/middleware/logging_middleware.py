import logging
import time
from fastapi import Request, Response
from fastapi.routing import APIRoute

logger = logging.getLogger("app_logger")

class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        start_time = time.time()
        response = Response(status_code=500)

        async def send_wrapper(message):
            nonlocal response
            if message["type"] == "http.response.start":
                response.status_code = message["status"]
            await send(message)

        await self.app(scope, receive, send_wrapper)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"completed in {process_time:.2f}ms"
        )

'''''''''