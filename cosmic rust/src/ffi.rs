use crate::synaptic::SynapticFunction;
use std::ffi::c_char;
use std::slice;

#[no_mangle]
pub extern "C" fn cst_rust_synaptic_spec_version() -> *const c_char {
    b"CST-SYNAPTIC-V1\0".as_ptr().cast()
}

#[no_mangle]
#[allow(clippy::not_unsafe_ptr_arg_deref)]
pub extern "C" fn cst_rust_synaptic_affinity(
    a: *const f64,
    b: *const f64,
    len: usize,
    sigma: f64,
    out: *mut f64,
) -> i32 {
    if a.is_null() || b.is_null() || out.is_null() {
        return 1;
    }
    if len == 0 || sigma <= 0.0 {
        return 2;
    }
    let (a, b) = unsafe { (slice::from_raw_parts(a, len), slice::from_raw_parts(b, len)) };
    match SynapticFunction::new(sigma, 0.5).and_then(|f| f.affinity(a, b)) {
        Ok(value) => {
            unsafe { *out = value };
            0
        }
        Err(_) => 2,
    }
}

#[no_mangle]
#[allow(clippy::not_unsafe_ptr_arg_deref)]
pub extern "C" fn cst_rust_synaptic_blend(
    standard: f64,
    affinity: f64,
    gate: f64,
    out: *mut f64,
) -> i32 {
    if out.is_null() {
        return 1;
    }
    match SynapticFunction::new(1.0, gate).and_then(|f| f.blend(standard, affinity, None)) {
        Ok(value) => {
            unsafe { *out = value };
            0
        }
        Err(_) => 2,
    }
}

#[no_mangle]
#[allow(clippy::not_unsafe_ptr_arg_deref)]
pub extern "C" fn cst_rust_synaptic_state_step(
    state: *mut f64,
    signal: *const f64,
    len: usize,
    decay: f64,
    gain: f64,
    dt: f64,
) -> i32 {
    if state.is_null() || signal.is_null() {
        return 1;
    }
    if len == 0 {
        return 2;
    }
    let state_in = unsafe { slice::from_raw_parts(state, len) };
    let signal = unsafe { slice::from_raw_parts(signal, len) };
    match SynapticFunction::default().step(state_in, signal, decay, gain, dt) {
        Ok(values) => {
            unsafe { slice::from_raw_parts_mut(state, len) }.copy_from_slice(&values);
            0
        }
        Err(_) => 2,
    }
}
