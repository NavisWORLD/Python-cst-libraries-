#include "cst/event.hpp"
#include <stdexcept>
namespace cst {Event::Event(std::string s,std::string k,std::unordered_map<std::string,std::string> p,double c):source(std::move(s)),kind(std::move(k)),payload(std::move(p)),confidence(c){if(confidence<0||confidence>1)throw std::invalid_argument("confidence must be between 0 and 1");timestamp=std::chrono::duration<double>(std::chrono::system_clock::now().time_since_epoch()).count();}}
