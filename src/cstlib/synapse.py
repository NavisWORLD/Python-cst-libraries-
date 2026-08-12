"""State affinity kernels for CST computation."""
import math
import statistics
from dataclasses import dataclass
from typing import Sequence


def _distance(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same dimension")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

@dataclass
class KernelDiagnostics:
    bandwidth: float
    diagonal_mean: float
    off_diagonal_mean: float
    off_diagonal_variance: float
    identity_like: bool
    uniform_like: bool

class GaussianSynapse:
    def __init__(self, bandwidth: float | str = "median") -> None:
        if isinstance(bandwidth, str) and bandwidth not in {"median", "auto"}:
            raise ValueError("bandwidth string must be 'median' or 'auto'")
        if isinstance(bandwidth, (int, float)) and bandwidth <= 0:
            raise ValueError("bandwidth must be positive")
        self.bandwidth = bandwidth
        self.fitted_bandwidth: float | None = None

    def fit(self, states: Sequence[Sequence[float]]) -> float:
        distances = []
        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                d = _distance(states[i], states[j])
                if d > 0:
                    distances.append(d)
        self.fitted_bandwidth = statistics.median(distances) if distances else 1.0
        return self.fitted_bandwidth

    def _sigma(self, states: Sequence[Sequence[float]]) -> float:
        if isinstance(self.bandwidth, (int, float)):
            return float(self.bandwidth)
        return self.fitted_bandwidth or self.fit(states)

    def affinity(self, states: Sequence[Sequence[float]]) -> list[list[float]]:
        if not states:
            return []
        sigma = self._sigma(states)
        denom = 2.0 * sigma * sigma
        return [[math.exp(-(_distance(a, b) ** 2) / denom) for b in states] for a in states]

    def diagnostics(self, states: Sequence[Sequence[float]]) -> KernelDiagnostics:
        matrix = self.affinity(states)
        if not matrix:
            return KernelDiagnostics(1.0, 0.0, 0.0, 0.0, False, False)
        diag = [matrix[i][i] for i in range(len(matrix))]
        off = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if i != j]
        off_mean = sum(off) / len(off) if off else 0.0
        off_var = sum((v - off_mean) ** 2 for v in off) / len(off) if off else 0.0
        return KernelDiagnostics(self._sigma(states), sum(diag) / len(diag), off_mean, off_var, off_mean < 1e-4, off_mean > 0.999 and off_var < 1e-8)
