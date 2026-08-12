# CST Libraries API Reference

## `cstlib.state`

`DynamicState(dimension, decay=0.92, gain=1.0)` exposes `update`, `vector`, `reset`, `snapshot`, `restore`, and `metrics`. Concrete classes: `Dyn12`, `Dyn42`, `Dyn54`.

## `cstlib.synapse`

`GaussianSynapse(bandwidth="median")` exposes `fit(states)`, `affinity(states)`, and `diagnostics(states)`. `KernelDiagnostics` reports bandwidth, diagonal/off-diagonal statistics, and identity/uniform collapse flags.

## `cstlib.memory`

`SemanticMemory(path=None, embedder=None, ...)` exposes `store`, `recall`, `snapshot`, and `reset`. `MemoryRecord` contains id, text, timestamp, salience, confidence, and metadata. `hashed_embedding` is the dependency-free deterministic fallback.

## `cstlib.hebbian`

`HebbianMemory(path=None, learning_rate=0.1, decay=0.001)` exposes `learn`, `associated_with`, and `snapshot`.

## `cstlib.bus`

`EventBus(history=256)` exposes `subscribe`, `emit`, `publish`, `history`, `errors`, and `health`.

## `cstlib.cns`

`CNS.standard()` creates seven named organ slots as explicit deferred components. Methods: `register`, `bind`, `process`, `health`.

## `cstlib.sensory`

`audio_summary`, `LumaMotionTracker`, and `SensorHub` provide dependency-free numeric summaries and sensor orchestration.

## `cstlib.quantum`

`QuantumMeasurement`, `MeasurementArchive`, `SystemEntropy`, and `MeasurementEntropy` provide provider-labelled measurement records and reproducible derivation.

## `cstlib.provenance`

`ExperimentManifest`, `ProvenanceRecord`, `sha256_file`, and `sha256_value` create reproducible receipts.

## `cstlib.runtime`

`Runtime` composes state, memory, associations, heartbeat, model, sensors, entropy, CNS, and event bus. Methods: `start`, `stop`, `respond`, `snapshot`, `health`; constructors: `Runtime.local`, `Runtime.from_config`.

## `cstlib.transformer`

Optional PyTorch: `MixtureOfStatesAttention`, `PhiFeedForward`, `CSTTransformerBlock`, and `torch_available`.

## `cstlib.adapters`

Model: `CallableModelAdapter`, `JSONTextAdapter`, `OllamaChatAdapter`. Embeddings: `HashedEmbeddingAdapter`, `CallableEmbeddingAdapter`, `OllamaEmbeddingAdapter`. Sensors: `AudioReaderAdapter`, `LumaReaderAdapter`. Quantum/entropy: `CallbackEntropyAdapter`, `IBMCountsAdapter`, `AzureResultsAdapter`. Registry: `AdapterRegistry`.

## `cstlib.lang`

`parse`, `load`, `Program.run`, `Program.inspect`, `Program.bind_model`, `Program.bind_sensor`, and `Program.bind_entropy`.
