cmake_minimum_required(VERSION 3.16)
project(cst_libraries LANGUAGES CXX)

include(CTest)
option(CST_BUILD_TESTS "Build C++ tests" ON)
option(CST_BUILD_PYTHON_BINDINGS "Build optional pybind11 module" OFF)

add_subdirectory(cpp)
