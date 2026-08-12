#[derive(Clone, Debug, PartialEq)]
pub struct PreflightReport {
    pub omega_varies: bool,
    pub state_varies: bool,
    pub kernel_not_identity: bool,
    pub kernel_not_uniform: bool,
    pub gate_gradient_live: bool,
}

impl PreflightReport {
    pub fn passed(&self) -> bool {
        self.omega_varies
            && self.state_varies
            && self.kernel_not_identity
            && self.kernel_not_uniform
            && self.gate_gradient_live
    }
}

pub fn check_preflight(
    omega: &[f64],
    states: &[Vec<f64>],
    kernel: &[Vec<f64>],
    gate_gradient: f64,
) -> PreflightReport {
    let flat_states: Vec<_> = states.iter().flatten().copied().collect();
    let mut off = Vec::new();
    for i in 0..kernel.len() {
        for j in 0..kernel[i].len() {
            if i != j {
                off.push(kernel[i][j]);
            }
        }
    }
    let off_mean = mean(&off);
    let off_variance = variance(&off);
    let identity_like = !off.is_empty() && off.iter().all(|value| value.abs() < 1e-4);
    let uniform_like = !off.is_empty() && off_mean > 0.999 && off_variance < 1e-8;
    PreflightReport {
        omega_varies: variance(omega) > 1e-8,
        state_varies: variance(&flat_states) > 1e-8,
        kernel_not_identity: !identity_like,
        kernel_not_uniform: !uniform_like,
        gate_gradient_live: gate_gradient.abs() > 1e-8,
    }
}

fn mean(values: &[f64]) -> f64 {
    if values.is_empty() {
        0.0
    } else {
        values.iter().sum::<f64>() / values.len() as f64
    }
}

fn variance(values: &[f64]) -> f64 {
    if values.is_empty() {
        return 0.0;
    }
    let average = mean(values);
    values
        .iter()
        .map(|value| (value - average).powi(2))
        .sum::<f64>()
        / values.len() as f64
}
