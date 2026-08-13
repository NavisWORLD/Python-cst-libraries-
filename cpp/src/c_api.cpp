#define CST_CAPI_BUILD
#include "cst/c_api.h"
#include "cst/synaptic.hpp"
#include <vector>
extern "C" {
int cst_synaptic_affinity(const double*a,const double*b,size_t len,double sigma,double*out){if(!a||!b||!out)return CST_ERR_NULL;if(!len||sigma<=0)return CST_ERR_ARGUMENT;try{*out=cst::SynapticFunction(sigma).affinity(std::vector<double>(a,a+len),std::vector<double>(b,b+len));return CST_OK;}catch(...){return CST_ERR_ARGUMENT;}}
int cst_synaptic_matrix(const double*s,size_t rows,size_t cols,double sigma,double*out){if(!s||!out)return CST_ERR_NULL;if(!rows||!cols||sigma<=0)return CST_ERR_ARGUMENT;try{cst::SynapticFunction f(sigma);for(size_t i=0;i<rows;++i)for(size_t j=0;j<rows;++j){std::vector<double>a(s+i*cols,s+(i+1)*cols),b(s+j*cols,s+(j+1)*cols);out[i*rows+j]=f.affinity(a,b);}return CST_OK;}catch(...){return CST_ERR_ARGUMENT;}}
int cst_synaptic_blend(double standard,double affinity,double gate,double*out){if(!out)return CST_ERR_NULL;if(gate<0||gate>1)return CST_ERR_ARGUMENT;*out=(1-gate)*standard+gate*affinity;return CST_OK;}
int cst_synaptic_state_step(double*state,const double*signal,size_t len,double decay,double gain,double dt){if(!state||!signal)return CST_ERR_NULL;if(!len||decay<0||decay>1||dt<0)return CST_ERR_ARGUMENT;try{auto o=cst::SynapticFunction().step(std::vector<double>(state,state+len),std::vector<double>(signal,signal+len),decay,gain,dt);for(size_t i=0;i<len;++i)state[i]=o[i];return CST_OK;}catch(...){return CST_ERR_ARGUMENT;}}
const char* cst_synaptic_spec_version(void){return "CST-SYNAPTIC-V1";}
}
