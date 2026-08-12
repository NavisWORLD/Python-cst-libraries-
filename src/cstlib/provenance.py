"""Hashable provenance records and experiment manifests."""
from __future__ import annotations
import hashlib, json, platform, sys, time, uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)

def sha256_value(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""): h.update(block)
    return h.hexdigest()

@dataclass(slots=True)
class ProvenanceRecord:
    source: str
    kind: str
    payload_hash: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    def to_dict(self) -> dict[str, Any]: return asdict(self)
    @classmethod
    def from_payload(cls, source: str, kind: str, payload: object, **metadata: Any) -> "ProvenanceRecord":
        return cls(source, kind, sha256_value(payload), metadata=metadata)

@dataclass
class ExperimentManifest:
    name: str
    config: dict[str, Any]
    seeds: list[int] = field(default_factory=list)
    dataset_hash: str | None = None
    code_hash: str | None = None
    status: str = "IMPLEMENTED"
    result: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    environment: dict[str, str] = field(default_factory=lambda:{"python":sys.version.split()[0],"platform":platform.platform()})

    def receipt(self) -> str: return sha256_value(asdict(self))
    def to_dict(self) -> dict[str, Any]:
        data=asdict(self); data["receipt"]=self.receipt(); return data
    def save(self, path: str | Path) -> Path:
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(self.to_dict(),indent=2,sort_keys=True),encoding="utf-8"); return path
