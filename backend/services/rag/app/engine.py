from __future__ import annotations

from dataclasses import dataclass

from shared.security.text_safety import detect_prompt_injection, redact_pii


@dataclass
class RagConfig:
    min_similarity: float = 0.92
    low_validation_threshold: float = 0.85


def hybrid_score(vector_similarity: float, bm25_score: float, metadata_match: float) -> float:
    return 0.5 * vector_similarity + 0.3 * bm25_score + 0.2 * metadata_match


def should_fetch_original(query: str, validation_score: float) -> bool:
    lowered = query.lower()
    technical = any(term in lowered for term in ["dimensions", "spec", "material", "warranty"])
    comparison = "compare" in lowered or "vs" in lowered
    return technical or comparison or validation_score < 0.85


def rewrite_query(query: str) -> str:
    return query.strip()


def sanitize_query(query: str) -> tuple[str, bool]:
    redacted, redacted_any = redact_pii(query)
    injection = detect_prompt_injection(redacted)
    return redacted, injection or redacted_any
