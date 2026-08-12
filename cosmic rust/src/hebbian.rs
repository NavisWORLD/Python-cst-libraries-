use std::collections::{HashMap, HashSet};

#[derive(Clone, Debug)]
pub struct HebbianMemory {
    learning_rate: f64,
    decay: f64,
    weights: HashMap<String, HashMap<String, f64>>,
}

impl Default for HebbianMemory {
    fn default() -> Self {
        Self::new(0.1, 0.001)
    }
}

impl HebbianMemory {
    pub fn new(learning_rate: f64, decay: f64) -> Self {
        Self {
            learning_rate,
            decay,
            weights: HashMap::new(),
        }
    }

    pub fn concepts(text: &str) -> Vec<String> {
        let mut set = HashSet::new();
        for token in text.split(|character: char| {
            !(character.is_ascii_alphanumeric() || character == '_' || character == '\'')
        }) {
            let token = token.trim().to_ascii_lowercase();
            if !token.is_empty() {
                set.insert(token);
            }
        }
        let mut values: Vec<_> = set.into_iter().collect();
        values.sort();
        values
    }

    pub fn learn(&mut self, text: &str) {
        let concepts = Self::concepts(text);
        for a in &concepts {
            for b in &concepts {
                if a == b {
                    continue;
                }
                let old = self
                    .weights
                    .get(a)
                    .and_then(|row| row.get(b))
                    .copied()
                    .unwrap_or(0.0);
                self.weights
                    .entry(a.clone())
                    .or_default()
                    .insert(b.clone(), (1.0 - self.decay) * old + self.learning_rate);
            }
        }
    }

    pub fn associated_with(&self, concept: &str, limit: usize) -> Vec<(String, f64)> {
        let mut pairs: Vec<_> = self
            .weights
            .get(&concept.to_ascii_lowercase())
            .map(|row| {
                row.iter()
                    .map(|(key, value)| (key.clone(), *value))
                    .collect()
            })
            .unwrap_or_default();
        pairs.sort_by(|a, b| b.1.total_cmp(&a.1));
        pairs.truncate(limit);
        pairs
    }
}
