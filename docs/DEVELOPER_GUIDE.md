# CST Libraries Developer Guide

## 1. Architecture

CST Libraries is intentionally not a monolith. The reference flow is:

```text
input event
  -> semantic recall
  -> sensory summaries
  -> entropy/provenance summary
  -> persistent dynamic state update
  -> CNS/event routing
  -> model adapter
  -> persistent dialogue + Hebbian association
  -> output event
  -> background heartbeat maintenance
```

Core modules are dependency-free. Provider-specific or heavy systems attach through protocols.

## 2. Core contracts

### State

`DynamicState` exposes `update(signal, dt=1.0)`, `vector()`, `snapshot()`, `restore(snapshot)`, `reset()`, and `metrics()`. Built-in forms are `Dyn12`, `Dyn42`, and `Dyn54`.

### Memory

`SemanticMemory` stores durable records and ranks them with semantic similarity, recency, salience, and confidence. The built-in hashed embedding is a deterministic fallback, not a replacement for a strong purpose-built embedding model.

### Hebbian association

`HebbianMemory` is a separate cross-concept association store. Do not call it transformer attention.

### Synapse

`GaussianSynapse` converts distances between state vectors into affinity. `bandwidth="median"`/`"auto"` calibrates the kernel from non-zero pairwise distances.

### Event bus

`EventBus` delivers events synchronously and fail-soft. Exact event kinds and `*` wildcard subscriptions are supported.

### CNS

`CNS.standard()` creates the seven historical project slots: quantum, dark_matter, emeth, plasticity, awareness, daemons, and surgeon. Unconfigured slots are explicit `DeferredOrgan` objects. They do nothing and report themselves as deferred; they are not fake implementations.

## 3. Writing an adapter

Adapters should have four properties: narrow interface, clear failures, health/configuration reporting, and no credential/raw-private-data leakage into runtime context.

```python
class MyModel:
    name = "my-model"
    def __call__(self, message, context):
        return my_backend_generate(message, context)
    def health(self):
        return {"name": self.name, "ok": True}
```

## 4. Runtime composition

```python
from cstlib import Runtime, SensorHub
from cstlib.adapters import OllamaChatAdapter
runtime = Runtime.local(".cst", model=OllamaChatAdapter("qwen3"), sensors=SensorHub())
```

The runtime does not own provider credentials. Inject configured adapters from your application.

## 5. Events

Useful built-in event kinds include `runtime.started`, `runtime.stopped`, `conversation.input`, `conversation.output`, `sensor.audio`, `sensor.vision`, `sensor.error`, and `organ.<name>`. Applications may define additional namespaced kinds.

## 6. Provenance

Use `ExperimentManifest` for reproducible experiment metadata and `ProvenanceRecord` for hashed artifacts.

```python
from cstlib import ExperimentManifest
manifest = ExperimentManifest("dyn12-ablation", config={"state":"dyn12","bandwidth":"median"}, seeds=[1,2,3], dataset_hash="...", code_hash="...")
manifest.save("results/run.json")
```

A manifest receipt is SHA-256 over canonical JSON.

## 7. Testing policy

Before accepting a state-kernel result, the driving signal must vary, state must vary, the kernel must not collapse to identity or uniform, and the learned gate path must receive non-zero gradient. Use `check_preflight` and publish a failing preflight as a failed experiment rather than a benchmark result.

## 8. Extension policy

Prefer a new adapter or module over modifying unrelated core behavior. Breaking public APIs require a version bump and migration note. Do not introduce heavy imports at `import cstlib` time unless caught as optional dependencies.

## 9. Adding a new state model

Subclass `DynamicState` or implement its observable contract, then add it to `make_state` only after tests exist.

## 10. Adding a new CST-L host binding

External systems are declared in CST-L but bound by the host program. This keeps credentials and arbitrary Python execution outside source files. Do not add unrestricted `eval`, shell, or arbitrary Python blocks to the default interpreter.
