# CST Libraries Teacher's Guide

## Course goal

Teach students how persistent state, semantic memory, associative learning, state affinity, nonlinear dynamics and reproducibility can be assembled into testable software without confusing metaphor with evidence.

## Learning outcomes

Students should be able to:

1. distinguish a stateless function from a persistent state machine;
2. implement and visualize a leaky dynamic state;
3. explain Gaussian affinity and detect identity/uniform kernel collapse;
4. separate durable storage, semantic retrieval and Hebbian association;
5. build a fail-soft maintenance loop;
6. explain deterministic chaos using the Lorenz system;
7. write and execute a small CST-L program;
8. design preflight checks before reporting benchmark results;
9. preserve null results and provenance;
10. build a project using only the CST modules it actually needs.

## Twelve lessons

### 1. State
Build an accumulator and compare it with a pure function. Discuss why equal inputs may produce different outputs when history matters.

### 2. Dynamic state
Implement `x[t+1] = decay*x[t] + (1-decay)*signal`. Compare several decay values.

### 3. dyn12
Use `Dyn12`, feed a sequence of observations and plot or print the 12 channels.

### 4. Synaptic affinity
Create state vectors and compute a Gaussian affinity matrix with `GaussianSynapse`.

### 5. Kill the kernel on purpose
Use an extremely small and extremely large fixed bandwidth. Explain identity-like and uniform-like collapse.

### 6. Durable memory
Store records in JSONL. Restart the program and confirm they reload.

### 7. Semantic recall
Hide one relevant record among distractors. Compare recall quality and discuss why storage alone is not retrieval.

### 8. Hebbian association
Repeatedly co-present concepts and inspect how pair weights change.

### 9. Nonlinear dynamics
Run two Lorenz systems from nearby initial conditions and observe divergence.

### 10. Heartbeat
Schedule a maintenance task. Intentionally make another task fail and verify the foreground program survives.

### 11. Preflight science
Run `check_preflight` before accepting a state-kernel experiment. Discuss why normal training loss can improve while an experimental mechanism is inactive.

### 12. CST-L final project
Create a `.cst` program that evolves state, remembers input, learns associations and emits inspectable output.

## Instructor rule

Ask one question repeatedly: **How do you know the mechanism you named is actually doing something?**

Require students to show internal state, controlled comparisons, provenance and failures rather than relying on names or visual presentation.
