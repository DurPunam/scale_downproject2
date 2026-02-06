from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import aiofiles
import aioredis


class CacheLayer:
    def __init__(self, redis_url: str, disk_path: str) -> None:
        self._redis_url = redis_url
        self._disk_path = Path(disk_path)
        self._redis: aioredis.Redis | None = None

    async def connect(self) -> None:
        self._redis = await aioredis.from_url(
            self._redis_url, encoding="utf-8", decode_responses=True
        )
        self._disk_path.mkdir(parents=True, exist_ok=True)

    async def get(self, key: str) -> dict[str, Any] | None:
        if not self._redis:
            raise RuntimeError("Cache not connected")
        val = await self._redis.get(key)
        if val:
            return json.loads(val)
        disk_val = await self._read_disk(key)
        if disk_val:
            await self._redis.set(key, json.dumps(disk_val))
        return disk_val

    async def set(self, key: str, value: dict[str, Any], ttl_seconds: int = 3600) -> None:
        if not self._redis:
            raise RuntimeError("Cache not connected")
        await self._redis.set(key, json.dumps(value), ex=ttl_seconds)
        await self._write_disk(key, value)

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    async def _read_disk(self, key: str) -> dict[str, Any] | None:
        path = self._disk_path / self._hash_key(key)
        if not path.exists():
            return None
        async with aiofiles.open(path, encoding="utf-8") as handle:
            data = await handle.read()
            return json.loads(data)

    async def _write_disk(self, key: str, value: dict[str, Any]) -> None:
        path = self._disk_path / self._hash_key(key)
        async with aiofiles.open(path, "w", encoding="utf-8") as handle:
            await handle.write(json.dumps(value))
