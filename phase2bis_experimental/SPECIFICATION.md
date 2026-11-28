# Phase II-bis — State Transition Specification

**Version:** 1.0-draft
**Date:** 2026-11-28
**Status:** DRAFT — not frozen. Requires review before freezing.
**Relation to Phase II:** Independent experimental cycle. Not a redefinition
of Phase II. H1/H2 in this document are new hypotheses with new seeds, new
implementation, new preregistration.

---

## 1. SystemState — final fields

```python
@dataclass
class SystemState:
    # Core state
    cycle: int = 0
    components: dict[str, Component] = field(default_factory=dict)
    shared_resources: dict[str, SharedResource] = field(default_factory=dict)

    # Authority and constraints
    vsm_authority: str = "nominal"           # "nominal" | "delegated" | "none"
    msm_authority_delegated: bool = True     # MSM authority for local action
    active_constraints: list[str] = field(default_factory=list)
    constraint_conflict: bool = False        # explicit, set from YAML

    # Knowledge
    local_resource_identified: bool = False  # local system knows affected resource
    vsm_resource_identified: bool = False    # VSM knows
    comm_channel: str = "up"                 # "up" | "down"

    # Capacity
    available_capacity: float = 0.0
    required_recovery_capacity: float = 0.0

    # Escalation and containment
    escalation_requested: bool = False
    escalation_requested_at: int | None = None
    vsm_acknowledged: bool = False
    vsm_acknowledged_at: int | None = None
    containment_effective: bool = False
    containment_effective_at: int | None = None

    # Actions and violations
    pending_local_action: str | None = None
    candidate_would_violate: bool = False
    candidate_violation_reason: str | None = None
    safety_violations: int = 0
    executed_violation_log: list[dict] = field(default_factory=list)

    # Outcomes
    secondary_damage: int = 0
    consistency: bool = True
    safe_mode_reached: bool = False
    safe_mode_cycle: int | None = None
    events: list[str] = field(default_factory=list)

    # Counters
    local_fault_count: int = 0
    local_recovery_failures: int = 0
    escalations_total: int = 0
    escalations_correct: int = 0
    escalations_false: int = 0
    escalations_missed: int = 0
```

---

2. Cycle event order (8 stages)

For each cycle in range(MAX_CYCLES):

1. VSM response — acknowledge previous cycle's escalation, attempt containment
2. Primary fault injection — once, at fault_at
3. Secondary propagation — every cycle after fault_at until persist_until or containment
4. State update — capacity, knowledge, constraints
5. Candidate action evaluation — compute candidate_would_violate
6. MSM decision — _choose_decision returns MSMAction
7. Action validation and execution — re-evaluate would_violate on the
   chosen action; increment safety_violations if violated; execute.
8. Event logging and consistency check

Critical: Stage 1 alone calls _vsm_acknowledge and
_vsm_attempt_containment. Stage 6 never calls VSM. Stage 3 runs before
Stage 6, so damage in cycle N occurs before MSM's decision in cycle N.

---

3. Four constraints (operational definitions)

```python
def would_violate(action: str, state: SystemState) -> tuple[bool, str | None]:
    if action != "recover_local":
        return (False, None)
    if not state.msm_authority_delegated:
        return (True, "authority_boundary")
    if any(not r.healthy for r in state.shared_resources.values()):
        return (True, "shared_resource")
    if state.constraint_conflict:
        return (True, "active_constraint")
    if state.required_recovery_capacity > state.available_capacity:
        return (True, "capacity_overflow")
    return (False, None)
```

Note: authority_boundary depends on msm_authority_delegated, NOT
on vsm_authority. This corrects a design error identified during review.

---

4. Containment chain

```
escalation_requested (cycle N)
    -> vsm_acknowledge (cycle N+1, if comm up)
    -> _vsm_attempt_containment (cycle N+1)
    -> containment_effective (cycle N+1, if _vsm_can_contain)
```

_vsm_can_contain requires all four:

1. vsm_authority == "delegated"
2. vsm_resource_identified == True
3. comm_channel == "up"
4. available_capacity >= required_recovery_capacity

---

5. Fault injection and propagation (separated)

· _apply_primary_fault runs once at fault_at.
· _propagate_secondary runs every cycle > fault_at and <= persist_until,
  if the shared resource is unhealthy and containment is not effective.
· containment_effective stops secondary propagation of the contained fault
  only. It does NOT restore the failed resource and does NOT suppress
  independent fault events.

---

6. RNG streams

Two independent streams per run:

```python
fault_rng  = random.Random(_seed_to_int(seed) ^ 0xA5A5)
policy_rng = random.Random(_seed_to_int(seed) ^ 0x5A5A)  # reserved
```

fault_rng drives fault injection and secondary propagation only. Different
MSM decisions do not affect the sequence of external faults.

---

7. Expected behavior (S1-S5)

Scenario Role would_violate safety_violations secondary_damage containment_effective
S1 Negative control False always 0 both conditions 0 False
S2 H2 True after SR failure 0 in control if resolve_local chosen treatment < control treatment=True after N+1
S3 H1 True after 2 failures treatment < control 0 False
S4 H1 True after constraint_conflict treatment < control 0 False
S5 Exploratory per design per design 0 False (comm_down)

---

8. Seven consistency tests (before confirmatory)

1. Existence: In S2, S3, S4: candidate_would_violate = True in >=1 cycle
   across >=50% of seeds. In S1: always False.
