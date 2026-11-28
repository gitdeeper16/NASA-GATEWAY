# Phase 1 — Closed (documentary)

**Date:** 2026-11-28
**Status:** CLOSED (documentary only; not a final freeze on disk)
**Phase 2:** NOT AUTHORIZED
**A.3:** NOT OPENED
**Code modified:** No
**Pilot / Confirmatory:** Not authorized
**Implicit design decision:** None
**Automatic transition:** None

---

## Scope of authorization

Phase 1 authorized the documentary and code review of 8 files, in order:

1. `SPECIFICATION.md`
2. `model/rules.py`
3. `model/engine.py`
4. `model/state.py`
5. `scenarios/S1.yaml`
6. `scenarios/S2.yaml`
7. `scenarios/S5.yaml`
8. `tests/test_unit_*.py` (all existing files)

---

## What was authorized

- Reading only.
- No execution of S1/S2/S5.
- No creation or modification of scripts.
- No simulation of new rule order.
- No Pilot / Confirmatory.
- No opening of A.3.

---

## What was completed

All 8 files were provided and reviewed within the authorized scope.
No execution, no modification, no design inference was made.

---

## What the tests actually cover

Per the review of `tests/test_unit_*.py`:

- `would_violate` is tested on all four constraints and their priority order.
- The S3 boundary → overflow transition is tested at the state-construction
  and function level.
- `_iter_faults` is tested for single-fault and multi-fault compatibility.

## What the tests do NOT cover

- The treatment guard in `_choose_decision`.
- The rule order inside `_choose_decision`.
- `_execute_local_action` behavior.
- The containment chain.
- `candidate_violations_count` semantics.
- `local_recovery_failures` vs `local_recovery_attempts` distinction.
- Full `run_scenario` behavior.

---

## Retained caveat (independently verified content)

The following caveat is retained as part of the documentary closure:

> The detailed content of `SPECIFICATION.md` was not independently verified
> in this context beyond the summary provided. The review of
> `model/rules.py`, `model/engine.py`, `model/state.py`, the scenario files,
> and the unit tests was based on their provided content. No claim of
> independent verification beyond that content is made.

---

## What remains NOT authorized

| Item | Status |
|---|---|
| Phase 2 — diagnostic execution of S1/S2/S5 | NOT AUTHORIZED |
| A.3 opening | NOT OPENED |
| Code modification | NOT AUTHORIZED |
| Pilot | NOT AUTHORIZED |
| Confirmatory | NOT AUTHORIZED |
| Simulation of new rule order | NOT AUTHORIZED |

---

## What is NOT decided

No design decision is implied by this closure. Specifically:

- Rule order is unchanged.
- R3 / R3c / R4 / R4c are not removed, redefined, or reordered.
- `failures` is not redefined.
- `_execute_local_action` is not modified.
- Counters are not modified.
- `treatment_escalations_due_to_guard` is not renamed or replaced.
- No H1-bis claim is made.
- Simulation remains simulation, not observational evidence.

---

## Closing line

**Phase 1 CLOSED (documentary). Phase 2 NOT AUTHORIZED. A.3 NOT OPENED.
No code changed. No implicit decision. No automatic transition.**
