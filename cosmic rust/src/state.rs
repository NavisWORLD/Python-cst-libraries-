use std::f64::consts::PI;

fn fnv1a64(bytes: &[u8], seed: u64) -> u64 {
    let mut hash = 0xcbf29ce484222325u64 ^ seed;
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

fn text_signal(text: &str, dimension: usize) -> Vec<f64> {
    (0..dimension)
        .map(|i| {
            let hash = fnv1a64(text.as_bytes(), i as u64);
            let unit = (hash as f64) / (u64::MAX as f64);
            unit * 2.0 - 1.0
        })
        .collect()
}

fn scalar_signal(value: f64, dimension: usize) -> Vec<f64> {
    (0..dimension)
        .map(|i| value * (((i + 1) as f64) * 0.618_033_988_749_894_8 * PI).sin())
        .collect()
}

#[derive(Clone, Debug, PartialEq)]
pub struct DynamicState {
    dimension: usize,
    decay: f64,
    gain: f64,
    values: Vec<f64>,
    updates: u64,
}

impl DynamicState {
    pub fn new(dimension: usize, decay: f64, gain: f64) -> Result<Self, String> {
        if dimension == 0 {
            return Err("dimension must be positive".into());
        }
        if !(0.0..1.0).contains(&decay) {
            return Err("decay must be in [0, 1)".into());
        }
        Ok(Self {
            dimension,
            decay,
            gain,
            values: vec![0.0; dimension],
            updates: 0,
        })
    }

    pub fn update(&mut self, signal: &[f64], dt: f64) -> Result<&[f64], String> {
        if signal.is_empty() {
            return Err("signal cannot be empty".into());
        }
        if dt <= 0.0 {
            return Err("dt must be positive".into());
        }
        let effective_decay = self.decay.powf(dt);
        let inject = 1.0 - effective_decay;
        for (i, value) in self.values.iter_mut().enumerate() {
            let input = signal[i % signal.len()];
            *value = effective_decay * *value + inject * self.gain * input.tanh();
        }
        self.updates += 1;
        Ok(&self.values)
    }

    pub fn update_text(&mut self, text: &str, dt: f64) -> Result<&[f64], String> {
        let signal = text_signal(text, self.dimension);
        self.update(&signal, dt)
    }

    pub fn update_scalar(&mut self, value: f64, dt: f64) -> Result<&[f64], String> {
        let signal = scalar_signal(value, self.dimension);
        self.update(&signal, dt)
    }

    pub fn vector(&self) -> &[f64] {
        &self.values
    }

    pub fn snapshot(&self) -> Vec<f64> {
        self.values.clone()
    }

    pub fn restore(&mut self, values: &[f64]) -> Result<(), String> {
        if values.len() != self.dimension {
            return Err("snapshot dimension mismatch".into());
        }
        self.values.copy_from_slice(values);
        Ok(())
    }

    pub fn reset(&mut self) {
        self.values.fill(0.0);
        self.updates = 0;
    }

    pub fn dimension(&self) -> usize {
        self.dimension
    }

    pub fn updates(&self) -> u64 {
        self.updates
    }

    pub fn variance(&self) -> f64 {
        if self.values.is_empty() {
            return 0.0;
        }
        let mean = self.values.iter().sum::<f64>() / self.values.len() as f64;
        self.values
            .iter()
            .map(|value| (value - mean).powi(2))
            .sum::<f64>()
            / self.values.len() as f64
    }

    pub fn l2(&self) -> f64 {
        self.values.iter().map(|value| value * value).sum::<f64>().sqrt()
    }
}

pub struct Dyn12(pub DynamicState);
pub struct Dyn42(pub DynamicState);
pub struct Dyn54(pub DynamicState);

impl Dyn12 {
    pub fn new() -> Self {
        Self(DynamicState::new(12, 0.92, 1.0).expect("valid dyn12 defaults"))
    }
}

impl Default for Dyn12 {
    fn default() -> Self {
        Self::new()
    }
}

impl Dyn42 {
    pub fn new() -> Self {
        Self(DynamicState::new(42, 0.94, 1.0).expect("valid dyn42 defaults"))
    }
}

impl Default for Dyn42 {
    fn default() -> Self {
        Self::new()
    }
}

impl Dyn54 {
    pub fn new() -> Self {
        Self(DynamicState::new(54, 0.95, 1.0).expect("valid dyn54 defaults"))
    }
}

impl Default for Dyn54 {
    fn default() -> Self {
        Self::new()
    }
}
