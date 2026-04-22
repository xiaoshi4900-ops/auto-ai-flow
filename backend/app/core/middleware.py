import json
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp


class ApiResponseWrapperMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        path = request.url.path

        skip_paths = ("/docs", "/openapi.json", "/redoc", "/healthz")
        if any(path.startswith(p) for p in skip_paths):
            await self.app(scope, receive, send)
            return

        response_started = False
        response_status = 200
        response_headers = []
        body_parts = []

        async def send_wrapper(message):
            nonlocal response_started, response_status, response_headers, body_parts

            if message["type"] == "http.response.start":
                response_started = True
                response_status = message["status"]
                response_headers = [(h[0].decode(), h[1].decode()) for h in message.get("headers", [])]
                return

            if message["type"] == "http.response.body":
                body_parts.append(message.get("body", b""))
                if not message.get("more_body", False):
                    full_body = b"".join(body_parts)
                    content_type = ""
                    for name, value in response_headers:
                        if name.lower() == "content-type":
                            content_type = value
                            break

                    if "application/json" in content_type and response_status < 500:
                        try:
                            data = json.loads(full_body)
                            if not isinstance(data, dict) or "code" not in data:
                                if isinstance(data, dict) and "error_code" in data:
                                    wrapped = {"code": response_status, "message": data.get("message", "error"), "data": data}
                                else:
                                    wrapped = {"code": 0, "message": "ok", "data": data}
                                new_body = json.dumps(wrapped, ensure_ascii=False).encode("utf-8")
                            else:
                                new_body = full_body
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            new_body = full_body
                    else:
                        new_body = full_body

                    headers = []
                    for name, value in response_headers:
                        if name.lower() == "content-length":
                            headers.append((name.encode(), str(len(new_body)).encode()))
                        else:
                            headers.append((name.encode(), value.encode()))
                    if not any(h[0].lower() == b"content-length" for h in headers):
                        headers.append((b"content-length", str(len(new_body)).encode()))

                    await send({"type": "http.response.start", "status": response_status, "headers": headers})
                    await send({"type": "http.response.body", "body": new_body})
                return

            await send(message)

        await self.app(scope, receive, send_wrapper)
