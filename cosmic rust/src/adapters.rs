use std::collections::HashMap;

/// Host-supplied model integration. Credentials and network clients stay outside the CST core.
pub trait ModelAdapter {
    fn generate(
        &mut self,
        message: &str,
        context: &HashMap<String, String>,
    ) -> Result<String, String>;
}

/// Host-supplied sensor integration. Implementations should prefer compact numeric summaries.
pub trait SensorAdapter {
    fn read(&mut self) -> Result<HashMap<String, f64>, String>;
}

/// Host-supplied entropy/provenance source.
///
/// Security-sensitive applications should bind a cryptographically secure implementation.
pub trait EntropySource {
    fn sample(&mut self, bytes: usize) -> Result<Vec<u8>, String>;
    fn label(&self) -> &str;
}

#[derive(Default)]
pub struct EchoModel;

impl ModelAdapter for EchoModel {
    fn generate(
        &mut self,
        message: &str,
        context: &HashMap<String, String>,
    ) -> Result<String, String> {
        let state = context.get("state").cloned().unwrap_or_default();
        Ok(format!("{message}\nstate={state}"))
    }
}
