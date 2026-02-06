from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    key: str | None
    value: dict[str, Any]


class QueueClient:
    def __init__(self, brokers: str, topic_prefix: str) -> None:
        self._brokers = brokers
        self._topic_prefix = topic_prefix

    async def publish(self, topic: str, value: dict[str, Any], key: str | None = None) -> None:
        # Placeholder for Kafka / RabbitMQ producers
        _ = topic, value, key

    async def consume(self, topic: str) -> AsyncIterator[Message]:
        # Placeholder for Kafka / RabbitMQ consumers
        _ = topic
        if False:
            yield Message(key=None, value={})
