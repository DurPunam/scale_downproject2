from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "compression-router"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class BatchProbe(BaseModel):
    queue_depth: int
    rate_limit_rps: float


@app.post("/batch-size")
async def batch_size(payload: BatchProbe) -> dict:
    base = max(4, min(128, int(payload.rate_limit_rps * 2)))
    if payload.queue_depth > 1000:
        base = min(128, int(base * 1.5))
    return {"batch_size": base}
