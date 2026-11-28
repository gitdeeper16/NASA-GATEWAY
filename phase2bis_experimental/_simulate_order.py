"""SIMULATED ONLY. Do not treat results as observed. Does not modify project files.

Simulates the effect of order = ["R5","R1","R4","R2","R3"] and
["R5c","R1c","R4c","R2c","R3c"] on S3/S4 across seeds, by re-implementing
the loop locally with the new order. The original _choose_decision is NOT
modified; instead we implement a local copy with the new order.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import yaml, random
from model.engine import (
    _build_initial_state, _update_state, _iter_faults,
    _apply_primary_fault, _propagate_secondary,
    _vsm_acknowledge, _vsm_attempt_containment,
    _execute_local_action, _check_consistency,
    _record_escalation_correctness, would_violate, MAX_CYCLES,
    MSMAction, _build_rule_view,
)
from model.rules import TREATMENT_RULES, CONTROL_RULES, RULE_POLARITY, CONTROL_POLARITY


def _choose_decision_simulated(state, scenario, condition, path_avail):
    """Local copy of _choose_decision with new order. Does NOT modify the engine."""
    view = _build_rule_view(state, path_avail)
    if condition == "treatment":
        rules = TREATMENT_RULES
        polarity = RULE_POLARITY
        order = ["R5", "R1", "R4", "R2", "R3"]
    else:
        rules = CONTROL_RULES
        polarity = CONTROL_POLARITY
        order = ["R5c", "R1c", "R4c", "R2c", "R3c"]
    for rule_name in order:
        fn = rules[rule_name]
        if fn(view):
            kind = polarity[rule_name]
            action_name = "recover_local" if kind == "resolve_local" else None
            if condition == "treatment" and kind == "resolve_local":
                violated, _reason = would_violate(action_name, state)
                if violated:
                    state.treatment_escalations_due_to_guard += 1
                    return MSMAction(kind="escalate", rule=rule_name + "_guard", action_name=None)
            return MSMAction(kind=kind, rule=rule_name, action_name=action_name)
    return MSMAction(kind="noop")


def run_sim(scenario, seed, condition):
    state = _build_initial_state(scenario)
    faults = _iter_faults(scenario)
    fbc = {}
    for f in faults:
        fbc.setdefault(f["at_cycle"], []).append(f)
    ff = faults[0]
    ff_at = ff["at_cycle"]
    ff_until = ff.get("persist_until", MAX_CYCLES)
    rng = random.Random(0xA5A5)

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
        _update_state(state, scenario)
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
        decision = _choose_decision_simulated(state, scenario, condition, path_avail)
        if decision.kind == "escalate":
            state.escalation_requested = True
            state.escalations_total += 1
            _record_escalation_correctness(state, decision, scenario)
        elif decision.kind == "resolve_local":
            state.local_recovery_attempts += 1
            v, r = would_violate(decision.action_name, state)
            if v:
                state.safety_violations += 1
                state.executed_violation_log.append({"cycle": cycle, "action": decision.action_name, "reason": r})
            _execute_local_action(state, decision.action_name)
        elif decision.kind == "safe_mode":
            state.safe_mode_reached = True
        _check_consistency(state, decision)
    return {
        "attempts": state.local_recovery_attempts,
        "guard": state.treatment_escalations_due_to_guard,
        "sv": state.safety_violations,
        "cand_count": state.candidate_violations_count,
        "exec_log": len(state.executed_violation_log),
        "esc_total": state.escalations_total,
    }


def load_seeds(path, n=5):
    seeds = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            seeds.append(int(line))
    return seeds[:n]


if __name__ == "__main__":
    seeds = load_seeds("experiments/seeds_pilot_bis.txt", n=5)
    print(f"[SIMULATED] pilot seeds (first 5): {seeds}\n")
    for sid in ("S3", "S4"):
        scen = yaml.safe_load(Path(f"scenarios/{sid}.yaml").read_text())
        print(f"\n=== [SIMULATED] {sid} ===")
        print(f"{'seed':>4} | {'cond':>9} | {'att':>3} {'guard':>5} {'sv':>3} "
              f"{'cand':>4} {'exec':>4} {'esc':>3}")
        print("-" * 60)
        for cond in ("control", "treatment"):
            for seed in seeds:
                s = run_sim(scen, seed, cond)
                print(f"{seed:>4} | {cond:>9} | {s['attempts']:>3} {s['guard']:>5} "
                      f"{s['sv']:>3} {s['cand_count']:>4} {s['exec_log']:>4} {s['esc_total']:>3}")
