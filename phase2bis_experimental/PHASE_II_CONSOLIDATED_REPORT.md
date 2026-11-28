# Phase II Consolidated Report — Evidence, Contradictions, Resolutions

**Date**: 2026-11-28
**Phases covered**: II-bis, II-ter, II-quater, II-quinquies
**Report type**: Documentary consolidation. No execution, no modification, no A.3.
**Author**: Samir Baladi (Principal Investigator)

---

## 1. Scope

This report consolidates the evidence gathered across four phases of independent review of the Phase 2 experimental pipeline (S1, S2, S5) in the NASA-GATEWAY project.

**What was examined**:
- Original Phase II-bis records (30 rows: 3 scenarios × 2 conditions × 5 seeds).
- Phase II-ter extended records (600 JSONL rows: 30 runs × 20 cycles).
- Code reading of `model/engine.py`, `model/rules.py`, `_trace_scenario.py`, `_trace_phase2.py` (READ-ONLY).

**What was NOT examined**:
- Scenarios S3 and S4 (not run).
- `_propagate_secondary` full body (not read).
- `_execute_local_action` design intent (cannot be determined from code alone).
- Any modification to project code.

---

## 2. Evidence Inventory

| Source | Content | Status |
|---|---|---|
| Phase II-bis records | 30 summary rows | OBSERVED |
| Phase II-ter JSONL | 600 cycle-level rows | OBSERVED |
| Phase II-ter log | 780 lines | OBSERVED |
| Code: `model/engine.py` | Functions: `_choose_decision`, `_update_state`, `_execute_local_action`, `_apply_primary_fault`, `_record_escalation_correctness`, `run_scenario`, `_seed_to_int` | READ |
| Code: `model/rules.py` | Polarity maps only | PARTIAL READ |
| Code: `_trace_scenario.py` | Full file (109 lines) | READ |
| Code: `_trace_phase2.py` | `safe` field reference only | PARTIAL READ |

---

## 3. What Is Established [OBSERVED]

### 3.1 Baseline Results (Phase II-bis)

| Scenario | att | guard | sv | cand | esc | vsm_ack | contain | 2nd | safe | avail |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 (both conditions) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2.0 |
| S2 (both conditions) | 0 | 0 | 0 | 0 | 18 | 1 | 1 | 0 | 0 | 4.0 |
| S5 (both conditions) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2.0 |

**Treatment = Control** in every field, in every scenario. [OBSERVED]

### 3.2 Seed Invariance (Phase II-ter)

- All five seeds produce identical `Final` results within each (scenario, condition) pair.
- 0/20 cycles differ across seeds in S2/treatment.
- This holds even with `random.Random(seed)` in `phase2ter_trace_seeded.py`.

**Root cause** [OBSERVED from code]: `_apply_primary_fault` (model/engine.py:100-125) does not use `rng` in the `component_failure` and `shared_resource_failure` branches. Fault injection is deterministic in these scenarios. Seed variance is structurally impossible in S1, S2, S5.

### 3.3 Escalation/Containment Sequence in S2

From Phase II-ter events (S2/treatment/382857):
- Cycle 2: primary fault `shared_resource_failure` on SR1 (severity=0.8).
- Cycle 2: `escalation_requested=True`, `escalations_correct=1`.
- Cycle 3: `vsm_acknowledged_at=3`, `containment_effective_at=3`.
- Cycles 4–19: continued escalation, `escalations_correct` increments to 18.

**Secondary damage = 0** [OBSERVED]: containment effective at cycle 3 precedes secondary propagation (which starts at cycle 3).

### 3.4 Escalation Correctness

- `escalations_correct` increments with each escalate decision.
- `escalations_false=0`, `escalations_missed=0` in S2.
- `executed_violation_log=[]` in all scenarios.

---

## 4. The Three Contradictions and Their Resolutions

### Contradiction 1 — `escalation_requested_at` always None

