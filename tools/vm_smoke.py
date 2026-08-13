#!/usr/bin/env python3
"""Clean-machine smoke test for CST Synaptic Function v1.

This script verifies the pure Python implementation, JSON bridge, compiled C++
shared library, and compiled Rust cdylib all produce the canonical conformance
values. It is intentionally dependency-light so GitHub-hosted clean machines
can run it after building the repository.
"""
from __future__ import annotations

import ctypes
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AFFINITY = 0.41111229050718745
EXPECTED_BLEND = 0.6638893016775156
EXPECTED_STEP0 = 0.13323507494835604
TOLERANCE = 1e-12
A = [0.0, 1.0, -1.0, 0.5]
B = [0.5, 0.5, -0.5, 1.0]
STATE = [0.1, -0.2, 0.3, -0.4]
SIGNAL = [1.0, -0.5, 0.25, -1.0]


def close(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= TOLERANCE


def require_close(label: str, actual: float, expected: float) -> None:
    if not close(actual, expected):
        raise RuntimeError(f"{label}: expected {expected:.17g}, got {actual:.17g}")


def python_smoke() -> None:
    from cstlib.synaptic import SynapticFunction

    fn = SynapticFunction(sigma=0.75, gate=0.35)
    affinity = fn.affinity(A, B)
    blend = fn.blend(0.8, affinity)
    stepped = fn.step(STATE, SIGNAL, decay=0.92, gain=1.2, dt=0.5)
    require_close("python affinity", affinity, EXPECTED_AFFINITY)
    require_close("python blend", blend, EXPECTED_BLEND)
    require_close("python state[0]", stepped[0], EXPECTED_STEP0)
    print("[ok] pure Python CST-SYNAPTIC-V1")


def json_bridge_smoke() -> None:
    request = {"op": "affinity", "a": A, "b": B, "sigma": 0.75}
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "synaptic_bridge.py")],
        input=json.dumps(request) + "\n",
        text=True,
        capture_output=True,
        check=True,
        cwd=ROOT,
    )
    response = json.loads(result.stdout.strip().splitlines()[-1])
    if not response.get("ok"):
        raise RuntimeError(f"JSON bridge failed: {response}")
    require_close("json affinity", float(response["value"]), EXPECTED_AFFINITY)
    print("[ok] JSON-lines bridge")


def find_library(root: Path, names: tuple[str, ...]) -> Path:
    matches: list[Path] = []
    for name in names:
        matches.extend(root.rglob(name))
    files = sorted({path.resolve() for path in matches if path.is_file()})
    if not files:
        raise FileNotFoundError(f"none of {names!r} found under {root}")
    return files[0]


def configure_affinity(lib: ctypes.CDLL, symbol: str):
    fn = getattr(lib, symbol)
    fn.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_double,
        ctypes.POINTER(ctypes.c_double),
    ]
    fn.restype = ctypes.c_int
    return fn


def configure_blend(lib: ctypes.CDLL, symbol: str):
    fn = getattr(lib, symbol)
    fn.argtypes = [
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.POINTER(ctypes.c_double),
    ]
    fn.restype = ctypes.c_int
    return fn


def configure_step(lib: ctypes.CDLL, symbol: str):
    fn = getattr(lib, symbol)
    fn.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
    ]
    fn.restype = ctypes.c_int
    return fn


def native_smoke(label: str, library: Path, prefix: str) -> None:
    lib = ctypes.CDLL(str(library))
    affinity_fn = configure_affinity(lib, f"{prefix}synaptic_affinity")
    blend_fn = configure_blend(lib, f"{prefix}synaptic_blend")
    step_fn = configure_step(lib, f"{prefix}synaptic_state_step")

    a = (ctypes.c_double * len(A))(*A)
    b = (ctypes.c_double * len(B))(*B)
    affinity = ctypes.c_double()
    rc = affinity_fn(a, b, len(A), 0.75, ctypes.byref(affinity))
    if rc != 0:
        raise RuntimeError(f"{label} affinity returned status {rc}")
    require_close(f"{label} affinity", affinity.value, EXPECTED_AFFINITY)

    blended = ctypes.c_double()
    rc = blend_fn(0.8, affinity.value, 0.35, ctypes.byref(blended))
    if rc != 0:
        raise RuntimeError(f"{label} blend returned status {rc}")
    require_close(f"{label} blend", blended.value, EXPECTED_BLEND)

    state = (ctypes.c_double * len(STATE))(*STATE)
    signal = (ctypes.c_double * len(SIGNAL))(*SIGNAL)
    rc = step_fn(state, signal, len(STATE), 0.92, 1.2, 0.5)
    if rc != 0:
        raise RuntimeError(f"{label} state step returned status {rc}")
    require_close(f"{label} state[0]", state[0], EXPECTED_STEP0)
    print(f"[ok] {label}: {library.relative_to(ROOT)}")


def main() -> int:
    print(f"CST clean-machine smoke: {platform.system()} {platform.machine()} / Python {platform.python_version()}")
    python_smoke()
    json_bridge_smoke()

    cpp = find_library(
        ROOT / "build-vm",
        ("cst_synaptic.dll", "libcst_synaptic.so", "libcst_synaptic.dylib"),
    )
    native_smoke("C++ C ABI", cpp, "cst_")

    rust = find_library(
        ROOT / "cosmic rust" / "target" / "release",
        ("cosmic_rust.dll", "libcosmic_rust.so", "libcosmic_rust.dylib"),
    )
    native_smoke("Rust C ABI", rust, "cst_rust_")

    print("VM_SMOKE_OK CST-SYNAPTIC-V1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
