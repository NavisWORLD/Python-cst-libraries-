#[derive(Debug, Clone, Copy)]
pub struct SynapticFunction {
    pub sigma: f64,
    pub gate: f64,
}

impl Default for SynapticFunction {
    fn default() -> Self {
        Self {
            sigma: 1.0,
            gate: 0.5,
        }
    }
}

impl SynapticFunction {
    pub fn new(sigma: f64, gate: f64) -> Result<Self, String> {
        if sigma <= 0.0 {
            return Err("sigma must be > 0".into());
        }
        if !(0.0..=1.0).contains(&gate) {
            return Err("gate must be in [0,1]".into());
        }
        Ok(Self { sigma, gate })
    }

    pub fn affinity(&self, a: &[f64], b: &[f64]) -> Result<f64, String> {
        if a.is_empty() || a.len() != b.len() {
            return Err("vectors must be non-empty and equal length".into());
        }
        let distance_sq: f64 = a
            .iter()
            .zip(b)
            .map(|(x, y)| {
                let d = x - y;
                d * d
            })
            .sum();
        Ok((-distance_sq / (2.0 * self.sigma * self.sigma)).exp())
    }

    pub fn matrix(&self, states: &[Vec<f64>]) -> Result<Vec<Vec<f64>>, String> {
        if states.is_empty() || states[0].is_empty() {
            return Err("states must be non-empty".into());
        }
        let dimension = states[0].len();
        if states.iter().any(|row| row.len() != dimension) {
            return Err("state dimensions must match".into());
        }
        states
            .iter()
            .map(|a| states.iter().map(|b| self.affinity(a, b)).collect())
            .collect()
    }

    pub fn blend(&self, standard: f64, affinity: f64, gate: Option<f64>) -> Result<f64, String> {
        let g = gate.unwrap_or(self.gate);
        if !(0.0..=1.0).contains(&g) {
            return Err("gate must be in [0,1]".into());
        }
        Ok((1.0 - g) * standard + g * affinity)
    }

    pub fn step(
        &self,
        state: &[f64],
        signal: &[f64],
        decay: f64,
        gain: f64,
        dt: f64,
    ) -> Result<Vec<f64>, String> {
        if state.is_empty() || state.len() != signal.len() {
            return Err("state and signal must be non-empty and equal length".into());
        }
        if !(0.0..=1.0).contains(&decay) || dt < 0.0 {
            return Err("invalid decay or dt".into());
        }
        let effective_decay = decay.powf(dt);
        Ok(state
            .iter()
            .zip(signal)
            .map(|(x, u)| effective_decay * x + (1.0 - effective_decay) * gain * u.tanh())
            .collect())
    }
}

pub fn gaussian_affinity(a: &[f64], b: &[f64], sigma: f64) -> Result<f64, String> {
    SynapticFunction::new(sigma, 0.5)?.affinity(a, b)
}

pub fn gated_blend(standard: f64, affinity: f64, gate: f64) -> Result<f64, String> {
    SynapticFunction::new(1.0, gate)?.blend(standard, affinity, None)
}

pub fn state_step(
    state: &[f64],
    signal: &[f64],
    decay: f64,
    gain: f64,
    dt: f64,
) -> Result<Vec<f64>, String> {
    SynapticFunction::default().step(state, signal, decay, gain, dt)
}