**Resolution** [OBSERVED from code]:
- `_trace_scenario.py` (lines 74-77) omits `state.escalation_requested_at = cycle` when handling `escalate`.
- `model/engine.py` (lines 437-438) includes this assignment.
- Phase II-ter records were produced by `_trace_scenario.py` — hence `None`.
- This is a defect in the monitoring script, not in the engine.

### Contradiction 2 — `safe=1` in S5 without `decision=safe_mode` in Phase II-ter

**Resolution** [OBSERVED from code]:
- `_choose_decision` returns `safe_mode` when rule R5 (treatment) or R5c (control) fires first.
- `model/rules.py` lines 74 and 133 map `"R5"` and `"R5c"` to `"safe_mode"`.
- `_trace_phase2.py` reads `safe_mode_reached` from `run_scenario`'s returned dict (line 26).
- Phase II-bis `safe=1` in S5 is correct — `run_scenario` produced it.
- Phase II-ter did not show `decision=safe_mode` in S5 because `_trace_scenario.py` constructs a different `RuleView` (missing `escalation_requested_at` propagation and possibly different `local_recovery_path_available`), so R5/R5c did not fire.

### Contradiction 3 — `local_recovery_failures=0` while C2 remains unhealthy

**Resolution** [OBSERVED from code]:
- `_apply_primary_fault` (model/engine.py:137) increments `local_recovery_failures` **only** when a fault of type `local_recovery_failure` is injected.
- Scenarios S1/S5 inject `component_failure`, not `local_recovery_failure` — hence `failures=0`.
- `_execute_local_action` (model/engine.py:306-320) does not heal the component (contains only `pass` inside the `if` block). It also does not record a failure.
- **The component remains unhealthy after `resolve_local` by design of the current code** (or due to incomplete implementation — cannot be determined from code alone).

---

## 5. What Remains [UNKNOWN]

1. **Design intent of `_execute_local_action`**: whether the empty `if` block is intentional (a model that acknowledges recovery attempts without simulating success) or incomplete (a placeholder for future healing logic). Cannot be determined from code alone.
2. **Behavior of S3 and S4**: not run under any phase. Any claim about seed invariance or contradiction resolution in those scenarios is outside the evidence base.
3. **Full body of `_propagate_secondary`**: not read. The claim "containment precedes secondary propagation" is inferred from cycle numbers in events, not from code.
4. **Full body of `model/rules.py`**: only polarity maps were read. The firing conditions for R5/R5c in S5 under `_trace_scenario.py` vs `run_scenario` were not traced line-by-line.

---

## 6. Status

| Item | Status |
|---|---|
| Phase II-bis | CLOSED |
| Phase II-ter | CLOSED |
| Phase II-quater | CLOSED |
| Phase II-quinquies | CLOSED |
| Consolidated Report | **This document** |
| A.3 | NOT OPENED |
| Code modification | None |
| Pilot/Confirmatory | Not authorized |

**A.3 NOT OPENED. No code changed. No automatic transition.**

---

## 7. Author

**Samir Baladi**
Principal Investigator, Author, and Protocol Designer
Ronin Institute / Rite of Renaissance

| | |
|---|---|
| Email | gitdeeper@gmail.com |
| ORCID | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) |
| GitHub | [gitdeeper16](https://github.com/gitdeeper16) |
| Website | [nasa-gateway.netlify.app](https://nasa-gateway.netlify.app) |

**Project identifiers**:

| Resource | Identifier |
|---|---|
| Zenodo DOI | `10.5281/zenodo.24559255` — https://doi.org/10.5281/zenodo.24559255 |
| Figshare DOI | `10.6084/m9.figshare.35136991` — https://doi.org/10.6084/m9.figshare.35136991 |
| GitHub | https://github.com/gitdeeper16/NASA-GATEWAY |
| Website | https://nasa-gateway.netlify.app |

**Citation**:

Baladi, S. (2026). *The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation* (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.24559255

---

**Author signature**: Samir Baladi
**Signature date**: 2026-11-28
