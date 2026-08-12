"""Dependency-free JSON HTTP helpers for local and remote adapters."""
from __future__ import annotations
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from .base import AdapterError

def post_json(url: str, payload: dict[str, object], *, timeout: float = 60.0, headers: dict[str, str] | None = None) -> dict[str, object]:
    body=json.dumps(payload).encode("utf-8"); request_headers={"Content-Type":"application/json","Accept":"application/json"}
    if headers:request_headers.update(headers)
    req=Request(url,data=body,headers=request_headers,method="POST")
    try:
        with urlopen(req,timeout=timeout) as response:raw=response.read().decode("utf-8")
    except HTTPError as exc:
        detail=exc.read().decode("utf-8",errors="replace");raise AdapterError(f"HTTP {exc.code} from {url}: {detail[:500]}") from exc
    except URLError as exc:raise AdapterError(f"unable to reach {url}: {exc.reason}") from exc
    try:value=json.loads(raw)
    except json.JSONDecodeError as exc:raise AdapterError(f"non-JSON response from {url}") from exc
    if not isinstance(value,dict):raise AdapterError(f"expected JSON object from {url}")
    return value

def get_json(url: str, *, timeout: float = 10.0, headers: dict[str, str] | None = None) -> dict[str, object]:
    request_headers={"Accept":"application/json"}
    if headers:request_headers.update(headers)
    req=Request(url,headers=request_headers,method="GET")
    try:
        with urlopen(req,timeout=timeout) as response:raw=response.read().decode("utf-8")
    except Exception as exc:raise AdapterError(f"unable to reach {url}: {exc}") from exc
    value=json.loads(raw)
    if not isinstance(value,dict):raise AdapterError(f"expected JSON object from {url}")
    return value
