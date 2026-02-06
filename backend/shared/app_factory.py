from __future__ import annotations

import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from shared.config.settings import Settings
from shared.metrics.metrics import REQUEST_COUNT, REQUEST_LATENCY, metrics_router


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, settings: Settings) -> None:
        super().__init__(app)
        self._service = settings.service_name

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        REQUEST_LATENCY.labels(self._service, request.method, request.url.path).observe(elapsed)
        REQUEST_COUNT.labels(
            self._service, request.method, request.url.path, str(response.status_code)
        ).inc()
        return response


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title=settings.service_name)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "service": settings.service_name}

    app.include_router(metrics_router())
    app.add_middleware(MetricsMiddleware, settings=settings)
    return app
