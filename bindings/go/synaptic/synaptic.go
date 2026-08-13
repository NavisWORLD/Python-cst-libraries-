package synaptic

import("errors";"math")
type Function struct{Sigma,Gate float64}
func New(sigma,gate float64)(Function,error){if sigma<=0{return Function{},errors.New("sigma must be > 0")};if gate<0||gate>1{return Function{},errors.New("gate must be in [0,1]")};return Function{Sigma:sigma,Gate:gate},nil}
func GaussianAffinity(a,b[]float64,sigma float64)(float64,error){if sigma<=0||len(a)==0||len(a)!=len(b){return 0,errors.New("invalid vectors or sigma")};var d2 float64;for i:=range a{d:=a[i]-b[i];d2+=d*d};return math.Exp(-d2/(2*sigma*sigma)),nil}
func(f Function)Affinity(a,b[]float64)(float64,error){return GaussianAffinity(a,b,f.Sigma)}
func(f Function)Blend(s,a float64,gate *float64)(float64,error){g:=f.Gate;if gate!=nil{g=*gate};if g<0||g>1{return 0,errors.New("gate must be in [0,1]")};return(1-g)*s+g*a,nil}
func StateStep(state,signal[]float64,decay,gain,dt float64)([]float64,error){if len(state)==0||len(state)!=len(signal)||decay<0||decay>1||dt<0{return nil,errors.New("invalid state update arguments")};ed:=math.Pow(decay,dt);out:=make([]float64,len(state));for i:=range state{out[i]=ed*state[i]+(1-ed)*gain*math.Tanh(signal[i])};return out,nil}
func(f Function)Step(state,signal[]float64,decay,gain,dt float64)([]float64,error){return StateStep(state,signal,decay,gain,dt)}
