"""Persistent dynamic state models used by CST runtimes."""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Iterable


def _text_signal(text: str, dimension: int) -> list[float]:
    out: list[float] = []
    counter = 0
    while len(out) < dimension:
        digest = hashlib.sha256(f"{counter}:{text}".encode("utf-8")).digest()
        for byte in digest:
            out.append((byte / 127.5) - 1.0)
            if len(out) == dimension:
                break
        counter += 1
    return out


def _as_vector(signal: float | str | Iterable[float], dimension: int) -> list[float]:
    if isinstance(signal, str):
        return _text_signal(signal, dimension)
    if isinstance(signal, (int, float)):
        value = float(signal)
        return [value * math.sin((i + 1) * 0.6180339887498948) for i in range(dimension)]
    values = [float(v) for v in signal]
    if not values:
        return [0.0] * dimension
    if len(values) == dimension:
        return values
    return [values[i % len(values)] for i in range(dimension)]


@dataclass
class DynamicState:
    dimension: int
    decay: float = 0.92
    gain: float = 1.0
    values: list[float] = field(default_factory=list)
    updates: int = 0

    def __post_init__(self) -> None:
        if self.dimension <= 0:
            raise ValueError("dimension must be positive")
        if not 0.0 <= self.decay < 1.0:
            raise ValueError("decay must be in [0, 1)")
        if not self.values:
            self.values = [0.0] * self.dimension
        if len(self.values) != self.dimension:
            raise ValueError("values length must match dimension")

    def update(self, signal: float | str | Iterable[float], dt: float = 1.0) -> list[float]:
        if dt <= 0:
            raise ValueError("dt must be positive")
        projected = _as_vector(signal, self.dimension)
        effective_decay = self.decay ** dt
        inject = 1.0 - effective_decay
        self.values = [effective_decay * old + inject * self.gain * math.tanh(new) for old, new in zip(self.values, projected)]
        self.updates += 1
        return self.vector()

    def vector(self) -> list[float]:
        return list(self.values)

    def reset(self) -> None:
        self.values = [0.0] * self.dimension
        self.updates = 0

    def snapshot(self) -> dict[str, object]:
        return {"dimension": self.dimension, "decay": self.decay, "gain": self.gain, "values": self.vector(), "updates": self.updates}

    def restore(self, state: dict[str, object]) -> None:
        if int(state["dimension"]) != self.dimension:
            raise ValueError("snapshot dimension mismatch")
        values = [float(v) for v in state["values"]]
        if len(values) != self.dimension:
            raise ValueError("snapshot values length mismatch")
        self.values = values
        self.updates = int(state.get("updates", 0))

    def metrics(self) -> dict[str, float | int]:
        mean = sum(self.values) / self.dimension
        variance = sum((v - mean) ** 2 for v in self.values) / self.dimension
        energy = math.sqrt(sum(v * v for v in self.values))
        return {"updates": self.updates, "mean": mean, "variance": variance, "l2": energy}


class Dyn12(DynamicState):
    def __init__(self, decay: float = 0.92, gain: float = 1.0):
        super().__init__(12, decay, gain)


class Dyn42(DynamicState):
    def __init__(self, decay: float = 0.94, gain: float = 1.0):
        super().__init__(42, decay, gain)


class Dyn54(DynamicState):
    def __init__(self, decay: float = 0.95, gain: float = 1.0):
        super().__init__(54, decay, gain)


def make_state(name: str, **kwargs: float) -> DynamicState:
    table = {"dyn12": Dyn12, "dyn42": Dyn42, "dyn54": Dyn54}
    if name.lower() not in table:
        raise ValueError(f"unknown state model: {name}")
    return table[name.lower()](**kwargs)
