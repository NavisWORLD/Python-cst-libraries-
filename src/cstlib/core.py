"""Shared CST event type."""
from dataclasses import asdict, dataclass
from time import time
from typing import Any

@dataclass(slots=True)
class Event:
    source: str
    kind: str
    payload: dict[str, Any]
    timestamp: float = 0.0
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if self.timestamp == 0.0:
            self.timestamp = time()
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
