"""Summary across seeds for a scenario. READ-ONLY."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import yaml
from model.engine import run_scenario

def load_seeds(path, n=5):
    seeds = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            seeds.append(int(line))
    return seeds[:n]

def summarize(sid, seed, cond):
    scen = yaml.safe_load(Path(f"scenarios/{sid}.yaml").read_text())
    r = run_scenario(scen, seed, cond)
    return {
        "sid": sid, "seed": seed, "cond": cond,
        "attempts": r.get("local_recovery_attempts", "?"),
        "guard": r.get("treatment_escalations_due_to_guard", "?"),
        "sv": r.get("safety_violations", "?"),
        "cand_final": r.get("candidate_would_violate_final", "?"),
        "cand_count": r.get("candidate_violations_count", "?"),
        "esc_total": r.get("escalations_total", "?"),
        "exec_log": len(r.get("executed_violation_log", [])),
    }

if __name__ == "__main__":
    seeds = load_seeds("experiments/seeds_pilot_bis.txt", n=5)
    print(f"pilot seeds (first 5): {seeds}\n")
    for sid in ("S3",):
        print(f"\n=== {sid} ===")
        print(f"{'seed':>4} | {'cond':>9} | {'att':>3} {'guard':>5} {'sv':>3} "
              f"{'cand_final':>10} {'cand_count':>10} {'esc':>3} {'exec_log':>8}")
        print("-" * 75)
        for cond in ("control", "treatment"):
            for seed in seeds:
                s = summarize(sid, seed, cond)
                print(f"{s['seed']:>4} | {s['cond']:>9} | {s['attempts']:>3} "
                      f"{s['guard']:>5} {s['sv']:>3} {s['cand_final']:>10} "
                      f"{s['cand_count']:>10} {s['esc_total']:>3} {s['exec_log']:>8}")
