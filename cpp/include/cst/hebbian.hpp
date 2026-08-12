#pragma once
#include <cstddef>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
namespace cst {
class HebbianMemory {
public:
    explicit HebbianMemory(double learning_rate=0.1,double decay=0.001);
    void learn(const std::vector<std::string>& concepts);
    std::vector<std::pair<std::string,double>> associated_with(const std::string&concept,std::size_t limit=10) const;
    std::size_t concepts() const noexcept{return weights_.size();}
private:
    double learning_rate_;double decay_;std::unordered_map<std::string,std::unordered_map<std::string,double>>weights_;
};}
