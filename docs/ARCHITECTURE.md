# CST Libraries 0.2 Architecture

## Layers

```text
APPLICATION / CST-L HOST
        |
        +-- model adapters
        +-- embedding adapters
        +-- sensory adapters
        +-- entropy/provenance adapters
        |
CST RUNTIME
        |
        +-- EventBus
        +-- CNS organ controller
        +-- Heartbeat
        |
COMPUTATIONAL PRIMITIVES
        |
        +-- DynamicState (dyn12/42/54)
        +-- GaussianSynapse
        +-- SemanticMemory
        +-- HebbianMemory
        +-- Lorenz dynamics
        +-- provenance manifests
        |
OPTIONAL ACCELERATION / RESEARCH
        |
        +-- PyTorch Mixture-of-States attention
        +-- C++17 core
        +-- pybind11 extension
```

## Dependency rule

The arrows point inward: heavy/provider-specific systems depend on CST contracts; CST core does not import provider SDKs.

## Timescales

CST separates multiple timescales: per-observation numeric features, per-token/per-event dynamic state, per-turn memory and association, cross-session persistence, scheduled heartbeat maintenance, and experiment/archive provenance.

## Data ownership

Adapters receive buffers or provider results from the host application. The host owns credentials, device permissions, and raw-media retention policy.

## Standard CNS slots

The seven historical names are retained as configurable slots. `CNS.standard()` makes unbound slots `DeferredOrgan` instances so a health report can say "not configured" instead of pretending a subsystem is active.

## Native boundary

The C++ layer implements computation-heavy, provider-independent primitives. Networking, cloud authentication, and device capture stay in Python/application adapters.
