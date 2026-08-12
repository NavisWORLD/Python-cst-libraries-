"""Serializable CST runtime configuration."""
from __future__ import annotations
import json, os
from dataclasses import asdict, dataclass, field
from pathlib import Path

@dataclass
class RuntimeConfig:
    state: str = "dyn12"
    state_decay: float = 0.92
    root: str = ".cst"
    memory_file: str = "memory.jsonl"
    associations_file: str = "associations.json"
    model_adapter: str = "diagnostic"
    model_name: str | None = None
    model_url: str = "http://localhost:11434"
    enable_sensors: bool = True
    enable_entropy: bool = True
    enable_cns: bool = True
    metadata: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str | Path) -> "RuntimeConfig":
        return cls(**json.loads(Path(path).read_text(encoding="utf-8")))
    @classmethod
    def from_env(cls, prefix: str = "CST_") -> "RuntimeConfig":
        cfg=cls(); mapping={"STATE":"state","ROOT":"root","MODEL_ADAPTER":"model_adapter","MODEL_NAME":"model_name","MODEL_URL":"model_url"}
        for key,attr in mapping.items():
            value=os.getenv(prefix+key)
            if value is not None: setattr(cfg,attr,value)
        if (v:=os.getenv(prefix+"STATE_DECAY")) is not None: cfg.state_decay=float(v)
        return cfg
    def save(self, path: str | Path) -> Path:
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(asdict(self),indent=2,sort_keys=True),encoding="utf-8"); return path
