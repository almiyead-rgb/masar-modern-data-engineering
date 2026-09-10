"""One entry point. No publishing, paid API, source deletion or fake engine output."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parent

def commands_for(action: str, day: int | None = None) -> list[list[str]]:
    python = sys.executable
    if action == "test":
        return [[python, "scripts/check_repository.py"],
                [python, "-m", "unittest", "discover", "-s", "tests", "-q"]]
    if action == "demo":
        return [[python, "scripts/demo_project.py"]]
    if action == "run":
        return [[python, "scripts/run_student_notebook.py"]]
    if action == "start":
        return [[python, "scripts/workbench.py", "prepare"],
                [python, "scripts/workbench.py", "start"],
                ["docker", "compose", "--project-name", "masar-training", "-f",
                 str(ROOT / "infrastructure/runtime/compose.yaml"),
                 "logs", "--tail", "30", "workbench"]]
    if action == "stop":
        return [[python, "scripts/workbench.py", "stop"]]
    if action == "day" and day in range(1, 6):
        result = [[python, f"scripts/run_day{day:02d}.py"]]
        if day == 2:
            result.append([python, "scripts/run_dbt.py"])
        return result
    raise ValueError("Choose demo, test, start, stop, run, or day 1..5.")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        epilog="demo = reference calculations, not Spark/Delta; run = actual eight-lab notebook.")
    parser.add_argument("action", nargs="?", choices=["demo", "test", "start", "stop", "run", "day"])
    parser.add_argument("day", nargs="?", type=int, choices=range(1, 6))
    args = parser.parse_args(argv)
    if args.action is None:
        parser.print_help(); return 0
    if (args.action == "day") != (args.day is not None):
        parser.error("A day number is used only with: day 1..5")
    for command in commands_for(args.action, args.day):
        print("\n> " + " ".join(command), flush=True)
        try:
            result = subprocess.run(command, cwd=ROOT, check=False)
        except (OSError, KeyboardInterrupt) as exc:
            print(f"Stopped: {exc}", file=sys.stderr)
            return 130 if isinstance(exc, KeyboardInterrupt) else 2
        if result.returncode:
            return result.returncode
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
