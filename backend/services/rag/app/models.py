from __future__ import annotations

from pydantic import BaseModel, Field


class RagQueryRequest(BaseModel):
    query: str
    user_id: str | None = None
    include_sources: bool = Field(default=True)


class RagAnswer(BaseModel):
    answer: str
    sources: list[dict] = Field(default_factory=list)
    tokens_used: int = 0
