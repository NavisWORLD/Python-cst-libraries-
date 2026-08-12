#pragma once

#include <cstddef>
#include <vector>

namespace cst {

class DynamicState {
public:
    explicit DynamicState(std::size_t dimension, double decay = 0.92, double gain = 1.0);
    std::vector<double> update(const std::vector<double>& signal, double dt = 1.0);
    const std::vector<double>& vector() const noexcept { return values_; }
    void reset() noexcept;
    std::size_t dimension() const noexcept { return values_.size(); }
    std::size_t updates() const noexcept { return updates_; }
    double decay() const noexcept { return decay_; }
    double gain() const noexcept { return gain_; }
private:
    std::vector<double> values_;
    double decay_;
    double gain_;
    std::size_t updates_ = 0;
};

class Dyn12 final : public DynamicState {
public:
    explicit Dyn12(double decay = 0.92, double gain = 1.0) : DynamicState(12, decay, gain) {}
};
class Dyn42 final : public DynamicState {
public:
    explicit Dyn42(double decay = 0.94, double gain = 1.0) : DynamicState(42, decay, gain) {}
};
class Dyn54 final : public DynamicState {
public:
    explicit Dyn54(double decay = 0.95, double gain = 1.0) : DynamicState(54, decay, gain) {}
};

} // namespace cst
