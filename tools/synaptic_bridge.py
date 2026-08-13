#!/usr/bin/env python3
"""Language-neutral JSON-lines bridge for the CST Synaptic Function v1."""
from __future__ import annotations
import json
import sys
from cstlib.synaptic import affinity_matrix, gated_blend, gaussian_affinity, state_step


def dispatch(request: dict) -> dict:
    op = request.get("op")
    if op == "affinity":
        return {"ok": True, "value": gaussian_affinity(request["a"], request["b"], request.get("sigma", 1.0))}
    if op == "matrix":
        return {"ok": True, "value": affinity_matrix(request["states"], request.get("sigma", 1.0))}
    if op == "blend":
        return {"ok": True, "value": gated_blend(request["standard"], request["affinity"], request["gate"])}
    if op == "step":
        return {"ok": True, "value": state_step(request["state"], request["signal"], decay=request.get("decay", 0.92), gain=request.get("gain", 1.0), dt=request.get("dt", 1.0))}
    raise ValueError(f"unsupported op: {op!r}")


def main() -> int:
    for raw in sys.stdin:
        if not raw.strip():
            continue
        try:
            response = dispatch(json.loads(raw))
        except Exception as exc:
            response = {"ok": False, "error": str(exc)}
        print(json.dumps(response, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
