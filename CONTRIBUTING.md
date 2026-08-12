# Contributing

Contributions are welcome.

1. Keep modules independently useful.
2. Add tests for new mechanisms.
3. Preserve deterministic behavior where promised.
4. Do not broaden scientific claims beyond measured evidence.
5. Keep optional integrations optional; the dependency-free Python core must remain usable.
6. Preserve upstream licenses and attribution for third-party code.
7. Do not commit secrets, API keys, private conversation data, raw biometric data, or proprietary model weights.

Run before submitting:

```bash
python -m pytest
cmake -S . -B build -DCST_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```
