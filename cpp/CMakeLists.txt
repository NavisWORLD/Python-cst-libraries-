add_library(cst_core STATIC
    src/state.cpp
    src/synapse.cpp
    src/event.cpp
    src/event_bus.cpp
    src/dynamics.cpp
    src/hebbian.cpp
    src/memory.cpp
)
set_target_properties(cst_core PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_compile_features(cst_core PUBLIC cxx_std_17)
target_include_directories(cst_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(cst_cpp_demo examples/demo.cpp)
target_link_libraries(cst_cpp_demo PRIVATE cst_core)

if(CST_BUILD_TESTS)
    enable_testing()
    add_executable(cst_cpp_tests tests/test_core.cpp)
    target_link_libraries(cst_cpp_tests PRIVATE cst_core)
    add_test(NAME cst_cpp_tests COMMAND cst_cpp_tests)
endif()

if(CST_BUILD_PYTHON_BINDINGS)
    find_package(pybind11 CONFIG REQUIRED)
    pybind11_add_module(_cst_native python/bindings.cpp)
    target_link_libraries(_cst_native PRIVATE cst_core)
    target_include_directories(_cst_native PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
endif()
