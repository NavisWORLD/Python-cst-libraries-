"""Composable CST reference runtime built from reusable primitives and adapters."""
from __future__ import annotations
from pathlib import Path
from typing import Callable
from .adapters.base import EntropyAdapter, ModelAdapter
from .bus import EventBus
from .cns import CNS
from .config import RuntimeConfig
from .hebbian import HebbianMemory
from .heartbeat import Heartbeat
from .memory import SemanticMemory
from .quantum import SystemEntropy
from .sensory import SensorHub
from .state import DynamicState, Dyn12, make_state
Model=Callable[[str,dict[str,object]],str]
def diagnostic_model(message:str,context:dict[str,object])->str:
    recalled=context.get("recalled",[]);return f"CST runtime received: {message}\nstate={context['state']}\nrecalled={recalled}"
class Runtime:
    def __init__(self,*,state:DynamicState|None=None,memory:SemanticMemory|None=None,associations:HebbianMemory|None=None,heartbeat:Heartbeat|None=None,model:Model|ModelAdapter|None=None,sensors:SensorHub|None=None,entropy:EntropyAdapter|None=None,cns:CNS|None=None,bus:EventBus|None=None)->None:
        self.state=state or Dyn12();self.memory=memory or SemanticMemory();self.associations=associations or HebbianMemory();self.heartbeat=heartbeat or Heartbeat();self.model=model or diagnostic_model;self.bus=bus or EventBus();self.sensors=sensors or SensorHub();self.entropy=entropy or SystemEntropy();self.cns=cns or CNS.standard(bus=self.bus);self.turns=0
    @classmethod
    def local(cls,directory:str|Path=".cst",**kwargs)->"Runtime":
        root=Path(directory);root.mkdir(parents=True,exist_ok=True);return cls(memory=SemanticMemory(root/"memory.jsonl"),associations=HebbianMemory(root/"associations.json"),**kwargs)
    @classmethod
    def from_config(cls,config:RuntimeConfig,*,model:Model|ModelAdapter|None=None)->"Runtime":
        root=Path(config.root);state=make_state(config.state,decay=config.state_decay);return cls(state=state,memory=SemanticMemory(root/config.memory_file),associations=HebbianMemory(root/config.associations_file),model=model)
    def start(self)->None:self.heartbeat.start();self.bus.publish("runtime","runtime.started",{"turns":self.turns})
    def stop(self)->None:self.heartbeat.stop();self.bus.publish("runtime","runtime.stopped",{"turns":self.turns})
    def respond(self,message:str)->str:
        if not message.strip():raise ValueError("message cannot be empty")
        input_event=self.bus.publish("user","conversation.input",{"text":message},tags=["conversation","input"]);recalled_pairs=self.memory.recall(message,limit=3);recalled=[record.text for record,_ in recalled_pairs];sensor_events=self.sensors.sample()
        for event in sensor_events.values():self.bus.emit(event)
        entropy_packet=self.entropy.sample(16);self.state.update(message);context={"state":self.state.vector(),"state_metrics":self.state.metrics(),"recalled":recalled,"sensors":{name:event.payload for name,event in sensor_events.items()},"entropy":entropy_packet.to_dict(include_bytes=False),"turn":self.turns+1};context["cns"]=self.cns.process(input_event,context);response=self.model(message,context)
        if not isinstance(response,str):raise TypeError("model adapter must return str")
        self.memory.store(message,metadata={"role":"input","turn":self.turns+1});self.memory.store(response,metadata={"role":"output","turn":self.turns+1});self.associations.learn(message);self.associations.learn(response);self.turns+=1;self.bus.publish("runtime","conversation.output",{"text":response,"turn":self.turns},tags=["conversation","output"]);return response
    def snapshot(self)->dict[str,object]:return {"turns":self.turns,"state":self.state.snapshot(),"memory":self.memory.snapshot(),"associations":self.associations.snapshot(),"heartbeat":self.heartbeat.health(),"sensors":self.sensors.health(),"entropy":self.entropy.health(),"cns":self.cns.health(),"bus":self.bus.health()}
    def health(self)->dict[str,object]:return self.snapshot()
