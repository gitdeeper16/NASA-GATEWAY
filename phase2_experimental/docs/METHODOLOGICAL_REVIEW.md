# Methodological Review — Phase II

**Reviewer:** Samir Baladi (self-review; see §8 for the limitation this implies).
**Date:** 2026-11-27.
**Version reviewed:** 2.0.0-experimental.
**Documents reviewed:** `PREREGISTRATION.md` (draft), `HYPOTHESES.md` (draft).
**Purpose:** this review is the condition required by `PREREGISTRATION.md`
§10.2 before the design may be frozen. It does not approve the design as
correct; it records whether the design is *internally coherent, falsifiable,
and separated from Phase I and from NASA's operational system*.

---

## 1. Review scope

This review addresses six questions, in the order in which they can
invalidate the design:

| § | Question | If the answer is "no" |
|---|---|---|
| 2 | Is the experimental unit well-defined and independent enough to support the tests? | H1–H4 are uninterpretable |
| 3 | Is the pilot/confirmatory separation real and enforced? | H1–H4 are contaminated by calibration |
| 4 | Are the statistical tests appropriate to the data and the unit? | H1–H4 are miscomputed |
| 5 | Is each hypothesis falsifiable with a pre-stated criterion? | H1–H6 are unfalsifiable |
| 6 | Is the model/operational boundary stated and respected? | the phase's claims are inflated |
| 7 | Is the transition from Phase I (documentary) to Phase II (experimental) methodologically licensed? | the project's logic is broken |

---

## 2. Independence of the experimental unit

**Question.** Is one run a defensible unit of analysis?

**Assessment.** Partially. A run is a clean unit *within* a scenario: the
model is deterministic (H6), the seed is fixed, and the condition is fixed.
But runs *within* a scenario share a scenario definition, so they are not
independent across the scenario dimension. `PREREGISTRATION.md` §5.4 states
this explicitly and §7.1 addresses it by testing **at the scenario level**
and applying Holm–Bonferroni across the five scenario-level tests.

**Residual risk.** A scenario-level test with 80 seeds per condition has
80 runs per cell, which is adequate for a Mann–Whitney U test of moderate
effect size, but the scenario definition itself is a single fixed object.
The result generalises to *this scenario*, not to a population of
scenarios. This is a scope limitation, not a flaw, and it is stated in
`PREREGISTRATION.md` §9.

**Verdict.** Adequate, provided §5.4 and §9 remain in the manuscript
verbatim.

---

## 3. Pilot / confirmatory separation

**Question.** Is the separation enforced at the file level and at the
seed level?

**Assessment.** Yes, in three independent ways:

1. **Seed disjointness** — pilot seeds and confirmatory seeds are written
   to separate files (`experiments/seeds_pilot.txt`,
   `experiments/seeds_confirmatory.txt`) at freeze time, and the two sets
   are required to be disjoint (§5.3).
2. **File-level separation** — pilot results live only in
   `results/pilot/`; confirmatory only in `results/confirmatory/`;
   `tests/test_separation.sh` is required to reject any confirmatory
   analysis that reads from `results/pilot/`.
3. **Amendment rule** — pilot observations may inform only *fault
   magnitude calibration*, and only via a dated amendment recorded
   **before** the confirmatory stage begins (§5.3). They may not inform
   hypotheses, tests, or thresholds.

**Residual risk.** The amendment rule is a procedural control, not a
technical one. It relies on the author recording amendments honestly and
before the affected runs. This is the standard limit of pre-registration
in single-author work and is stated in §8 below.

**Verdict.** Adequate.

---

## 4. Appropriateness of the statistical tests

**Question.** Are the chosen tests correct for the data and the unit?

**Assessment.** Yes, with two notes.

