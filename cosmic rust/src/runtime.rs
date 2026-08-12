use std::collections::HashMap;
use std::path::Path;

use crate::adapters::{EchoModel, ModelAdapter};
use crate::event::{Event, EventBus};
use crate::hebbian::HebbianMemory;
use crate::memory::SemanticMemory;
use crate::state::DynamicState;

pub struct CosmicRuntime<M: ModelAdapter = EchoModel> {
    pub state: DynamicState,
    pub memory: SemanticMemory,
    pub associations: HebbianMemory,
    pub events: EventBus,
    pub model: M,
}

impl CosmicRuntime<EchoModel> {
    pub fn local(path: impl AsRef<Path>) -> Result<Self, String> {
        let memory_path = path.as_ref().join("memory.tsv");
        Ok(Self {
            state: DynamicState::new(12, 0.92, 1.0)?,
            memory: SemanticMemory::new(Some(memory_path), 128)?,
            associations: HebbianMemory::default(),
            events: EventBus::new(),
            model: EchoModel,
        })
    }
}

impl<M: ModelAdapter> CosmicRuntime<M> {
    pub fn with_model(path: impl AsRef<Path>, model: M) -> Result<Self, String> {
        let memory_path = path.as_ref().join("memory.tsv");
        Ok(Self {
            state: DynamicState::new(12, 0.92, 1.0)?,
            memory: SemanticMemory::new(Some(memory_path), 128)?,
            associations: HebbianMemory::default(),
            events: EventBus::new(),
            model,
        })
    }

    pub fn respond(&mut self, message: &str) -> Result<String, String> {
        let recalled = self.memory.recall(message, 3);
        self.state.update_text(message, 1.0)?;
        let mut context = HashMap::new();
        context.insert("state".into(), format!("{:?}", self.state.vector()));
        context.insert(
            "recalled".into(),
            recalled
                .iter()
                .map(|(record, _)| record.text.as_str())
                .collect::<Vec<_>>()
                .join(" | "),
        );
        self.events.emit(
            &Event::new("cosmic-rust", "runtime.before_generate")
                .with_payload("message", message),
        );
        let response = self.model.generate(message, &context)?;
        self.memory.store(message)?;
        self.memory.store(&response)?;
        self.associations.learn(message);
        self.associations.learn(&response);
        self.events.emit(
            &Event::new("cosmic-rust", "runtime.after_generate")
                .with_payload("response", &response),
        );
        Ok(response)
    }
}
