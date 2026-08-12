"""Optional loader for the C++/pybind11 CST core."""
from __future__ import annotations

def available() -> bool:
    try: import _cst_native
    except ImportError: return False
    return True

def module():
    try: import _cst_native
    except ImportError as exc: raise ImportError("CST native bindings are not installed. Build with CST_BUILD_PYTHON_BINDINGS=ON.") from exc
    return _cst_native

def health()->dict[str,object]: return {"available":available(),"module":"_cst_native"}
