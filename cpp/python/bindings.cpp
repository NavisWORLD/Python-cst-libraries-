#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "cst/state.hpp"
#include "cst/synapse.hpp"
#include "cst/synaptic.hpp"
#include "cst/dynamics.hpp"
#include "cst/hebbian.hpp"
#include "cst/memory.hpp"
namespace py=pybind11;
PYBIND11_MODULE(_cst_native,m){
 m.doc()="CST native C++17 core";
 py::class_<cst::DynamicState>(m,"DynamicState").def(py::init<std::size_t,double,double>(),py::arg("dimension"),py::arg("decay")=.92,py::arg("gain")=1.0).def("update",&cst::DynamicState::update,py::arg("signal"),py::arg("dt")=1.0).def("vector",&cst::DynamicState::vector).def("reset",&cst::DynamicState::reset).def_property_readonly("dimension",&cst::DynamicState::dimension).def_property_readonly("updates",&cst::DynamicState::updates);
 py::class_<cst::GaussianSynapse>(m,"GaussianSynapse").def(py::init<double>(),py::arg("bandwidth")=0.0).def("fit",&cst::GaussianSynapse::fit).def("affinity",&cst::GaussianSynapse::affinity).def_property_readonly("bandwidth",&cst::GaussianSynapse::bandwidth);
 py::class_<cst::SynapticFunction>(m,"SynapticFunction").def(py::init<double,double>(),py::arg("sigma")=1.0,py::arg("gate")=.5).def("affinity",&cst::SynapticFunction::affinity).def("matrix",&cst::SynapticFunction::matrix).def("blend",&cst::SynapticFunction::blend,py::arg("standard"),py::arg("state_affinity"),py::arg("gate_override")=-1.0).def("step",&cst::SynapticFunction::step,py::arg("state"),py::arg("signal"),py::arg("decay")=.92,py::arg("gain")=1.0,py::arg("dt")=1.0).def_property_readonly("sigma",&cst::SynapticFunction::sigma).def_property_readonly("gate",&cst::SynapticFunction::gate);
 py::class_<cst::Lorenz>(m,"Lorenz").def(py::init<double,double,double,double,double,double>(),py::arg("sigma")=10.0,py::arg("rho")=28.0,py::arg("beta")=8.0/3.0,py::arg("x")=1.0,py::arg("y")=1.0,py::arg("z")=1.0).def("step",&cst::Lorenz::step,py::arg("dt")=.01).def("state",&cst::Lorenz::state);
 py::class_<cst::HebbianMemory>(m,"HebbianMemory").def(py::init<double,double>(),py::arg("learning_rate")=.1,py::arg("decay")=.001).def("learn",&cst::HebbianMemory::learn).def("associated_with",&cst::HebbianMemory::associated_with,py::arg("concept"),py::arg("limit")=10).def_property_readonly("concepts",&cst::HebbianMemory::concepts);
 py::class_<cst::TextMemoryRecord>(m,"TextMemoryRecord").def_readonly("text",&cst::TextMemoryRecord::text).def_readonly("salience",&cst::TextMemoryRecord::salience).def_readonly("confidence",&cst::TextMemoryRecord::confidence);
 py::class_<cst::TextMemory>(m,"TextMemory").def(py::init<>()).def("store",&cst::TextMemory::store,py::arg("text"),py::arg("salience")=.5,py::arg("confidence")=1.0).def("recall",&cst::TextMemory::recall,py::arg("query"),py::arg("limit")=5).def_property_readonly("size",&cst::TextMemory::size);
}
