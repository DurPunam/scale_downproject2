from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging
from .validator import validate

settings = get_settings()
settings.service_name = "quality-validator"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class ValidationRequest(BaseModel):
    semantic_similarity: float
    compression_ratio: float


@app.post("/validate")
async def run_validation(payload: ValidationRequest) -> dict:
    result = validate(payload.semantic_similarity, payload.compression_ratio)
    return {"action": result.action}
