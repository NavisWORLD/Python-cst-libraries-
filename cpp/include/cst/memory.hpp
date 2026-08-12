#pragma once
#include <cstddef>
#include <string>
#include <utility>
#include <vector>
namespace cst {
struct TextMemoryRecord{std::string text;double salience=0.5;double confidence=1.0;};
class TextMemory {
public:
    void store(std::string text,double salience=0.5,double confidence=1.0);
    std::vector<std::pair<TextMemoryRecord,double>> recall(const std::string&query,std::size_t limit=5)const;
    std::size_t size()const noexcept{return records_.size();}
private:std::vector<TextMemoryRecord>records_;
};}
