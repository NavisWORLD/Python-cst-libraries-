# CST Libraries

**CST Libraries** is an open, modular SDK for the computational mechanisms developed in the COSMOS / Davis Cosmic Synapse Theory project lineage: persistent dynamic state, state affinity ("synapses"), durable semantic memory, Hebbian association, nonlinear dynamics, fail-soft background maintenance, experiment preflight checks, and the starter **CST-L** domain-specific language.

This repository intentionally separates engineering mechanisms from metaphor. It does **not** claim that software state is literal biology, that CST is established physical law, that quantum randomness makes models smarter, or that persistence establishes consciousness.

## What you can build

- stateful AI and agent experiments
- semantic memory systems
- persistent local assistants
- adaptive games and simulations
- reactive music or sensor applications
- dynamic-state neural research prototypes
- reproducible mechanism tests
- CST-L programs that orchestrate state + memory + association

## Python install

Requires Python 3.10+.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -U pip
pip install -e .
```

Development tools:

```bash
pip install -e ".[dev]"
python -m pytest
```

The Python core has **zero runtime dependencies**. You can plug in NumPy, PyTorch, sentence-transformers, FAISS, Qiskit, audio libraries, or your own model adapter without making them mandatory for everyone else.

## Five-minute Python example

```python
from cstlib import Dyn12, GaussianSynapse, HebbianMemory, SemanticMemory

state = Dyn12()
memory = SemanticMemory(".cst/memory.jsonl")
hebb = HebbianMemory(".cst/links.json")

history = []
for message in [
    "music follows rhythm",
    "rhythm follows motion",
    "memory follows meaning",
]:
    history.append(state.update(message))
    memory.store(message)
    hebb.learn(message)

kernel = GaussianSynapse("median")
print(kernel.affinity(history))
print(memory.recall("music and rhythm"))
print(hebb.associated_with("rhythm"))
```

## Reference runtime

```python
from cstlib import Runtime

cosmos = Runtime.local(".cst")
print(cosmos.respond("hello persistent world"))
```

`Runtime` deliberately accepts a normal Python callable as its model adapter, so the core library is not locked to one LLM provider.

## CST-L: the computational language layer

Create `hello.cst`:

```cst
state mind dyn12 decay=0.92
memory life path=.cst/memory.jsonl
hebbian links path=.cst/links.json

loop message
  recall life as remembered
  evolve mind
  associate links
  store life
  emit "INPUT={message}"
  emit "STATE={state.mind}"
  emit "RECALLED={remembered}"
end
```

Run once:

```bash
cst run hello.cst --message "hello from CST-L"
```

Or interactively:

```bash
cst run hello.cst
```

Health check:

```bash
cst doctor
```

Reference demo:

```bash
cst demo
```

See [`docs/LANGUAGE_SPEC.md`](docs/LANGUAGE_SPEC.md) for the current 0.1 grammar and execution model.

## C++ core

The C++17 core implements the low-level dynamic-state and Gaussian-affinity primitives with no third-party runtime dependencies.

```bash
cmake -S . -B build -DCST_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

Run the demo:

```bash
./build/cpp/cst_cpp_demo
```

On multi-config generators such as Visual Studio, the executable may be under `build/cpp/Debug/` or `build/cpp/Release/`.

### Optional Python/C++ bindings

If `pybind11` is installed, the repository can also build the optional `_cst_native` extension:

```bash
pip install pybind11
cmake -S . -B build-native \
  -DCST_BUILD_PYTHON_BINDINGS=ON \
  -Dpybind11_DIR="$(python -m pybind11 --cmakedir)"
cmake --build build-native
```

The native module is intentionally optional. The Python reference implementation remains the portability baseline.

## Package map

| Module | Purpose |
|---|---|
| `cstlib.state` | `DynamicState`, `Dyn12`, `Dyn42`, `Dyn54` |
| `cstlib.synapse` | Gaussian state-affinity kernel + diagnostics |
| `cstlib.memory` | durable JSONL memory + semantic retrieval |
| `cstlib.hebbian` | persistent concept-association weights |
| `cstlib.dynamics` | deterministic nonlinear systems (Lorenz) |
| `cstlib.heartbeat` | fail-soft recurring maintenance tasks |
| `cstlib.proof` | preflight checks for experimental mechanisms |
| `cstlib.runtime` | composable reference runtime |
| `cstlib.lang` | CST-L parser and interpreter |
| `cpp/` | C++17 state/synapse core and optional pybind11 bindings |

## Core computational pattern

```text
observe
  -> remember
  -> evolve state
  -> calculate relationships
  -> choose/act
  -> learn associations
  -> persist
  -> repeat
```

The practical idea is not that every ingredient is novel. It is that state, retrieval, association, background maintenance, and mechanism validation are made explicit and reusable rather than hidden inside one monolithic application.

## Scientific / engineering discipline

Use these labels when documenting results:

- **IMPLEMENTED** — a code path exists.
- **OBSERVED** — the component executed in a captured run.
- **MEASURED** — a defined metric was produced.
- **NULL** — the tested success criterion was not met.
- **HYPOTHESIS** — a falsifiable proposition to test.
- **MODEL / METAPHOR** — a conceptual design lens, not automatically a literal physical or biological statement.

Before accepting a state-kernel benchmark, use `cstlib.proof.check_preflight` to test that the driving signal and state vary, the kernel is neither identity-like nor uniform-like, and the learned gate receives non-zero gradient.

## Teaching

[`docs/TEACHERS_GUIDE.md`](docs/TEACHERS_GUIDE.md) provides a 12-lesson course using the actual SDK: persistent state, dyn12, Gaussian affinity, memory, Hebbian learning, Lorenz dynamics, heartbeat tasks, preflight science, and a CST-L final project.

## Reuse and upstream libraries

This repository's original source is licensed under Apache-2.0. Third-party libraries are **not** relicensed by this repository. If you add PyTorch, NumPy, Qiskit, FAISS, model weights, datasets, or copied/modified upstream code, preserve their original licenses and attribution.

Do not claim authorship of upstream libraries. Document the exact upstream version, what CST changes or wraps, and what evidence supports any performance claim.

## Research lineage

Associated CST research record: DOI `10.5281/zenodo.17574447`.

The broader COSMOS project includes additional transformer, sensory, memory, quantum-provenance, and runtime research. This repository is deliberately the **reusable library layer**, so builders can use individual mechanisms without needing the complete COSMOS application.

## Status

**0.1.0 — working reference SDK / alpha API.**

The Python package, CLI, CST-L interpreter, C++ core, examples, and tests are intended to run now. The API is still young and should evolve through versioned releases rather than silent breaking changes.
