#pragma once
#include <chrono>
#include <string>
#include <unordered_map>
namespace cst {
struct Event {
    std::string source;
    std::string kind;
    std::unordered_map<std::string,std::string> payload;
    double confidence=1.0;
    double timestamp=0.0;
    Event(std::string source_,std::string kind_,std::unordered_map<std::string,std::string> payload_={},double confidence_=1.0);
};
}
