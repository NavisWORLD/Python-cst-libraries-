"""Composable multi-organ controller for CST runtimes."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Protocol, runtime_checkable
from .core import Event
from .bus import EventBus

@runtime_checkable
class Organ(Protocol):
    name: str
    def process(self, event: Event, context: dict[str, object]) -> dict[str, object] | None: ...
    def health(self) -> dict[str, object]: ...

@dataclass
class FunctionOrgan:
    name: str
    handler: Callable[[Event, dict[str, object]], dict[str, object] | None]
    enabled: bool = True
    calls: int = 0
    failures: int = 0
    last_error: str | None = None

    def process(self, event: Event, context: dict[str, object]) -> dict[str, object] | None:
        if not self.enabled:
            return None
        try:
            result = self.handler(event, context)
            self.calls += 1
            self.last_error = None
            return result
        except Exception as exc:
            self.failures += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            return None

    def health(self) -> dict[str, object]:
        return {"name": self.name, "enabled": self.enabled, "calls": self.calls, "failures": self.failures, "last_error": self.last_error}

@dataclass
class DeferredOrgan:
    name: str
    reason: str = "deferred"
    def process(self, event: Event, context: dict[str, object]) -> None:
        return None
    def health(self) -> dict[str, object]:
        return {"name": self.name, "enabled": False, "deferred": True, "reason": self.reason}

class CNS:
    STANDARD_SLOTS = ("quantum", "dark_matter", "emeth", "plasticity", "awareness", "daemons", "surgeon")

    def __init__(self, *, bus: EventBus | None = None) -> None:
        self.bus = bus or EventBus()
        self.organs: dict[str, Organ] = {}

    @classmethod
    def standard(cls, *, bus: EventBus | None = None) -> "CNS":
        cns = cls(bus=bus)
        for name in cls.STANDARD_SLOTS:
            cns.register(DeferredOrgan(name))
        return cns

    def register(self, organ: Organ, *, replace: bool = True) -> None:
        if not replace and organ.name in self.organs:
            raise KeyError(f"organ already registered: {organ.name}")
        self.organs[organ.name] = organ

    def bind(self, name: str, handler: Callable[[Event, dict[str, object]], dict[str, object] | None]) -> FunctionOrgan:
        organ = FunctionOrgan(name, handler)
        self.register(organ)
        return organ

    def process(self, event: Event, context: dict[str, object] | None = None) -> dict[str, object]:
        context = dict(context or {})
        outputs: dict[str, object] = {}
        for name, organ in list(self.organs.items()):
            result = organ.process(event, context)
            if result is not None:
                outputs[name] = result
                context[name] = result
                self.bus.publish("cns", f"organ.{name}", result, tags=["cns", name])
        return outputs

    def health(self) -> dict[str, object]:
        return {"organs": {name: organ.health() for name, organ in self.organs.items()}, "bus": self.bus.health()}
