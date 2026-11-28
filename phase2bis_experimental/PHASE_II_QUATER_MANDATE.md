# Phase II-quater Mandate — Code Reading Only (READ-ONLY)

**Date**: 2026-11-28
**Previous phase**: Phase II-ter (complete — 600 JSONL rows, 780 log lines)
**Mandate type**: Code reading only. No execution, no modification, no writing to project files.

---

## 1. Objective

Explain three contradictions documented in Phase II-ter that cannot be resolved from records alone.

---

## 2. The Three Contradictions

### Contradiction 1 — `escalation_requested_at` is never populated

**Evidence** [OBSERVED in Phase II-ter]:
- S2/treatment/382857: `esc_req=True` from cycle 2 through 19.
- But `escalation_requested_at=None` in all twenty rows.
- Meanwhile `vsm_acknowledged_at=3` and `containment_effective_at=3` work correctly.

**Question**: Where is `state.escalation_requested_at` supposed to be set? Is it a code defect or intended behavior?

**Functions permitted to read**:
- `model/engine.py` — any location referencing `escalation_requested_at`.
- `model/engine.py` — `_record_escalation_correctness` (if it exists).
- `model/engine.py` — any location setting `state.escalation_requested = True`.

---

### Contradiction 2 — `safe=1` in S5 without `decision=safe_mode`

**Evidence** [OBSERVED in Phase II-ter]:
- S5/treatment/382857: `decision` in every cycle is either `resolve_local` (cycle 3) or `noop` (remainder).
- No cycle has `decision=safe_mode`.
- Yet Phase II-bis recorded `safe=1` in S5.

**Question**: How is `state.safe_mode_reached` set in S5? Via `_choose_decision`, `_update_state`, or elsewhere?

**Functions permitted to read**:
- `model/engine.py` — `_choose_decision`.
- `model/engine.py` — `_update_state`.
- `model/engine.py` — any location referencing `safe_mode_reached` or `safe_mode`.

---

### Contradiction 3 — `local_recovery_failures=0` while C2 remains unhealthy

**Evidence** [OBSERVED in Phase II-ter]:
- S1/treatment/382857: `resolve_local` at cycle 3, `C2=0` from cycle 3 through 19.
- `attempts=1`, `failures=0`.
- S5/treatment/382857: same pattern.

**Question**: Does `_execute_local_action` fail to heal C2 without recording `local_recovery_failures`? Or does it never attempt healing in this case?

**Functions permitted to read**:
- `model/engine.py` — `_execute_local_action`.
- `model/engine.py` — any location referencing `local_recovery_failures`.

---

## 3. Mandate Boundaries

**Permitted**:
- Reading `model/engine.py` (only the functions listed above, or directly related sections).
- Reading `scenarios/S1.yaml`, `scenarios/S2.yaml`, `scenarios/S5.yaml` if needed to interpret behavior.
- Reading `run_scenario` (in `_trace_phase2.py` or wherever it resides) to understand data flow.

**Forbidden**:
- Executing any script.
- Modifying any file.
- Writing any file to the project (except the review report if requested).
- Opening A.3.
- Running Pilot/Confirmatory.
- Issuing design recommendations.
- Inferring causal relationships beyond what the code demonstrates.

---

## 4. Required Outputs

A report distinguishing:
- **[OBSERVED from code]**: what the code explicitly demonstrates.
- **[UNKNOWN]**: what the code does not demonstrate (requires experiment or additional data).

For each of the three contradictions, answer:
1. Where is the field supposed to be set?
2. Is it a code defect or intended behavior?
3. What prevents confirmation from code alone?

---

## 5. State at Signing

| Item | Status |
|---|---|
| Phase II-bis | CLOSED |
| Phase II-ter | Complete (pending documentary closure) |
| Phase II-quater | **OPEN under this mandate** |
| A.3 | NOT OPENED |
| Code modification | None |
| Pilot/Confirmatory | Not authorized |

**A.3 NOT OPENED. No code changed. No automatic transition.**

---

## 6. Authorizer

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

**Authorizer signature**: Samir Baladi
**Signature date**: 2026-11-28
