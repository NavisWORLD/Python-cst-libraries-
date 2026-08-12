from cstlib import Dyn12, EventBus, GaussianSynapse, HebbianMemory, SemanticMemory
state=Dyn12();memory=SemanticMemory(".cst/memory.jsonl");hebb=HebbianMemory(".cst/links.json");bus=EventBus();bus.subscribe("demo",lambda event:print("EVENT",event.payload));history=[]
for message in ["music follows rhythm","rhythm follows motion","memory follows meaning"]:
    history.append(state.update(message));memory.store(message);hebb.learn(message);bus.publish("example","demo",{"message":message})
kernel=GaussianSynapse("median");print(kernel.affinity(history));print(memory.recall("music and rhythm"));print(hebb.associated_with("rhythm"))
