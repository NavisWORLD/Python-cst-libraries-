# Cosmic Rust

`cosmic rust/` is the Rust implementation layer for CST Libraries.

The crate is intentionally dependency-free. It mirrors the reusable engineering concepts in the Python and C++ layers while using idiomatic Rust ownership, traits, `Result`-based errors, and strongly typed structures.

## Included modules

- `state` — persistent `DynamicState`, `Dyn12`, `Dyn42`, `Dyn54`
- `synapse` — Gaussian state affinity and kernel diagnostics
- `memory` — durable semantic memory with deterministic hashed embeddings
- `hebbian` — concept-association learning
- `dynamics` — RK4 Lorenz system
- `event` — typed events and synchronous event bus
- `preflight` — mechanism-liveness checks
- `adapters` — model, sensor, and entropy integration traits
- `runtime` — composable persistent `CosmicRuntime`

## Build

```bash
cd "cosmic rust"
cargo build
cargo test
cargo run --example quickstart
```

## Use from another Rust project

```toml
[dependencies]
cosmic-rust = { path = "../Python-cst-libraries-/cosmic rust" }
```

```rust
use cosmic_rust::{Dyn12, GaussianSynapse};

let mut state = Dyn12::new();
state.0.update_text("hello persistent world", 1.0)?;

let states = vec![vec![0.0, 0.0], vec![1.0, 0.5]];
let diagnostics = GaussianSynapse::auto().diagnostics(&states)?;
# Ok::<(), String>(())
```

## Adapter boundary

Rust host applications implement these traits:

```rust
pub trait ModelAdapter { /* generate */ }
pub trait SensorAdapter { /* numeric summary */ }
pub trait EntropySource { /* labelled bytes */ }
```

That keeps credentials, network clients, hardware handles, and raw sensor ownership outside the core crate.

## Scientific boundary

The Rust layer follows the same claim discipline as the rest of CST Libraries. Persistent state is software state, not evidence of consciousness. Lorenz dynamics are deterministic nonlinear dynamics, not a claim of literal dark-matter coupling. Entropy provenance and model performance are separate questions.

## License

Apache-2.0, matching the parent repository's original CST Libraries code.
