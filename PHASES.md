# NASA Gateway — Project Phases

This repository hosts a two-phase research programme. The phases are kept
strictly separate: Phase I is a documentary analysis; Phase II is an
experimental study. Neither phase claims to validate NASA's operational
Gateway system.

---

## Phase I — Documentary and Architectural Analysis

**Status:** Complete (v1.0.0, 2026-11-26)

**Nature:** Documentary research. Audits the traceability of publicly
documented Gateway mechanisms. It makes claims about documents, never about
implementation.

**Deliverables:** manuscript (~6,829 words), 6 figures, 3 analytical CSV
files, 49 validation tests, Zenodo + Figshare records.

**Location in this repository:** root (`paper/`, `figures/`, `data/`,
`docs/`, `tests/`, `scripts/`, `sources/`, and the Netlify site).

**Result:** The reviewed public documentation does not establish a complete
traceability chain from hazard-derived autonomy boundaries to specific MSM
decision and escalation rules and their corresponding verification
properties.

---

## Phase II — Experimental Modeling and Formal Validation

**Status:** Pre-registration stage (v2.0.0-experimental, in progress)

**Nature:** Experimental research. Builds an independent research model
*inspired by* the MSM–VSM interface, and tests whether safety-derived
escalation rules preserve system safety and decision consistency under
faults. It does **not** test NASA's operational Gateway.

**Location in this repository:** `phase2_experimental/`.

**Pre-registration principle:**

> The experimental design must be fixed before the implementation begins,
> and the implementation must not redefine the hypotheses it is supposed to
> test.

**Deliverables (planned):** pre-registration document, hypotheses with
falsification criteria, Python model, TLA+ specification, five fault
scenarios, pilot and confirmatory runs, statistical analysis, and a
Phase II manuscript.

---

## NASA Operational Systems

**Status:** Out of scope for both phases.

Neither phase tests, models, or validates NASA's operational Gateway. All
findings concern either public documentation (Phase I) or an independent
research model (Phase II). The distinction is maintained throughout.
