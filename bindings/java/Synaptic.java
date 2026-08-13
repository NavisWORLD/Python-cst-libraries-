package org.cosmos.cst;
public final class Synaptic{
 private Synaptic(){}
 public static double affinity(double[]a,double[]b,double sigma){if(sigma<=0||a==null||b==null||a.length==0||a.length!=b.length)throw new IllegalArgumentException("invalid vectors or sigma");double d2=0;for(int i=0;i<a.length;i++){double d=a[i]-b[i];d2+=d*d;}return Math.exp(-d2/(2*sigma*sigma));}
 public static double blend(double s,double a,double g){if(g<0||g>1)throw new IllegalArgumentException("gate must be in [0,1]");return(1-g)*s+g*a;}
 public static double[] step(double[]state,double[]signal,double decay,double gain,double dt){if(state==null||signal==null||state.length==0||state.length!=signal.length||decay<0||decay>1||dt<0)throw new IllegalArgumentException("invalid state update arguments");double ed=Math.pow(decay,dt);double[]o=new double[state.length];for(int i=0;i<state.length;i++)o[i]=ed*state[i]+(1-ed)*gain*Math.tanh(signal[i]);return o;}
 public static final class Function{public final double sigma,gate;public Function(double sigma,double gate){if(sigma<=0||gate<0||gate>1)throw new IllegalArgumentException("invalid sigma or gate");this.sigma=sigma;this.gate=gate;}public double affinity(double[]a,double[]b){return Synaptic.affinity(a,b,sigma);}public double blend(double s,double a){return Synaptic.blend(s,a,gate);}public double[] step(double[]s,double[]u,double d,double k,double dt){return Synaptic.step(s,u,d,k,dt);}}
}
