#include <iostream>
#include <vector>

#include "cst/state.hpp"
#include "cst/synapse.hpp"

int main() {
    cst::Dyn12 state;
    std::vector<std::vector<double>> history;
    for (int i = 0; i < 4; ++i) {
        history.push_back(state.update({0.1 * i, 0.2 * i, -0.1 * i}));
    }
    cst::GaussianSynapse kernel;
    const auto matrix = kernel.affinity(history);
    std::cout << "CST C++ demo\n";
    std::cout << "dimension=" << state.dimension() << " updates=" << state.updates() << "\n";
    std::cout << "bandwidth=" << kernel.bandwidth() << " H[0][1]=" << matrix[0][1] << "\n";
    return 0;
}
