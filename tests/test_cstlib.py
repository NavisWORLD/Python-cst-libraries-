from pathlib import Path
import math
from cstlib import CNS,Dyn12,Event,EventBus,GaussianSynapse,HebbianMemory,Lorenz,MeasurementEntropy,Runtime,SemanticMemory,SensorHub,SystemEntropy,audio_summary,check_preflight
from cstlib.adapters import AudioReaderAdapter,AzureResultsAdapter,CallableModelAdapter,HashedEmbeddingAdapter,IBMCountsAdapter,LumaReaderAdapter
from cstlib.lang import parse
from cstlib.provenance import ExperimentManifest

def test_dyn12_persists_state():
    state=Dyn12(decay=0.5);a=state.update([1.0]);b=state.update([0.0]);assert len(a)==len(b)==12 and state.updates==2 and abs(b[0])>0

def test_synapse_auto_bandwidth():
    states=[[0.0,0.0],[1.0,0.0],[0.0,1.0]];kernel=GaussianSynapse("median");h=kernel.affinity(states);assert h[0][0]==1.0 and 0<h[0][1]<1 and kernel.diagnostics(states).bandwidth>0

def test_memory_and_hebbian(tmp_path:Path):
    memory=SemanticMemory(tmp_path/"memory.jsonl");memory.store("the red guitar lives in the studio",salience=1);memory.store("bananas are yellow");assert memory.recall("where is the guitar?",limit=1)[0][0].text=="the red guitar lives in the studio";hebb=HebbianMemory(tmp_path/"hebb.json",learning_rate=0.5);hebb.learn(["guitar","music","stage"]);assert hebb.associated_with("guitar")[0][0] in {"music","stage"}

def test_lorenz_moves():
    system=Lorenz();before=system.snapshot();system.step();assert system.snapshot()!=before

def test_preflight_detects_live_kernel():
    states=[[0,0],[1,.5],[.2,1]];h=GaussianSynapse("median").affinity(states);assert check_preflight([0,1,2],states,h,gate_gradient=.1).passed

def test_event_bus_fail_soft():
    bus=EventBus();seen=[];bus.subscribe("x",lambda e:seen.append(e.payload["n"]));bus.subscribe("x",lambda e:(_ for _ in ()).throw(RuntimeError("boom")));errors=bus.emit(Event("test","x",{"n":3}));assert seen==[3] and len(errors)==1 and bus.health()["errors"]==1

def test_standard_cns_slots_and_binding():
    cns=CNS.standard();assert set(cns.organs)==set(CNS.STANDARD_SLOTS);cns.bind("awareness",lambda event,ctx:{"kind":event.kind});out=cns.process(Event("t","hello",{}));assert out["awareness"]["kind"]=="hello"

def test_sensory_summaries_and_adapters():
    samples=[math.sin(2*math.pi*440*i/8000) for i in range(256)];summary=audio_summary(samples,sample_rate=8000);assert summary.rms>0 and summary.peak>0 and summary.spectral_centroid_hz>0;audio=AudioReaderAdapter(lambda:samples,sample_rate=8000);assert audio.sample().kind=="sensor.audio";frames=iter([[0,0,255,255],[255,255,0,0]]);vision=LumaReaderAdapter(lambda:next(frames));first=vision.sample();second=vision.sample();assert first.kind=="sensor.vision" and second.payload["motion"]>0

def test_quantum_provenance_adapters():
    ibm=IBMCountsAdapter.measurement({"00":5,"11":3},backend="test_backend",job_id="abc",hardware=False);assert ibm.provider=="IBM" and ibm.deterministic_seed()==ibm.deterministic_seed();packet=MeasurementEntropy(ibm).sample(20);assert len(packet.data)==20 and packet.provenance["measurement_receipt"]==ibm.receipt();azure=AzureResultsAdapter.measurement({(0,1):.25,(1,0):.75},target="sim",hardware=False);assert set(azure.counts)=={"01","10"};assert len(SystemEntropy().sample(8).data)==8

def test_embedding_adapter():
    embed=HashedEmbeddingAdapter(64);assert len(embed("hello world"))==64 and embed.health()["dimension"]==64

def test_runtime_adapters_and_events(tmp_path:Path):
    model=CallableModelAdapter(lambda message,context:f"answer:{message}:{len(context['recalled'])}");hub=SensorHub();hub.register(AudioReaderAdapter(lambda:[0.0,0.2,-0.2,0.1],sample_rate=1000));runtime=Runtime.local(tmp_path,model=model,sensors=hub);out=runtime.respond("alpha beta");assert out.startswith("answer:alpha beta") and runtime.turns==1 and runtime.memory.snapshot()["count"]==2;assert any(e.kind=="conversation.output" for e in runtime.bus.history())

def test_manifest_receipt(tmp_path:Path):
    manifest=ExperimentManifest("demo",{"model":"dyn12"},seeds=[1,2]);first=manifest.receipt();path=manifest.save(tmp_path/"manifest.json");assert path.exists() and manifest.receipt()==first

def test_cst_language_01_compatibility(tmp_path:Path):
    source='''\n    state mind dyn12 decay=0.8\n    memory life path=memory.jsonl\n    hebbian links path=links.json\n    loop message\n      recall life as remembered\n      evolve mind\n      associate links\n      store life\n      emit "message={message} memory={remembered} state={state.mind}"\n    end\n    ''';program=parse(source,base_dir=tmp_path);first=program.run("message","alpha beta");second=program.run("message","alpha again");assert "message=alpha beta" in first and "alpha beta" in second and (tmp_path/"memory.jsonl").exists()

def test_cst_language_external_bindings(tmp_path:Path):
    source='''\n    state mind dyn12\n    memory life path=memory.jsonl\n    model local external\n    sensor mic external\n    entropy q external\n    loop message\n      observe mic as sensed\n      sample q as random bytes=8\n      evolve mind\n      generate local as answer\n      store life from=answer\n      snapshot mind as now\n      emit "{answer}"\n    end\n    ''';program=parse(source,base_dir=tmp_path);program.bind_model("local",CallableModelAdapter(lambda msg,ctx:"ok:"+msg));program.bind_sensor("mic",AudioReaderAdapter(lambda:[0,.1,-.1]));program.bind_entropy("q",SystemEntropy());out=program.run("message","hello");assert out=="ok:hello" and program.memories["life"].records[0].text=="ok:hello"

def test_torch_mixture_attention_if_available():
    try:import torch
    except ImportError:return
    from cstlib.transformer import MixtureOfStatesAttention
    layer=MixtureOfStatesAttention(16,4,bandwidth="auto");hidden=torch.randn(2,5,16);state=torch.randn(2,5,12);out,diag=layer(hidden,state,return_diagnostics=True);assert out.shape==(2,5,16) and 0<float(diag["gate"])<1 and float(diag["sigma"])>0
