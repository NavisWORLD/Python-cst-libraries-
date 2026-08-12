#include "cst/state.hpp"
#include "cst/synapse.hpp"
#include "cst/dynamics.hpp"
#include "cst/hebbian.hpp"
#include "cst/memory.hpp"
#include "cst/event_bus.hpp"
#include <cassert>
int main(){
    cst::Dyn12 state(0.5);auto a=state.update({1.0});auto b=state.update({0.0});assert(a.size()==12&&b.size()==12&&state.updates()==2&&b[0]!=0.0);
    cst::GaussianSynapse syn;auto h=syn.affinity({{0,0},{1,0},{0,1}});assert(h[0][0]==1.0&&h[0][1]>0&&h[0][1]<1);assert(syn.diagnostics({{0,0},{1,0},{0,1}}).bandwidth>0);
    cst::Lorenz l;auto before=l.state();auto after=l.step();assert(before!=after);
    cst::HebbianMemory hebb;hebb.learn({"guitar","music","stage"});assert(!hebb.associated_with("guitar").empty());
    cst::TextMemory memory;memory.store("red guitar studio",1.0);memory.store("yellow banana");assert(memory.recall("guitar",1)[0].first.text=="red guitar studio");
    cst::EventBus bus;int seen=0;bus.subscribe("x",[&](const cst::Event&){++seen;});bus.subscribe("x",[](const cst::Event&){throw 1;});auto failures=bus.emit(cst::Event("test","x"));assert(seen==1&&failures==1&&bus.errors()==1);
    return 0;
}
