"""Quantum provenance records and entropy packets."""
from __future__ import annotations
import hashlib, json, secrets, time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from .provenance import canonical_json, sha256_value

@dataclass(slots=True)
class QuantumMeasurement:
    provider: str
    backend: str
    counts: dict[str, float]
    hardware: bool | None = None
    job_id: str | None = None
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    def __post_init__(self) -> None:
        cleaned={}
        for bitstring,value in self.counts.items():
            key=str(bitstring).replace(" ","")
            if not key or any(c not in "01" for c in key): raise ValueError(f"invalid bitstring: {bitstring!r}")
            fv=float(value)
            if fv<0: raise ValueError("count/probability values must be non-negative")
            cleaned[key]=cleaned.get(key,0.0)+fv
        if not cleaned: raise ValueError("measurement counts cannot be empty")
        self.counts=cleaned
    def to_dict(self)->dict[str,Any]: return asdict(self)
    def receipt(self)->str: return sha256_value(self.to_dict())
    def deterministic_seed(self)->int:
        digest=hashlib.sha256(canonical_json(self.to_dict()).encode("utf-8")).digest(); return int.from_bytes(digest[:8],"big")

@dataclass(slots=True)
class EntropyPacket:
    source: str
    data: bytes
    provenance: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    @property
    def hex(self)->str:return self.data.hex()
    @property
    def seed(self)->int:return int.from_bytes(hashlib.sha256(self.data).digest()[:8],"big")
    def to_dict(self, *, include_bytes: bool = False)->dict[str,Any]:
        out={"source":self.source,"sha256":hashlib.sha256(self.data).hexdigest(),"bytes":len(self.data),"seed":self.seed,"timestamp":self.timestamp,"provenance":self.provenance}
        if include_bytes: out["hex"]=self.hex
        return out

class SystemEntropy:
    name="system"
    def sample(self,nbytes:int=32)->EntropyPacket:
        if nbytes<=0:raise ValueError("nbytes must be positive")
        return EntropyPacket(self.name,secrets.token_bytes(nbytes),{"kind":"os-csprng"})
    def health(self)->dict[str,object]:return {"name":self.name,"ok":True,"kind":"os-csprng"}

class MeasurementArchive:
    def __init__(self,path:str|Path)->None:self.path=Path(path)
    def append(self,measurement:QuantumMeasurement)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open("a",encoding="utf-8") as h:h.write(json.dumps(measurement.to_dict(),sort_keys=True)+"\n")
    def load(self)->list[QuantumMeasurement]:
        if not self.path.exists():return []
        return [QuantumMeasurement(**json.loads(line)) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

class MeasurementEntropy:
    name="measurement"
    def __init__(self,measurement:QuantumMeasurement)->None:self.measurement=measurement
    def sample(self,nbytes:int=32)->EntropyPacket:
        if nbytes<=0:raise ValueError("nbytes must be positive")
        seed=canonical_json(self.measurement.to_dict()).encode("utf-8"); out=bytearray(); counter=0
        while len(out)<nbytes:
            out.extend(hashlib.sha256(counter.to_bytes(8,"big")+seed).digest()); counter+=1
        return EntropyPacket(self.name,bytes(out[:nbytes]),{"measurement_receipt":self.measurement.receipt(),"provider":self.measurement.provider,"backend":self.measurement.backend,"hardware":self.measurement.hardware,"job_id":self.measurement.job_id,"derivation":"sha256-counter"})
    def health(self)->dict[str,object]:return {"name":self.name,"ok":True,"measurement_receipt":self.measurement.receipt()}
