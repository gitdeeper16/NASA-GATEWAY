"""
Phase II — Escalation rules (treatment R1–R5 + control R1c–R5c).

These functions are PURE: no state, no side effects, no I/O. Each function
takes a snapshot of the system state and returns a boolean decision:
"should this rule fire?"

Design constraints (from PREREGISTRATION.md and HYPOTHESES.md):

1. The treatment rules R1–R5 are derived from safety constraints. Their
   logic must be traceable to the rule catalogue in HYPOTHESES.md.
2. The control rules R1c–R5c are structurally equivalent but their
   thresholds are set independently of any safety constraint. They are
   fixed in experiments/control_thresholds.txt.
3. No rule may read any outcome variable (safety_violations, consistency,
   etc.). Rules see only state, never results.
4. No rule may read NASA/Gateway references. The mapping to Phase I
   documents lives in HYPOTHESES.md, not in code.
5. These functions MUST be able to return False. If they always return
   True, the hypotheses cannot be falsified.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Rule thresholds (treatment)
# These are the frozen values from HYPOTHESES.md rule catalogue.
# R3's N is the "repeated local failures" bound.
# ---------------------------------------------------------------------------

R3_TREATMENT_N = 3  # cycles of consecutive local recovery failures

# Control thresholds (frozen in experiments/control_thresholds.txt)
# Loaded at import time from the frozen file, NOT hard-coded, so that a
# change to the file is visible in the digest.
import pathlib as _pathlib

_CONTROL_FILE = _pathlib.Path(__file__).resolve().parent.parent / "experiments" / "control_thresholds.txt"


def _load_control_thresholds() -> dict[str, int]:
    """Load the frozen control thresholds. Fails loudly if the file is absent."""
    if not _CONTROL_FILE.exists():
        raise FileNotFoundError(
            f"Control thresholds not found at {_CONTROL_FILE}. "
            "This file is frozen at PREREGISTRATION freeze 2026-11-27."
        )
    thresholds: dict[str, int] = {}
    for line in _CONTROL_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            thresholds[k.strip()] = int(v.strip())
    return thresholds


CONTROL = _load_control_thresholds()


# ---------------------------------------------------------------------------
# State view passed to rules.
# Rules see a *snapshot*, not the live model. This keeps them pure and
# testable, and prevents a rule from observing its own effect.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RuleView:
    """Immutable view of the system state at the moment a rule is evaluated."""
    cycle: int
    # Local / MSM domain
    local_fault_count: int = 0
    local_recovery_failures: int = 0  # consecutive cycles
    local_containable: bool = True
    # Shared resources
    shared_resource_affected: bool = False
    shared_resource_severity: float = 0.0
    # Constraint conflict
    constraint_violated_by_local_action: bool = False
    # Communication
    comm_lost: bool = False
    comm_silence_cycles: int = 0


# ---------------------------------------------------------------------------
# Treatment rules R1–R5
# Each returns True iff the MSM should escalate (to VSM) or act (safe mode).
# ---------------------------------------------------------------------------

def R1_local_containable(view: RuleView) -> bool:
    """
    R1 — fault contained within MSM domain.
    Traceable to HYPOTHESES.md rule catalogue, Phase I ref L2-GW-0199.

    Fires when the local fault is containable AND there is a non-zero
    local fault count. That is: local resolution is the right action,
    so the rule "fires" in the sense of "no escalation needed; resolve
    locally". To keep the interface uniform (all rules return "act"),
    R1 returns True when local resolution should proceed.

    IMPORTANT: in the engine, R1=True means "do NOT escalate; resolve
    locally". The engine interprets each rule's meaning. R1 is the only
    rule with inverted polarity.
    """
    return view.local_containable and view.local_fault_count > 0


def R2_shared_resource(view: RuleView) -> bool:
    """
    R2 — fault touches shared resource.
    Fires when a shared resource is affected and severity is non-trivial.
    Severity threshold > 0.0 is intentional: any non-zero shared-resource
    impact requires escalation, because the MSM has no authority over it.
    """
    return view.shared_resource_affected and view.shared_resource_severity > 0.0


def R3_local_recovery_failed(view: RuleView) -> bool:
    """
    R3 — local recovery failed for N consecutive cycles.
    N is R3_TREATMENT_N (frozen at 3).
    """
    return view.local_recovery_failures >= R3_TREATMENT_N


def R4_constraint_conflict(view: RuleView) -> bool:
    """
    R4 — local action would violate a vehicle-level constraint.
    Fires when the pending local action is known to violate a constraint.
    The rule does NOT check whether the action was already taken; that is
    the engine's responsibility. R4 is a pre-condition check.
    """
    return view.constraint_violated_by_local_action


def R5_comm_lost(view: RuleView) -> bool:
    """
    R5 — communication with VSM lost.
    Fires when the comm channel is down. Safe mode is the required action.
    """
    return view.comm_lost


# ---------------------------------------------------------------------------
# Control rules R1c–R5c
# Structurally parallel to R1–R5, thresholds from CONTROL.
# These MUST be evaluable on the same RuleView. If they need a different
# state shape, the control is not structurally equivalent and the design
# is broken (see PREREGISTRATION.md §3.2).
# ---------------------------------------------------------------------------

def R1_control(view: RuleView) -> bool:
    """Control for R1: escalate if local_fault_count >= threshold."""
    return view.local_fault_count >= CONTROL["R1_control_threshold"]


def R2_control(view: RuleView) -> bool:
    """Control for R2: escalate if shared_resource_count >= threshold.
    Uses severity > 0 as the "affected" signal, with an arbitrary extra
    threshold on severity magnitude."""
    return (
        view.shared_resource_affected
        and view.shared_resource_severity
        >= CONTROL["R2_control_threshold"] / 10.0
    )


def R3_control(view: RuleView) -> bool:
    """Control for R3: escalate after N consecutive failures, N from file."""
    return view.local_recovery_failures >= CONTROL["R3_control_threshold"]


def R4_control(view: RuleView) -> bool:
    """Control for R4: escalate if local_action_count >= threshold.
    The control does not look at constraint violation at all — that is the
    point of the control: it is structurally parallel but blind to the
    safety constraint."""
    # We use cycle as a proxy for "local_action_count" here because the
    # RuleView does not carry action count (the engine will provide it).
    # This is intentional: the control must NOT depend on the safety
    # signal. We use a monotonic proxy that the treatment does not use.
    return view.cycle >= CONTROL["R4_control_threshold"]


def R5_control(view: RuleView) -> bool:
    """Control for R5: safe mode after N cycles of silence."""
    return view.comm_silence_cycles >= CONTROL["R5_control_threshold"]


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

TREATMENT_RULES = {
    "R1": R1_local_containable,
    "R2": R2_shared_resource,
    "R3": R3_local_recovery_failed,
    "R4": R4_constraint_conflict,
    "R5": R5_comm_lost,
}

CONTROL_RULES = {
    "R1_control": R1_control,
    "R2_control": R2_control,
    "R3_control": R3_control,
    "R4_control": R4_control,
    "R5_control": R5_control,
}

RULE_POLARITY = {
    # True means "R1's condition holds; resolve locally, do NOT escalate"
    "R1": "resolve_local",
    # True means "escalate to VSM"
    "R2": "escalate",
    "R3": "escalate",
    "R4": "escalate",  # defer to VSM instead of local action
    "R5": "safe_mode",
}
