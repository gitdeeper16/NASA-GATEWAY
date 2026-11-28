# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] — 2026-11-28

### Added

- **Phase II Independent Evidence Review** — consolidated across four sub-phases:
  - Phase II-bis: baseline records (30 rows, 3 scenarios × 2 conditions × 5 seeds).
  - Phase II-ter: extended cycle-level records (600 JSONL rows, 780 log lines).
  - Phase II-quater: code reading to resolve three contradictions.
  - Phase II-quinquies: final code reading to resolve the remaining `safe=1` contradiction.
- `PHASE_II_CONSOLIDATED_REPORT.md` — unified report with evidence, contradictions, and resolutions.
- `phase2ter_trace_seeded.py` — read-only tracing script using `random.Random(seed)`.
- `phase2ter_trace.jsonl` — 600 cycle-level records.
- `phase2ter_trace.log` — 780-line human-readable log.
- `PHASE_II_QUATER_MANDATE.md` — signed mandate for code reading (Phase II-quater).
- `PHASE_II_QUINQUIES_MANDATE.md` — signed mandate for code reading (Phase II-quinquies).

### Documented (no code change)

- **Contradiction 1**: `escalation_requested_at` is never populated in `_trace_scenario.py` (defect in monitoring script, not engine).
- **Contradiction 2**: `safe=1` in S5 is correct; `run_scenario` produces it via rule R5/R5c. `_trace_scenario.py` does not reproduce it due to a different `RuleView`.
- **Contradiction 3**: `local_recovery_failures=0` while C2 remains unhealthy is consistent with `_execute_local_action` (which contains only `pass` and does not record failure).
- **Seed invariance**: S1/S2/S5 are deterministic in fault injection (`_apply_primary_fault` does not use `rng` in these branches). Seed variance is structurally impossible in these scenarios.

### Unchanged

- No modification to `model/engine.py`, `model/rules.py`, `model/state.py`, or any project source.
- A.3 remains **NOT OPENED**.
- Pilot/Confirmatory remains **not authorized**.

### Known limitations (documented, not fixed)

- `_execute_local_action` does not heal components and does not record failures.
- `_trace_scenario.py` omits `escalation_requested_at = cycle`.
- Scenarios S3 and S4 were not run in Phase II.
- `_propagate_secondary` full body was not read.

---

## [1.0.0] — 2026-11-27

### Added

- Initial public release.
- Phase 1 documentary analysis.
- Phase 2 experimental pipeline (S1, S2, S5).
- `AUTHORS.md`, `CITATION.cff`, `LICENSE`.

---

[1.1.0]: https://github.com/gitdeeper16/NASA-GATEWAY/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/gitdeeper16/NASA-GATEWAY/releases/tag/v1.0.0
