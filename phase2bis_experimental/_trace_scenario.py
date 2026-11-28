"""Trace any scenario cycle-by-cycle. READ-ONLY. Does not modify project files."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import yaml, random
from model.engine import (
    _build_initial_state, _update_state, _iter_faults,
    _apply_primary_fault, _propagate_secondary,
    _vsm_acknowledge, _vsm_attempt_containment,
    _choose_decision, _execute_local_action, _check_consistency,
    _record_escalation_correctness, would_violate, MAX_CYCLES,
)

def trace(scenario_id, condition, seed=1):
    scen = yaml.safe_load(Path(f"scenarios/{scenario_id}.yaml").read_text())
    print(f"\n{'='*120}")
    print(f"{scenario_id} | condition={condition} | seed={seed}")
    print(f"{'='*120}")
    print(f"{'cyc':>3} | {'C1':>3} {'C2':>3} {'C3':>3} | "
          f"{'avail':>5} {'req':>4} | {'cand':>4} {'exec':>4} | "
          f"{'pend':>14} | {'att':>3} {'fail':>4} {'guard':>5} {'sv':>3} {'esc':>3} | decision")
    print("-" * 125)

    state = _build_initial_state(scen)
    faults = _iter_faults(scen)
    fbc = {}
    for f in faults:
        fbc.setdefault(f["at_cycle"], []).append(f)
    if not faults:
        print("NO FAULTS"); return
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

        c1 = "H" if state.components["C1"].healthy else "U"
        c2 = "H" if state.components["C2"].healthy else "U"
        c3 = "H" if len(state.components) >= 3 and state.components["C3"].healthy else "-"
        cand = int(state.candidate_would_violate)
        pend = state.pending_local_action or "-"
        exec_v = "-"
        if decision.kind == "escalate":
            state.escalation_requested = True
            state.escalations_total += 1
            _record_escalation_correctness(state, decision, scen)
        elif decision.kind == "resolve_local":
            state.local_recovery_attempts += 1
            v, r = would_violate(decision.action_name, state)
            if v:
                state.safety_violations += 1
                exec_v = "Y"
                state.executed_violation_log.append({"cycle": cycle, "action": decision.action_name, "reason": r})
            _execute_local_action(state, decision.action_name)
        elif decision.kind == "safe_mode":
            state.safe_mode_reached = True
        elif decision.kind == "noop":
            pass

        dec = decision.kind + (f"/{decision.rule}" if decision.rule else "")
        print(f"{cycle:>3} | {c1:>3} {c2:>3} {c3:>3} | "
              f"{state.available_capacity:>5.2f} {state.required_recovery_capacity:>4.1f} | "
              f"{cand:>4} {exec_v:>4} | {pend:>14} | "
              f"{state.local_recovery_attempts:>3} {state.local_recovery_failures:>4} "
              f"{state.treatment_escalations_due_to_guard:>5} {state.safety_violations:>3} "
              f"{state.escalations_total:>3} | {dec}")
        _check_consistency(state, decision)

    print(f"\nFinal: attempts={state.local_recovery_attempts} "
          f"failures={state.local_recovery_failures} "
          f"guard={state.treatment_escalations_due_to_guard} "
          f"safety_violations={state.safety_violations} "
          f"escalations_total={state.escalations_total} "
          f"candidate_violations_count={state.candidate_violations_count}")

if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "S3"
    for cond in ("treatment", "control"):
        trace(sid, cond, seed=1)
