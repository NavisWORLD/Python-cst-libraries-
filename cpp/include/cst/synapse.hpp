#pragma once

#include <vector>

namespace cst {

class GaussianSynapse {
public:
    explicit GaussianSynapse(double bandwidth = 0.0);
    double fit(const std::vector<std::vector<double>>& states);
    std::vector<std::vector<double>> affinity(const std::vector<std::vector<double>>& states);
    double bandwidth() const noexcept { return fitted_bandwidth_; }
private:
    double configured_bandwidth_;
    double fitted_bandwidth_;
};

} // namespace cst
