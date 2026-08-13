import json
import subprocess
import sys
from pathlib import Path
from cstlib import SynapticFunction, affinity_matrix, gated_blend, gaussian_affinity

def close(a,b): return abs(a-b)<1e-12

def test_synaptic_conformance():
    f=SynapticFunction(sigma=.75,gate=.35);a=[0,1,-1,.5];b=[.5,.5,-.5,1];h=f.affinity(a,b)
    assert close(h,.41111229050718745)
    assert close(gaussian_affinity(a,b,.75),h)
    assert close(f.blend(.8,h),.6638893016775156)
    assert close(gated_blend(.8,h,.35),.6638893016775156)
    out=f.step([.1,-.2,.3,-.4],[1,-.5,.25,-1],decay=.92,gain=1.2,dt=.5)
    assert close(out[0],.13323507494835604)
    assert affinity_matrix([a,b],.75)[0][0]==1.0

def test_json_bridge_roundtrip():
    root=Path(__file__).resolve().parents[1]
    request=json.dumps({"op":"affinity","a":[0,1,-1,.5],"b":[.5,.5,-.5,1],"sigma":.75})+"\n"
    proc=subprocess.run([sys.executable,str(root/"tools"/"synaptic_bridge.py")],input=request,text=True,capture_output=True,check=True)
    payload=json.loads(proc.stdout)
    assert payload["ok"] and close(payload["value"],.41111229050718745)
