from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

from .engine import ThompsonBandit

settings = get_settings()
settings.service_name = "recommendation-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)
bandit = ThompsonBandit(["compression_v1", "compression_v2"])


class Feedback(BaseModel):
    arm: str
    reward: bool


@app.get("/recommend")
async def recommend() -> dict:
    selected = bandit.select()
    return {"variant": selected}


@app.post("/feedback")
async def feedback(payload: Feedback) -> dict:
    bandit.update(payload.arm, payload.reward)
    return {"status": "ok"}
