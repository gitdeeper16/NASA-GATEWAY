"""
Phase II — Vehicle System Manager (VSM).

The VSM is the higher-level autonomy layer. It acts only after an
escalation from the MSM. It may resolve shared-resource faults.

The VSM does not evaluate rules. It responds to escalations. Its behavior
is deliberately simple: act on the affected shared resource, and clear
the MSM's pending local action (so the MSM does not later take it).
"""

from __future__ import annotations


def respond_to_escalation(state) -> None:
    """VSM acts after receiving an escalation. Mutates state."""
    # Resolve all unhealthy shared resources.
    resolved_any = False
    for r in state.shared_resources.values():
        if not r.healthy:
            r.healthy = True
            r.severity_lost = 0.0
            resolved_any = True
    if resolved_any:
        state.events.append(f"cycle {state.cycle}: VSM resolved shared resource")
    # Clear MSM pending local action — VSM has authority.
    if state.pending_local_action is not None:
        state.pending_local_action = None
        state.pending_local_action_would_violate = False
