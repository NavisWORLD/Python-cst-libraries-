import Foundation

enum SynapticError: Error { case invalidArgument }
struct SynapticFunction {
    let sigma: Double
    let gate: Double
    init(sigma: Double = 1.0, gate: Double = 0.5) throws { guard sigma > 0, (0...1).contains(gate) else { throw SynapticError.invalidArgument }; self.sigma=sigma; self.gate=gate }
    func affinity(_ a:[Double],_ b:[Double]) throws -> Double { guard !a.isEmpty, a.count==b.count else { throw SynapticError.invalidArgument }; let d2=zip(a,b).reduce(0.0){$0+($1.0-$1.1)*($1.0-$1.1)}; return exp(-d2/(2*sigma*sigma)) }
    func blend(_ standard:Double,_ affinity:Double,gate override:Double?=nil)throws->Double{let g=override ?? gate;guard(0...1).contains(g)else{throw SynapticError.invalidArgument};return(1-g)*standard+g*affinity}
    func step(_ state:[Double],_ signal:[Double],decay:Double=0.92,gain:Double=1.0,dt:Double=1.0)throws->[Double]{guard !state.isEmpty,state.count==signal.count,(0...1).contains(decay),dt>=0 else{throw SynapticError.invalidArgument};let ed=pow(decay,dt);return zip(state,signal).map{ed*$0.0+(1-ed)*gain*tanh($0.1)}}
}
