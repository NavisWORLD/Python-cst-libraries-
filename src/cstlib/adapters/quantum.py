"""Provider-result adapters for CST quantum provenance."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping
from cstlib.quantum import EntropyPacket, QuantumMeasurement
@dataclass
class CallbackEntropyAdapter:
    fetcher:Callable[[int],EntropyPacket|bytes];name:str="callback-entropy";calls:int=0;failures:int=0
    def sample(self,nbytes:int=32)->EntropyPacket:
        try:
            value=self.fetcher(nbytes);self.calls+=1;return value if isinstance(value,EntropyPacket) else EntropyPacket(self.name,bytes(value),{"adapter":"callback"})
        except Exception:self.failures+=1;raise
    def health(self)->dict[str,object]:return {"name":self.name,"calls":self.calls,"failures":self.failures,"ok":self.failures==0}
class IBMCountsAdapter:
    @staticmethod
    def measurement(counts:Mapping[str,int|float],*,backend:str,job_id:str|None=None,hardware:bool|None=True,metadata:dict[str,Any]|None=None)->QuantumMeasurement:
        return QuantumMeasurement("IBM",backend,{str(k):float(v) for k,v in counts.items()},hardware,job_id,metadata=metadata or {})
class AzureResultsAdapter:
    @staticmethod
    def measurement(results:Mapping[Any,Any],*,target:str,job_id:str|None=None,provider:str="Azure Quantum",hardware:bool|None=None,metadata:dict[str,Any]|None=None)->QuantumMeasurement:
        counts={}
        for key,value in results.items():
            bitstring="".join(str(int(v)) for v in key) if isinstance(key,(list,tuple)) else str(key).replace(" ","").replace("[","").replace("]","").replace(",","")
            try:numeric=float(value)
            except (TypeError,ValueError):continue
            if bitstring and all(c in "01" for c in bitstring):counts[bitstring]=counts.get(bitstring,0.0)+numeric
        if not counts:raise ValueError("could not find bitstring-frequency/probability pairs in Azure results")
        return QuantumMeasurement(provider,target,counts,hardware,job_id,metadata=metadata or {})
