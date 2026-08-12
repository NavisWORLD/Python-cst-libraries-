from cstlib import Runtime
from cstlib.adapters import OllamaChatAdapter,OllamaEmbeddingAdapter
from cstlib.memory import SemanticMemory
model=OllamaChatAdapter(model="qwen3");embed=OllamaEmbeddingAdapter(model="embeddinggemma");memory=SemanticMemory(".cst-ollama/memory.jsonl",embedder=embed);runtime=Runtime.local(".cst-ollama",model=model);runtime.memory=memory;print(model.probe());print(runtime.respond("Hello from the CST Ollama adapter."))
