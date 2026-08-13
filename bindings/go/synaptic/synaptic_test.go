package synaptic
import("math";"testing")
func close(a,b float64)bool{return math.Abs(a-b)<1e-12}
func TestConformance(t *testing.T){f,_:=New(.75,.35);h,_:=f.Affinity([]float64{0,1,-1,.5},[]float64{.5,.5,-.5,1});if !close(h,.41111229050718745){t.Fatal(h)};b,_:=f.Blend(.8,h,nil);if !close(b,.6638893016775156){t.Fatal(b)};o,_:=f.Step([]float64{.1,-.2,.3,-.4},[]float64{1,-.5,.25,-1},.92,1.2,.5);if !close(o[0],.13323507494835604){t.Fatal(o)}}
