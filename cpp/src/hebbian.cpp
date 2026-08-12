#include "cst/hebbian.hpp"
#include <algorithm>
#include <stdexcept>
namespace cst {
HebbianMemory::HebbianMemory(double lr,double decay):learning_rate_(lr),decay_(decay){if(lr<0||decay<0||decay>=1)throw std::invalid_argument("invalid learning parameters");}
void HebbianMemory::learn(const std::vector<std::string>&concepts){for(const auto&a:concepts)for(const auto&b:concepts)if(a!=b){double old=0;auto it=weights_[a].find(b);if(it!=weights_[a].end())old=it->second;weights_[a][b]=(1-decay_)*old+learning_rate_;}}
std::vector<std::pair<std::string,double>> HebbianMemory::associated_with(const std::string&concept,std::size_t limit)const{std::vector<std::pair<std::string,double>>out;auto it=weights_.find(concept);if(it==weights_.end())return out;for(const auto&kv:it->second)out.push_back(kv);std::sort(out.begin(),out.end(),[](const auto&a,const auto&b){return a.second>b.second;});if(out.size()>limit)out.resize(limit);return out;}
}
