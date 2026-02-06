from __future__ import annotations

from datetime import UTC, datetime, timedelta


def should_move_to_cold(last_accessed: datetime | None, access_count: int) -> bool:
    if last_accessed is None:
        return False
    cutoff = datetime.now(UTC) - timedelta(days=30)
    return last_accessed < cutoff and access_count < 5
