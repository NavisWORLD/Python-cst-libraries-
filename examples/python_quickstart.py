from cstlib import Dyn12, GaussianSynapse, HebbianMemory, SemanticMemory

state = Dyn12()
memory = SemanticMemory()
hebb = HebbianMemory()

history = []
for message in ["music follows rhythm", "rhythm follows motion", "memory follows meaning"]:
    history.append(state.update(message))
    memory.store(message)
    hebb.learn(message)

kernel = GaussianSynapse("median")
print("state:", state.vector())
print("affinity:", kernel.affinity(history))
print("recall:", [(r.text, round(score, 3)) for r, score in memory.recall("music rhythm")])
print("associations:", hebb.associated_with("rhythm"))
