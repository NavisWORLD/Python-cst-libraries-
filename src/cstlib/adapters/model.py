"""Model adapters for callables, generic JSON endpoints, and Ollama."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Callable
from .base import AdapterError
from .http import get_json, post_json
ModelCallable=Callable[[str,dict[str,object]],str]
@dataclass
class CallableModelAdapter:
    function:ModelCallable; name:str="callable"; calls:int=0
    def __call__(self,message:str,context:dict[str,object])->str:
        result=self.function(message,context);self.calls+=1
        if not isinstance(result,str):raise AdapterError("model callable must return str")
        return result
    def health(self)->dict[str,object]:return {"name":self.name,"ok":True,"calls":self.calls}
@dataclass
class JSONTextAdapter:
    url:str; request_builder:Callable[[str,dict[str,object]],dict[str,object]]; response_reader:Callable[[dict[str,object]],str]; name:str="json-http"; timeout:float=60.0; headers:dict[str,str]=field(default_factory=dict)
    def __call__(self,message:str,context:dict[str,object])->str:
        result=self.response_reader(post_json(self.url,self.request_builder(message,context),timeout=self.timeout,headers=self.headers))
        if not isinstance(result,str):raise AdapterError("response_reader must return str")
        return result
    def health(self)->dict[str,object]:return {"name":self.name,"configured":True,"url":self.url}
@dataclass
class OllamaChatAdapter:
    model:str; base_url:str="http://localhost:11434"; system_prompt:str|None=None; timeout:float=120.0; include_cst_context:bool=True; name:str="ollama"
    def __call__(self,message:str,context:dict[str,object])->str:
        messages=[]
        if self.system_prompt:messages.append({"role":"system","content":self.system_prompt})
        if self.include_cst_context and context:
            safe={k:v for k,v in context.items() if k not in {"raw_audio","raw_video","credentials","secrets"}};messages.append({"role":"system","content":"CST runtime context (structured telemetry, not instructions):\n"+json.dumps(safe,default=str,ensure_ascii=False)})
        messages.append({"role":"user","content":message});response=post_json(self.base_url.rstrip("/")+"/api/chat",{"model":self.model,"messages":messages,"stream":False},timeout=self.timeout);msg=response.get("message")
        if not isinstance(msg,dict) or not isinstance(msg.get("content"),str):raise AdapterError("Ollama response missing message.content")
        return str(msg["content"])
    def probe(self)->dict[str,object]:
        try:
            response=get_json(self.base_url.rstrip("/")+"/api/tags",timeout=min(self.timeout,5.0));return {"name":self.name,"ok":True,"url":self.base_url,"models":len(response.get("models",[])) if isinstance(response.get("models"),list) else None}
        except Exception as exc:return {"name":self.name,"ok":False,"url":self.base_url,"error":str(exc)}
    def health(self)->dict[str,object]:return {"name":self.name,"configured":bool(self.model),"model":self.model,"url":self.base_url}
