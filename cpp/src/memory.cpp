#include "cst/memory.hpp"
#include <algorithm>
#include <cctype>
#include <set>
#include <sstream>
#include <stdexcept>
namespace {std::set<std::string>tokens(const std::string&s){std::string clean;for(unsigned char c:s)clean.push_back(std::isalnum(c)||c=='_'?static_cast<char>(std::tolower(c)):' ');std::istringstream in(clean);std::set<std::string>out;std::string t;while(in>>t)out.insert(t);return out;}double jaccard(const std::string&a,const std::string&b){auto x=tokens(a),y=tokens(b);if(x.empty()&&y.empty())return 1;std::size_t inter=0;for(const auto&t:x)if(y.count(t))++inter;std::size_t uni=x.size()+y.size()-inter;return uni?static_cast<double>(inter)/uni:0;}}
namespace cst {void TextMemory::store(std::string text,double salience,double confidence){if(text.empty())throw std::invalid_argument("memory text cannot be empty");records_.push_back({std::move(text),salience,confidence});}std::vector<std::pair<TextMemoryRecord,double>> TextMemory::recall(const std::string&q,std::size_t limit)const{std::vector<std::pair<TextMemoryRecord,double>>out;for(const auto&r:records_)out.push_back({r,0.8*jaccard(q,r.text)+0.15*r.salience+0.05*r.confidence});std::sort(out.begin(),out.end(),[](const auto&a,const auto&b){return a.second>b.second;});if(out.size()>limit)out.resize(limit);return out;}}
