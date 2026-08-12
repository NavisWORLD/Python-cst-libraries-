#include <cassert>
#include <cmath>
#include <vector>

#include "cst/state.hpp"
#include "cst/synapse.hpp"

int main() {
    cst::Dyn12 state;
    auto first = state.update({1.0, -1.0});
    assert(first.size() == 12);
    assert(state.updates() == 1);
    assert(std::abs(first[0]) > 0.0);

    std::vector<std::vector<double>> states = {{0.0, 0.0}, {1.0, 0.0}, {0.0, 1.0}};
    cst::GaussianSynapse kernel;
    auto h = kernel.affinity(states);
    assert(h.size() == 3);
    assert(std::abs(h[0][0] - 1.0) < 1e-12);
    assert(h[0][1] < 1.0);
    return 0;
}
