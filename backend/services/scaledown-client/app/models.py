from __future__ import annotations

from pydantic import BaseModel, Field


class CompressItem(BaseModel):
    id: str
    text: str
    metadata: dict = Field(default_factory=dict)


class CompressBatchRequest(BaseModel):
    items: list[CompressItem]
    shadow_mode: bool = Field(default=False)


class CompressResult(BaseModel):
    id: str
    original: str
    compressed: str
    ratio: float
    similarity: float
    used_fallback: bool


class CompressBatchResponse(BaseModel):
    results: list[CompressResult]
