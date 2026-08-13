# CST Synaptic Function v1 — Cross-Language Specification

**Protocol ID:** `CST-SYNAPTIC-V1`

This document defines the portable numerical core used by the Python, C, C++, Rust, JavaScript/TypeScript, Go, Java/Kotlin, C#, and Swift implementations.

## Gaussian synaptic affinity

`H(a,b;sigma) = exp(-||a-b||^2 / (2 sigma^2))` for equal-length non-empty vectors and `sigma > 0`.

## Gated blend

`F = (1-g)S + gH` for gate `g` in `[0,1]`.

## Persistent state step

`effective_decay = decay^dt`

`x' = effective_decay*x + (1-effective_decay)*gain*tanh(u)`

The update is elementwise. Implementations reject empty/dimension-mismatched vectors, non-positive sigma, gate or decay outside `[0,1]`, and negative `dt`.

## Conformance

Canonical values are stored in `protocol/conformance.json`. Expected affinity is `0.41111229050718745`, expected blend is `0.6638893016775156`, and the expected first state-step component is `0.13323507494835604`. Double-precision ports should match within `1e-12`.

## Native ABI

C++ builds a shared `cst_synaptic` library exposing `cst_synaptic_affinity`, `cst_synaptic_matrix`, `cst_synaptic_blend`, `cst_synaptic_state_step`, and `cst_synaptic_spec_version` through `cpp/include/cst/c_api.h`. Cosmic Rust builds `rlib`, `cdylib`, and `staticlib` outputs and exports equivalent `cst_rust_synaptic_*` functions.

## JSON bridge

`tools/synaptic_bridge.py` supports `affinity`, `matrix`, `blend`, and `step` over JSON Lines using `protocol/synaptic-v1.schema.json`.

A new language binding is conformant when it implements the same formulas, boundaries, and conformance vector. This lets the project support essentially any FFI- or stdio-capable language without falsely claiming every language ever created is hand-maintained here.
