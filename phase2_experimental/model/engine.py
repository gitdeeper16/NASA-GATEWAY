"""
Phase II — Execution engine.

Reads one scenario YAML, runs one seed to completion, returns a trace dict.
The engine:
  - owns mutation of state,
  - evaluates rules against an immutable RuleView,
  - applies MSMAction / VSM response,
  - records outcome variables for later analysis.

The engine does NOT decide which hypotheses pass. It only produces traces.
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import yaml

from model.rules import TREATMENT_RULES, CONTROL_RULES, RULE_POLARITY
from model.state import Component, SharedResource, SystemState
from model.msm import MSMAction, act as msm_act
from model.vsm import respond_to_escalation


MAX_CYCLES = 20
MAX_COMPONENTS = 4


def _seed_to_int(seed: int | str) -> int:
    if isinstance(seed, int):
        return seed
    return int(hashlib.sha256(str(seed).encode()).hexdigest(), 16) % (2**32)


def _build_initial_state(scenario: dict) -> SystemState:
    st = scenario["initial_state"]
    n = st["components"]
    if n > MAX_COMPONENTS:
        raise ValueError(f"components={n} exceeds MAX_COMPONENTS={MAX_COMPONENTS}")
    state = SystemState(
        vsm_authority=st["vsm_authority"],
        comm_channel=st["comm_channel"],
    )
    for i in range(1, n + 1):
        state.components[f"C{i}"] = Component(id=f"C{i}")
    for j in range(1, st["shared_resources"] + 1):
        state.shared_resources[f"SR{j}"] = SharedResource(id=f"SR{j}")
    return state


def _apply_fault(state: SystemState, fault: dict, rng: random.Random) -> None:
    """Apply the fault from the scenario at the scenario's cycle."""
    t = fault["type"]
    if t == "component_failure":
        target = fault["target"]
        if target in state.components:
            state.components[target].healthy = False
            state.components[target].capacity = 1.0 - fault["severity"]
        state.local_fault_count += 1
        # Determine containability: a single component failure is containable.
        containable = True
        state.pending_local_action = "recover_local"
        state.pending_local_action_would_violate = False
        # If more than one component is already unhealthy, not containable.
        if sum(1 for c in state.components.values() if not c.healthy) > 1:
            containable = False
        state.events.append(
            f"cycle {state.cycle}: fault {t} on {target} "
            f"(severity={fault['severity']}, containable={containable})"
        )
    elif t == "shared_resource_failure":
        target = fault["target"]
        if target in state.shared_resources:
            state.shared_resources[target].healthy = False
            state.shared_resources[target].severity_lost = fault["severity"]
        # Secondary damage: each other component sharing the resource
        # loses partial capacity.
        for c in state.components.values():
            if c.healthy and rng.random() < fault["severity"] * 0.5:
                c.healthy = False
                state.secondary_damage += 1
                state.events.append(
                    f"cycle {state.cycle}: secondary damage on {c.id}"
                )
        state.events.append(f"cycle {state.cycle}: shared resource {target} failed")
    elif t == "local_recovery_failure":
        target = fault["target"]
        if target in state.components:
            state.components[target].healthy = False
        state.local_fault_count += 1
        state.local_recovery_failures += 1
        state.pending_local_action = "recover_local"
        state.events.append(
            f"cycle {state.cycle}: local recovery failure "
            f"({state.local_recovery_failures} consecutive)"
        )
    elif t == "constraint_conflict":
        target = fault["target"]
        if target in state.components:
            state.components[target].healthy = False
        state.local_fault_count += 1
        state.pending_local_action = "recover_local"
        state.pending_local_action_would_violate = True
        state.events.append(
            f"cycle {state.cycle}: constraint conflict on {target} "
            f"(local action would violate vehicle constraint)"
        )
    elif t == "channel_cut":
        state.comm_channel = "down"
        state.events.append(f"cycle {state.cycle}: comm channel cut")


