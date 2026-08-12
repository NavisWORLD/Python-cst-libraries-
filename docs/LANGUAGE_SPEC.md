# CST-L 0.1 Language Specification

CST-L is a small executable domain-specific language layered on top of the CST Python libraries. Version 0.1 deliberately uses line-oriented syntax so generated execution is inspectable.

## Declarations

```cst
state mind dyn12 decay=0.92
memory life path=.cst/memory.jsonl
hebbian links path=.cst/links.json
```

Supported state types: `dyn12`, `dyn42`, `dyn54`.

## Event loops

```cst
loop message
  recall life as remembered
  evolve mind
  associate links
  store life
  emit "message={message}"
  emit "state={state.mind}"
  emit "memory={remembered}"
end
```

`loop message` is executed by `cst run FILE --message TEXT` or by interactive mode.

## Instructions

- `recall MEMORY as NAME` — semantic recall using the incoming message as the query.
- `evolve STATE` — update a persistent dynamic state using the incoming message.
- `associate HEBBIAN` — learn co-occurring concepts in the incoming message.
- `store MEMORY` — append the incoming message to durable memory.
- `emit "TEXT"` — produce output with substitutions.

## Substitutions

- `{message}` — current message.
- `{state.NAME}` — current state vector.
- `{NAME}` — environment value, such as a recall alias.

## Philosophy

CST-L is not presented as a replacement for Python. It is a readable orchestration language for persistent state, memory, association and experimental computation. Features should compile or map to transparent Python mechanisms rather than hide them.
