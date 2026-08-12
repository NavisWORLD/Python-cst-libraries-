"""Deterministic nonlinear systems for CST experiments."""
from dataclasses import dataclass

@dataclass
class Lorenz:
    sigma: float = 10.0
    rho: float = 28.0
    beta: float = 8.0 / 3.0
    x: float = 1.0
    y: float = 1.0
    z: float = 1.0

    def _f(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        return self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z

    def step(self, dt: float = 0.01) -> tuple[float, float, float]:
        if dt <= 0:
            raise ValueError("dt must be positive")
        x, y, z = self.x, self.y, self.z
        k1 = self._f(x, y, z)
        k2 = self._f(x + dt*k1[0]/2, y + dt*k1[1]/2, z + dt*k1[2]/2)
        k3 = self._f(x + dt*k2[0]/2, y + dt*k2[1]/2, z + dt*k2[2]/2)
        k4 = self._f(x + dt*k3[0], y + dt*k3[1], z + dt*k3[2])
        self.x += dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6
        self.y += dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        self.z += dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6
        return self.x, self.y, self.z

    def snapshot(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}
