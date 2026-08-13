add_library(cst_core STATIC
    src/state.cpp
    src/synapse.cpp
    src/synaptic.cpp
    src/event.cpp
    src/event_bus.cpp
    src/dynamics.cpp
    src/hebbian.cpp
    src/memory.cpp
)
set_target_properties(cst_core PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_compile_features(cst_core PUBLIC cxx_std_17)
target_include_directories(cst_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(cst_capi SHARED src/c_api.cpp)
target_link_libraries(cst_capi PRIVATE cst_core)
target_compile_features(cst_capi PRIVATE cxx_std_17)
target_include_directories(cst_capi PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
set_target_properties(cst_capi PROPERTIES OUTPUT_NAME cst_synaptic)

add_executable(cst_cpp_demo examples/demo.cpp)
target_link_libraries(cst_cpp_demo PRIVATE cst_core)

if(CST_BUILD_TESTS)
    enable_testing()
    add_executable(cst_cpp_tests tests/test_core.cpp)
    target_link_libraries(cst_cpp_tests PRIVATE cst_core)
    add_test(NAME cst_cpp_tests COMMAND cst_cpp_tests)
    add_executable(cst_synaptic_tests tests/test_synaptic.cpp)
    target_link_libraries(cst_synaptic_tests PRIVATE cst_core cst_capi)
    add_test(NAME cst_synaptic_tests COMMAND cst_synaptic_tests)
    add_executable(cst_c_api_tests tests/test_c_api.c)
    target_link_libraries(cst_c_api_tests PRIVATE cst_capi)
    target_include_directories(cst_c_api_tests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
    add_test(NAME cst_c_api_tests COMMAND cst_c_api_tests)
endif()

if(CST_BUILD_PYTHON_BINDINGS)
    find_package(pybind11 CONFIG REQUIRED)
    pybind11_add_module(_cst_native python/bindings.cpp)
    target_link_libraries(_cst_native PRIVATE cst_core)
    target_include_directories(_cst_native PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
endif()
