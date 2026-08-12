"""Durable semantic memory with a dependency-free hashed embedding fallback."""
from __future__ import annotations

import hashlib
import json
import math
import re
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

Embedding = list[float]
Embedder = Callable[[str], Iterable[float]]
_TOKEN = re.compile(r"[A-Za-z0-9_']+")


def hashed_embedding(text: str, dimension: int = 128) -> Embedding:
    vector = [0.0] * dimension
    for token in _TOKEN.findall(text.lower()):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
        index = int.from_bytes(digest[:8], "big") % dimension
        sign = 1.0 if digest[8] & 1 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(v * v for v in vector))
    return [v / norm for v in vector] if norm else vector


def cosine(a: Iterable[float], b: Iterable[float]) -> float:
    av, bv = list(a), list(b)
    if len(av) != len(bv):
        raise ValueError("embedding dimensions differ")
    denom = math.sqrt(sum(x * x for x in av)) * math.sqrt(sum(y * y for y in bv))
    return sum(x * y for x, y in zip(av, bv)) / denom if denom else 0.0

@dataclass(slots=True)
class MemoryRecord:
    id: str
    text: str
    timestamp: float
    salience: float = 0.5
    confidence: float = 1.0
    metadata: dict[str, object] | None = None

class SemanticMemory:
    def __init__(self, path: str | Path | None = None, *, embedder: Embedder | None = None, similarity_weight: float = 0.70, recency_weight: float = 0.10, salience_weight: float = 0.15, confidence_weight: float = 0.05) -> None:
        self.path = Path(path) if path else None
        self.embedder = embedder or hashed_embedding
        self.weights = (similarity_weight, recency_weight, salience_weight, confidence_weight)
        self.records: list[MemoryRecord] = []
        self._embeddings: dict[str, Embedding] = {}
        if self.path and self.path.exists():
            self._load()

    def _load(self) -> None:
        assert self.path is not None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = MemoryRecord(**json.loads(line))
            self.records.append(record)
            self._embeddings[record.id] = list(self.embedder(record.text))

    def store(self, text: str, *, salience: float = 0.5, confidence: float = 1.0, metadata: dict[str, object] | None = None) -> MemoryRecord:
        if not text.strip():
            raise ValueError("memory text cannot be empty")
        record = MemoryRecord(uuid.uuid4().hex, text, time.time(), max(0.0, min(1.0, salience)), max(0.0, min(1.0, confidence)), metadata)
        self.records.append(record)
        self._embeddings[record.id] = list(self.embedder(record.text))
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        return record

    def recall(self, query: str, *, limit: int = 5) -> list[tuple[MemoryRecord, float]]:
        if limit <= 0:
            return []
        q = list(self.embedder(query))
        now = time.time()
        sw, rw, salw, cw = self.weights
        ranked = []
        for record in self.records:
            semantic = cosine(q, self._embeddings[record.id])
            age_hours = max(0.0, (now - record.timestamp) / 3600.0)
            recency = 1.0 / (1.0 + age_hours / 24.0)
            score = sw * semantic + rw * recency + salw * record.salience + cw * record.confidence
            ranked.append((record, score))
        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:limit]

    def snapshot(self) -> dict[str, object]:
        return {"count": len(self.records), "path": str(self.path) if self.path else None}

    def reset(self) -> None:
        self.records.clear()
        self._embeddings.clear()
