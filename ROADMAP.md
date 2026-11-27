# Roadmap — NASA Gateway v1.0.0

**Project:** NASA Gateway — Safety Assurance & Formal Verification
**Current version:** 1.0.0
**Last updated:** 2026-11-26

---

## Phase I — Documentary Analysis (COMPLETE)

**Status:** ✅ Complete — released as v1.0.0

| Deliverable | Status |
|---|:-:|
| Manuscript (~6,829 words) | ✅ |
| 6 figures (Fig1 … Fig6) | ✅ |
| 3 analytical CSV files | ✅ |
| Methodology & figure provenance docs | ✅ |
| 49 validation tests (49/49 passing) | ✅ |
| Zenodo archival record (`10.5281/zenodo.24559255`) | ✅ |
| Figshare dataset record (`10.6084/m9.figshare.35136991`) | ✅ |
| GitHub repository (`gitdeeper16/NASA-GATEWAY`) | ✅ |
| Project website (`nasa-gateway.netlify.app`) | ✅ |

**Finding:** Public documentation does not establish a complete traceability chain from hazard-derived autonomy boundaries to specific MSM decision and escalation rules and their verification properties.

**Scope caveat:** This finding concerns public documentation only. It makes no claim about the absence of mechanisms in implementation.

---

## Phase II — Experimental / Simulation (NOT STARTED)

**Status:** ⏸ Not started — out of scope for v1.0.0

Phase II would require executable artefacts that are not part of the documentary study:

| Planned area | Description |
|---|---|
| Reference MSM–VSM model | An abstract executable model of the interface, for illustrative purposes only |
| Sample AGC contracts | Toy assume-guarantee contracts encoding example decision rules |
| Property demonstrations | Model-checking demos (TLA+/Spin) of sample properties |
| Runtime monitor prototype | Illustrative R2U2-style monitor over a synthetic timeline |
| Synthetic data | Generated telemetry for demonstration, not flight data |

> **Caveat:** Any Phase II artefact would be **illustrative**, not a model of Gateway. It would not constitute evidence about NASA's implementation.

---

## Phase III — Community Review (PLANNED)

**Status:** ⏸ Not started

| Planned activity | Description |
|---|---|
| Independent review | Solicit external review of the documentary method and findings |
| Response to review | Publish reviewer comments and author responses |
| Versioned updates | Release v1.x if corrections or additions are warranted |
| Related-work expansion | Extend the source register if new public documents are located |

---

## Publication mirrors

| Platform | Identifier | Status |
|---|---|---|
| Zenodo | `10.5281/zenodo.24559255` | ✅ Published |
| Figshare | `10.6084/m9.figshare.35136991` | ✅ Published |
| GitHub | `gitdeeper16/NASA-GATEWAY` | ✅ Public |
| Website | `nasa-gateway.netlify.app` | ✅ Live |

---

## What is explicitly NOT planned

- Claims about NASA's internal implementation.
- A full inventory of Gateway artefacts.
- A redesign proposal or architectural recommendation.
- Any assertion that Gateway autonomy is unsafe.

---

© 2026 Samir Baladi · Ronin Institute / Rite of Renaissance · CC-BY-4.0
