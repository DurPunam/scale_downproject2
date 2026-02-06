from __future__ import annotations

from fastapi import FastAPI

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging
from .engine import rewrite_query, sanitize_query
from .models import RagAnswer, RagQueryRequest

settings = get_settings()
settings.service_name = "rag-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


@app.post("/query", response_model=RagAnswer)
async def rag_query(req: RagQueryRequest) -> RagAnswer:
    safe_query, flagged = sanitize_query(req.query)
    if flagged:
        return RagAnswer(answer="Request blocked by safety filters.", sources=[])
    rewritten = rewrite_query(safe_query)
    # Placeholder for retrieval and generation pipeline
    return RagAnswer(answer=f"RAG response for: {rewritten}", sources=[], tokens_used=len(rewritten.split()))
