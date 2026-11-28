"""
Phase II — Module System Manager (MSM).

The MSM is the lower-level autonomy layer. It owns local components and
may take local actions. It escalates to the VSM when a treatment or
control rule fires (see rules.RULE_POLARITY).

The MSM does NOT decide whether a rule fires. The engine evaluates the
rules and hands the MSM a decision. This keeps the MSM a pure actor:
it can only execute what it was told.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MSMAction:
    kind: str  # "resolve_local" | "escalate" | "safe_mode" | "noop"
    rule: str | None = None


def act(state, decision: MSMAction) -> None:
    """Execute an MSM action. Mutates state; returns None."""
    if decision.kind == "resolve_local":
        # R1 path: attempt local recovery.
        # A local recovery succeeds iff the fault is containable and at
        # least one component is unhealthy.
        unhealthy = [c for c in state.components.values() if not c.healthy]
        if unhealthy and state.local_fault_count > 0:
            # Successful local recovery: mark all unhealthy components healthy.
            for c in unhealthy:
                c.healthy = True
            state.local_fault_count = 0
            state.local_recovery_failures = 0
            state.events.append(f"cycle {state.cycle}: MSM local recovery succeeded")
        else:
            # Recovery failed; count it.
            state.local_recovery_failures += 1
            state.events.append(
                f"cycle {state.cycle}: MSM local recovery failed "
                f"({state.local_recovery_failures} consecutive)"
            )
    elif decision.kind == "escalate":
        state.escalations_total += 1
        state.events.append(f"cycle {state.cycle}: MSM escalated via {decision.rule}")
        # Escalation hands control to VSM; MSM does not act this cycle.
    elif decision.kind == "safe_mode":
        state.safe_mode_reached = True
        state.safe_mode_cycle = state.cycle
        state.events.append(f"cycle {state.cycle}: MSM entered safe mode")
        # In safe mode, no local actions are taken.
    elif decision.kind == "noop":
        # No rule fired. If a local action was pending and would violate a
        # constraint, taking it is a safety violation.
        if state.pending_local_action is not None and state.pending_local_action_would_violate:
            state.safety_violations += 1
            state.events.append(
                f"cycle {state.cycle}: safety violation — local action taken "
                f"despite constraint conflict"
            )
        state.pending_local_action = None
        state.pending_local_action_would_violate = False
