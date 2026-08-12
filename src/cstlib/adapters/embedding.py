"""Embedding adapters including the dependency-free and Ollama paths."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable
from cstlib.memory import hashed_embedding
from .base import AdapterError
from .http import post_json
@dataclass
class HashedEmbeddingAdapter:
    dimension:int=128; name:str="hashed"
    def __call__(self,text:str)->list[float]:return hashed_embedding(text,self.dimension)
    def health(self)->dict[str,object]:return {"name":self.name,"ok":True,"dimension":self.dimension}
@dataclass
class CallableEmbeddingAdapter:
    function:Callable[[str],Iterable[float]]; name:str="callable"
    def __call__(self,text:str)->list[float]:return [float(v) for v in self.function(text)]
    def health(self)->dict[str,object]:return {"name":self.name,"ok":True}
@dataclass
class OllamaEmbeddingAdapter:
    model:str="embeddinggemma"; base_url:str="http://localhost:11434"; timeout:float=60.0; dimensions:int|None=None; name:str="ollama-embed"
    def __call__(self,text:str)->list[float]:
        payload={"model":self.model,"input":text}
        if self.dimensions is not None:payload["dimensions"]=self.dimensions
        response=post_json(self.base_url.rstrip("/")+"/api/embed",payload,timeout=self.timeout);embeddings=response.get("embeddings")
        if not isinstance(embeddings,list) or not embeddings or not isinstance(embeddings[0],list):raise AdapterError("Ollama response missing embeddings[0]")
        return [float(v) for v in embeddings[0]]
    def health(self)->dict[str,object]:return {"name":self.name,"configured":True,"model":self.model,"url":self.base_url}
