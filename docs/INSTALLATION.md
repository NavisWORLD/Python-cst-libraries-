# CST Libraries Installation Manual

## Supported baseline

- Python 3.10+
- C++17 compiler for the native core
- CMake 3.18+
- No mandatory Python runtime dependencies

The zero-dependency Python implementation is the compatibility reference. Optional adapters are installed only when the host application needs them.

## Python development install

```bash
git clone https://github.com/NavisWORLD/Python-cst-libraries-.git
cd Python-cst-libraries-
python -m venv .venv
```

Activate the environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Then:

```bash
python -m pip install -U pip
pip install -e .
cst doctor
python -m pytest
```

## Optional extras

```bash
pip install -e ".[dev]"      # pytest, ruff, build
pip install -e ".[torch]"    # transformer/Mixture-of-States components
pip install -e ".[native]"   # pybind11 build dependency
pip install -e ".[ibm]"      # convenience IBM/Qiskit environment
pip install -e ".[azure]"    # convenience Azure Quantum environment
```

CST's IBM/Azure result adapters themselves do not require the cloud SDKs. The extras are conveniences for applications that also submit jobs through those providers.

## First CST-L project

```bash
cst init hello-cst
cst inspect hello-cst/main.cst
cst run hello-cst/main.cst --message "hello"
```

## C++ core

Linux/macOS:

```bash
cmake -S . -B build -DCST_BUILD_TESTS=ON
cmake --build build -j
ctest --test-dir build --output-on-failure
./build/cpp/cst_cpp_demo
```

Windows with Visual Studio:

```powershell
cmake -S . -B build -DCST_BUILD_TESTS=ON
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
.\build\cpp\Release\cst_cpp_demo.exe
```

## Optional pybind11 native module

Install pybind11:

```bash
pip install -e ".[native]"
```

Configure:

```bash
cmake -S . -B build-native \
  -DCST_BUILD_PYTHON_BINDINGS=ON \
  -Dpybind11_DIR="$(python -m pybind11 --cmakedir)"
cmake --build build-native
```

On Windows, replace the shell substitution with the path printed by:

```powershell
python -m pybind11 --cmakedir
```

Place the resulting `_cst_native` extension on `PYTHONPATH` or install it through the packaging system of your application.

## Ollama adapter

No Python Ollama package is required. The built-in adapter talks to Ollama's local HTTP API.

```python
from cstlib.adapters import OllamaChatAdapter

model = OllamaChatAdapter(model="qwen3")
print(model.probe())
```

Default base URL: `http://localhost:11434`.

## Troubleshooting

### `cst` command not found

Use:

```bash
python -m cstlib doctor
```

and confirm the virtual environment is active.

### CMake cannot find pybind11

Use the exact directory from:

```bash
python -m pybind11 --cmakedir
```

and pass it as `-Dpybind11_DIR=...`.

### Optional cloud packages conflict

Create separate virtual environments for provider experiments. The CST core does not need IBM, Azure, Torch, audio, vision, or model-provider packages to run.
