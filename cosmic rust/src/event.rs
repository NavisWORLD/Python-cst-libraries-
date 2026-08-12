use std::collections::HashMap;
use std::sync::Arc;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Clone, Debug, PartialEq)]
pub struct Event {
    pub source: String,
    pub kind: String,
    pub payload: HashMap<String, String>,
    pub timestamp: f64,
    pub confidence: f64,
}

impl Event {
    pub fn new(source: impl Into<String>, kind: impl Into<String>) -> Self {
        Self {
            source: source.into(),
            kind: kind.into(),
            payload: HashMap::new(),
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map(|duration| duration.as_secs_f64())
                .unwrap_or(0.0),
            confidence: 1.0,
        }
    }

    pub fn with_payload(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.payload.insert(key.into(), value.into());
        self
    }
}

type Handler = Arc<dyn Fn(&Event) + Send + Sync + 'static>;

#[derive(Default)]
pub struct EventBus {
    exact: HashMap<String, Vec<Handler>>,
    all: Vec<Handler>,
}

impl EventBus {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn subscribe<F>(&mut self, kind: impl Into<String>, handler: F)
    where
        F: Fn(&Event) + Send + Sync + 'static,
    {
        self.exact
            .entry(kind.into())
            .or_default()
            .push(Arc::new(handler));
    }

    pub fn subscribe_all<F>(&mut self, handler: F)
    where
        F: Fn(&Event) + Send + Sync + 'static,
    {
        self.all.push(Arc::new(handler));
    }

    pub fn emit(&self, event: &Event) {
        for handler in &self.all {
            handler(event);
        }
        if let Some(handlers) = self.exact.get(&event.kind) {
            for handler in handlers {
                handler(event);
            }
        }
    }
}
