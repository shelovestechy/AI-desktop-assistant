from __future__ import annotations

from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class SystemSnapshot:
    cpu_percent: float
    memory_percent: float


class SystemService:
    """Read-only access to lightweight system health information."""

    def snapshot(self) -> SystemSnapshot:
        return SystemSnapshot(
            cpu_percent=psutil.cpu_percent(interval=None),
            memory_percent=psutil.virtual_memory().percent,
        )
