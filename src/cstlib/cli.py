"""Command-line interface for CST Libraries and CST-L."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from . import __version__
from .config import RuntimeConfig
from .lang import load
from .native import health as native_health
from .provenance import sha256_file
from .runtime import Runtime
from .transformer import torch_available
STARTER='''# CST-L 0.2 starter\nstate mind dyn12 decay=0.92\nmemory life path=.cst/memory.jsonl\nhebbian links path=.cst/links.json\n\nloop message\n  recall life as remembered\n  evolve mind\n  associate links\n  store life\n  snapshot mind as state_snapshot\n  emit "INPUT={message}"\n  emit "RECALLED={remembered}"\n  emit "STATE={state_snapshot}"\nend\n'''
def cmd_doctor(_args):
    runtime=Runtime();print(json.dumps({"version":__version__,"python_core":"ok","torch_optional":torch_available(),"native":native_health(),"health":runtime.health()},indent=2,default=str));return 0
def cmd_run(args):
    program=load(args.file)
    if args.message is not None:print(program.run("message",args.message));return 0
    print(f"CST-L {__version__} interactive mode. Ctrl-D/Ctrl-C to exit.")
    try:
        while True:
            message=input("cst> ");output=program.run("message",message)
            if output:print(output)
    except (EOFError,KeyboardInterrupt):print()
    return 0
def cmd_demo(_args):
    runtime=Runtime.local(Path(".cst-demo"));print(runtime.respond("hello from the CST runtime"));return 0
def cmd_inspect(args):print(json.dumps(load(args.file).inspect(),indent=2));return 0
def cmd_init(args):
    root=Path(args.directory);root.mkdir(parents=True,exist_ok=True);program=root/"main.cst";config=root/"cst.json"
    if program.exists() and not args.force:raise SystemExit(f"refusing to overwrite {program}; use --force")
    program.write_text(STARTER,encoding="utf-8");RuntimeConfig(root=str(root/".cst")).save(config);print(program);print(config);return 0
def cmd_hash(args):print(sha256_file(args.file));return 0
def cmd_adapters(_args):print(json.dumps({"model":["callable","json-http","ollama"],"embedding":["hashed","callable","ollama-embed"],"sensor":["audio-reader","luma-reader"],"entropy":["system","measurement","callback"],"quantum-results":["IBM-counts","Azure-results"],"native":["pybind11 optional"]},indent=2));return 0
def build_parser():
    parser=argparse.ArgumentParser(prog="cst",description="CST/COSMOS computational libraries");parser.add_argument("--version",action="version",version=__version__);sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("doctor");p.set_defaults(func=cmd_doctor);p=sub.add_parser("run");p.add_argument("file");p.add_argument("--message");p.set_defaults(func=cmd_run);p=sub.add_parser("inspect");p.add_argument("file");p.set_defaults(func=cmd_inspect);p=sub.add_parser("init");p.add_argument("directory",nargs="?",default="cst-project");p.add_argument("--force",action="store_true");p.set_defaults(func=cmd_init);p=sub.add_parser("hash");p.add_argument("file");p.set_defaults(func=cmd_hash);p=sub.add_parser("adapters");p.set_defaults(func=cmd_adapters);p=sub.add_parser("demo");p.set_defaults(func=cmd_demo);return parser
def main()->int:args=build_parser().parse_args();return int(args.func(args))
if __name__=="__main__":raise SystemExit(main())
