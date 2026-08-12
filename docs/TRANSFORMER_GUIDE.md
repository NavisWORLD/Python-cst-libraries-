# Mixture-of-States Transformer Guide

## Purpose

`cstlib.transformer` provides an optional PyTorch implementation of the project's state-conditioned attention mechanism.

## Mathematical form

Standard causal attention per head:

```text
A_standard = softmax(QK^T / sqrt(d_h))
```

For token state vectors `x_i`, CST builds:

```text
H_ij = exp(-||x_i - x_j||^2 / (2 sigma^2))
```

`H` is row-normalized. The final attention matrix is:

```text
A_final = (1 - g) A_standard + g H
```

where `g = sigmoid(gate_logit)`.

## Usage

```python
import torch
from cstlib.transformer import MixtureOfStatesAttention
layer = MixtureOfStatesAttention(embed_dim=256, num_heads=8, bandwidth="auto")
hidden = torch.randn(4, 128, 256)
state = torch.randn(4, 128, 12)
output, diagnostics = layer(hidden, state, causal=True, return_diagnostics=True)
```

## Auto bandwidth

`bandwidth="auto"` uses the median positive pairwise state distance for the current batch as a detached calibration value. Production research should record sigma values and test sensitivity rather than assuming auto calibration is universally optimal.

## Diagnostics

Returned diagnostics include learned gate value, calibrated sigma, state-kernel variance, and standard-attention entropy. The project-level preflight principle still applies: confirm state variance, kernel non-degeneracy, and gate gradients before interpreting task loss.

## `CSTTransformerBlock`

The optional block combines RMSNorm, Mixture-of-States attention, residual connection, RMSNorm, phi-width feed-forward network, and another residual connection.

```python
from cstlib.transformer import CSTTransformerBlock
block = CSTTransformerBlock(256, 8)
```

The phi feed-forward width is an architectural hypothesis/configuration, not a universal constant claim.

## Performance notes

The reference implementation prioritizes inspectability. It uses explicit Q/K/V projections and attention matrices so the state mixture can be measured. Production kernels may require optimized fused implementations.

## Masking

The reference layer supports causal masking and an additive attention mask. If you add padding-mask support, create explicit tests for shape broadcasting and verify that the state kernel is masked identically to standard attention.
