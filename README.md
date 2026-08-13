# CST Libraries 0.3

CST Libraries is an open, modular Python/C++/Rust SDK for persistent-state computation, semantic memory, Hebbian association, state affinity, Mixture-of-States attention, event/CNS routing, sensory summaries, provenance, entropy adapters, CST-L, and packaged CST Studio applications.

The dependency-free Python core remains the portability baseline. Optional integrations are adapters, not hard requirements.

## Download the apps

The **v0.3.0 Packaged Apps** release workflow produces:

- ✅ `CST-Libraries-Windows-Setup.exe` — one-click Windows installer
- ✅ `CST-Libraries-macOS.dmg` + zipped `.app` — macOS application bundle
- ✅ `CST-Cosmic-Mobile-Android.apk` — installable Android application
- ✅ iOS application source + Simulator app + unsigned iPhoneOS IPA for Apple signing
- ✅ Python wheel/source distribution bundled into the GitHub Release

Apple requires developer signing/provisioning for a physical iPhone and notarization credentials for warning-free public macOS distribution. The repository automates everything up to that credential boundary. See `docs/INSTALLERS_AND_APPS.md`.

## Install the developer SDK

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\Activate.ps1
python -m pip install -U pip
pip install -e .
cst doctor
```

Optional components:

```bash
pip install -e ".[dev]"
pip install -e ".[torch]"      # Mixture-of-States transformer components
pip install -e ".[native]"     # pybind11 build dependency
pip install -e ".[ibm]"        # convenience IBM Quantum SDK dependencies
pip install -e ".[azure]"      # convenience Azure Quantum SDK dependency
```

## First project

```bash
cst init my-cst-project
cst run my-cst-project/main.cst --message "hello CST"
```

## Python runtime

```python
from cstlib import Runtime
from cstlib.adapters import OllamaChatAdapter

runtime = Runtime.local(
    ".cst",
    model=OllamaChatAdapter(model="qwen3")
)
print(runtime.respond("Remember that my synth is tuned to A=432 for this experiment."))
```

## Adapter families

```bash
cst adapters
```

Built-in adapter contracts cover:

- model generation: callable, generic JSON HTTP, Ollama chat
- embeddings: hashed fallback, callable, Ollama embed
- sensory: application-owned audio reader, numeric luma/motion reader
- entropy: OS CSPRNG, archived measurement derivation, callback source
- quantum result provenance: IBM counts, Azure result mappings
- CNS/event routing: replaceable organ handlers and deferred named slots
- optional PyTorch Mixture-of-States attention
- optional C++/pybind11 low-level core
- dependency-free Rust implementation layer in `cosmic rust/`

## CST-L 0.2 language layer

CST-L remains intentionally small and auditable. It can declare persistent state/memory and host-bound external adapters without embedding credentials in source.

```cst
state mind dyn12 decay=0.92
memory life path=.cst/memory.jsonl
hebbian links path=.cst/links.json
model band external
sensor mic external
entropy provenance external

loop message
  recall life as remembered
  observe mic as audio
  sample provenance as entropy bytes=16
  evolve mind
  generate band as answer
  store life from=answer
  associate links from=answer
  snapshot mind as now
  emit "{answer}"
  emit "state={now}"
end
```

External declarations are bindings supplied by the host application; CST-L does not execute arbitrary Python.

## C++17

```bash
cmake -S . -B build -DCST_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

The native library exposes dependency-free state, Gaussian affinity, events/event bus, Hebbian association, simple durable memory, and Lorenz dynamics. Optional pybind11 bindings expose the low-level primitives to Python.

## Cosmic Rust

A Rust implementation lives in **`cosmic rust/`**.

```bash
cd "cosmic rust"
cargo build
cargo test
cargo run --example quickstart
```

The `cosmic-rust` crate mirrors CST's reusable state, synapse, memory, Hebbian, dynamics, event, preflight, adapter-trait, and runtime concepts using idiomatic Rust and no third-party dependencies.

## Application source

- `apps/desktop/` — CST Studio desktop application used by Windows/macOS packaging
- `apps/mobile/` — Capacitor mobile application used by Android/iOS packaging
- `packaging/` — installer scripts and packaged-release notes
- `.github/workflows/release.yml` — multi-platform binary build + GitHub Release automation

## Documentation

- `docs/INSTALLATION.md` — Python/C++/native install matrix
- `docs/INSTALLERS_AND_APPS.md` — Windows, macOS, Android, iOS and release guide
- `docs/DEVELOPER_GUIDE.md` — architecture and extension contracts
- `docs/ADAPTER_GUIDE.md` — model, embedding, sensory, quantum, CNS adapters
- `docs/LANGUAGE_SPEC.md` — CST-L grammar and host bindings
- `docs/TRANSFORMER_GUIDE.md` — Mixture-of-States attention
- `docs/QUANTUM_PROVENANCE.md` — provider-result discipline
- `docs/TEACHERS_GUIDE.md` — teachable course/labs
- `docs/SECURITY_PRIVACY.md` — credentials, raw-media, provenance boundaries
- `cosmic rust/MANUAL.md` — Rust architecture, APIs, testing, and interoperability

## Scientific boundary

CST Libraries distinguishes **implemented**, **observed**, **measured**, **null**, **hypothesis**, and **model/metaphor**. Persistent software state is not evidence of consciousness. Quantum provenance is not quantum advantage. Simulation variables are not automatically physical law.

## License

Original repository code is Apache-2.0. Third-party SDKs, models, weights, and datasets retain their own licenses.
