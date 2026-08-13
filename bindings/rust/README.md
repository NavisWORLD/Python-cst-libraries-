# Rust

The native implementation is `cosmic rust/src/synaptic.rs` and is re-exported as `cosmic_rust::SynapticFunction`. The crate also builds `rlib`, `cdylib` and `staticlib` outputs and exports `cst_rust_synaptic_*` C ABI functions for cross-language consumers.
