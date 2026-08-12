"""CST-L: a tiny executable DSL for persistent-state programs."""
from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from pathlib import Path
from .hebbian import HebbianMemory
from .memory import SemanticMemory
from .state import DynamicState, make_state

@dataclass
class Instruction:
    op: str
    args: list[str]

@dataclass
class Program:
    states: dict[str, DynamicState] = field(default_factory=dict)
    memories: dict[str, SemanticMemory] = field(default_factory=dict)
    hebbian: dict[str, HebbianMemory] = field(default_factory=dict)
    loops: dict[str, list[Instruction]] = field(default_factory=dict)

    def run(self, event: str, message: str) -> str:
        env: dict[str, object] = {"message": message}
        emitted: list[str] = []
        for inst in self.loops.get(event, []):
            if inst.op == "recall":
                memory_name, alias = inst.args
                env[alias] = [r.text for r, _ in self.memories[memory_name].recall(message)]
            elif inst.op == "evolve":
                self.states[inst.args[0]].update(message)
            elif inst.op == "store":
                self.memories[inst.args[0]].store(message)
            elif inst.op == "associate":
                self.hebbian[inst.args[0]].learn(message)
            elif inst.op == "emit":
                template = " ".join(inst.args)
                rendered = template.replace("{message}", message)
                for name, state in self.states.items():
                    rendered = rendered.replace(f"{{state.{name}}}", repr(state.vector()))
                for key, value in env.items():
                    rendered = rendered.replace(f"{{{key}}}", repr(value) if not isinstance(value, str) else value)
                emitted.append(rendered)
            else:
                raise ValueError(f"unknown instruction: {inst.op}")
        return "\n".join(emitted)

def _options(tokens: list[str]) -> dict[str, str]:
    options = {}
    for token in tokens:
        if "=" not in token:
            raise ValueError(f"expected key=value, got: {token}")
        key, value = token.split("=", 1)
        options[key] = value
    return options

def parse(source: str, *, base_dir: str | Path = ".") -> Program:
    program = Program()
    current_loop: str | None = None
    root = Path(base_dir)
    for lineno, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tokens = shlex.split(line)
        try:
            if current_loop is not None:
                if tokens[0] == "end":
                    current_loop = None
                    continue
                op = tokens[0]
                if op == "recall":
                    if len(tokens) != 4 or tokens[2] != "as":
                        raise ValueError("syntax: recall MEMORY as NAME")
                    args = [tokens[1], tokens[3]]
                elif op in {"evolve", "store", "associate"}:
                    args = [tokens[1]]
                elif op == "emit":
                    args = tokens[1:]
                else:
                    raise ValueError(f"unknown loop operation: {op}")
                program.loops[current_loop].append(Instruction(op, args))
                continue
            if tokens[0] == "state":
                name, kind = tokens[1], tokens[2]
                opts = {k: float(v) for k, v in _options(tokens[3:]).items()}
                program.states[name] = make_state(kind, **opts)
            elif tokens[0] == "memory":
                name = tokens[1]
                path = _options(tokens[2:]).get("path")
                program.memories[name] = SemanticMemory(root / path if path else None)
            elif tokens[0] == "hebbian":
                name = tokens[1]
                path = _options(tokens[2:]).get("path")
                program.hebbian[name] = HebbianMemory(root / path if path else None)
            elif tokens[0] == "loop":
                current_loop = tokens[1]
                program.loops[current_loop] = []
            else:
                raise ValueError(f"unknown declaration: {tokens[0]}")
        except (IndexError, ValueError) as exc:
            raise ValueError(f"CST-L line {lineno}: {exc}") from exc
    if current_loop is not None:
        raise ValueError(f"unclosed loop: {current_loop}")
    return program

def load(path: str | Path) -> Program:
    path = Path(path)
    return parse(path.read_text(encoding="utf-8"), base_dir=path.parent)
