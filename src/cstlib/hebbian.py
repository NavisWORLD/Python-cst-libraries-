"""Simple persistent Hebbian association memory."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

_TOKEN = re.compile(r"[A-Za-z0-9_']+")

class HebbianMemory:
    def __init__(self, path: str | Path | None = None, *, learning_rate: float = 0.1, decay: float = 0.001) -> None:
        self.path = Path(path) if path else None
        self.learning_rate = learning_rate
        self.decay = decay
        self.weights: dict[str, dict[str, float]] = defaultdict(dict)
        if self.path and self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.weights = defaultdict(dict, {k: {kk: float(vv) for kk, vv in v.items()} for k, v in raw.items()})

    @staticmethod
    def concepts(value: str | Iterable[str]) -> list[str]:
        tokens = _TOKEN.findall(value.lower()) if isinstance(value, str) else [str(v).lower() for v in value]
        return sorted(set(tokens))

    def learn(self, value: str | Iterable[str]) -> None:
        concepts = self.concepts(value)
        for a in concepts:
            for b in concepts:
                if a == b:
                    continue
                old = self.weights[a].get(b, 0.0)
                self.weights[a][b] = (1.0 - self.decay) * old + self.learning_rate
        self._persist()

    def associated_with(self, concept: str, *, limit: int = 10) -> list[tuple[str, float]]:
        pairs = list(self.weights.get(concept.lower(), {}).items())
        pairs.sort(key=lambda item: item[1], reverse=True)
        return pairs[:limit]

    def _persist(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.weights, indent=2, sort_keys=True), encoding="utf-8")
