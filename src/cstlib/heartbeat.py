"""Fail-soft background maintenance scheduler."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class Task:
    name: str
    interval: float
    callback: Callable[[], None]
    next_run: float
    failures: int = 0
    runs: int = 0

class Heartbeat:
    def __init__(self, tick: float = 0.25) -> None:
        self.tick = tick
        self.tasks: list[Task] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def every(self, seconds: float, callback: Callable[[], None], *, name: str | None = None) -> Task:
        if seconds <= 0:
            raise ValueError("seconds must be positive")
        task = Task(name or getattr(callback, "__name__", "task"), seconds, callback, time.monotonic() + seconds)
        self.tasks.append(task)
        return task

    def run_due(self) -> None:
        now = time.monotonic()
        for task in self.tasks:
            if now < task.next_run:
                continue
            try:
                task.callback()
                task.runs += 1
            except Exception:
                task.failures += 1
            finally:
                task.next_run = now + task.interval

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        def worker() -> None:
            while not self._stop.wait(self.tick):
                self.run_due()
        self._thread = threading.Thread(target=worker, name="cst-heartbeat", daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout)

    def health(self) -> dict[str, object]:
        return {"running": bool(self._thread and self._thread.is_alive()), "tasks": [{"name": t.name, "runs": t.runs, "failures": t.failures, "interval": t.interval} for t in self.tasks]}
