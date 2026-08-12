#include "cst/state.hpp"
#include "cst/synapse.hpp"
#include "cst/dynamics.hpp"
#include "cst/hebbian.hpp"
#include "cst/memory.hpp"
#include "cst/event_bus.hpp"
#include <iostream>
int main(){
    cst::Dyn12 state;auto a=state.update({1.0,0.5,-0.25});auto b=state.update({0.25,-0.5,1.0});
    cst::GaussianSynapse syn;auto h=syn.affinity({a,b});
    cst::Lorenz lorenz;auto xyz=lorenz.step();
    cst::HebbianMemory hebb;hebb.learn({"music","rhythm","motion"});
    cst::TextMemory memory;memory.store("the red guitar lives in the studio",1.0);auto recalled=memory.recall("guitar studio",1);
    cst::EventBus bus;bus.subscribe("demo",[](const cst::Event&e){std::cout<<"event="<<e.kind<<"\n";});bus.emit(cst::Event("demo","demo",{{"status","ok"}}));
    std::cout<<"dyn12_updates="<<state.updates()<<" affinity="<<h[0][1]<<" lorenz_z="<<xyz[2]<<" recall="<<recalled[0].first.text<<"\n";
    return 0;
}
