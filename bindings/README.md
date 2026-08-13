# CST Cross-Language Bindings

The CST Synaptic Function is defined once in `docs/SYNAPTIC_CROSS_LANGUAGE.md` and implemented in multiple languages with one conformance vector.

First-class implementations are provided for Python, C, C++17, Rust, JavaScript/TypeScript, Go, Java/Kotlin, C#, and Swift.

Languages without a dedicated folder can integrate through the stable C ABI (`cpp/include/cst/c_api.h`), the equivalent Cosmic Rust C ABI exports, or the language-neutral JSON Lines bridge in `tools/synaptic_bridge.py`.

`protocol/conformance.json` is the shared numerical test vector. Double-precision ports should match within `1e-12`.
