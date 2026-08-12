"""Adapters that turn application-owned sensor readers into CST events."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable
from cstlib.core import Event
from cstlib.sensory import LumaMotionTracker, audio_summary
@dataclass
class AudioReaderAdapter:
    reader:Callable[[],bytes|Iterable[float|int]];sample_rate:int=16000;pcm16:bool=False;name:str="audio";samples:int=0;failures:int=0
    def sample(self)->Event:
        try:
            summary=audio_summary(self.reader(),sample_rate=self.sample_rate,pcm16=self.pcm16);self.samples+=1;return Event(self.name,"sensor.audio",summary.to_dict(),tags=["sensor","audio"])
        except Exception:self.failures+=1;raise
    def health(self)->dict[str,object]:return {"name":self.name,"ok":self.failures==0,"samples":self.samples,"failures":self.failures,"sample_rate":self.sample_rate}
class LumaReaderAdapter:
    def __init__(self,reader:Callable[[],Iterable[float|int]],*,name:str="vision")->None:self.reader=reader;self.name=name;self.tracker=LumaMotionTracker();self.samples=0;self.failures=0
    def sample(self)->Event:
        try:
            summary=self.tracker.summarize(self.reader());self.samples+=1;return Event(self.name,"sensor.vision",summary.to_dict(),tags=["sensor","vision"])
        except Exception:self.failures+=1;raise
    def health(self)->dict[str,object]:return {"name":self.name,"ok":self.failures==0,"samples":self.samples,"failures":self.failures}
