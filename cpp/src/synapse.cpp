#include "cst/synapse.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace {
double distance(const std::vector<double>& a, const std::vector<double>& b) {
    if (a.size() != b.size()) throw std::invalid_argument("vectors must have the same dimension");
    double sum = 0.0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        const double delta = a[i] - b[i];
        sum += delta * delta;
    }
    return std::sqrt(sum);
}
}

namespace cst {
GaussianSynapse::GaussianSynapse(double bandwidth)
    : configured_bandwidth_(bandwidth), fitted_bandwidth_(bandwidth) {
    if (bandwidth < 0.0) throw std::invalid_argument("bandwidth must be non-negative; 0 means auto");
}

double GaussianSynapse::fit(const std::vector<std::vector<double>>& states) {
    if (configured_bandwidth_ > 0.0) {
        fitted_bandwidth_ = configured_bandwidth_;
        return fitted_bandwidth_;
    }
    std::vector<double> distances;
    for (std::size_t i = 0; i < states.size(); ++i) {
        for (std::size_t j = i + 1; j < states.size(); ++j) {
            const double d = distance(states[i], states[j]);
            if (d > 0.0) distances.push_back(d);
        }
    }
    if (distances.empty()) {
        fitted_bandwidth_ = 1.0;
        return fitted_bandwidth_;
    }
    std::sort(distances.begin(), distances.end());
    const std::size_t mid = distances.size() / 2;
    fitted_bandwidth_ = distances.size() % 2 ? distances[mid] : 0.5 * (distances[mid - 1] + distances[mid]);
    return fitted_bandwidth_;
}

std::vector<std::vector<double>> GaussianSynapse::affinity(const std::vector<std::vector<double>>& states) {
    const double sigma = fit(states);
    const double denom = 2.0 * sigma * sigma;
    std::vector<std::vector<double>> out(states.size(), std::vector<double>(states.size(), 0.0));
    for (std::size_t i = 0; i < states.size(); ++i) {
        for (std::size_t j = 0; j < states.size(); ++j) {
            const double d = distance(states[i], states[j]);
            out[i][j] = std::exp(-(d * d) / denom);
        }
    }
    return out;
}
} // namespace cst
