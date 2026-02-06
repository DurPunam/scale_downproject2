from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationResult:
    semantic_similarity: float
    compression_ratio: float
    action: str


def validate(semantic_similarity: float, compression_ratio: float) -> ValidationResult:
    if semantic_similarity < 0.80:
        return ValidationResult(semantic_similarity, compression_ratio, "human_review")
    if semantic_similarity < 0.85:
        return ValidationResult(semantic_similarity, compression_ratio, "reprocess")
    if not (0.75 <= compression_ratio <= 0.85):
        return ValidationResult(semantic_similarity, compression_ratio, "reprocess")
    return ValidationResult(semantic_similarity, compression_ratio, "accept")
