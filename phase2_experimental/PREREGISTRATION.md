# Pre-Registration — Phase II

**Title:** Experimental Validation of Safety-Derived Autonomy Boundaries in
Multi-Level Autonomous Systems.

**Version:** 2.0.0-experimental.
**Date frozen:** 2026-11-27.
**Status:** FROZEN (2026-11-27). Amendments require a dated, pre-registered addendum that does not alter hypotheses or falsification criteria.

> This document fixes the experimental design before implementation begins.
> After the freeze date, no element of this document may be changed except
> by a dated amendment that is itself pre-registered and that does not
> redefine the hypotheses.

---

## 1. Research question

Do escalation rules derived from safety constraints preserve system safety
and decision consistency at the MSM–VSM interface under injected faults,
compared with escalation rules that are not derived from safety constraints?

**Sub-questions:**

1. Do safety-derived escalation rules reduce violations of safety
   constraints under faults? (H1)
2. Does early escalation reduce secondary damage when shared resources are
   affected? (H2)
3. Do escalation rules preserve MSM–VSM decision consistency in non-critical
   scenarios? (H3)
4. Does the "safe mode on communication loss" rule prevent safety
   violations when the MSM–VSM channel is cut? (H4)
5. Are all escalation rules formally verified in TLA+ against the stated
   properties? (H5)
6. Is the experimental model deterministic under a fixed seed? (H6)

---

## 2. Experimental unit

**Unit of analysis:** one *run*.

A run is one execution of the model against one scenario, starting from a
defined initial state and using a fixed random seed. Each run produces a
trace and a set of outcome variables (see §6).

**Why one run and not one scenario:** scenarios contain stochastic elements
(fault timing, fault magnitude). Treating a scenario as the unit would hide
variance and inflate apparent significance.

**What is held constant within a run:** the model code version, the
scenario definition, the escalation-rule set (safety-derived or
arbitrary), and the seed.

**What varies across runs:** the scenario, the escalation-rule set, and the
seed.

---

## 3. Conditions and control group

### 3.1 Treatment condition — safety-derived escalation rules

Escalation rules that are explicitly derived from safety constraints and
traceable to a hazard-derived requirement. The rule set is fixed at freeze
time (see `HYPOTHESES.md` §3 for the rule catalogue).

### 3.2 Control condition — arbitrary escalation rules

Escalation rules that are structurally equivalent (same number of rules,
same interface, same execution path) but whose thresholds are set
independently of the safety constraints — e.g. fixed random thresholds
drawn from a seeded distribution, or hand-set thresholds not tied to any
hazard.

**Why this control:** it isolates the effect of *derivation from safety*
from the effect of *having escalation rules at all*. Without this control,
a positive result for the treatment condition could be explained by the
mere presence of any escalation mechanism.

**What the control is not:** the control is not "no escalation". "No
escalation" is a third condition that may be reported as a descriptive
baseline, but it is not the inferential comparison.

### 3.3 Third condition (descriptive only) — no escalation

A model variant with escalation disabled. Reported descriptively to
characterise the fault response of a purely local system. **Not used for
inferential comparison.**

---

## 4. Scenarios

Five fault scenarios, each defined in `scenarios/*.yaml`:

| ID | Scenario | Injected fault |
|---|---|---|
| S1 | Local containable fault | single-component failure |
| S2 | Fault exceeds MSM authority | fault touching a shared resource |
| S3 | Local recovery fails | repeated local failures beyond a bound |
| S4 | Local decision conflicts with a vehicle-level safety constraint | local action that would violate a constraint |
| S5 | MSM–VSM communication loss | channel cut |

Each scenario is executed under both the treatment and the control
condition. The "no escalation" condition is executed as a descriptive
baseline.

---

## 5. Sampling design

### 5.1 Pilot stage

**Target:** 200 runs.
**Allocation:** 5 scenarios × 2 conditions × 20 seeds = 200 runs.
**Purpose:** calibrate the fault magnitudes and timing distributions; check
that outcomes vary (i.e. the model is not trivially safe or trivially
unsafe); confirm determinism.
**Pilot outputs are not used for hypothesis testing.**

### 5.2 Confirmatory stage

**Target:** 800 runs.
**Allocation:** 5 scenarios × 2 conditions × 80 seeds = 800 runs.
**Purpose:** hypothesis testing.

### 5.3 Independence and leakage

- Pilot and confirmatory seeds are **disjoint**. The seed sets are fixed at
  freeze time and stored in `experiments/seeds_pilot.txt` and
  `experiments/seeds_confirmatory.txt`.
- Pilot results are stored only in `results/pilot/`. Confirmatory results
  only in `results/confirmatory/`.
