#!/usr/bin/env python3
"""
phase2ter_trace_seeded.py
Phase II-ter — إعادة إنتاج منطق _trace_scenario.py مع بذرة عشوائية حقيقية.
READ-ONLY على المشروع: لا يُعدّل أي ملف.
"""

import json
import random
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import yaml

from model.engine import (
    _build_initial_state,
    _update_state,
    _iter_faults,
    _apply_primary_fault,
    _propagate_secondary,
    _vsm_acknowledge,
    _vsm_attempt_containment,
    _choose_decision,
    _execute_local_action,
    _check_consistency,
    _record_escalation_correctness,
    would_violate,
    MAX_CYCLES,
)

SEEDS = [382857, 1203392, 1344673, 2149014, 2273391]
SCENARIOS = ["S1", "S2", "S5"]
CONDITIONS = ["treatment", "control"]

EXTRA_STATE_FIELDS = [
    "escalation_requested_at",
    "vsm_acknowledged_at",
    "containment_effective_at",
    "secondary_damage_at",
    "events",
    "executed_violation_log",
    "escalations_correct",
    "escalations_false",
    "escalations_missed",
    "candidate_violations_count",
    "local_recovery_failures",
]


def trace_one(scenario_id, condition, seed, out_fh, log_fh):
    scen = yaml.safe_load(Path(f"scenarios/{scenario_id}.yaml").read_text())

    header = f"\n{'='*120}\n{scenario_id} | condition={condition} | seed={seed}\n{'='*120}"
    print(header, file=log_fh)

    state = _build_initial_state(scen)
    faults = _iter_faults(scen)
    fbc = {}
    for f in faults:
        fbc.setdefault(f["at_cycle"], []).append(f)
    if not faults:
        print("NO FAULTS", file=log_fh)
        return

    ff = faults[0]
    ff_at = ff["at_cycle"]
    ff_until = ff.get("persist_until", MAX_CYCLES)

    rng = random.Random(seed)

    per_cycle = []

    for cycle in range(MAX_CYCLES):
        state.cycle = cycle

        if state.escalation_requested and not state.vsm_acknowledged:
            _vsm_acknowledge(state)
        if state.vsm_acknowledged and not state.containment_effective:
            _vsm_attempt_containment(state)

        for _f in fbc.get(cycle, ()):
            _apply_primary_fault(state, _f, rng)

        if cycle > ff_at and cycle <= ff_until:
            _propagate_secondary(state, ff, rng)

        _update_state(state, scen)

        path_avail = (
            state.pending_local_action is not None
            and not any(not r.healthy for r in state.shared_resources.values())
        )

        if state.pending_local_action is not None:
            cv, cr = would_violate(state.pending_local_action, state)
            state.candidate_would_violate = cv
        else:
            state.candidate_would_violate = False

        if state.candidate_would_violate:
            state.candidate_violations_count += 1

        decision = _choose_decision(state, scen, condition, path_avail)

        if decision.kind == "escalate":
            state.escalation_requested = True
            state.escalations_total += 1
            _record_escalation_correctness(state, decision, scen)
        elif decision.kind == "resolve_local":
            state.local_recovery_attempts += 1
            v, r = would_violate(decision.action_name, state)
            if v:
                state.safety_violations += 1
                state.executed_violation_log.append(
                    {"cycle": cycle, "action": decision.action_name, "reason": r}
                )
            _execute_local_action(state, decision.action_name)
        elif decision.kind == "safe_mode":
            state.safe_mode_reached = True

        _check_consistency(state, decision)

        snap = {
            "scenario": scenario_id,
            "condition": condition,
            "seed": seed,
            "cycle": cycle,
            "C1_healthy": state.components["C1"].healthy,
            "C2_healthy": state.components["C2"].healthy,
            "C3_healthy": (len(state.components) >= 3 and state.components["C3"].healthy),
            "available_capacity": state.available_capacity,
            "required_recovery_capacity": state.required_recovery_capacity,
            "decision": decision.kind,
            "rule": decision.rule,
            "escalation_requested": getattr(state, "escalation_requested", None),
            "vsm_acknowledged": getattr(state, "vsm_acknowledged", None),
            "containment_effective": getattr(state, "containment_effective", None),
        }
        for fld in EXTRA_STATE_FIELDS:
            snap[fld] = getattr(state, fld, "MISSING")
        per_cycle.append(snap)

        print(
            f"cyc={cycle:>3} C1={int(state.components['C1'].healthy)} "
            f"C2={int(state.components['C2'].healthy)} "
            f"esc={getattr(state,'escalation_requested',0)} "
            f"ack={getattr(state,'vsm_acknowledged',0)} "
            f"contain={getattr(state,'containment_effective',0)} "
            f"dec={decision.kind}",
            file=log_fh,
        )

    for snap in per_cycle:
        out_fh.write(json.dumps(snap, ensure_ascii=False, default=str) + "\n")

    print(
        f"\nFinal seed={seed} cond={condition}: "
        f"attempts={state.local_recovery_attempts} "
        f"failures={state.local_recovery_failures} "
        f"guard={state.treatment_escalations_due_to_guard} "
        f"sv={state.safety_violations} "
        f"esc={state.escalations_total} "
        f"cand={state.candidate_violations_count}",
        file=log_fh,
    )


def main():
    out_path = Path("phase2ter_trace.jsonl")
    log_path = Path("phase2ter_trace.log")

    with open(out_path, "w", encoding="utf-8") as out_fh, \
         open(log_path, "w", encoding="utf-8") as log_fh:
        for scenario in SCENARIOS:
            for condition in CONDITIONS:
                for seed in SEEDS:
                    try:
                        trace_one(scenario, condition, seed, out_fh, log_fh)
                    except Exception as e:
                        print(
                            f"[ERROR] scenario={scenario} cond={condition} seed={seed}: "
                            f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
                            file=sys.stderr,
                        )
                        log_fh.write(
                            f"[ERROR] scenario={scenario} cond={condition} seed={seed}: "
                            f"{type(e).__name__}: {e}\n"
                        )

    print(f"[OK] wrote {out_path} and {log_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
