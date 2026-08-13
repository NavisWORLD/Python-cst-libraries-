import Foundation
func close(_ a:Double,_ b:Double)->Bool{abs(a-b)<1e-12}
let f=try SynapticFunction(sigma:0.75,gate:0.35)
let h=try f.affinity([0,1,-1,0.5],[0.5,0.5,-0.5,1]);precondition(close(h,0.41111229050718745))
let blended=try f.blend(0.8,h);precondition(close(blended,0.6638893016775156))
let out=try f.step([0.1,-0.2,0.3,-0.4],[1,-0.5,0.25,-1],decay:0.92,gain:1.2,dt:0.5);precondition(close(out[0],0.13323507494835604))
print("swift conformance ok")
