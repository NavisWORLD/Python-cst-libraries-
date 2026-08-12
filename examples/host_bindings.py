from pathlib import Path
from cstlib import SystemEntropy
from cstlib.adapters import AudioReaderAdapter,CallableModelAdapter
from cstlib.lang import load
program=load(Path(__file__).with_name("external_adapters.cst"));program.bind_model("local",CallableModelAdapter(lambda message,context:"local answer: "+message));program.bind_sensor("mic",AudioReaderAdapter(lambda:[0.0,0.1,-0.1,0.2]));program.bind_entropy("q",SystemEntropy());print(program.run("message","hello from host bindings"))
