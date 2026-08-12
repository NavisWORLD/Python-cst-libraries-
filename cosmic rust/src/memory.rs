use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Clone, Debug, PartialEq)]
pub struct MemoryRecord {
    pub id: u64,
    pub text: String,
    pub timestamp: f64,
    pub salience: f64,
    pub confidence: f64,
}

#[derive(Clone, Debug)]
pub struct SemanticMemory {
    path: Option<PathBuf>,
    records: Vec<MemoryRecord>,
    embeddings: Vec<Vec<f64>>,
    dimension: usize,
    next_id: u64,
}

impl Default for SemanticMemory {
    fn default() -> Self {
        Self::new(None::<&Path>, 128).expect("in-memory semantic memory")
    }
}

impl SemanticMemory {
    pub fn new(path: Option<impl AsRef<Path>>, dimension: usize) -> Result<Self, String> {
        if dimension == 0 {
            return Err("embedding dimension must be positive".into());
        }
        let path = path.map(|value| value.as_ref().to_path_buf());
        let mut memory = Self {
            path,
            records: Vec::new(),
            embeddings: Vec::new(),
            dimension,
            next_id: 1,
        };
        memory.load()?;
        Ok(memory)
    }

    pub fn store(&mut self, text: impl Into<String>) -> Result<MemoryRecord, String> {
        self.store_scored(text, 0.5, 1.0)
    }

    pub fn store_scored(
        &mut self,
        text: impl Into<String>,
        salience: f64,
        confidence: f64,
    ) -> Result<MemoryRecord, String> {
        let text = text.into();
        if text.trim().is_empty() {
            return Err("memory text cannot be empty".into());
        }
        let record = MemoryRecord {
            id: self.next_id,
            text,
            timestamp: now(),
            salience: salience.clamp(0.0, 1.0),
            confidence: confidence.clamp(0.0, 1.0),
        };
        self.next_id += 1;
        self.embeddings.push(hashed_embedding(&record.text, self.dimension));
        self.records.push(record.clone());
        self.append(&record)?;
        Ok(record)
    }

    pub fn recall(&self, query: &str, limit: usize) -> Vec<(MemoryRecord, f64)> {
        let query_embedding = hashed_embedding(query, self.dimension);
        let current = now();
        let mut ranked: Vec<_> = self
            .records
            .iter()
            .zip(&self.embeddings)
            .map(|(record, embedding)| {
                let semantic = cosine(&query_embedding, embedding);
                let age_hours = ((current - record.timestamp).max(0.0)) / 3600.0;
                let recency = 1.0 / (1.0 + age_hours / 24.0);
                let score = 0.70 * semantic
                    + 0.10 * recency
                    + 0.15 * record.salience
                    + 0.05 * record.confidence;
                (record.clone(), score)
            })
            .collect();
        ranked.sort_by(|a, b| b.1.total_cmp(&a.1));
        ranked.truncate(limit);
        ranked
    }

    pub fn records(&self) -> &[MemoryRecord] {
        &self.records
    }

    fn append(&self, record: &MemoryRecord) -> Result<(), String> {
        let Some(path) = &self.path else {
            return Ok(());
        };
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|error| error.to_string())?;
        }
        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(path)
            .map_err(|error| error.to_string())?;
        writeln!(
            file,
            "{}\t{}\t{}\t{}\t{}",
            record.id,
            record.timestamp,
            record.salience,
            record.confidence,
            hex_encode(record.text.as_bytes())
        )
        .map_err(|error| error.to_string())
    }

    fn load(&mut self) -> Result<(), String> {
        let Some(path) = &self.path else {
            return Ok(());
        };
        if !path.exists() {
            return Ok(());
        }
        let content = fs::read_to_string(path).map_err(|error| error.to_string())?;
        for line in content.lines().filter(|line| !line.trim().is_empty()) {
            let parts: Vec<_> = line.splitn(5, '\t').collect();
            if parts.len() != 5 {
                continue;
            }
            let id = parts[0].parse::<u64>().map_err(|error| error.to_string())?;
            let timestamp = parts[1].parse::<f64>().map_err(|error| error.to_string())?;
            let salience = parts[2].parse::<f64>().map_err(|error| error.to_string())?;
            let confidence = parts[3].parse::<f64>().map_err(|error| error.to_string())?;
            let bytes = hex_decode(parts[4])?;
            let text = String::from_utf8(bytes).map_err(|error| error.to_string())?;
            let record = MemoryRecord {
                id,
                text,
                timestamp,
                salience,
                confidence,
            };
            self.next_id = self.next_id.max(id + 1);
            self.embeddings.push(hashed_embedding(&record.text, self.dimension));
            self.records.push(record);
        }
        Ok(())
    }
}

pub fn hashed_embedding(text: &str, dimension: usize) -> Vec<f64> {
    let mut vector = vec![0.0; dimension];
    for token in text
        .split(|character: char| !(character.is_ascii_alphanumeric() || character == '_'))
        .filter(|token| !token.is_empty())
    {
        let lowercase = token.to_ascii_lowercase();
        let hash = fnv1a64(lowercase.as_bytes());
        let index = (hash as usize) % dimension;
        let sign = if (hash >> 8) & 1 == 1 { 1.0 } else { -1.0 };
        vector[index] += sign;
    }
    let norm = vector.iter().map(|value| value * value).sum::<f64>().sqrt();
    if norm > 0.0 {
        for value in &mut vector {
            *value /= norm;
        }
    }
    vector
}

fn cosine(a: &[f64], b: &[f64]) -> f64 {
    let denominator = a.iter().map(|value| value * value).sum::<f64>().sqrt()
        * b.iter().map(|value| value * value).sum::<f64>().sqrt();
    if denominator == 0.0 {
        0.0
    } else {
        a.iter().zip(b).map(|(x, y)| x * y).sum::<f64>() / denominator
    }
}

fn now() -> f64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_secs_f64())
        .unwrap_or(0.0)
}

fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut hash = 0xcbf29ce484222325u64;
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

fn hex_encode(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut output = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        output.push(HEX[(byte >> 4) as usize] as char);
        output.push(HEX[(byte & 0x0f) as usize] as char);
    }
    output
}

fn hex_decode(value: &str) -> Result<Vec<u8>, String> {
    if value.len() % 2 != 0 {
        return Err("invalid hex string".into());
    }
    let mut output = Vec::with_capacity(value.len() / 2);
    let bytes = value.as_bytes();
    for index in (0..bytes.len()).step_by(2) {
        let high = hex_value(bytes[index])?;
        let low = hex_value(bytes[index + 1])?;
        output.push((high << 4) | low);
    }
    Ok(output)
}

fn hex_value(value: u8) -> Result<u8, String> {
    match value {
        b'0'..=b'9' => Ok(value - b'0'),
        b'a'..=b'f' => Ok(value - b'a' + 10),
        b'A'..=b'F' => Ok(value - b'A' + 10),
        _ => Err("invalid hex digit".into()),
    }
}
