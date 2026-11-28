"""Phase 2 diagnostic: trace S1/S2/S5 per seed per condition. READ-ONLY."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import yaml
from model.engine import run_scenario

SEEDS = [382857, 1203392, 1344673, 2149014, 2273391]
SCENARIOS = ["S1", "S2", "S5"]
CONDITIONS = ["treatment", "control"]

for sid in SCENARIOS:
    scen = yaml.safe_load(Path(f"scenarios/{sid}.yaml").read_text())
    for cond in CONDITIONS:
        for seed in SEEDS:
            r = run_scenario(scen, seed, cond)
            print(f"{sid},{cond},{seed},"
                  f"att={r['local_recovery_attempts']},"
                  f"guard={r['treatment_escalations_due_to_guard']},"
                  f"sv={r['safety_violations']},"
                  f"cand={r['candidate_violations_count']},"
                  f"esc={r['escalations_total']},"
                  f"vsm_ack={r['vsm_acknowledged']},"
                  f"contain={r['containment_effective']},"
                  f"2nd={r['secondary_damage']},"
                  f"safe={r['safe_mode_reached']},"
                  f"avail={r['available_capacity_final']},"
                  f"req={r['required_recovery_capacity']}")
