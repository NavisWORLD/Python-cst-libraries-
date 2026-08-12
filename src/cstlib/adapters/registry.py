"""Explicit adapter registry used by applications and CST-L hosts."""
from __future__ import annotations
from typing import Any
class AdapterRegistry:
    def __init__(self)->None:self._groups={"model":{},"embedding":{},"sensor":{},"entropy":{},"organ":{}}
    def register(self,group:str,name:str,adapter:Any)->Any:
        if group not in self._groups:raise KeyError(f"unknown adapter group: {group}")
        self._groups[group][name]=adapter;return adapter
    def get(self,group:str,name:str)->Any:
        try:return self._groups[group][name]
        except KeyError as exc:raise KeyError(f"adapter not registered: {group}:{name}") from exc
    def snapshot(self)->dict[str,list[str]]:return {g:sorted(v) for g,v in self._groups.items()}
