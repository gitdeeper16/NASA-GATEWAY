<div align="center">

# NASA Gateway — Safety Assurance & Formal Verification

### A Traceability Gap in Public Documentation

*A documentary analysis of safety-derived autonomy boundaries and formal verification mechanisms at the MSM–VSM interface in NASA Gateway autonomous systems.*

[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24559255.svg)](https://doi.org/10.5281/zenodo.24559255)
[![Figshare DOI](https://img.shields.io/badge/Figshare-10.6084%2Fm9.figshare.35136991-orange)](https://doi.org/10.6084/m9.figshare.35136991)
[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![GitHub](https://img.shields.io/badge/GitHub-gitdeeper16%2FNASA--GATEWAY-181717?logo=github&logoColor=white)](https://github.com/gitdeeper16/NASA-GATEWAY)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](CHANGELOG.md)
[![Figures](https://img.shields.io/badge/Figures-6-blue)](#figures)
[![Words](https://img.shields.io/badge/Manuscript-~6%2C800%20words-blue)](#manuscript)

[Website](https://nasa-gateway.netlify.app) ·
[Paper (MD)](paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.md) ·
[Paper (PDF)](paper/NASA_Gateway_Traceability_Gap_Research_Paper_v1.0.0.pdf) ·
[Zenodo](https://doi.org/10.5281/zenodo.24559255) ·
[Figshare](https://doi.org/10.6084/m9.figshare.35136991) ·
[GitHub](https://github.com/gitdeeper16/NASA-GATEWAY) ·
[Figures](figures/) ·
[Data](data/)

</div>

---

> [!IMPORTANT]
> **Status (v1.0.0):** The documentary analysis is complete. The manuscript (~6,800 words) identifies a traceability gap in public documentation at the MSM–VSM interface.
>
> **Scope:** This finding concerns **public documentation only**. It does not claim that mechanisms are absent from implementation.

## Contents

- [Overview](#overview)
- [Central question](#central-question)
- [Research questions](#research-questions)
- [Scope](#scope)
- [Methodological framework](#methodological-framework)
- [Evidence classification](#evidence-classification)
- [Findings](#findings)
- [Figures](#figures)
- [Repository structure](#repository-structure)
- [Key sources](#key-sources)
- [What this repository does not claim](#what-this-repository-does-not-claim)
- [Research limitations](#research-limitations)
- [Citation](#citation)
- [Author](#author)
- [License](#license)

---

## Overview

**NASA Gateway — Safety Assurance & Formal Verification** is a documentary study examining whether safety-derived boundaries of local autonomy can be traced to formally verifiable decision and escalation rules at the interface between Module System Managers (MSMs) and the Vehicle System Manager (VSM) in NASA Gateway.

The study identifies two independently documented pathways:

- a **safety-assurance pathway** (hazard analysis → safety requirements → autonomous functions → authority boundaries)
- a **formal-verification pathway** (software requirements → AGC contracts → formal models → runtime verification via R2U2)

> **This study does not propose a new architecture.** It treats publicly documented Gateway mechanisms as objects whose *traceability* is audited.

## Central question

> How are safety-derived boundaries of local autonomy translated into formally verifiable decision and escalation rules at the interface between Module System Managers (MSMs) and the Vehicle System Manager (VSM) in NASA Gateway?

**Sub-question:** Does the publicly available documentation establish a demonstrable requirement-to-decision-to-verification traceability relationship at the MSM–VSM interface?

| # | Component | Focus | Status |
|:-:|---|---|:-:|
| 1 | **Safety-assurance pathway** | Hazard analysis, controls, autonomy requirements | ✅ Documented publicly |
| 2 | **Formal-verification pathway** | AGC contracts, model checking, R2U2 | ✅ Documented publicly |
| 3 | **Traceability chain** | Connection between the two pathways | ⚠️ Not established in public docs |

## Research questions

| ID | Question | Status |
|:-:|---|:-:|
| **RQ1** | How does Gateway distribute control responsibilities between MSM and VSM? | ✅ Documented |
| **RQ2** | What safety requirements establish the need for autonomous hazard control? | ✅ Documented (L2-GW-0199) |
| **RQ3** | What formal verification mechanisms are documented for Gateway autonomy? | ✅ Documented (AGC, R2U2, TLA+) |
| **RQ4** | Does public documentation establish a complete traceability chain? | ⚠️ **Not established** |

## Scope

**In scope**

- Documentary analysis of public NASA Gateway documentation
- Safety-assurance pathway: DSG-RQMT-001, GLS-RQMT-001, GLS-006
- Formal-verification pathway: AGC, TLA+, Spin, R2U2
- MSM–VSM interface
- Traceability from hazard to verification evidence

**Out of scope**

- Implementation claims (not documented publicly)
- Internal NASA artifacts (ITAR/export-controlled)
- Architectural redesign or recommendations
- Performance evaluation
- Operational deployment verification

**Explicit non-goals**

- Proving that NASA lacks any mechanism
- Proving that Gateway autonomy is unsafe
- Proving that the traceability gap reflects an implementation deficiency

## Methodological framework

The analysis applies an **eight-step traceability sequence**:

| Step | Description | Evidence Status |
|:-:|---|:-:|
| 1 | Hazard identified | ✅ Documented |
| 2 | Safety requirement derived | ✅ Documented (L2-GW-0199) |
| 3 | Autonomous function allocated | ✅ Documented |
| 4 | Authority boundary defined | ⚠️ Partial |
| 5 | **Decision/escalation rule specified** | ❌ **Not established** |
| 6 | Formal property represented | ⚠️ Partial (AGC examples) |
| 7 | Verification evidence produced | ⚠️ Partial (R2U2, TLA+) |
| 8 | Operational response documented | ⚠️ Partial (FDIR docs) |

## Evidence classification

Six evidence categories are used throughout the analysis:

| Category | Purpose |
|---|---|
| **Requirement evidence** | What a system is required to do |
| **Architectural evidence** | Intended organization and responsibilities |
| **Formal specification evidence** | Properties or contracts |
| **Verification evidence** | Application of verification methods |
| **Operational evidence** | Behavior in operational context |
| **Experimental evidence** | Concept demonstration in research environment |

## Findings

| Finding | Status |
|---|:-:|
| Gateway distributes autonomy across MSM and VSM | ✅ Documented |
| Local autonomy is a formal safety obligation (L2-GW-0199) | ✅ Documented |
| Distributed fault management is described | ✅ Documented |
| AGC and R2U2 provide formal verification mechanisms | ✅ Documented |
| Contracts and Fault Management are complementary | ✅ Documented |
| **Complete traceability chain from hazard to verification** | ❌ **Not established in public docs** |

> [!NOTE]
> "Not established in public documentation" is not the same as "absent from implementation." The manuscript maintains this distinction throughout.

## Figures

| Figure | File | Location in Paper |
|:-:|---|---|
| 1 | `Fig1_Traceability_Chain_Gap.png` | Section 5.3 |
| 2 | `Fig2_Two_Pathways_Interface.png` | Section 5.1 |
| 3 | `Fig3_MSM_VSM_Architecture.png` | Section 4.1 |
| 4 | `Fig4_Evidence_Classification_Taxonomy.png` | Section 3.4 |
| 5 | `Fig5_Gateway_Lunar_Orbit.png` | Section 1 |
| 6 | `Fig6_Assurance_Case_GSN_Structure.png` | Section 5.3 |

## Repository structure

```text
NASA-GATEWAY/
├── README.md
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── INVENTORY.md
├── LICENSE
├── PROJECT_SUMMARY.txt
├── ROADMAP.md
├── VERSION
├── manifest.json
├── netlify.toml
├── scientific_state.json
├── .gitignore
├── .gitattributes
│
├── paper/
│   ├── NASA_Gateway_Safety_Assurance_and_Formal_Verification.md
│   └── NASA_Gateway_Traceability_Gap_Research_Paper_v1.0.0.pdf
│
├── figures/            # Fig1 … Fig6 (PNG)
│
├── sources/            # Referenced NASA documents (links)
│
├── data/               # Analytical artifacts (CSV)
│   ├── traceability_matrix.csv
│   ├── evidence_classification.csv
│   └── requirement_to_property.csv
│
├── docs/               # Methodology, glossary
│   ├── methodology_notes.md
│   └── figure_provenance.md
│
├── scripts/            # Validation and build scripts
│   ├── validate.py
│   ├── build_pdf.sh
│   └── build_latex.sh
│
└── tests/              # 49 validation tests
    ├── run_all.sh
    ├── test_structure.sh
    ├── test_metadata.sh
    ├── test_data.sh
    ├── test_figures.sh
    └── test_content.sh
```

Key sources

ID Source Role
S1 NASA DSG-RQMT-001 (2019) Gateway System Requirements
S2 NASA GLS-RQMT-001 Logistics Services Requirements
S3 NASA GLS-006 (2019) Safety Data Package
P1 When the Eyes Don't Have It (2020) Locus of control / control authority
P2 Using AGCs for Operational Verification (2023) Formal verification pathway
P3 Gateway at the Crossroads (2023) Distributed fault management
P4 Trustworthy Autonomy for VSM (2023) Domain of Control
P5 MAST (2019) Distributed fault management
P6 Gateway Risk-Reduction (2022) MSM–VSM scenarios
P7 Refueling Systems (2024) Ground authorization + autonomy
P8 Stochastic Timeline Validation (2026) R2U2 + AGC integration

What this repository does not claim

· ✖ That NASA lacks a traceability mechanism in implementation.
· ✖ That Gateway autonomy is unsafe or deficient.
· ✖ That the public documentation gap implies implementation failure.
· ✖ Any causal claim beyond the executed documentary analysis.
· ✖ A complete inventory of all internal NASA artifacts.

Research limitations

# Threat Description
L1 Access to internal documents DSG-SPEC-VSM-003, MSM ICD, DSG-RQMT-011, DSG-RPT-001 not publicly available
L2 Requirements vs. implementation Requirements establish obligations, not implementations
L3 Experimental evidence MAST and risk-reduction are not operational Gateway
L4 Module-specific requirements GLS-RQMT-001 applies to Logistics Module only
L5 Incomplete public verification coverage Published AGC examples are not exhaustive
L6 Author-on-author reasoning No independent review to date

Citation

Machine-readable metadata is in CITATION.cff.

APA

Baladi, S. (2026). The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.24559255

<details>
<summary><b>BibTeX</b></summary>

```bibtex
@misc{baladi2026nasagateway,
  author    = {Baladi, Samir},
  title     = {The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24559255},
  url       = {https://doi.org/10.5281/zenodo.24559255}
}
```

</details>

Author

Samir Baladi — Principal Investigator, Author, and Protocol Designer
Ronin Institute / Rite of Renaissance

 
Email gitdeeper@gmail.com
ORCID 0009-0003-8903-0029
Website nasa-gateway.netlify.app
GitHub gitdeeper16/NASA-GATEWAY

License

Documentation and paper: CC BY 4.0 (see LICENSE).

---

<div align="center">

NASA Gateway — Safety Assurance & Formal Verification v1.0.0

© 2026 Samir Baladi · Ronin Institute / Rite of Renaissance

</div>
