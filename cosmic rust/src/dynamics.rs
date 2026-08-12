#[derive(Clone, Debug, PartialEq)]
pub struct Lorenz {
    pub sigma: f64,
    pub rho: f64,
    pub beta: f64,
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Default for Lorenz {
    fn default() -> Self {
        Self {
            sigma: 10.0,
            rho: 28.0,
            beta: 8.0 / 3.0,
            x: 1.0,
            y: 1.0,
            z: 1.0,
        }
    }
}

impl Lorenz {
    fn derivative(&self, x: f64, y: f64, z: f64) -> (f64, f64, f64) {
        (
            self.sigma * (y - x),
            x * (self.rho - z) - y,
            x * y - self.beta * z,
        )
    }

    pub fn step(&mut self, dt: f64) -> Result<(f64, f64, f64), String> {
        if dt <= 0.0 {
            return Err("dt must be positive".into());
        }
        let (x, y, z) = (self.x, self.y, self.z);
        let k1 = self.derivative(x, y, z);
        let k2 = self.derivative(
            x + dt * k1.0 / 2.0,
            y + dt * k1.1 / 2.0,
            z + dt * k1.2 / 2.0,
        );
        let k3 = self.derivative(
            x + dt * k2.0 / 2.0,
            y + dt * k2.1 / 2.0,
            z + dt * k2.2 / 2.0,
        );
        let k4 = self.derivative(x + dt * k3.0, y + dt * k3.1, z + dt * k3.2);
        self.x += dt * (k1.0 + 2.0 * k2.0 + 2.0 * k3.0 + k4.0) / 6.0;
        self.y += dt * (k1.1 + 2.0 * k2.1 + 2.0 * k3.1 + k4.1) / 6.0;
        self.z += dt * (k1.2 + 2.0 * k2.2 + 2.0 * k3.2 + k4.2) / 6.0;
        Ok((self.x, self.y, self.z))
    }
}
