from __future__ import annotations

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

from .alignment import AlignmentModel

settings = get_settings()
settings.service_name = "embedding-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)
model_original = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
model_compressed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
aligner = AlignmentModel()


class EmbedRequest(BaseModel):
    text: str


class AlignmentTrainRequest(BaseModel):
    compressed_embeddings: list[list[float]]
    original_embeddings: list[list[float]]


@app.post("/embed")
async def embed(payload: EmbedRequest) -> dict:
    emb_orig = model_original.encode([payload.text], normalize_embeddings=True)[0]
    emb_comp = model_compressed.encode([payload.text], normalize_embeddings=True)[0]
    try:
        emb_aligned = aligner.transform(np.array([emb_comp]))[0]
    except RuntimeError:
        emb_aligned = np.zeros(768)
    return {
        "embedding_original": emb_orig.tolist(),
        "embedding_compressed": emb_comp.tolist(),
        "embedding_aligned": emb_aligned.tolist(),
    }


@app.post("/alignment/train")
async def train_alignment(payload: AlignmentTrainRequest) -> dict:
    comp = np.array(payload.compressed_embeddings)
    orig = np.array(payload.original_embeddings)
    aligner.fit(comp, orig)
    return {"status": "trained", "samples": len(payload.compressed_embeddings)}
