#include "cst/synaptic.hpp"
#include "cst/c_api.h"
#include <cassert>
#include <cmath>
#include <vector>
static bool close(double a,double b){return std::abs(a-b)<1e-12;}
int main(){const std::vector<double>a{0,1,-1,.5},b{.5,.5,-.5,1};cst::SynapticFunction f(.75,.35);double h=f.affinity(a,b);assert(close(h,.41111229050718745));assert(close(f.blend(.8,h),.6638893016775156));auto o=f.step({.1,-.2,.3,-.4},{1,-.5,.25,-1},.92,1.2,.5);assert(close(o[0],.13323507494835604));double c=0;assert(cst_synaptic_affinity(a.data(),b.data(),a.size(),.75,&c)==CST_OK);assert(close(c,h));return 0;}
