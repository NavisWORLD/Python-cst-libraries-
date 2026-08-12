# CST Adapter Guide

## Adapter philosophy

CST core owns computation; adapters own integration. The host application is responsible for credentials, provider accounts, hardware access, and user consent.

## Model adapters

### Callable

```python
from cstlib.adapters import CallableModelAdapter
model = CallableModelAdapter(lambda message, context: f"echo: {message}")
```

### Ollama chat

```python
from cstlib.adapters import OllamaChatAdapter
model = OllamaChatAdapter(model="qwen3", base_url="http://localhost:11434", system_prompt="You are the local synthesis model.")
```

`include_cst_context=True` attaches structured CST telemetry in a system message. Keys named `raw_audio`, `raw_video`, `credentials`, or `secrets` are excluded by the built-in adapter.

### Generic JSON HTTP

```python
from cstlib.adapters import JSONTextAdapter
model = JSONTextAdapter(url="http://127.0.0.1:9000/generate", request_builder=lambda message, context: {"prompt": message, "state": context["state"]}, response_reader=lambda payload: payload["text"])
```

## Embedding adapters

`HashedEmbeddingAdapter` is the dependency-free baseline. `OllamaEmbeddingAdapter` targets a local Ollama embedding model. Always use the same embedding model for indexing and querying a given store.

## Sensory adapters

CST does not take ownership of cameras or microphones. Your application supplies reader callbacks. `AudioReaderAdapter` emits numeric RMS, peak, mean absolute amplitude, zero-crossing rate, and a bounded spectral-centroid estimate. `LumaReaderAdapter` accepts normalized or 0-255 luma arrays and emits brightness, contrast, and motion summaries.

## Entropy adapters

`SystemEntropy` provides OS CSPRNG bytes. `MeasurementEntropy` produces reproducible derived bytes from a provider-labelled measurement record. `CallbackEntropyAdapter` accepts an application-owned source. Measurement-derived bytes are documented as deterministic derivation, not as preserved physical entropy.

## IBM result adapter

```python
from cstlib.adapters import IBMCountsAdapter
measurement = IBMCountsAdapter.measurement(counts, backend=backend_name, job_id=job_id, hardware=True)
```

Cloud submission remains in the host application, keeping the persistent CST provenance schema independent of one Qiskit Runtime client version.

## Azure result adapter

```python
from cstlib.adapters import AzureResultsAdapter
measurement = AzureResultsAdapter.measurement(results, target=target_name, job_id=job_id, hardware=False)
```

Explicitly set `hardware` when known. Simulator records must never be re-labelled as hardware provenance.

## CNS organ adapters

```python
from cstlib import CNS
cns = CNS.standard()
cns.bind("plasticity", lambda event, context: {"reward": 0.2})
cns.bind("surgeon", lambda event, context: {"healthy": True})
```

Deferred organs remain visible in `cns.health()`.

## CST-L external bindings

CST-L source declares requirements:

```cst
model local external
sensor mic external
entropy q external
```

The host binds them:

```python
program.bind_model("local", model)
program.bind_sensor("mic", sensor)
program.bind_entropy("q", entropy)
```

This split keeps credentials, device handles, and arbitrary integration code outside shareable CST-L source.
