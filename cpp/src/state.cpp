#include "cst/state.hpp"

#include <cmath>
#include <stdexcept>

namespace cst {

DynamicState::DynamicState(std::size_t dimension, double decay, double gain)
    : values_(dimension, 0.0), decay_(decay), gain_(gain) {
    if (dimension == 0) throw std::invalid_argument("dimension must be positive");
    if (decay < 0.0 || decay >= 1.0) throw std::invalid_argument("decay must be in [0, 1)");
}

std::vector<double> DynamicState::update(const std::vector<double>& signal, double dt) {
    if (signal.empty()) throw std::invalid_argument("signal cannot be empty");
    if (dt <= 0.0) throw std::invalid_argument("dt must be positive");
    const double effective_decay = std::pow(decay_, dt);
    const double inject = 1.0 - effective_decay;
    for (std::size_t i = 0; i < values_.size(); ++i) {
        const double input = signal[i % signal.size()];
        values_[i] = effective_decay * values_[i] + inject * gain_ * std::tanh(input);
    }
    ++updates_;
    return values_;
}

void DynamicState::reset() noexcept {
    for (double& value : values_) value = 0.0;
    updates_ = 0;
}

} // namespace cst
