"""Command-line interface for CST libraries and CST-L."""
import argparse
import json
from pathlib import Path
from . import __version__
from .lang import load
from .runtime import Runtime

def cmd_doctor(_args: argparse.Namespace) -> int:
    runtime = Runtime()
    print(json.dumps({"version": __version__, "python_core": "ok", "health": runtime.health()}, indent=2))
    return 0

def cmd_run(args: argparse.Namespace) -> int:
    program = load(args.file)
    if args.message is not None:
        print(program.run("message", args.message))
        return 0
    print(f"CST-L {__version__} interactive mode. Ctrl-D/Ctrl-C to exit.")
    try:
        while True:
            message = input("cst> ")
            output = program.run("message", message)
            if output:
                print(output)
    except (EOFError, KeyboardInterrupt):
        print()
    return 0

def cmd_demo(_args: argparse.Namespace) -> int:
    runtime = Runtime.local(Path(".cst-demo"))
    print(runtime.respond("hello from the CST runtime"))
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cst", description="CST/COSMOS computational libraries")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor", help="check the Python core")
    doctor.set_defaults(func=cmd_doctor)
    run = sub.add_parser("run", help="run a CST-L program")
    run.add_argument("file")
    run.add_argument("--message")
    run.set_defaults(func=cmd_run)
    demo = sub.add_parser("demo", help="run the reference runtime")
    demo.set_defaults(func=cmd_demo)
    return parser

def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))

if __name__ == "__main__":
    raise SystemExit(main())
