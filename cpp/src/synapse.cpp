#include "cst/synapse.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>
namespace {double dist(const std::vector<double>&a,const std::vector<double>&b){if(a.size()!=b.size())throw std::invalid_argument("vectors must have same dimension");double s=0;for(std::size_t i=0;i<a.size();++i){double d=a[i]-b[i];s+=d*d;}return std::sqrt(s);}}
namespace cst {
GaussianSynapse::GaussianSynapse(double bandwidth):configured_bandwidth_(bandwidth),fitted_bandwidth_(bandwidth){if(bandwidth<0)throw std::invalid_argument("bandwidth must be non-negative; 0 means auto");}
double GaussianSynapse::fit(const std::vector<std::vector<double>>&states){if(configured_bandwidth_>0)return fitted_bandwidth_=configured_bandwidth_;std::vector<double>ds;for(std::size_t i=0;i<states.size();++i)for(std::size_t j=i+1;j<states.size();++j){double d=dist(states[i],states[j]);if(d>0)ds.push_back(d);}if(ds.empty())return fitted_bandwidth_=1.0;std::sort(ds.begin(),ds.end());std::size_t m=ds.size()/2;return fitted_bandwidth_=ds.size()%2?ds[m]:0.5*(ds[m-1]+ds[m]);}
std::vector<std::vector<double>> GaussianSynapse::affinity(const std::vector<std::vector<double>>&states){double s=fit(states),den=2*s*s;std::vector<std::vector<double>>out(states.size(),std::vector<double>(states.size()));for(std::size_t i=0;i<states.size();++i)for(std::size_t j=0;j<states.size();++j){double d=dist(states[i],states[j]);out[i][j]=std::exp(-(d*d)/den);}return out;}
KernelDiagnostics GaussianSynapse::diagnostics(const std::vector<std::vector<double>>&states){auto m=affinity(states);KernelDiagnostics d;d.bandwidth=fitted_bandwidth_;std::vector<double>off;for(std::size_t i=0;i<m.size();++i)for(std::size_t j=0;j<m.size();++j)if(i!=j)off.push_back(m[i][j]);if(off.empty())return d;for(double v:off)d.off_diagonal_mean+=v;d.off_diagonal_mean/=off.size();for(double v:off){double x=v-d.off_diagonal_mean;d.off_diagonal_variance+=x*x;}d.off_diagonal_variance/=off.size();d.identity_like=d.off_diagonal_mean<1e-4;d.uniform_like=d.off_diagonal_mean>0.999&&d.off_diagonal_variance<1e-8;return d;}
}
