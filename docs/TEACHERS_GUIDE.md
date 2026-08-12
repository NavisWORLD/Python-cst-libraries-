# CST Libraries Teacher's Guide

## Course purpose

This course teaches how a speculative systems idea becomes executable software, then measurable mechanisms. Students are not asked to accept CST as physical law. They are asked to build, inspect, break, measure, and reproduce computational systems.

## Audience

Suitable for advanced high school programming, undergraduate computer science/AI, independent engineering study, machine-learning clubs, and creative coding/computational music. Recommended prerequisites are basic Python, functions/classes, lists/dictionaries, and introductory algebra.

## Learning outcomes

Students should be able to:

1. distinguish state from stateless computation
2. explain persistence and time-dependent behavior
3. implement and inspect a leaky dynamic state
4. turn state distance into Gaussian affinity
5. identify identity-like and uniform-like kernel collapse
6. separate durable storage, semantic retrieval, and Hebbian association
7. explain deterministic chaos with Lorenz dynamics
8. build privacy-preserving numeric sensor summaries
9. distinguish quantum provenance from performance advantage
10. construct event-driven software and fail-soft components
11. use experiment manifests and hashes
12. write and host-bind a CST-L program
13. explain what evidence would and would not support a scientific claim

# Twelve lessons

## Lesson 1 — State and history

Build a stateless adder and a persistent accumulator.

Discussion: Why can identical inputs produce different outputs in a stateful system? Which variable encodes history?

Lab:

```python
from cstlib import Dyn12
state = Dyn12(decay=0.5)
print(state.update([1]))
print(state.update([0]))
```

Explain why the second state remains non-zero.

## Lesson 2 — Twelve-dimensional dynamic state

Visualize all 12 channels after a sequence of signals. Compare decay values 0.1, 0.5, 0.92, and 0.99. Ask which setting retains information longest.

## Lesson 3 — State relationships

Create several vectors and compute:

```python
GaussianSynapse("median").affinity(states)
```

Students inspect the matrix and identify close/far pairs.

## Lesson 4 — Break the kernel

Run a kernel with an extremely small bandwidth and an extremely large bandwidth. Measure off-diagonal mean, off-diagonal variance, `identity_like`, and `uniform_like`.

Core lesson: code can run while the proposed mechanism is functionally inert.

## Lesson 5 — Memory is not storage

Create 50 memory records with one relevant sentence among distractors. Compare chronological last-N retrieval, token matching, the built-in hashed semantic fallback, and an optional purpose-built embedding adapter.

Students must explain why a file on disk is not enough to call a system useful memory.

## Lesson 6 — Hebbian association

Train repeated concept groups:

```text
music rhythm stage
music rhythm tempo
rain umbrella weather
```

Query association strengths. Discuss the difference between this association store and neural-network attention.

## Lesson 7 — Event-driven systems

Use `EventBus`. Create one normal handler and one handler that intentionally throws an exception. Verify the other handler still runs. Discuss fail-soft design.

## Lesson 8 — Sensory summaries

Students synthesize a sine wave in Python and compute `audio_summary`. No microphone is required. Then use two fake luma frames and calculate motion.

Privacy question: what is lost and what is preserved when raw media becomes numeric telemetry?

## Lesson 9 — Chaos and deterministic dynamics

Run two Lorenz systems with nearly identical initial conditions. Record divergence. Students must explain why deterministic chaos is not identical to randomness.

## Lesson 10 — Provenance and quantum controls

Use synthetic provider counts:

```python
measurement = IBMCountsAdapter.measurement(
    {"00": 500, "11": 524},
    backend="classroom-fixture",
    hardware=False,
)
```

Create a receipt and deterministic derived seed. Discuss what provenance establishes and what would be required to claim performance advantage.

## Lesson 11 — Mixture-of-States attention

If PyTorch is available, construct a tiny layer and inspect gate/sigma diagnostics. If PyTorch is unavailable, derive the mixture by hand using two 3x3 matrices.

Students must explain why a learned gate value changing is insufficient evidence of task benefit.

## Lesson 12 — CST-L final project

Students create a `.cst` program with state, memory, association, an external model placeholder, optional synthetic sensor, snapshot, and generated response. The teacher provides safe host bindings.

# Final project choices

1. persistent study assistant
2. reactive musical state engine
3. stateful NPC/game controller
4. experiment evidence recorder
5. CST-L educational compiler visualization
6. simulated sensor/CNS dashboard
7. tiny state-conditioned transformer experiment

# Rubric

## Mechanism correctness — 30%

The student can show internal state and explain every update.

## Reproducibility — 20%

Seeds/configuration/data are documented and a manifest is produced.

## Claim discipline — 20%

The report distinguishes implementation, observation, measurement, nulls, and hypothesis.

## Tests — 20%

The student intentionally tests at least one failure mode.

## Communication — 10%

Another student can install and run the project from the instructions.

# Oral exam questions

1. Why can an added neural mechanism be present in code but absent in behavior?
2. What happens to a Gaussian affinity kernel when sigma is too small? Too large?
3. Why does persistent JSON not automatically equal semantic memory?
4. What is the difference between Hebbian association and attention?
5. Why does a Lorenz trajectory remain deterministic?
6. Why should raw camera/audio retention be a separate decision from feature extraction?
7. What does a quantum job receipt prove?
8. What would a matched quantum-vs-classical control require?
9. Why are external CST-L adapters host-bound?
10. What evidence would be necessary before making a consciousness claim?

# Suggested answers

1. The baseline path may optimize loss while the added path is constant, identity-like, uniform, clamped, or gradient-dead.
2. Too small tends toward identity; too large tends toward uniform affinity.
3. Useful memory requires retrieval, ranking, policy, and compact reinsertion into current context.
4. Hebbian association is a persistent learned relationship store; attention is a per-forward-pass neural weighting mechanism.
5. Its future follows deterministic differential equations from the initial condition, even though nearby trajectories can diverge rapidly.
6. Feature summaries can support a task without automatically creating a permanent archive of sensitive media.
7. It proves integrity/provenance of the recorded data under the stated provider metadata; it does not prove ML advantage.
8. Same architecture/data/training protocol/distribution and predeclared metric, with multiple seeds and a strong classical control.
9. To keep credentials, devices, and arbitrary integration code outside shareable language source.
10. A validated operational definition and independent causal/behavioral evidence far beyond persistence or self-description.
