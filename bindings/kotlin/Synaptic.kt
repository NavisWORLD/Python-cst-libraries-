package org.cosmos.cst
import kotlin.math.exp
import kotlin.math.pow
import kotlin.math.tanh
object SynapticKotlin{
 fun affinity(a:DoubleArray,b:DoubleArray,sigma:Double=1.0):Double{require(sigma>0&&a.isNotEmpty()&&a.size==b.size);var d2=0.0;for(i in a.indices){val d=a[i]-b[i];d2+=d*d};return exp(-d2/(2*sigma*sigma))}
 fun blend(standard:Double,affinity:Double,gate:Double):Double{require(gate in 0.0..1.0);return(1-gate)*standard+gate*affinity}
 fun step(state:DoubleArray,signal:DoubleArray,decay:Double=.92,gain:Double=1.0,dt:Double=1.0):DoubleArray{require(state.isNotEmpty()&&state.size==signal.size&&decay in 0.0..1.0&&dt>=0);val ed=decay.pow(dt);return DoubleArray(state.size){i->ed*state[i]+(1-ed)*gain*tanh(signal[i])}}
}
