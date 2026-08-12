"""Privacy-oriented numeric sensory summaries with no required media dependencies."""
from __future__ import annotations
import math
from dataclasses import asdict, dataclass
from typing import Iterable, Protocol, runtime_checkable
from .core import Event

@dataclass(slots=True)
class AudioSummary:
    rms: float; peak: float; mean_abs: float; zero_crossing_rate: float; spectral_centroid_hz: float; samples: int; sample_rate: int
    def to_dict(self) -> dict[str, object]: return asdict(self)
@dataclass(slots=True)
class VisionSummary:
    brightness: float; contrast: float; motion: float; samples: int
    def to_dict(self) -> dict[str, object]: return asdict(self)
@runtime_checkable
class Sensor(Protocol):
    name: str
    def sample(self) -> Event: ...
    def health(self) -> dict[str, object]: ...

def _normalized_samples(samples: bytes | Iterable[float | int], *, pcm16: bool = False) -> list[float]:
    if isinstance(samples, bytes):
        if len(samples) % 2: raise ValueError("PCM16 byte length must be even")
        return [int.from_bytes(samples[i:i+2], "little", signed=True) / 32768.0 for i in range(0, len(samples), 2)]
    values=[float(v) for v in samples]
    if pcm16: return [max(-1.0,min(1.0,v/32768.0)) for v in values]
    peak=max((abs(v) for v in values),default=0.0)
    if peak>1.5:
        scale=max(peak,32768.0); values=[v/scale for v in values]
    return [max(-1.0,min(1.0,v)) for v in values]

def audio_summary(samples: bytes | Iterable[float | int], *, sample_rate: int = 16000, pcm16: bool = False, fft_bins: int = 64) -> AudioSummary:
    if sample_rate<=0: raise ValueError("sample_rate must be positive")
    x=_normalized_samples(samples,pcm16=pcm16)
    if not x:return AudioSummary(0,0,0,0,0,0,sample_rate)
    rms=math.sqrt(sum(v*v for v in x)/len(x)); peak=max(abs(v) for v in x); mean_abs=sum(abs(v) for v in x)/len(x); zc=sum(1 for a,b in zip(x,x[1:]) if (a<0<=b) or (a>=0>b))/max(1,len(x)-1)
    n=min(len(x),max(16,fft_bins*2)); window=x[:n]; half=min(fft_bins,n//2); mags=[]
    for k in range(half):
        re=0.0; im=0.0
        for i,v in enumerate(window):
            angle=2*math.pi*k*i/n; re+=v*math.cos(angle); im-=v*math.sin(angle)
        mags.append(math.hypot(re,im))
    mag_sum=sum(mags); centroid=(sum((k*sample_rate/n)*m for k,m in enumerate(mags))/mag_sum) if mag_sum else 0.0
    return AudioSummary(rms,peak,mean_abs,zc,centroid,len(x),sample_rate)

class LumaMotionTracker:
    def __init__(self) -> None:self.previous:list[float]|None=None
    def summarize(self,pixels:Iterable[float|int])->VisionSummary:
        raw=[float(v) for v in pixels]
        if not raw:return VisionSummary(0,0,0,0)
        scale=255.0 if max(abs(v) for v in raw)>1.5 else 1.0; x=[max(0,min(1,v/scale)) for v in raw]; mean=sum(x)/len(x); contrast=math.sqrt(sum((v-mean)**2 for v in x)/len(x)); motion=0.0
        if self.previous is not None and len(self.previous)==len(x):motion=sum(abs(a-b) for a,b in zip(x,self.previous))/len(x)
        self.previous=x; return VisionSummary(mean,contrast,motion,len(x))

class SensorHub:
    def __init__(self)->None:self.sensors:dict[str,Sensor]={}
    def register(self,sensor:Sensor)->None:self.sensors[sensor.name]=sensor
    def sample(self)->dict[str,Event]:
        out={}
        for name,sensor in list(self.sensors.items()):
            try:out[name]=sensor.sample()
            except Exception as exc:out[name]=Event(name,"sensor.error",{"error":f"{type(exc).__name__}: {exc}"},confidence=0.0,tags=["sensor","error"])
        return out
    def health(self)->dict[str,object]:return {name:s.health() for name,s in self.sensors.items()}
