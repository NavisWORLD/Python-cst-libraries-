"""CST-L 0.2: executable DSL for persistent-state programs and host-bound adapters."""
from __future__ import annotations
import shlex
from dataclasses import dataclass,field
from pathlib import Path
from typing import Any
from .adapters.base import EntropyAdapter,ModelAdapter,SensorAdapter
from .hebbian import HebbianMemory
from .memory import SemanticMemory
from .state import DynamicState,make_state
@dataclass(slots=True)
class Instruction:op:str;args:list[str];options:dict[str,str]=field(default_factory=dict)
@dataclass
class Program:
    states:dict[str,DynamicState]=field(default_factory=dict);memories:dict[str,SemanticMemory]=field(default_factory=dict);hebbian:dict[str,HebbianMemory]=field(default_factory=dict);loops:dict[str,list[Instruction]]=field(default_factory=dict);external_models:set[str]=field(default_factory=set);external_sensors:set[str]=field(default_factory=set);external_entropy:set[str]=field(default_factory=set);models:dict[str,ModelAdapter|Any]=field(default_factory=dict);sensors:dict[str,SensorAdapter|Any]=field(default_factory=dict);entropy:dict[str,EntropyAdapter|Any]=field(default_factory=dict)
    def bind_model(self,name:str,adapter:ModelAdapter|Any)->None:self.models[name]=adapter
    def bind_sensor(self,name:str,adapter:SensorAdapter|Any)->None:self.sensors[name]=adapter
    def bind_entropy(self,name:str,adapter:EntropyAdapter|Any)->None:self.entropy[name]=adapter
    def inspect(self)->dict[str,object]:return {"states":sorted(self.states),"memories":sorted(self.memories),"hebbian":sorted(self.hebbian),"loops":{k:[i.op for i in v] for k,v in self.loops.items()},"external":{"models":sorted(self.external_models),"sensors":sorted(self.external_sensors),"entropy":sorted(self.external_entropy)}}
    def run(self,event:str,message:str)->str:
        env={"message":message};emitted=[]
        for inst in self.loops.get(event,[]):
            if inst.op=="recall":
                memory_name,alias=inst.args;env[alias]=[r.text for r,_ in self.memories[memory_name].recall(str(env.get(inst.options.get("from","message"),message)))]
            elif inst.op=="evolve":
                source=env.get(inst.options.get("from","message"),message);self.states[inst.args[0]].update(source if isinstance(source,(str,int,float,list,tuple)) else repr(source))
            elif inst.op=="store":source=env.get(inst.options.get("from","message"),message);self.memories[inst.args[0]].store(str(source))
            elif inst.op=="associate":source=env.get(inst.options.get("from","message"),message);self.hebbian[inst.args[0]].learn(str(source))
            elif inst.op=="snapshot":state_name,alias=inst.args;env[alias]=self.states[state_name].snapshot()
            elif inst.op=="observe":
                name,alias=inst.args
                if name not in self.sensors:raise RuntimeError(f"external sensor not bound: {name}")
                env[alias]=self.sensors[name].sample().to_dict()
            elif inst.op=="sample":
                name,alias=inst.args
                if name not in self.entropy:raise RuntimeError(f"external entropy adapter not bound: {name}")
                env[alias]=self.entropy[name].sample(int(inst.options.get("bytes","16"))).to_dict(include_bytes=False)
            elif inst.op=="generate":
                name,alias=inst.args
                if name not in self.models:raise RuntimeError(f"external model not bound: {name}")
                env[alias]=self.models[name](message,{"env":env,"states":{n:s.snapshot() for n,s in self.states.items()}})
            elif inst.op=="emit":
                template=" ".join(inst.args);rendered=template.replace("{message}",message)
                for name,state in self.states.items():rendered=rendered.replace(f"{{state.{name}}}",repr(state.vector()))
                for key,value in env.items():rendered=rendered.replace(f"{{{key}}}",repr(value) if not isinstance(value,str) else value)
                emitted.append(rendered)
            else:raise ValueError(f"unknown instruction: {inst.op}")
        return "\n".join(emitted)
def _options(tokens:list[str])->dict[str,str]:
    options={}
    for token in tokens:
        if "=" not in token:raise ValueError(f"expected key=value, got: {token}")
        key,value=token.split("=",1);options[key]=value
    return options
def parse(source:str,*,base_dir:str|Path=".")->Program:
    program=Program();current_loop=None;root=Path(base_dir)
    for lineno,raw in enumerate(source.splitlines(),start=1):
        line=raw.strip()
        if not line or line.startswith("#"):continue
        tokens=shlex.split(line)
        try:
            if current_loop is not None:
                if tokens[0]=="end":current_loop=None;continue
                op=tokens[0]
                if op=="recall":
                    if len(tokens)<4 or tokens[2]!="as":raise ValueError("syntax: recall MEMORY as NAME [from=VAR]")
                    args=[tokens[1],tokens[3]];opts=_options(tokens[4:])
                elif op in {"evolve","store","associate"}:args=[tokens[1]];opts=_options(tokens[2:])
                elif op=="snapshot":
                    if len(tokens)!=4 or tokens[2]!="as":raise ValueError("syntax: snapshot STATE as NAME")
                    args=[tokens[1],tokens[3]];opts={}
                elif op in {"observe","generate"}:
                    if len(tokens)!=4 or tokens[2]!="as":raise ValueError(f"syntax: {op} ADAPTER as NAME")
                    args=[tokens[1],tokens[3]];opts={}
                elif op=="sample":
                    if len(tokens)<4 or tokens[2]!="as":raise ValueError("syntax: sample ENTROPY as NAME [bytes=N]")
                    args=[tokens[1],tokens[3]];opts=_options(tokens[4:])
                elif op=="emit":args=tokens[1:];opts={}
                else:raise ValueError(f"unknown loop operation: {op}")
                program.loops[current_loop].append(Instruction(op,args,opts));continue
            head=tokens[0]
            if head=="state":name,kind=tokens[1],tokens[2];program.states[name]=make_state(kind,**{k:float(v) for k,v in _options(tokens[3:]).items()})
            elif head=="memory":name=tokens[1];path=_options(tokens[2:]).get("path");program.memories[name]=SemanticMemory(root/path if path else None)
            elif head=="hebbian":name=tokens[1];path=_options(tokens[2:]).get("path");program.hebbian[name]=HebbianMemory(root/path if path else None)
            elif head in {"model","sensor","entropy"}:
                if len(tokens)!=3 or tokens[2]!="external":raise ValueError(f"syntax: {head} NAME external")
                getattr(program,f"external_{'models' if head=='model' else 'sensors' if head=='sensor' else 'entropy'}").add(tokens[1])
            elif head=="loop":current_loop=tokens[1];program.loops[current_loop]=[]
            else:raise ValueError(f"unknown declaration: {head}")
        except (IndexError,ValueError) as exc:raise ValueError(f"CST-L line {lineno}: {exc}") from exc
    if current_loop is not None:raise ValueError(f"unclosed loop: {current_loop}")
    return program
def load(path:str|Path)->Program:path=Path(path);return parse(path.read_text(encoding="utf-8"),base_dir=path.parent)
