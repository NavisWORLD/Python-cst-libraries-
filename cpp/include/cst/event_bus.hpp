#pragma once
#include "cst/event.hpp"
#include <functional>
#include <string>
#include <unordered_map>
#include <vector>
namespace cst {
class EventBus {
public:
    using Handler=std::function<void(const Event&)>;
    void subscribe(const std::string&kind,Handler handler);
    std::size_t emit(const Event&event) noexcept;
    std::size_t errors() const noexcept{return errors_;}
    std::size_t deliveries() const noexcept{return deliveries_;}
private:std::unordered_map<std::string,std::vector<Handler>>handlers_;std::size_t errors_=0;std::size_t deliveries_=0;
};}
