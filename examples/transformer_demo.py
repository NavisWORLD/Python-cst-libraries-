import torch
from cstlib.transformer import MixtureOfStatesAttention
layer=MixtureOfStatesAttention(32,4,bandwidth="auto");hidden=torch.randn(2,8,32);state=torch.randn(2,8,12);out,diagnostics=layer(hidden,state,return_diagnostics=True);print(out.shape);print({k:float(v) for k,v in diagnostics.items()})
