# Cosmic Rust Engineering Manual

## 1. Design goal

Cosmic Rust exists so builders can use CST mechanisms in native Rust applications without embedding Python or depending on the C++ ABI. The crate emphasizes deterministic behavior, explicit state ownership, low dependency risk, and adapter boundaries.

## 2. State

`DynamicState` is a leaky persistent vector. Each update mixes prior state with a bounded projection of the new signal. `Dyn12`, `Dyn42`, and `Dyn54` provide the same dimensional families used by the other CST language layers.

Use `update(&[f64], dt)`, `update_text`, or `update_scalar`. Inspect state with `vector`, `variance`, `l2`, and `updates`. Use `snapshot`/`restore` for explicit persistence boundaries.

## 3. Synaptic affinity

`GaussianSynapse` converts vector distance into pairwise affinity. `auto()` calibrates bandwidth from the median non-zero pairwise distance. `diagnostics()` reports whether the kernel is collapsing toward identity or a uniform matrix.

## 4. Memory

`SemanticMemory` stores durable records and ranks them with a deterministic hashed-embedding fallback, recency, salience, and confidence. Persistence uses a transparent tab-separated record format with hex-encoded UTF-8 text so the crate can remain dependency-free.

For high-quality semantic search, a host application should wrap a production embedding service and either extend this crate or maintain the external vector index alongside the CST record IDs.

## 5. Hebbian association

`HebbianMemory` strengthens pairwise concept weights when terms co-occur. This is association memory, not transformer attention and not neural weight training.

## 6. Event bus

`EventBus` offers synchronous typed routing. Applications can use it to connect state, memory, simulation, telemetry, or agent components without hard dependencies between them.

## 7. Adapter traits

`ModelAdapter`, `SensorAdapter`, and `EntropySource` are intentionally host-owned boundaries. They do not ship cloud credentials, model vendor SDKs, raw camera access, or fake randomness inside the core crate.

Security-sensitive entropy providers must supply a cryptographically secure implementation. The crate does not label a deterministic PRNG as secure entropy.

## 8. Runtime

`CosmicRuntime` composes dynamic state, semantic memory, Hebbian association, an event bus, and a model adapter. `CosmicRuntime::local()` uses the built-in echo model for a zero-dependency demonstration. `with_model()` accepts an application model implementation.

## 9. Testing

The parent repository CI runs:

```bash
cargo fmt --check
cargo clippy --all-targets
cargo test
cargo run --example quickstart
```

The Rust layer should not be considered release-green until the GitHub Actions Rust job passes on the public commit.

## 10. Interoperability roadmap

Recommended future bridges include:

1. `pyo3` Python extension package for direct Rust/Python calls
2. `cxx` or stable C ABI bridge for C++/Rust integration
3. optional `serde` feature for JSON manifests
4. optional async adapter traits for Tokio applications
5. vector-database adapters
6. WASM build for browser CST applications

These are extensions, not requirements for the dependency-free base crate.
