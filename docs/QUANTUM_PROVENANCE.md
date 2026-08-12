# Quantum Provenance Manual

## Core rule

**Quantum provenance and quantum advantage are different questions.**

CST Libraries stores provider/backend/job/result metadata so an experiment can establish where a measurement record came from. It does not infer that the source improves model quality.

## `QuantumMeasurement`

```python
from cstlib import QuantumMeasurement
measurement = QuantumMeasurement(provider="IBM", backend="backend-name", counts={"00":501,"11":523}, hardware=True, job_id="provider-job-id")
```

Fields include provider, backend, counts, hardware (`True`, `False`, or `None`), job_id, timestamp, and metadata. `receipt()` hashes canonical serialized content.

## Provider adapters

IBM:

```python
measurement = IBMCountsAdapter.measurement(counts, backend=backend_name, job_id=job_id, hardware=True)
```

Azure:

```python
measurement = AzureResultsAdapter.measurement(results, target=target_name, job_id=job_id, hardware=False)
```

CST deliberately accepts results after execution instead of owning cloud authentication/submission. Set `hardware` from provider metadata; never infer hardware from a brand name.

## Archive

```python
from cstlib import MeasurementArchive
archive = MeasurementArchive("quantum/measurements.jsonl")
archive.append(measurement)
```

Archive files are append-only by convention. Version or hash them before training.

## Deterministic derivation

```python
from cstlib import MeasurementEntropy
packet = MeasurementEntropy(measurement).sample(32)
```

This expands the canonical measurement record through counter-mode SHA-256 for reproducible seed derivation. It is not described as preserving every bit of physical entropy in the original experiment.

## Matched controls

A defensible experiment compares quantum-measurement-derived and high-quality classical random seeds under identical architecture, data, and training protocol, with multiple seeds and a pre-declared metric. If the quantum arm does not beat the control under the declared criterion, record a null result.

## Hardware/simulator labeling

```text
hardware=True   verified physical QPU execution
hardware=False  simulator/emulator/local primitive
hardware=None   insufficient provenance to decide
```

Never convert `None` to `True` merely because a record mentions a quantum provider.
