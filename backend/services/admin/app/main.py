from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "admin-mlops"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class FeatureFlag(BaseModel):
    key: str
    enabled: bool


@app.post("/flags")
async def set_flag(payload: FeatureFlag) -> dict:
    return {"key": payload.key, "enabled": payload.enabled}
