# Release Checklist

Before tagging a CST Libraries release:

- [ ] bump `pyproject.toml` version
- [ ] bump `cstlib.__version__`
- [ ] bump CMake project version
- [ ] update `CITATION.cff`
- [ ] update migration notes
- [ ] run dependency-free Python tests
- [ ] run optional PyTorch tests when available
- [ ] build Python package
- [ ] run `cst doctor`
- [ ] run CST-L example
- [ ] build C++17 core
- [ ] run CTest
- [ ] run C++ demo
- [ ] build optional pybind11 extension in CI
- [ ] review third-party licenses
- [ ] confirm no secrets/credentials in repository
- [ ] record any null/failing research result without deleting it
- [ ] tag only after CI is green
