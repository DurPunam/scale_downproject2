from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "spatial-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class SpatialQuery(BaseModel):
    product_dimensions: list[float]
    room_dimensions: list[float]


@app.post("/fit-check")
async def fit_check(payload: SpatialQuery) -> dict:
    px, py, pz = payload.product_dimensions
    rx, ry, rz = payload.room_dimensions
    fit = px <= rx and py <= ry and pz <= rz
    space_used = (px * py * pz) / max(rx * ry * rz, 1.0)
    return {"fit": fit, "space_used": round(space_used, 4)}
