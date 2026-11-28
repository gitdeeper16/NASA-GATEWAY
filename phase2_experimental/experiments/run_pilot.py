"""
Phase II — Pilot runner.

Reads seeds_pilot.txt and scenarios/S{1..5}.yaml, runs 5 scenarios × 2
conditions × 20 seeds = 200 runs, writes results/pilot/{scenario}_{condition}.jsonl.

Pilot outputs are DESCRIPTIVE ONLY. They are not used for hypothesis
testing (H1–H4). They are used to:
  - confirm the model is not trivially safe or trivially unsafe;
  - calibrate fault magnitudes (if needed, via a dated amendment);
  - confirm determinism (already covered by H6 test).

See PREREGISTRATION.md §5.1 and §5.3.
"""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.engine import run_scenario


def read_seeds(path: Path) -> list[int]:
    seeds = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        seeds.append(int(line))
    return seeds


def main() -> int:
    seeds_file = ROOT / "experiments" / "seeds_pilot.txt"
    seeds = read_seeds(seeds_file)
    if len(seeds) != 20:
        print(f"❌ expected 20 pilot seeds, got {len(seeds)}", file=sys.stderr)
        return 1

    out_dir = ROOT / "results" / "pilot"
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [f"S{i}" for i in range(1, 6)]
    conditions = ["treatment", "control"]

    total_runs = 0
    for sid in scenarios:
        scenario_path = ROOT / "scenarios" / f"{sid}.yaml"
        scenario = yaml.safe_load(scenario_path.read_text())
        for cond in conditions:
            out_path = out_dir / f"{sid}_{cond}.jsonl"
            with out_path.open("w") as f:
                for seed in seeds:
                    trace = run_scenario(scenario, seed, cond)
                    # Strip the free-text events list to keep the JSONL
                    # compact and machine-readable; events are only for
                    # debugging and are reproducible from (scenario, seed, cond).
                    trace_out = {k: v for k, v in trace.items() if k != "events"}
                    f.write(json.dumps(trace_out, ensure_ascii=False) + "\n")
                    total_runs += 1
            print(f"  {sid}/{cond}: {len(seeds)} runs -> {out_path.name}")

    print(f"\n✅ pilot complete: {total_runs} runs across {len(scenarios)}×{len(conditions)} files")
    print(f"   results in {out_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
