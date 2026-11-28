"""Phase II — CLI entry point.

Usage:
    python -m model.run --scenario scenarios/S1.yaml --seed 42 --condition treatment
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model.engine import run_scenario


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--seed", required=True, type=int)
    ap.add_argument("--condition", required=True, choices=["treatment", "control"])
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()

    scenario = yaml.safe_load(Path(args.scenario).read_text())
    trace = run_scenario(scenario, args.seed, args.condition)
    print(json.dumps(trace, indent=2 if args.pretty else None, ensure_ascii=False))


if __name__ == "__main__":
    main()
