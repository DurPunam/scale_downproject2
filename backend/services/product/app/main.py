from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "product-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class AccessEvent(BaseModel):
    product_id: str


@app.post("/access")
async def track_access(payload: AccessEvent) -> dict:
    return {"product_id": payload.product_id, "status": "tracked"}


class ColdStorageProbe(BaseModel):
    last_accessed: datetime | None
    access_count: int


@app.post("/cold-storage/check")
async def cold_storage_check(payload: ColdStorageProbe) -> dict:
    from .storage import should_move_to_cold

    return {"move_to_cold": should_move_to_cold(payload.last_accessed, payload.access_count)}