- **H1, H2 — Mann–Whitney U.** Correct. `safety_violations` and
  `secondary_damage` are counts, bounded below by zero, not plausibly
  normal. Mann–Whitney U tests stochastic dominance, which is the right
  question ("does treatment tend to produce fewer violations than
  control?"). Cohen's *d* is reported alongside *p*, which is correct
  practice.
- **Multiplicity (H1).** Holm–Bonferroni across five scenario-level tests
  is appropriate and conservative. Stated in §7.1.
- **H3 — proportion test.** Correct. `consistency` is binary; the
  proportion test on S1 + S4 combined tests whether the treatment
  preserves consistency at the stated rate. The threshold (0.95) is
  pre-stated.
- **H4 — exact binomial.** Correct. `safe_mode_reached` is binary and S5
  has a fixed number of runs; the exact binomial avoids the normal
  approximation that would be unjustified at this sample size for a
  near-1 proportion.

**Note 1.** The design does not state a power analysis. A power analysis
would require an assumed effect size, which is not available before the
pilot. The design therefore reports effect sizes and confidence intervals
rather than claiming a power guarantee. This is honest but should be
stated in the manuscript as a limitation.

**Note 2.** H2 uses a *relative reduction* threshold (20%) rather than a
standardised effect size, because the baseline rate of secondary damage in
S2 is a count whose scale is defined by the scenario. This is defensible
but should be justified in the manuscript by reference to the scenario
definition.

**Verdict.** Adequate, with Notes 1 and 2 carried into the manuscript.

---

## 5. Falsifiability of each hypothesis

**Question.** Does each hypothesis have a pre-stated criterion that could,
in principle, be met by data?

**Assessment.** Yes for all six.

| ID | Criterion | Falsifiable? |
|---|---|---|
| H1 | *p* ≥ 0.05 after correction, or *d* < 0.3 | yes — both are computable from run outcomes |
| H2 | relative reduction < 20% | yes |
| H3 | proportion < 0.95 | yes |
| H4 | any violation in S5 under treatment | yes |
| H5 | any TLC counterexample | yes |
| H6 | any differing trace | yes |

**Residual risk.** H5's falsifiability depends on the state space being
fixed at freeze time (§7.3). If the state space is expanded after freeze
to avoid a counterexample, H5 becomes unfalsifiable in practice. The
design fixes the state space in `formal/model_check.sh` at freeze, and
this review records that the state-space file must be hashed at freeze
alongside the design documents.

**Verdict.** Adequate, conditional on hashing `formal/model_check.sh` at
freeze (see §7 below and the freeze protocol).

---

## 6. Model / operational boundary

**Question.** Is the boundary between the research model and NASA's
operational Gateway stated and respected?

**Assessment.** Yes, in four places:

1. `PREREGISTRATION.md` §9 ("What this design does not test").
2. `PREREGISTRATION.md` §12 (three-level separation, structural).
3. `HYPOTHESES.md` H5 ("what H5 does not claim").
4. `README.md` ("What this phase is not").

**Residual risk.** The phrase "inspired by the MSM–VSM interface" is the
only link to Gateway, and it is a conceptual link, not a parametric one.
The design does not claim that any model parameter matches a Gateway
parameter. This is correct, but it must be repeated in the manuscript's
abstract, not only in its limitations section, because a reader who sees
"MSM" and "VSM" may assume a Gateway model.

**Verdict.** Adequate, with the requirement that the manuscript's abstract
state the model/operational boundary explicitly.

---

## 7. The Phase I → Phase II transition

**Question.** Is the move from documentary analysis (Phase I) to
experimental research (Phase II) methodologically licensed, or does it
smuggle a documentary finding into an experimental premise?

**Assessment.** Licensed, but only because of three explicit constraints:

1. Phase II **cites** Phase I as motivation, not as a premise. The
   hypotheses H1–H6 are about the *model*, not about the documents.
2. The rule catalogue (R1–R5) in `HYPOTHESES.md` maps each rule to a
   Phase I reference, but the mapping is a *design choice*, not a *claim*
   that Phase I established those rules as necessary. The manuscript must
   state that the mapping is motivational.
3. No Phase II result may be reported as evidence about Level 3
   (operational). `PREREGISTRATION.md` §12 rule 1.

**Residual risk.** The most likely failure mode is a reader (or the
author, in the discussion section) sliding from "the model with
safety-derived rules had fewer violations" to "safety-derived rules are
the right design for Gateway". The design forbids this slide (§12 rule 1
and rule 3), but the manuscript must actively police it.

**Verdict.** Adequate, conditional on the manuscript's discussion section
repeating §12 rule 1 verbatim.

---

## 8. Limitations of this review

This is a **self-review**. The author of the design is the reviewer. This
is the weakest possible form of methodological review and is recorded as
such. Its function is not to certify the design as correct, but to make
the design's assumptions and residual risks explicit **before** freeze, so
that a later reader can see what was and was not checked.

**What this review does not do:**

- It does not provide independent statistical review.
- It does not provide independent domain review (spacecraft autonomy).
- It does not check the correctness of the TLA+ properties, which do not
  yet exist.
- It does not check the Python model, which does not yet exist.

**What would strengthen it (recorded as future work, not as a blocker):**

- An external reviewer with formal-methods expertise to check the TLA+
  properties after they are written (post-freeze, pre-confirmatory).
- An external reviewer with statistics expertise to check the analysis
  script after it is written (post-freeze, pre-confirmatory).

Neither is required for freeze under §10; both are recorded here so that
the manuscript's limitations section can cite them.

---

## 9. Conditions attached to this review

This review does not block freeze, but attaches four conditions that must
be satisfied at freeze time:

| # | Condition | Where satisfied |
|---|---|---|
| C1 | `formal/model_check.sh` (state space) must be hashed at freeze, alongside `PREREGISTRATION.md` and `HYPOTHESES.md` | §10 freeze protocol (extended) |
| C2 | `experiments/seeds_pilot.txt` and `experiments/seeds_confirmatory.txt` must be disjoint and hashed at freeze | §10.4 |
| C3 | `experiments/control_thresholds.txt` must be written and hashed at freeze | §10.5 |
| C4 | The manuscript must state the model/operational boundary in the abstract, not only in limitations | manuscript (post-confirmatory) |

C1–C3 are satisfied at freeze (next stage). C4 is a manuscript-stage
condition.

---

## 10. Verdict

**The design is internally coherent, falsifiable, and separated from
Phase I and from NASA's operational system, subject to conditions C1–C4.**

**Recommendation:** proceed to freeze, recording C1–C3 in the freeze
digest, and carrying C1–C4 into the manuscript.

---

## 11. Signature

Samir Baladi — Ronin Institute / Rite of Renaissance.
ORCID: 0009-0003-8903-0029.
Date: 2026-11-27.