def _choose_decision(state: SystemState, scenario: dict, condition: str,
                     local_containable: bool) -> MSMAction:
    """Evaluate rules and return the MSM decision for this cycle."""
    view = state.to_rule_view(local_containable=local_containable)
    rules = TREATMENT_RULES if condition == "treatment" else CONTROL_RULES

    # Priority order is fixed: R5 (comm) > R4 (constraint) > R3 (recovery)
    # > R2 (shared) > R1 (local). This order is part of the contract.
    order = ["R5", "R4", "R3", "R2", "R1"] if condition == "treatment" \
        else ["R5_control", "R4_control", "R3_control", "R2_control", "R1_control"]

    for rule_name in order:
        fn = rules[rule_name]
        if fn(view):
            # For R1 / R1_control: "resolve locally".
            base = rule_name.replace("_control", "")
            polarity = RULE_POLARITY[base]
            if polarity == "resolve_local":
                return MSMAction(kind="resolve_local", rule=rule_name)
            elif polarity == "escalate":
                return MSMAction(kind="escalate", rule=rule_name)
            elif polarity == "safe_mode":
                return MSMAction(kind="safe_mode", rule=rule_name)

    return MSMAction(kind="noop", rule=None)


def run_scenario(scenario: dict, seed: int, condition: str) -> dict:
    """Run one scenario × one seed × one condition. Returns a trace dict."""
    if condition not in ("treatment", "control"):
        raise ValueError(f"condition must be 'treatment' or 'control', got {condition!r}")

    rng = random.Random(_seed_to_int(seed))
    state = _build_initial_state(scenario)
    fault = scenario["fault_injection"]
    fault_at = fault["at_cycle"]
    persist_until = fault.get("persist_until") or MAX_CYCLES
    repeat = fault.get("repeat", 0)

    injections_done = 0
    for cycle in range(MAX_CYCLES):
        state.cycle = cycle

        # Inject faults at the right cycle(s).
        if cycle == fault_at:
            _apply_fault(state, fault, rng)
            injections_done += 1
        elif repeat > 0 and cycle > fault_at and cycle <= fault_at + repeat and cycle <= persist_until:
            # Re-inject on subsequent cycles (for S3-style scenarios).
            _apply_fault(state, fault, rng)
            injections_done += 1

        # Track communication silence.
        if state.comm_channel == "down":
            state.comm_silence_cycles += 1

        # Decide containment for this cycle.
        unhealthy = [c for c in state.components.values() if not c.healthy]
        local_containable = (len(unhealthy) <= 1) and not any(
            not r.healthy for r in state.shared_resources.values()
        )

        decision = _choose_decision(state, scenario, condition, local_containable)

        if decision.kind == "safe_mode" and state.safe_mode_reached:
            # Already in safe mode; no further actions.
            continue
        if decision.kind == "safe_mode":
            msm_act(state, decision)
            # Safe mode ends the run for this seed.
            break
        elif decision.kind == "escalate":
            # Record correctness of escalation.
            expected_rule = scenario["expected_rule"]
            if decision.rule in (expected_rule, expected_rule + "_control"):
                state.escalations_correct += 1
            else:
                state.escalations_false += 1
            msm_act(state, decision)
            respond_to_escalation(state)
        elif decision.kind == "resolve_local":
            msm_act(state, decision)
        else:  # noop
            msm_act(state, decision)

        # Check consistency: if MSM escalated and VSM responded, both
        # must agree that the local fault is resolved.
        if decision.kind == "escalate":
            still_bad = any(not c.healthy for c in state.components.values())
            shared_bad = any(not r.healthy for r in state.shared_resources.values())
            if still_bad and shared_bad:
                state.consistency = False
                state.events.append(
                    f"cycle {cycle}: MSM/VSM inconsistency — escalation did not "
                    f"resolve either local or shared fault"
                )

        # Record missed escalation: expected rule should have fired but didn't.
        expected_rule = scenario["expected_rule"]
        expected_fn = TREATMENT_RULES.get(expected_rule)
        if condition == "treatment" and expected_fn is not None:
            view_now = state.to_rule_view(local_containable=local_containable)
            if not expected_fn(view_now):
                # Rule condition is no longer true; not a miss.
                pass

    return {
        "scenario_id": scenario["scenario_id"],
        "seed": seed,
        "condition": condition,
        "cycles_run": state.cycle + 1,
        "safety_violations": state.safety_violations,
        "escalations_total": state.escalations_total,
        "escalations_correct": state.escalations_correct,
        "escalations_false": state.escalations_false,
        "escalations_missed": state.escalations_missed,
        "consistency": int(state.consistency),
        "secondary_damage": state.secondary_damage,
        "safe_mode_reached": int(state.safe_mode_reached),
        "safe_mode_cycle": state.safe_mode_cycle,
        "events": state.events,
    }