- Confirmatory analysis code must not read from `results/pilot/`.
- A separation check (`tests/test_separation.sh`) enforces this at the file
  level.
- Pilot observations may inform **calibration of fault magnitudes** only if
  those calibrations are recorded as dated amendments to this document
  *before* the confirmatory stage begins. Pilot observations may **not**
  inform the choice of hypotheses, the choice of statistical tests, or the
  choice of falsification thresholds.

### 5.4 What "200" and "800" mean

These numbers are **planned** run counts, not guaranteed independent
observations. Because runs within a scenario share a scenario definition,
the effective sample size for a scenario-level question is smaller than the
run count. The statistical analysis in §7 is designed to respect this.

---

## 6. Outcome measures

For each run:

| Measure | Type | Definition |
|---|---|---|
| `safety_violations` | count | Number of safety-constraint violations during the run |
| `escalations_total` | count | Number of escalations MSM → VSM |
| `escalations_correct` | count | Escalations matching the rule-derived expected escalation |
| `escalations_false` | count | Escalations that were not required by the rule set |
| `escalations_missed` | count | Escalations required by the rule set but not performed |
| `consistency` | binary | MSM and VSM produced consistent decisions throughout |
| `time_to_resolution` | cycles | Cycles from fault injection to safe state |
| `safe_mode_reached` | binary | (S5 only) safe mode reached after communication loss |

---

## 7. Statistical design

### 7.1 Primary test (H1)

- **Unit of analysis:** run, grouped by scenario.
- **Test:** Mann–Whitney U test on `safety_violations`, treatment vs control.
- **Why non-parametric:** count data, bounded, non-normal.
- **Effect size:** Cohen's *d* (reported alongside *p*).
- **Significance threshold:** α = 0.05.
- **Multiplicity:** Holm–Bonferroni correction across the five scenario-level
  tests.

### 7.2 Secondary tests (H2–H4)

| Hypothesis | Test | Effect size | Threshold |
|---|---|---|---|
| H2 | Mann–Whitney U on secondary damage, S2 only | Cohen's d | α = 0.05 |
| H3 | Proportion test on `consistency`, S1 + S4 | Cohen's h | α = 0.05 |
| H4 | Exact binomial on `safe_mode_reached`, S5 | — | α = 0.05 |

### 7.3 Formal verification (H5)

- TLA+ model, TLC model checker.
- All properties in `formal/properties.tla` must hold in every scenario.
- A single counterexample fails H5.
- **What H5 does and does not establish:** H5 establishes that the *model*
  satisfies the *stated properties*. It does not establish that any
  operational system satisfies them. This is stated in the Phase II
  manuscript and in `docs/THREATS_TO_VALIDITY.md`.

### 7.4 Determinism (H6)

- Two runs with the same seed and same scenario must produce identical
  traces.
- Verified by `tests/test_model_determinism.sh`.

---

## 8. Falsification criteria

A hypothesis is **rejected** if its falsification criterion is met. A
hypothesis is **not accepted** merely because its criterion is not met — it
is reported as "not rejected", with the observed effect size and
confidence interval.

| ID | Rejected if |
|---|---|
| H1 | Mann–Whitney U test on `safety_violations` does not reach *p* < 0.05 after Holm–Bonferroni correction, **or** Cohen's *d* < 0.3 |
| H2 | Reduction in secondary damage in S2 is < 20% |
| H3 | `consistency` proportion in S1 + S4 is < 0.95 |
| H4 | Any safety violation in S5 under the treatment condition |
| H5 | TLC finds any counterexample to any stated property |
| H6 | Two runs with identical seed and scenario differ in any trace element |

---

## 9. What this design does not test

- It does not test NASA's operational Gateway.
- It does not test any real spacecraft, flight software, or hardware.
- It does not claim that the model's parameters match Gateway's parameters.
- It does not establish that the escalation rules are the ones NASA uses or
  should use.
- It does not establish that safety-derived escalation rules are necessary
  for safety in general — only whether they help in this model.

---

## 10. Freeze protocol

This document is frozen when:

1. All sections above are complete.
2. An independent methodological review has been recorded in
   `docs/METHODOLOGICAL_REVIEW.md`.
3. The freeze date is written at the top of this file.
4. The seed sets are written to `experiments/seeds_pilot.txt` and
   `experiments/seeds_confirmatory.txt`.
5. A SHA-256 digest of this file is recorded in `results/.preregistration.sha256`.

After freeze, any change requires a dated amendment that:

- Does not alter the hypotheses.
- Does not alter the falsification criteria.
- Is itself committed before the affected runs are executed.

---

## 11. Author

Samir Baladi — Ronin Institute / Rite of Renaissance.
ORCID: 0009-0003-8903-0029.
