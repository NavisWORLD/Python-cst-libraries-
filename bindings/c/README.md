# C ABI

Include `cpp/include/cst/c_api.h` and link the CMake-produced `cst_synaptic` shared library. The ABI is intentionally plain C so Fortran, Julia, R, Ruby native extensions, PHP FFI, LuaJIT FFI, Zig, Nim, D, Delphi and other FFI-capable languages can call the same implementation without a dedicated port.
