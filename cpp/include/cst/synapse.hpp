#pragma once
#include <vector>
namespace cst {
struct KernelDiagnostics{double bandwidth=1.0;double off_diagonal_mean=0.0;double off_diagonal_variance=0.0;bool identity_like=false;bool uniform_like=false;};
class GaussianSynapse{
public:explicit GaussianSynapse(double bandwidth=0.0);double fit(const std::vector<std::vector<double>>&states);std::vector<std::vector<double>> affinity(const std::vector<std::vector<double>>&states);KernelDiagnostics diagnostics(const std::vector<std::vector<double>>&states);double bandwidth()const noexcept{return fitted_bandwidth_;}
private:double configured_bandwidth_;double fitted_bandwidth_;
};}
