from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "review-analysis"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class ReviewRequest(BaseModel):
    product_id: str
    review_text: str


@app.post("/analyze")
async def analyze(payload: ReviewRequest) -> dict:
    sentiment = 0.0
    fake_prob = 0.0
    return {"product_id": payload.product_id, "sentiment": sentiment, "fake_probability": fake_prob}
