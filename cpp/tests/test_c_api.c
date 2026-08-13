#include "cst/c_api.h"
#include <assert.h>
#include <math.h>
#include <string.h>
int main(void){double a[]={0,1,-1,.5},b[]={.5,.5,-.5,1},out=0;assert(strcmp(cst_synaptic_spec_version(),"CST-SYNAPTIC-V1")==0);assert(cst_synaptic_affinity(a,b,4,.75,&out)==CST_OK);assert(fabs(out-.41111229050718745)<1e-12);double state[]={.1,-.2,.3,-.4},signal[]={1,-.5,.25,-1};assert(cst_synaptic_state_step(state,signal,4,.92,1.2,.5)==CST_OK);assert(fabs(state[0]-.13323507494835604)<1e-12);return 0;}
