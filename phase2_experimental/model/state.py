"""
Phase II — System state.

State is a plain dataclass. No behavior, no I/O. The engine owns mutation;
rules see an immutable RuleView derived from state.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Component:
    id: str
    healthy: bool = True
    capacity: float = 1.0


@dataclass
class SharedResource:
    id: str
    healthy: bool = True
    severity_lost: float = 0.0


@dataclass
class SystemState:
    cycle: int = 0
    components: dict[str, Component] = field(default_factory=dict)
    shared_resources: dict[str, SharedResource] = field(default_factory=dict)
    vsm_authority: str = "nominal"
    comm_channel: str = "up"
    # Counters
    local_fault_count: int = 0
    local_recovery_failures: int = 0
    comm_silence_cycles: int = 0
    # Pending local action
    pending_local_action: Optional[str] = None
    pending_local_action_would_violate: bool = False
    # Per-run outcome counters (engine-owned; NEVER visible to rules)
    safety_violations: int = 0
    escalations_total: int = 0
    escalations_correct: int = 0
    escalations_false: int = 0
    escalations_missed: int = 0
    secondary_damage: int = 0
    consistency: bool = True
    safe_mode_reached: bool = False
    safe_mode_cycle: Optional[int] = None
    events: list[str] = field(default_factory=list)

    def to_rule_view(self, *, local_containable: bool):
        """Build the immutable RuleView that rules are allowed to see.
        Outcome counters are intentionally NOT included."""
        from model.rules import RuleView
        return RuleView(
            cycle=self.cycle,
            local_fault_count=self.local_fault_count,
            local_recovery_failures=self.local_recovery_failures,
            local_containable=local_containable,
            shared_resource_affected=any(not r.healthy for r in self.shared_resources.values()),
            shared_resource_severity=max(
                (r.severity_lost for r in self.shared_resources.values()), default=0.0
            ),
            constraint_violated_by_local_action=self.pending_local_action_would_violate,
            comm_lost=(self.comm_channel == "down"),
            comm_silence_cycles=self.comm_silence_cycles,
        )
