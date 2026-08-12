# Migration Guide: 0.1 -> 0.2

## Compatibility promise

Existing 0.1 Python imports and basic CST-L programs remain supported. Unchanged core names include `Dyn12`, `Dyn42`, `Dyn54`, `DynamicState`, `GaussianSynapse`, `SemanticMemory`, `HebbianMemory`, `Heartbeat`, `Lorenz`, `check_preflight`, and `Runtime`.

## Runtime changes

`Runtime` now owns optional `EventBus`, `SensorHub`, entropy adapter, and standard CNS. Defaults remain dependency-free. `Runtime.health()` now returns a richer snapshot.

## CST-L additions

New declarations: `model NAME external`, `sensor NAME external`, and `entropy NAME external`. New instructions: `observe`, `sample`, `generate`, and `snapshot`. `store`, `associate`, `evolve`, and `recall` accept `from=VARIABLE` where applicable.

## New adapter namespace

```python
from cstlib.adapters import OllamaChatAdapter, OllamaEmbeddingAdapter
```

Provider-specific integrations no longer need to be hard-coded into `Runtime`.

## Native core

The C++ static library now includes event bus, Lorenz, Hebbian association, and text-memory primitives in addition to state/synapse.

## Version pinning

Applications depending on 0.1 exact behavior should pin `cst-libraries==0.1.*` until their tests pass on 0.2.
