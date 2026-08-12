#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "cst/state.hpp"
#include "cst/synapse.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_cst_native, m) {
    m.doc() = "Optional native C++ accelerators for CST libraries";

    py::class_<cst::DynamicState>(m, "DynamicState")
        .def(py::init<std::size_t, double, double>(), py::arg("dimension"), py::arg("decay") = 0.92, py::arg("gain") = 1.0)
        .def("update", &cst::DynamicState::update, py::arg("signal"), py::arg("dt") = 1.0)
        .def("vector", &cst::DynamicState::vector)
        .def("reset", &cst::DynamicState::reset)
        .def_property_readonly("dimension", &cst::DynamicState::dimension)
        .def_property_readonly("updates", &cst::DynamicState::updates);

    py::class_<cst::GaussianSynapse>(m, "GaussianSynapse")
        .def(py::init<double>(), py::arg("bandwidth") = 0.0)
        .def("fit", &cst::GaussianSynapse::fit)
        .def("affinity", &cst::GaussianSynapse::affinity)
        .def_property_readonly("bandwidth", &cst::GaussianSynapse::bandwidth);
}
