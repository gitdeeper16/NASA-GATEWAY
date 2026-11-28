# Hypotheses — Phase II

Six hypotheses, each with a measurement, a statistical test, and a
falsification criterion. This document is frozen before any code is
written. It is referenced by `PREREGISTRATION.md`.

---

## Overview

| ID | Hypothesis (short form) | Primary measure | Test | Falsified if |
|---|---|---|---|---|
| H1 | Safety-derived escalation rules reduce safety violations | `safety_violations` | Mann–Whitney U (Holm–Bonferroni) | *p* ≥ 0.05 after correction, or *d* < 0.3 |
| H2 | Early escalation reduces secondary damage | secondary damage (S2) | Mann–Whitney U | reduction < 20% |
| H3 | Escalation rules preserve MSM–VSM consistency | `consistency` (S1 + S4) | proportion test | proportion < 0.95 |
| H4 | Safe mode on communication loss prevents safety violations | `safe_mode_reached` and `safety_violations` (S5) | exact binomial | any violation in S5 under treatment |
| H5 | All escalation rules are formally verified | TLC verdict on `properties.tla` | model checking | any counterexample |
| H6 | The model is deterministic under a fixed seed | trace equality | byte comparison | any differing trace |

---

## H1 — Safety-derived escalation rules reduce safety violations

**Statement.** Under injected faults, a system whose escalation rules are
derived from safety constraints produces fewer safety-constraint
violations than a system whose escalation rules are structurally
equivalent but not derived from safety constraints.

**Measurement.** `safety_violations` per run, per scenario.

**Test.** Mann–Whitney U test, treatment vs control, one test per scenario,
Holm–Bonferroni correction across the five scenarios. Effect size: Cohen's
*d*. α = 0.05.

**Falsified if.** After correction, no scenario reaches *p* < 0.05, **or**
the pooled effect size is *d* < 0.3.

**What H1 does not claim.** It does not claim that safety-derived rules are
the only way to reduce violations, nor that the observed reduction
generalises to any operational system.

---

## H2 — Early escalation reduces secondary damage

**Statement.** In scenario S2 (fault exceeds MSM authority, touching a
shared resource), early escalation reduces secondary damage compared with
the control condition.

**Measurement.** Secondary damage, defined as the number of *additional*
components affected after the fault (recorded per run in S2).

**Test.** Mann–Whitney U test, S2 only. Effect size: relative reduction.

**Falsified if.** The reduction in secondary damage is < 20%.

**What H2 does not claim.** It does not claim that early escalation is
always better; S1 is the case where early escalation would be *worse* (it
would escalate a containable fault).

---

## H3 — Escalation rules preserve MSM–VSM decision consistency

**Statement.** In non-critical scenarios (S1 and S4), escalation rules
preserve consistency between MSM and VSM decisions — i.e. the two levels
never disagree about who has authority over a given condition.

**Measurement.** `consistency` (binary per run).

**Test.** Proportion test, treatment condition, S1 + S4 combined.

**Falsified if.** The consistency proportion is < 0.95.

**What H3 does not claim.** It does not claim that consistency is preserved
in S2, S3, or S5, where the scenario intentionally exercises disagreement.

---

## H4 — Safe mode on communication loss prevents safety violations

**Statement.** In scenario S5 (MSM–VSM communication loss), a rule that
puts the MSM into safe mode on loss of communication prevents safety
violations.

**Measurement.** `safe_mode_reached` (binary) and `safety_violations`
(count), S5 only.

**Test.** Exact binomial on `safe_mode_reached`, plus descriptive count of
`safety_violations`.

**Falsified if.** Any safety violation is observed in S5 under the
treatment condition.

**What H4 does not claim.** It does not claim that safe mode is the only
correct response to communication loss; it claims only that, in this model,
it prevents violations.

---

## H5 — All escalation rules are formally verified

**Statement.** Every escalation rule in the treatment condition is
represented as a TLA+ property, and TLC finds no counterexample to any of
them in any of the five scenarios.

**Measurement.** TLC verdict per property per scenario.

**Test.** Exhaustive model checking within the stated state space. The
state space is fixed at freeze time in `formal/model_check.sh`.

**Falsified if.** TLC finds any counterexample to any property.

**What H5 does not claim.** H5 establishes that the *model* satisfies the
*stated properties*. It does not establish that any operational system
satisfies them. The gap between model and operational system is documented
in `docs/THREATS_TO_VALIDITY.md`.

---

## H6 — The model is deterministic under a fixed seed

**Statement.** Two runs with the same scenario and the same seed produce
identical traces.

**Measurement.** Byte-for-byte equality of the two traces.

**Test.** `tests/test_model_determinism.sh`.

**Falsified if.** Any trace element differs.

**What H6 does not claim.** It does not claim that determinism implies
correctness; it is a precondition for reproducibility.

---

## Rule catalogue (treatment condition)

Five escalation rules, each traceable to a hazard-derived requirement in
Phase I. The mapping is fixed at freeze time.

| Rule | Condition | Phase I reference | Formal property |
|---|---|---|---|
| R1 | fault contained within MSM domain | L2-GW-0199 (autonomy) | `[] (local_containable -> <> resolved_locally)` |
| R2 | fault touches shared resource | DSG-RQMT-001 hazard allocation | `[] (shared_resource_affected -> <> escalated)` |
| R3 | local recovery failed for N cycles | fault management documentation | `[] (local_recovery_failed -> <> escalated)` |
| R4 | local action would violate a vehicle-level constraint | L2-GW-0111 (hazard control) | `[] (conflict -> ~local_action)` |
| R5 | communication with VSM lost | L2-GW-0199 (no Earth dependency) | `[] (comm_lost -> <> safe_mode)` |

The control condition uses five structurally equivalent rules with
thresholds set independently of the safety constraints (fixed at freeze
time; the thresholds are recorded in `experiments/control_thresholds.txt`).

---

## Freeze note

This document is frozen at the same time as `PREREGISTRATION.md`. The
freeze date is recorded in `PREREGISTRATION.md` §10.
