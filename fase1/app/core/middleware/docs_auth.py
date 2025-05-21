from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import secrets
import base64

class DocsAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            auth = request.headers.get("Authorization")
            if auth:
                scheme, credentials = auth.split()
                decoded = base64.b64decode(credentials).decode("utf-8")
                username, password = decoded.split(":")
                if secrets.compare_digest(username, "admin") and secrets.compare_digest(password, "!@#$Fiap2025"):
                    return await call_next(request)
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": "Basic"},
                content="Não autorizado"
            )
        return await call_next(request)