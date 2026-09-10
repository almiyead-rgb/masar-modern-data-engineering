"""Run the verified inspect_sources helper from any working directory."""
from pathlib import Path
import argparse, json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.sources import profile_sources
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional JSON output; an existing file is never overwritten")
    args = parser.parse_args()
    result = profile_sources(ROOT / "data" / "masar-small-v1")
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    print(payload)
if __name__ == "__main__":
    main()
