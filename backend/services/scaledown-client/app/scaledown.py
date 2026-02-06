from __future__ import annotations

import asyncio
import time
import uuid
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

import httpx
import numpy as np
from sentence_transformers import SentenceTransformer

from shared.config.settings import Settings


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CallMetric:
    latency_ms: float
    tokens: int


class SlidingMetrics:
    def __init__(self, capacity: int = 1000) -> None:
        self._capacity = capacity
        self._items: deque[CallMetric] = deque(maxlen=capacity)

    def add(self, latency_ms: float, tokens: int) -> None:
        self._items.append(CallMetric(latency_ms=latency_ms, tokens=tokens))

    def tokens_per_second(self) -> float:
        if not self._items:
            return 0.0
        total_tokens = sum(i.tokens for i in self._items)
        total_latency = sum(i.latency_ms for i in self._items) / 1000.0
        return total_tokens / max(total_latency, 0.001)

    def p95_latency_ms(self) -> float:
        if not self._items:
            return 0.0
        latencies = [i.latency_ms for i in self._items]
        return float(np.percentile(latencies, 95))


class AdaptiveBatcher:
    def __init__(self, min_size: int = 4, max_size: int = 128) -> None:
        self._min = min_size
        self._max = max_size
        self._metrics = SlidingMetrics()

    def record(self, latency_ms: float, tokens: int) -> None:
        self._metrics.add(latency_ms, tokens)

    def calculate_batch_size(self, queue_depth: int, rate_limit_rps: float) -> int:
        tps = self._metrics.tokens_per_second()
        p95 = self._metrics.p95_latency_ms()
        base = 16
        if tps > 0:
            base = min(self._max, max(self._min, int(tps / 200)))
        if p95 > 1200:
            base = max(self._min, int(base * 0.6))
        elif p95 < 400:
            base = min(self._max, int(base * 1.3))
        if queue_depth > 1000:
            base = min(self._max, int(base * 1.5))
        if rate_limit_rps > 0:
            base = min(base, int(rate_limit_rps * 2))
        return max(self._min, min(self._max, base))


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 30.0) -> None:
        self._failure_threshold = failure_threshold
        self._reset_timeout = reset_timeout
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at = 0.0
        self._half_open_remaining = 0

    def allow(self) -> bool:
        if self._state == CircuitState.CLOSED:
            return True
        if self._state == CircuitState.OPEN:
            if time.time() - self._opened_at >= self._reset_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_remaining = 3
                return True
            return False
        if self._state == CircuitState.HALF_OPEN:
            return self._half_open_remaining > 0
        return False

    def record_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_remaining -= 1
            if self._half_open_remaining <= 0:
                self._state = CircuitState.CLOSED
                self._failures = 0
        else:
            self._failures = 0

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self._failure_threshold:
            self._state = CircuitState.OPEN
            self._opened_at = time.time()

    @property
    def state(self) -> CircuitState:
        return self._state


class FallbackCompressor:
    def __init__(self) -> None:
        self._model: SentenceTransformer | None = None

    def _ensure_model(self) -> None:
        if self._model is None:
            self._model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def compress_with_t5(self, text: str) -> str:
        # Placeholder for a local T5 compression model.
        if len(text) <= 240:
            return text
        return text[:240] + "..."

    def compress_extractive(self, text: str) -> str:
        sentences = text.split(".")
        return ".".join(sentences[:2]).strip() or text[:200]

    def similarity(self, original: str, compressed: str) -> float:
        try:
            self._ensure_model()
            embeddings = self._model.encode([original, compressed], normalize_embeddings=True)
            return float(np.dot(embeddings[0], embeddings[1]))
        except Exception:
            if not original or not compressed:
                return 0.0
            overlap = len(set(original.split()) & set(compressed.split()))
            return overlap / max(len(set(original.split())), 1)


class ScaleDownClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._batcher = AdaptiveBatcher()
        self._breaker = CircuitBreaker(failure_threshold=5, reset_timeout=30.0)
        self._fallback = FallbackCompressor()
        self._client = httpx.AsyncClient(
            base_url=settings.scaledown.base_url,
            timeout=settings.scaledown.timeout_seconds,
            headers={"Authorization": f"Bearer {settings.scaledown.api_key}"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def compress_batch(
        self,
        items: Iterable[tuple[str, str]],
        queue_depth: int,
        rate_limit_rps: float,
        shadow_mode: bool,
    ) -> list[dict]:
        batch = [{"id": item_id, "text": text} for item_id, text in items]
        if not batch:
            return []

        if not self._breaker.allow():
            return await self._fallback_batch(batch)

        idempotency_key = str(uuid.uuid4())
        url = self._settings.scaledown.batch_endpoint
        payload = {"items": batch}
        max_retries = 3

        for attempt in range(max_retries + 1):
            start = time.perf_counter()
            try:
                response = await self._client.post(
                    url,
                    json=payload,
                    headers={"Idempotency-Key": idempotency_key},
                )
                elapsed_ms = (time.perf_counter() - start) * 1000
                tokens = sum(len(item["text"].split()) for item in batch)
                self._batcher.record(elapsed_ms, tokens)

                if response.status_code >= 500:
                    raise httpx.HTTPError(f"Server error {response.status_code}")
                data = response.json()
                self._breaker.record_success()

                results = self._format_results(batch, data)
                if shadow_mode:
                    await self._shadow_compare(batch, results)
                return results
            except Exception:
                self._breaker.record_failure()
                if attempt >= max_retries:
                    return await self._fallback_batch(batch)
                await asyncio.sleep(2**attempt)
        return await self._fallback_batch(batch)

    def get_batch_size(self, queue_depth: int, rate_limit_rps: float) -> int:
        return self._batcher.calculate_batch_size(queue_depth, rate_limit_rps)

    async def _fallback_batch(self, batch: list[dict]) -> list[dict]:
        results = []
        for item in batch:
            compressed = self._fallback.compress_with_t5(item["text"])
            if compressed == item["text"]:
                compressed = self._fallback.compress_extractive(item["text"])
            similarity = self._fallback.similarity(item["text"], compressed)
            ratio = len(compressed) / max(len(item["text"]), 1)
            results.append(
                {
                    "id": item["id"],
                    "original": item["text"],
                    "compressed": compressed,
                    "ratio": ratio,
                    "similarity": similarity,
                    "used_fallback": True,
                }
            )
        return results

    def _format_results(self, batch: list[dict], data: dict) -> list[dict]:
        results = []
        compressed_items = {item["id"]: item for item in data.get("results", [])}
        for item in batch:
            compressed = compressed_items.get(item["id"], {}).get("compressed", "")
            ratio = len(compressed) / max(len(item["text"]), 1)
            similarity = self._fallback.similarity(item["text"], compressed)
            results.append(
                {
                    "id": item["id"],
                    "original": item["text"],
                    "compressed": compressed,
                    "ratio": ratio,
                    "similarity": similarity,
                    "used_fallback": False,
                }
            )
        return results

    async def _shadow_compare(self, batch: list[dict], results: list[dict]) -> None:
        for item, result in zip(batch, results):
            original = item["text"]
            compressed = result["compressed"]
            drift = 1.0 - self._fallback.similarity(original, compressed)
            if drift > 0.1:
                # In production this should emit to a monitoring pipeline
                pass
