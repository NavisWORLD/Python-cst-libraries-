"""Synchronous, fail-soft CST event bus."""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from threading import RLock
from typing import Callable
from .core import Event

Handler = Callable[[Event], None]

@dataclass(slots=True)
class DeliveryError:
    event_kind: str
    handler: str
    error: str

class EventBus:
    def __init__(self, *, history: int = 256) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._history: deque[Event] = deque(maxlen=max(0, history))
        self._errors: deque[DeliveryError] = deque(maxlen=max(16, history or 16))
        self._lock = RLock()

    def subscribe(self, kind: str, handler: Handler) -> Callable[[], None]:
        if not kind:
            raise ValueError("event kind cannot be empty")
        with self._lock:
            self._handlers[kind].append(handler)
        def unsubscribe() -> None:
            with self._lock:
                if handler in self._handlers.get(kind, []):
                    self._handlers[kind].remove(handler)
        return unsubscribe

    def emit(self, event: Event) -> list[DeliveryError]:
        with self._lock:
            if self._history.maxlen:
                self._history.append(event)
            handlers = list(self._handlers.get(event.kind, ())) + list(self._handlers.get("*", ()))
        failures: list[DeliveryError] = []
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                failure = DeliveryError(event.kind, getattr(handler, "__name__", repr(handler)), f"{type(exc).__name__}: {exc}")
                failures.append(failure)
                with self._lock:
                    self._errors.append(failure)
        return failures

    def publish(self, source: str, kind: str, payload: dict[str, object], *, confidence: float = 1.0, tags: list[str] | None = None) -> Event:
        event = Event(source=source, kind=kind, payload=payload, confidence=confidence, tags=tags or [])
        self.emit(event)
        return event

    def history(self) -> list[Event]:
        with self._lock:
            return list(self._history)

    def errors(self) -> list[DeliveryError]:
        with self._lock:
            return list(self._errors)

    def health(self) -> dict[str, object]:
        with self._lock:
            return {"subscriptions": sum(len(v) for v in self._handlers.values()), "kinds": sorted(self._handlers), "history": len(self._history), "errors": len(self._errors)}
