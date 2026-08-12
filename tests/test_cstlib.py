from pathlib import Path

from cstlib import Dyn12, GaussianSynapse, HebbianMemory, Lorenz, SemanticMemory, check_preflight
from cstlib.lang import parse


def test_dyn12_persists_state():
    state = Dyn12(decay=0.5)
    a = state.update([1.0])
    b = state.update([0.0])
    assert len(a) == 12
    assert len(b) == 12
    assert state.updates == 2
    assert abs(b[0]) > 0.0


def test_synapse_auto_bandwidth():
    states = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
    kernel = GaussianSynapse("median")
    h = kernel.affinity(states)
    assert h[0][0] == 1.0
    assert 0.0 < h[0][1] < 1.0
    assert kernel.diagnostics(states).bandwidth > 0.0


def test_memory_and_hebbian(tmp_path: Path):
    memory = SemanticMemory(tmp_path / "memory.jsonl")
    memory.store("the red guitar lives in the studio", salience=1.0)
    memory.store("bananas are yellow")
    recalled = memory.recall("where is the guitar?", limit=1)
    assert recalled[0][0].text == "the red guitar lives in the studio"
    hebb = HebbianMemory(tmp_path / "hebb.json", learning_rate=0.5)
    hebb.learn(["guitar", "music", "stage"])
    assert hebb.associated_with("guitar")[0][0] in {"music", "stage"}


def test_lorenz_moves():
    system = Lorenz()
    before = system.snapshot()
    system.step()
    assert system.snapshot() != before


def test_preflight_detects_live_kernel():
    states = [[0.0, 0.0], [1.0, 0.5], [0.2, 1.0]]
    h = GaussianSynapse("median").affinity(states)
    report = check_preflight([0.0, 1.0, 2.0], states, h, gate_gradient=0.1)
    assert report.passed


def test_cst_language_executes(tmp_path: Path):
    source = """
    state mind dyn12 decay=0.8
    memory life path=memory.jsonl
    hebbian links path=links.json
    loop message
      recall life as remembered
      evolve mind
      associate links
      store life
      emit "message={message} memory={remembered} state={state.mind}"
    end
    """
    program = parse(source, base_dir=tmp_path)
    first = program.run("message", "alpha beta")
    second = program.run("message", "alpha again")
    assert "message=alpha beta" in first
    assert "alpha beta" in second
    assert (tmp_path / "memory.jsonl").exists()
