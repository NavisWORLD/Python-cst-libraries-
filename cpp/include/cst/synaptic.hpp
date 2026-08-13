#pragma once
#include <vector>
namespace cst {
class SynapticFunction {
public:
    explicit SynapticFunction(double sigma = 1.0, double gate = 0.5);
    double affinity(const std::vector<double>& a, const std::vector<double>& b) const;
    std::vector<std::vector<double>> matrix(const std::vector<std::vector<double>>& states) const;
    double blend(double standard, double state_affinity, double gate_override = -1.0) const;
    std::vector<double> step(const std::vector<double>& state, const std::vector<double>& signal, double decay = 0.92, double gain = 1.0, double dt = 1.0) const;
    double sigma() const noexcept { return sigma_; }
    double gate() const noexcept { return gate_; }
private:
    double sigma_;
    double gate_;
};
}
