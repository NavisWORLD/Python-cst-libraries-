# Security and Privacy Guide

## Default boundaries

CST Libraries is designed around summaries and explicit host adapters. The library should not automatically persist microphone waveforms, camera frames, passwords, API tokens, private keys, cloud credentials, or raw health/biometric streams.

## Sensory data

`AudioReaderAdapter` and `LumaReaderAdapter` convert application-owned buffers into numeric summaries. The CST adapter does not write the raw buffer to disk. If your host records raw media, document and obtain consent for that policy separately.

## Model context

The Ollama model adapter excludes context keys named `raw_audio`, `raw_video`, `credentials`, and `secrets`. Do not rely only on those names; the host should avoid putting secrets in runtime context in the first place.

## CST-L

CST-L source files should be shareable. They contain external adapter placeholders instead of credentials. Do not add tokens to `.cst` source.

## Quantum credentials

Cloud authentication belongs to IBM/Azure SDK configuration controlled by the host. CST receives result records after execution.

## Persistent memory

Memory JSONL can contain personal text. Treat `.cst/` as private application data unless explicitly sanitized for publication. For public research, prefer schemas, hashes, aggregate metrics, synthetic fixtures, and redacted text while retaining provenance locally.

## Untrusted model output

Model output is text, not authority. Do not execute it as shell commands or source code without a separate, explicit action/sandbox layer.

## Network adapters

`JSONTextAdapter`, `OllamaChatAdapter`, and `OllamaEmbeddingAdapter` send data to the configured URL. Use localhost by default for private workloads and review any remote endpoint before enabling it.
