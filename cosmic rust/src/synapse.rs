#[derive(Clone, Debug, PartialEq)]
pub struct KernelDiagnostics {
    pub bandwidth: f64,
    pub diagonal_mean: f64,
    pub off_diagonal_mean: f64,
    pub off_diagonal_variance: f64,
    pub identity_like: bool,
    pub uniform_like: bool,
}

#[derive(Clone, Debug)]
pub struct GaussianSynapse {
    configured_bandwidth: Option<f64>,
    fitted_bandwidth: Option<f64>,
}

impl GaussianSynapse {
    pub fn auto() -> Self {
        Self {
            configured_bandwidth: None,
            fitted_bandwidth: None,
        }
    }

    pub fn fixed(bandwidth: f64) -> Result<Self, String> {
        if bandwidth <= 0.0 {
            return Err("bandwidth must be positive".into());
        }
        Ok(Self {
            configured_bandwidth: Some(bandwidth),
            fitted_bandwidth: Some(bandwidth),
        })
    }

    fn distance(a: &[f64], b: &[f64]) -> Result<f64, String> {
        if a.len() != b.len() {
            return Err("vectors must have the same dimension".into());
        }
        Ok(a.iter()
            .zip(b)
            .map(|(x, y)| (x - y).powi(2))
            .sum::<f64>()
            .sqrt())
    }

    pub fn fit(&mut self, states: &[Vec<f64>]) -> Result<f64, String> {
        if let Some(value) = self.configured_bandwidth {
            self.fitted_bandwidth = Some(value);
            return Ok(value);
        }
        let mut distances = Vec::new();
        for i in 0..states.len() {
            for j in (i + 1)..states.len() {
                let distance = Self::distance(&states[i], &states[j])?;
                if distance > 0.0 {
                    distances.push(distance);
                }
            }
        }
        let value = if distances.is_empty() {
            1.0
        } else {
            distances.sort_by(|a, b| a.total_cmp(b));
            let mid = distances.len() / 2;
            if distances.len() % 2 == 0 {
                (distances[mid - 1] + distances[mid]) / 2.0
            } else {
                distances[mid]
            }
        };
        self.fitted_bandwidth = Some(value);
        Ok(value)
    }

    pub fn affinity(&mut self, states: &[Vec<f64>]) -> Result<Vec<Vec<f64>>, String> {
        if states.is_empty() {
            return Ok(Vec::new());
        }
        let sigma = self.fit(states)?;
        let denominator = 2.0 * sigma * sigma;
        let mut matrix = vec![vec![0.0; states.len()]; states.len()];
        for i in 0..states.len() {
            for j in 0..states.len() {
                let distance = Self::distance(&states[i], &states[j])?;
                matrix[i][j] = (-(distance * distance) / denominator).exp();
            }
        }
        Ok(matrix)
    }

    pub fn diagnostics(&mut self, states: &[Vec<f64>]) -> Result<KernelDiagnostics, String> {
        let matrix = self.affinity(states)?;
        if matrix.is_empty() {
            return Ok(KernelDiagnostics {
                bandwidth: 1.0,
                diagonal_mean: 0.0,
                off_diagonal_mean: 0.0,
                off_diagonal_variance: 0.0,
                identity_like: false,
                uniform_like: false,
            });
        }
        let mut diagonal = Vec::new();
        let mut off = Vec::new();
        for i in 0..matrix.len() {
            for j in 0..matrix.len() {
                if i == j {
                    diagonal.push(matrix[i][j]);
                } else {
                    off.push(matrix[i][j]);
                }
            }
        }
        let diagonal_mean = mean(&diagonal);
        let off_diagonal_mean = mean(&off);
        let off_diagonal_variance = variance(&off);
        Ok(KernelDiagnostics {
            bandwidth: self.fitted_bandwidth.unwrap_or(1.0),
            diagonal_mean,
            off_diagonal_mean,
            off_diagonal_variance,
            identity_like: !off.is_empty() && off.iter().all(|value| value.abs() < 1e-4),
            uniform_like: !off.is_empty()
                && off_diagonal_mean > 0.999
                && off_diagonal_variance < 1e-8,
        })
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
