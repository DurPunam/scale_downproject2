from __future__ import annotations

from fastapi import FastAPI

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

from .models import CompressBatchRequest, CompressBatchResponse
from .scaledown import ScaleDownClient

settings = get_settings()
settings.service_name = "scaledown-client"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)
client = ScaleDownClient(settings)


@app.post("/compress", response_model=CompressBatchResponse)
async def compress(req: CompressBatchRequest) -> CompressBatchResponse:
    items = [(item.id, item.text) for item in req.items]
    results = await client.compress_batch(
        items=items,
        queue_depth=len(items),
        rate_limit_rps=50.0,
        shadow_mode=req.shadow_mode,
    )
    return CompressBatchResponse(results=results)
