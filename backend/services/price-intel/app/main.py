from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "price-intel"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class PriceAlert(BaseModel):
    product_id: str
    price: float


@app.post("/price-alert")
async def price_alert(payload: PriceAlert) -> dict:
    return {"status": "queued", "product_id": payload.product_id}
