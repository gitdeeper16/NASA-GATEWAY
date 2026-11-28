# Scenario schema — Phase II

Every scenario file `S{n}.yaml` must conform to this schema. The schema is
part of the experimental scenario contract: it fixes the input structure,
not the outcome. Outcome variables, thresholds, and falsification criteria
live in `HYPOTHESES.md` and `PREREGISTRATION.md` and MUST NOT appear here.

---

## Immutable header (every file)

Every scenario file begins with these keys, verbatim:

```yaml
scenario_id: S1          # S1..S5
version: "1.0"           # frozen at PREREGISTRATION freeze 2026-11-27
frozen_at: "2026-11-27"
preregistration_ref: "PREREGISTRATION.md#4"
hypotheses_ref: ["H1"]   # which hypotheses this scenario exercises
```

hypotheses_ref is informational; it does not change falsification logic.

---

Required keys

Key Type Meaning
description string One-paragraph description of the scenario
initial_state object Deterministic initial condition (see §initial_state)
fault_injection object What is injected, when, with what severity
expected_rule string Which rule R1–R5 the treatment condition should fire
treatment_property string TLA+ property the treatment must satisfy (in formal/properties.tla)
control_rule string Which control rule is the structural parallel
can_fail_how list Exhaustive list of failure modes this scenario can expose

can_fail_how is the anti-tautology field: it must enumerate the ways in
which the treatment could still produce a safety violation, a missed
escalation, or a consistency break. If it cannot enumerate any, the
scenario is not a test.

---

initial_state

Key Type Range Meaning
components int 1..4 Number of MSM-controlled components (bounded by MAX_COMPONENTS)
shared_resources int 0..2 Shared resources reachable from MSM
vsm_authority string "nominal" \| "restricted" VSM authority at t=0
comm_channel string "up" \| "down" MSM–VSM channel state at t=0

---

fault_injection

Key Type Range Meaning
type string see table Fault family
target string component id or resource id What is affected
at_cycle int 0..20 When the fault is injected (bounded by MAX_CYCLES)
severity float 0.0..1.0 Fraction of the component's capacity lost
repeat int 0..5 Repetitions (for S3)
persist_until int \| null 0..20 \| null Cycle at which the fault stops

Fault types: component_failure, shared_resource_failure,
local_recovery_failure, constraint_conflict, channel_cut.

---

can_fail_how — required content

Each scenario must list at least three distinct failure modes, each of
the form:

· FM-{n}: a concrete condition under which the treatment (R1–R5) could
  fail to prevent a violation, fail to escalate when required, escalate
  when not required, or break MSM–VSM consistency.

Failure modes are hypotheses about how the design could be wrong. They are
the reason H1–H4 can be falsified. A scenario with fewer than three is
rejected by tests/test_scenarios_schema.sh (to be written post-freeze,
under the "tests" phase).

---

What must NOT appear in a scenario file

· Any threshold, effect size, or significance level.
· Any statement like "treatment should win" or "control should lose".
· Any outcome variable (e.g. safety_violations, consistency).
· Any reference to NASA, Gateway, or flight parameters.

Scenarios describe inputs and failure modes, never results.
