# Architecture

The SDK is intentionally layered.

```text
input
  -> DynamicState (persistent control state)
  -> GaussianSynapse (state relationships)
  -> SemanticMemory (durable meaning-based recall)
  -> HebbianMemory (slow concept association)
  -> Runtime (composition and model adapter)
  -> Heartbeat (background maintenance)
  -> Proof (mechanism preflight)
```

The C++ core currently implements the lowest-level state and Gaussian affinity mechanisms. Python provides the reference runtime, persistence, scheduler, testing utilities and CST-L interpreter.

## Evidence boundaries

Names such as `CST`, `COSMOS`, `heartbeat`, `synapse`, or `organ` are software vocabulary. They do not imply literal biology, consciousness, new physics, or quantum performance advantage.

The core engineering principle is to keep every mechanism inspectable and replace broad claims with tests.
