import math
from cstlib import Runtime,SensorHub
from cstlib.adapters import AudioReaderAdapter,CallableModelAdapter,LumaReaderAdapter
phase={"n":0}
def audio_reader():phase["n"]+=1;return [math.sin(2*math.pi*220*i/8000) for i in range(128)]
frames=iter([[0,0,64,255],[255,64,0,0]]);hub=SensorHub();hub.register(AudioReaderAdapter(audio_reader,sample_rate=8000));hub.register(LumaReaderAdapter(lambda:next(frames)));model=CallableModelAdapter(lambda message,context:f"{message}\nsensors={context['sensors']}");runtime=Runtime(sensors=hub,model=model);print(runtime.respond("first sensor frame"));print(runtime.respond("second sensor frame"))
