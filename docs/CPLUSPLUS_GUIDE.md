# C++17 Core Guide

## Purpose

The native layer provides a small dependency-free implementation of CST's reusable low-level primitives. It is not intended to reimplement every Python integration.

## Headers

```text
cst/state.hpp
cst/synapse.hpp
cst/event.hpp
cst/event_bus.hpp
cst/dynamics.hpp
cst/hebbian.hpp
cst/memory.hpp
```

## Dynamic state

```cpp
#include <cst/state.hpp>
cst::Dyn12 state;
auto x = state.update({1.0, 0.2, -0.4});
```

## Gaussian affinity

```cpp
#include <cst/synapse.hpp>
cst::GaussianSynapse synapse; // 0 = auto/median
std::vector<std::vector<double>> states = {x1, x2, x3};
auto H = synapse.affinity(states);
auto diagnostic = synapse.diagnostics(states);
```

## Events

```cpp
cst::EventBus bus;
bus.subscribe("message", [](const cst::Event& event) { /* handle event */ });
bus.emit(cst::Event("app", "message"));
```

Delivery is synchronous and fail-soft; `emit` returns the number of failing handlers.

## Lorenz

```cpp
cst::Lorenz system;
auto xyz = system.step(0.01);
```

## Hebbian association

```cpp
cst::HebbianMemory memory;
memory.learn({"music", "rhythm", "motion"});
auto related = memory.associated_with("rhythm");
```

## Text memory

The C++ `TextMemory` is intentionally simpler than Python `SemanticMemory`; it uses token-overlap ranking plus salience/confidence. It exists as a no-dependency native baseline, not as a claim of embedding-equivalent semantic retrieval.

## Linking

CMake consumers may add this repository as a subdirectory and link `cst_core`.

```cmake
add_subdirectory(path/to/Python-cst-libraries-)
target_link_libraries(my_app PRIVATE cst_core)
```
