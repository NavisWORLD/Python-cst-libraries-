#include "cst/synaptic.hpp"
#include <cmath>
#include <stdexcept>
namespace cst {
SynapticFunction::SynapticFunction(double sigma, double gate):sigma_(sigma),gate_(gate){if(sigma_<=0)throw std::invalid_argument("sigma must be > 0");if(gate_<0||gate_>1)throw std::invalid_argument("gate must be in [0,1]");}
double SynapticFunction::affinity(const std::vector<double>&a,const std::vector<double>&b)const{if(a.empty()||a.size()!=b.size())throw std::invalid_argument("vectors must be non-empty and equal length");double d2=0;for(std::size_t i=0;i<a.size();++i){double d=a[i]-b[i];d2+=d*d;}return std::exp(-d2/(2*sigma_*sigma_));}
std::vector<std::vector<double>> SynapticFunction::matrix(const std::vector<std::vector<double>>&s)const{if(s.empty()||s.front().empty())throw std::invalid_argument("states must be non-empty");auto d=s.front().size();for(auto&r:s)if(r.size()!=d)throw std::invalid_argument("state dimensions must match");std::vector<std::vector<double>>o(s.size(),std::vector<double>(s.size()));for(std::size_t i=0;i<s.size();++i)for(std::size_t j=0;j<s.size();++j)o[i][j]=affinity(s[i],s[j]);return o;}
double SynapticFunction::blend(double standard,double state_affinity,double gate_override)const{double g=gate_override<0?gate_:gate_override;if(g<0||g>1)throw std::invalid_argument("gate must be in [0,1]");return(1-g)*standard+g*state_affinity;}
std::vector<double> SynapticFunction::step(const std::vector<double>&state,const std::vector<double>&signal,double decay,double gain,double dt)const{if(state.empty()||state.size()!=signal.size())throw std::invalid_argument("state and signal must be non-empty and equal length");if(decay<0||decay>1||dt<0)throw std::invalid_argument("invalid decay or dt");double ed=std::pow(decay,dt);std::vector<double>o(state.size());for(std::size_t i=0;i<state.size();++i)o[i]=ed*state[i]+(1-ed)*gain*std::tanh(signal[i]);return o;}
}
