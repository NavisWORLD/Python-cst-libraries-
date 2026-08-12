"""Mechanism preflight checks for state-kernel experiments."""
from dataclasses import dataclass
from typing import Iterable, Sequence

def variance(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)

@dataclass(slots=True)
class PreflightReport:
    omega_varies: bool
    state_varies: bool
    kernel_not_identity: bool
    kernel_not_uniform: bool
    gate_gradient_live: bool

    @property
    def passed(self) -> bool:
        return all((self.omega_varies, self.state_varies, self.kernel_not_identity, self.kernel_not_uniform, self.gate_gradient_live))

    def require_pass(self) -> None:
        if not self.passed:
            raise RuntimeError(f"CST preflight failed: {self}")

def check_preflight(omega: Iterable[float], states: Sequence[Sequence[float]], kernel: Sequence[Sequence[float]], *, gate_gradient: float, epsilon: float = 1e-8) -> PreflightReport:
    flat_states = [v for row in states for v in row]
    n = len(kernel)
    off = [kernel[i][j] for i in range(n) for j in range(n) if i != j]
    off_mean = sum(off) / len(off) if off else 0.0
    identity_like = all(abs(v) < 1e-4 for v in off) if off else False
    uniform_like = bool(off) and off_mean > 0.999 and variance(off) < epsilon
    return PreflightReport(variance(omega) > epsilon, variance(flat_states) > epsilon, not identity_like, not uniform_like, abs(gate_gradient) > epsilon)
