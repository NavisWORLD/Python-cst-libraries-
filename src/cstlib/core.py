"""Shared CST event and health types."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from time import time
from typing import Any

@dataclass(slots=True)
class Event:
    source: str
    kind: str
    payload: dict[str, Any]
    timestamp: float = 0.0
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.timestamp == 0.0:
            self.timestamp = time()
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(slots=True)
class Health:
    name: str
    ok: bool
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
