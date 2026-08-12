"""Optional PyTorch Mixture-of-States transformer components."""
from __future__ import annotations
import math
from typing import Any
PHI=(1+5**0.5)/2

def torch_available()->bool:
    try: import torch
    except ImportError:return False
    return True
try:
    import torch
    from torch import nn
except ImportError:
    torch=None;nn=None
if nn is not None:
    class MixtureOfStatesAttention(nn.Module):
        def __init__(self,embed_dim:int,num_heads:int,*,dropout:float=0.0,bandwidth:float|str="auto",gate_init:float=-2.0)->None:
            super().__init__()
            if embed_dim%num_heads:raise ValueError("embed_dim must be divisible by num_heads")
            if isinstance(bandwidth,(int,float)) and bandwidth<=0:raise ValueError("bandwidth must be positive")
            if isinstance(bandwidth,str) and bandwidth!="auto":raise ValueError("bandwidth must be positive float or 'auto'")
            self.embed_dim=embed_dim;self.num_heads=num_heads;self.head_dim=embed_dim//num_heads;self.bandwidth=bandwidth
            self.q_proj=nn.Linear(embed_dim,embed_dim);self.k_proj=nn.Linear(embed_dim,embed_dim);self.v_proj=nn.Linear(embed_dim,embed_dim);self.out_proj=nn.Linear(embed_dim,embed_dim);self.gate_logit=nn.Parameter(torch.tensor(float(gate_init)));self.dropout=nn.Dropout(dropout)
        def _split(self,x):
            b,l,_=x.shape;return x.view(b,l,self.num_heads,self.head_dim).transpose(1,2)
        def _state_kernel(self,state):
            distances=torch.cdist(state,state,p=2)
            if self.bandwidth=="auto":
                with torch.no_grad():
                    positive=distances[distances>0];sigma=positive.median() if positive.numel() else torch.tensor(1.0,device=state.device,dtype=state.dtype)
                sigma=sigma.clamp_min(torch.finfo(state.dtype).eps)
            else:sigma=torch.as_tensor(float(self.bandwidth),device=state.device,dtype=state.dtype)
            kernel=torch.exp(-(distances**2)/(2*sigma**2));kernel=kernel/kernel.sum(dim=-1,keepdim=True).clamp_min(torch.finfo(kernel.dtype).eps);return kernel,sigma
        def forward(self,hidden,state,*,causal:bool=True,attention_mask=None,return_diagnostics:bool=False):
            if hidden.ndim!=3 or state.ndim!=3:raise ValueError("hidden and state must be [batch, seq, dim]")
            if hidden.shape[:2]!=state.shape[:2]:raise ValueError("hidden/state batch and sequence dimensions must match")
            q=self._split(self.q_proj(hidden));k=self._split(self.k_proj(hidden));v=self._split(self.v_proj(hidden));logits=(q@k.transpose(-2,-1))/math.sqrt(self.head_dim);l=hidden.shape[1]
            if causal:
                mask=torch.ones((l,l),device=hidden.device,dtype=torch.bool).triu(1);logits=logits.masked_fill(mask,float("-inf"))
            if attention_mask is not None:logits=logits+attention_mask
            standard=torch.softmax(logits,dim=-1);kernel,sigma=self._state_kernel(state)
            if causal:
                visible=torch.ones((l,l),device=hidden.device,dtype=kernel.dtype).tril();kernel=kernel*visible;kernel=kernel/kernel.sum(dim=-1,keepdim=True).clamp_min(torch.finfo(kernel.dtype).eps)
            kernel_h=kernel.unsqueeze(1).expand(-1,self.num_heads,-1,-1);gate=torch.sigmoid(self.gate_logit);mixed=self.dropout((1-gate)*standard+gate*kernel_h);out=mixed@v;out=out.transpose(1,2).contiguous().view(hidden.shape[0],l,self.embed_dim);out=self.out_proj(out)
            if return_diagnostics:
                diag={"gate":gate.detach(),"sigma":sigma.detach(),"state_kernel_variance":kernel.var().detach(),"standard_entropy":(-(standard.clamp_min(1e-12).log()*standard).sum(-1).mean()).detach()};return out,diag
            return out
    class PhiFeedForward(nn.Module):
        def __init__(self,embed_dim:int,*,multiplier:float=PHI,dropout:float=0.0)->None:
            super().__init__();hidden=max(1,int(math.floor(embed_dim*multiplier)));self.net=nn.Sequential(nn.Linear(embed_dim,hidden),nn.GELU(),nn.Dropout(dropout),nn.Linear(hidden,embed_dim))
        def forward(self,x):return self.net(x)
    class CSTTransformerBlock(nn.Module):
        def __init__(self,embed_dim:int,num_heads:int,*,dropout:float=0.0,bandwidth:float|str="auto")->None:
            super().__init__();self.norm1=nn.RMSNorm(embed_dim);self.attn=MixtureOfStatesAttention(embed_dim,num_heads,dropout=dropout,bandwidth=bandwidth);self.norm2=nn.RMSNorm(embed_dim);self.ff=PhiFeedForward(embed_dim,dropout=dropout)
        def forward(self,hidden,state,*,causal:bool=True):
            hidden=hidden+self.attn(self.norm1(hidden),state,causal=causal);return hidden+self.ff(self.norm2(hidden))
else:
    class _TorchMissing:
        def __init__(self,*args:Any,**kwargs:Any)->None:raise ImportError("PyTorch is optional. Install cst-libraries[torch] to use transformer components.")
    MixtureOfStatesAttention=_TorchMissing;PhiFeedForward=_TorchMissing;CSTTransformerBlock=_TorchMissing