2. Variance: would_violate not trivially constant across seeds in S2-S4.
3. Separation: In S2-S4: cases with candidate_would_violate = True and
   safety_violations = 0 must exist (policy chose safe_mode/escalate).
4. H1 effect: In S3, S4: safety_violations (treatment) < (control) in
   =50% of seeds.
5. H2 effect: In S2: mean secondary_damage (treatment) < (control);
   containment_effective occurs earlier in treatment.
6. Determinism: Same seed -> same trace. Same seed -> same external
   fault sequence in control and treatment.
7. Separation of seeds: pilot_bis and confirmatory_bis disjoint, and
   disjoint from original pilot/confirmatory.

---

9. Open points (to be resolved before freezing)

· O1: vsm_resource_identified initial value — per S*.yaml (proposed: c)
· O2: constraint_conflict source — explicit from YAML (proposed: a)
· O3: _terminal_condition — cycle == MAX_CYCLES - 1 only (proposed: a)
· O4: active_constraints types — resource_reservation only (proposed: a)
· O5: _execute_local_action mutates state — yes, only if no violation
  (proposed: c)

---

10. What this specification does NOT define

· Scoring formulas (deferred to confirmatory analysis)
· TLC properties (deferred to formal verification phase)
· Publication plan (deferred to manuscript phase)

This document is frozen only after all open points are resolved and a
SHA-256 digest is recorded in results/.spec.sha256.

## Appendix — Note on CONTROL_THRESHOLDS["R2c"]

**Status:** dead value (documented 2026-11-28).

CONTROL_THRESHOLDS["R2c"] is currently set to 20 with the inline
comment "# x10: severity threshold". However, R2_control does NOT
read this threshold:

    def R2_control(view: RuleView) -> bool:
        return view.shared_resource_unhealthy  # same as R2 (structural)

The threshold is defined but not consumed. It is therefore a dead value,
preserved in place to avoid confusing diffs during the H1-bis repair.
It does NOT affect S2 behavior, and it does NOT need to be unified with
the treatment side (which also does not use it).

**Decision:** Do not change R2c in this repair cycle. If a future change
makes R2_control consume the threshold, that change must be accompanied
by a spec revision and a fresh test of S2.

**Follow-up (not in this cycle):** either remove the dead entry or
activate it with a documented semantic. Both require a spec revision.

## Appendix — Conceptual separation: candidate, path, safety, feasibility

**Added:** 2026-11-28 (H1-bis repair cycle).

Four distinct concepts were previously collapsed into a single variable
(`local_containable`). They are now named explicitly. Conflating them
produced a design contradiction in S3 that no numeric tweak could resolve.

| Concept | Definition | Question answered |
|---|---|---|
| `candidate_available` | `pending_local_action is not None` | Is there a local candidate action? |
| `local_recovery_path_available` | `candidate_available AND no shared resource unhealthy` | Is the local-recovery path open for an attempt? |
| `candidate_safe` | `not would_violate(pending_local_action, state)[0]` | Does executing the candidate respect all constraints? |
| `local_containment_feasible` | NOT derivable from the above alone | Will the local containment actually succeed? |

**Naming decision.** The variable that drives rule R1/R1c matching is
`local_recovery_path_available`, NOT `local_containment_feasible`.

Reason: the variable answers "can the local recovery path be attempted?",
not "will local containment succeed?". Feasibility of containment is a
downstream question (depends on capacity, on the outcome of the recovery,
and potentially on future constraints). It must not be collapsed into the
path-availability signal.

**What the old `local_containable` meant.** Prior to this repair,
`local_containable = (len(unhealthy) <= 1 AND no shared unhealthy)`.
That definition mixed "how many components are unhealthy?" (a state
descriptor) with "is the local path available?" (a precondition for R1).
The new definition uses only what is needed for R1 to be evaluated:

    local_recovery_path_available =
        (pending_local_action is not None)
        AND NOT any(not r.healthy for r in shared_resources.values())

**Non-implication chain (load-bearing for H1-bis).**

- `candidate_available = True` does NOT imply `candidate_safe = True`.
  Having a candidate says nothing about whether executing it is safe.
- `local_recovery_path_available = True` does NOT imply that capacity is
  sufficient. Path availability opens the door to an attempt; it does not
  guarantee the attempt is permitted by capacity constraints.
- `candidate_safe = False` does NOT imply a safety violation occurred.
  A violation is recorded only when a violating action is EXECUTED.
- `local_containment_feasible` is a separate question, evaluated (if at
  all) after the above three. It is NOT assumed by any of them.

**Where the separation is enforced.**

- `_update_state` / `_build_rule_view` compute `local_recovery_path_available`
  from state, without reference to `would_violate`.
- `would_violate` evaluates `candidate_safe` independently.
- `_choose_decision` (treatment only) consults `candidate_safe` BEFORE
  returning a `resolve_local` decision.
- `run_scenario` (Stage 7) records a safety violation only when a
  violating action is EXECUTED — not merely because a candidate exists.

**Test obligation.** The unit tests must include a case that demonstrates:

    candidate_available = True
    local_recovery_path_available = True
    available_capacity = 2.0
    required_recovery_capacity = 2.5
    candidate_safe = False
    would_violate reason = "capacity_overflow"

i.e. the four concepts coexist without contradiction. The specific values
2.0 and 2.5 are synthetic test values used only to prove the separation;
they are NOT a proposed operational value for S3 and do NOT introduce a
new safety margin into any scenario.

