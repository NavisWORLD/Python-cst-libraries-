"""Canonical CST Synaptic Function v1.

This module is intentionally dependency-free and mirrors the reference C++, Rust,
JavaScript, Go, Java, C#, Swift, Kotlin and C ABI implementations.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, tanh
from typing import Sequence


def gaussian_affinity(a: Sequence[float], b: Sequence[float], sigma: float = 1.0) -> float:
    """Return exp(-||a-b||^2 / (2*sigma^2))."""
    if sigma <= 0:
        raise ValueError("sigma must be > 0")
    if len(a) != len(b) or not a:
        raise ValueError("a and b must be non-empty and have equal length")
    distance_sq = sum((float(x) - float(y)) ** 2 for x, y in zip(a, b))
    return exp(-distance_sq / (2.0 * sigma * sigma))


def affinity_matrix(states: Sequence[Sequence[float]], sigma: float = 1.0) -> list[list[float]]:
    if not states:
        raise ValueError("states must be non-empty")
    dimension = len(states[0])
    if dimension == 0 or any(len(row) != dimension for row in states):
        raise ValueError("all states must be non-empty and have equal dimension")
    return [[gaussian_affinity(a, b, sigma) for b in states] for a in states]


def gated_blend(standard: float, state_affinity: float, gate: float) -> float:
    if not 0.0 <= gate <= 1.0:
        raise ValueError("gate must be in [0, 1]")
    return (1.0 - gate) * float(standard) + gate * float(state_affinity)


def state_step(state: Sequence[float], signal: Sequence[float], *, decay: float = 0.92, gain: float = 1.0, dt: float = 1.0) -> list[float]:
    if len(state) != len(signal) or not state:
        raise ValueError("state and signal must be non-empty and have equal length")
    if not 0.0 <= decay <= 1.0:
        raise ValueError("decay must be in [0, 1]")
    if dt < 0:
        raise ValueError("dt must be >= 0")
    effective_decay = decay**dt
    return [effective_decay * float(x) + (1.0 - effective_decay) * float(gain) * tanh(float(u)) for x, u in zip(state, signal)]


@dataclass(frozen=True)
class SynapticFunction:
    sigma: float = 1.0
    gate: float = 0.5

    def __post_init__(self) -> None:
        if self.sigma <= 0:
            raise ValueError("sigma must be > 0")
        if not 0.0 <= self.gate <= 1.0:
            raise ValueError("gate must be in [0, 1]")

    def affinity(self, a: Sequence[float], b: Sequence[float]) -> float:
        return gaussian_affinity(a, b, self.sigma)

    def matrix(self, states: Sequence[Sequence[float]]) -> list[list[float]]:
        return affinity_matrix(states, self.sigma)

    def blend(self, standard: float, state_affinity: float, gate: float | None = None) -> float:
        return gated_blend(standard, state_affinity, self.gate if gate is None else gate)

    def step(self, state: Sequence[float], signal: Sequence[float], *, decay: float = 0.92, gain: float = 1.0, dt: float = 1.0) -> list[float]:
        return state_step(state, signal, decay=decay, gain=gain, dt=dt)
