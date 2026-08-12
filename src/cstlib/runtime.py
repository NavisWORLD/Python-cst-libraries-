"""Composable reference runtime built from CST primitives."""
from pathlib import Path
from typing import Callable
from .hebbian import HebbianMemory
from .heartbeat import Heartbeat
from .memory import SemanticMemory
from .state import DynamicState, Dyn12

Model = Callable[[str, dict[str, object]], str]

def diagnostic_model(message: str, context: dict[str, object]) -> str:
    recalled = context.get("recalled", [])
    return f"CST runtime received: {message}\nstate={context['state']}\nrecalled={recalled}"

class Runtime:
    def __init__(self, *, state: DynamicState | None = None, memory: SemanticMemory | None = None, associations: HebbianMemory | None = None, heartbeat: Heartbeat | None = None, model: Model | None = None) -> None:
        self.state = state or Dyn12()
        self.memory = memory or SemanticMemory()
        self.associations = associations or HebbianMemory()
        self.heartbeat = heartbeat or Heartbeat()
        self.model = model or diagnostic_model

    @classmethod
    def local(cls, directory: str | Path = ".cst") -> "Runtime":
        root = Path(directory)
        return cls(memory=SemanticMemory(root / "memory.jsonl"), associations=HebbianMemory(root / "associations.json"))

    def start(self) -> None:
        self.heartbeat.start()

    def stop(self) -> None:
        self.heartbeat.stop()

    def respond(self, message: str) -> str:
        recalled_pairs = self.memory.recall(message, limit=3)
        recalled = [record.text for record, _score in recalled_pairs]
        self.state.update(message)
        context = {"state": self.state.vector(), "state_metrics": self.state.metrics(), "recalled": recalled}
        response = self.model(message, context)
        self.memory.store(message, metadata={"role": "input"})
        self.memory.store(response, metadata={"role": "output"})
        self.associations.learn(message)
        return response

    def health(self) -> dict[str, object]:
        return {"state": self.state.metrics(), "memory": self.memory.snapshot(), "heartbeat": self.heartbeat.health()}
