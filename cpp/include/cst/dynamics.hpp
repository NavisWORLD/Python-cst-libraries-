#pragma once
#include <array>
namespace cst {class Lorenz{public:Lorenz(double sigma=10.0,double rho=28.0,double beta=8.0/3.0,double x=1.0,double y=1.0,double z=1.0);std::array<double,3> step(double dt=0.01);std::array<double,3> state()const noexcept{return{x_,y_,z_};}private:std::array<double,3> f(double x,double y,double z)const;double sigma_,rho_,beta_,x_,y_,z_;};}
