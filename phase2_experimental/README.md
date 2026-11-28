# Phase II — Experimental Validation of Safety-Derived Autonomy Boundaries in Multi-Level Autonomous Systems

**Status:** Pre-registration stage.
**Version:** 2.0.0-experimental.
**Scope:** Independent research model, inspired by the MSM–VSM interface. Not a model of NASA's operational Gateway.

---

## What this phase is

An experimental study that builds a small, executable research model of a
two-level autonomous system (a Module System Manager and a Vehicle System
Manager), populates it with safety-derived escalation rules, and tests
whether those rules preserve system safety and decision consistency under
fault conditions.

## What this phase is not

- Not a simulation of Gateway.
- Not a validation of NASA's operational system.
- Not a claim that Phase II proves Phase I.
- Not a performance benchmark of any real spacecraft.

## Why Phase II is separate from Phase I

Phase I is documentary: it audits the traceability of public documents.
Phase II is experimental: it tests hypotheses on a constructed model. The
two phases share a conceptual vocabulary (MSM, VSM, safety constraints,
escalation rules, formal verification), but they answer different questions.

| Phase | Unit of analysis | Claim type |
|---|---|---|
| Phase I | The document | What public documents do and do not establish |
| Phase II | The research model | What safety-derived escalation rules do under faults |
| NASA operational | The flight system | Out of scope for both phases |

## Pre-registration principle

> The experimental design must be fixed before the implementation begins,
> and the implementation must not redefine the hypotheses it is supposed to
> test.

This principle governs every artefact in this directory. The design
documents (`PREREGISTRATION.md`, `HYPOTHESES.md`) are frozen before any
Python or TLA+ file is written.

## Directory layout

```

phase2_experimental/
├── README.md                 # this file
├── PREREGISTRATION.md        # fixed experimental design (frozen before code)
├── HYPOTHESES.md             # H1–H6 with falsification criteria
├── model/                    # Python model (written only after freeze)
├── formal/                   # TLA+ specification (written only after freeze)
├── scenarios/                # five fault scenarios (YAML)
├── experiments/              # pilot and confirmatory runners
├── results/                  # pilot/ and confirmatory/
├── tests/                    # determinism, formal, scenario, separation
├── docs/                     # methodology, threats to validity, traceability
└── paper/                    # Phase II manuscript (planned)

```

## Planned deliverables

| Deliverable | Status |
|---|---|
| Pre-registration document | in progress |
| Hypotheses H1–H6 with falsification criteria | in progress |
| Independent methodological review | pending |
| Python model | not started (blocked on freeze) |
| TLA+ specification | not started (blocked on freeze) |
| Five fault scenarios | not started (blocked on freeze) |
| Pilot runs (200) | not started |
| Confirmatory runs (800) | not started |
| Statistical analysis | not started |
| Phase II manuscript | not started |

## Link to Phase I

Phase II cites Phase I as its motivating documentary result. It does not
inherit Phase I's claims. In particular, Phase II does not assert that
NASA's implementation lacks any mechanism; it tests whether a class of
escalation rules, when specified and verified, preserves safety in a
constructed system.

See the root [`PHASES.md`](../PHASES.md) for the full two-phase statement.
