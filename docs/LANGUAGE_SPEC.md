# CST-L 0.2 Language Specification

## Status

CST-L is an executable domain-specific language implemented by `cstlib.lang`. Version 0.2 is intentionally small, deterministic, and incapable of arbitrary Python or shell execution.

## Program structure

```cst
state mind dyn12 decay=0.92
memory life path=.cst/memory.jsonl
hebbian links path=.cst/links.json
model local external
sensor mic external
entropy q external

loop message
  recall life as remembered
  observe mic as audio
  sample q as entropy_packet bytes=16
  evolve mind
  generate local as answer
  store life from=answer
  associate links from=answer
  snapshot mind as current_state
  emit "{answer}"
end
```

## Lexical rules

- one statement per line
- leading/trailing whitespace ignored
- `#` begins a full-line comment
- quoted strings use shell-like quoting through Python `shlex`
- identifiers are case-sensitive
- paths are resolved relative to the `.cst` source file

## Declarations

State: `state NAME dyn12|dyn42|dyn54 [decay=FLOAT] [gain=FLOAT]`.
Memory: `memory NAME [path=PATH]`.
Hebbian store: `hebbian NAME [path=PATH]`.
External bindings: `model NAME external`, `sensor NAME external`, `entropy NAME external`.

External declarations do not instantiate providers. The host must bind them.

## Loops

`loop EVENT_NAME` begins a loop and `end` closes it. `Program.run(EVENT_NAME, message)` executes the loop.

## Instructions

- `recall MEMORY as VARIABLE [from=VARIABLE]` — default query source is `message`.
- `evolve STATE [from=VARIABLE]` — default source is `message`.
- `store MEMORY [from=VARIABLE]`.
- `associate HEBBIAN [from=VARIABLE]`.
- `snapshot STATE as VARIABLE`.
- `observe SENSOR as VARIABLE` — sensor must be host-bound.
- `sample ENTROPY as VARIABLE [bytes=N]` — template environment receives a safe packet summary, not raw entropy bytes.
- `generate MODEL as VARIABLE` — model receives user message plus environment/state context.
- `emit "template"` — supports `{message}`, `{VARIABLE}`, and `{state.NAME}`.

## Host API

```python
from cstlib.lang import load
program = load("main.cst")
program.bind_model("local", model)
program.bind_sensor("mic", sensor)
program.bind_entropy("q", entropy)
print(program.run("message", "hello"))
```

## Compatibility

0.1 programs using `state`, `memory`, `hebbian`, `loop`, `recall`, `evolve`, `associate`, `store`, and `emit` remain valid.

## Security model

CST-L 0.2 has no arbitrary file-read command, shell execution, Python evaluation, network primitive, secret declaration, or dynamic import. Those capabilities belong in explicit host adapters where normal application security rules apply.

## Future grammar direction

Potential future additions should remain declarative: typed event schemas, provenance/experiment blocks, deterministic conditionals, versioned module imports, static validation, and compiler/AST output. Arbitrary code execution should not be added merely for convenience; Python already exists as the host language.
