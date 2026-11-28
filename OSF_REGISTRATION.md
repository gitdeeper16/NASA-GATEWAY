# NASA Gateway: A Traceability Gap in Public Documentation (v1.1.0)

---

**Registration DOI:** [10.17605/OSF.IO/FN2QW](https://doi.org/10.17605/OSF.IO/FN2QW)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 28, 2026, 1:33 PM
**Date Registered:** Nov 28, 2026, 1:33 PM
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `README.md`
- `CHANGELOG.md`
- `NASA_Gateway_Traceability_Gap_Research_Paper_v1.0.0.pdf`

---

## Overview

### Research questions or hypotheses

This study addresses four research questions concerning NASA Gateway's publicly documented safety assurance and formal verification mechanisms at the MSM–VSM interface:

- **RQ1:** How does Gateway distribute control responsibilities between Module System Managers (MSMs) and the Vehicle System Manager (VSM)?
- **RQ2:** What safety requirements establish the need for autonomous hazard control, and how are they documented in public sources?
- **RQ3:** What formal and runtime verification mechanisms are documented for Gateway autonomy (e.g., Assume-Guarantee Contracts, R2U2, TLA+)?
- **RQ4:** Does the publicly available documentation establish a complete traceability chain from safety-derived autonomy boundaries to formally verifiable decision and escalation rules?

**Hypothesis (for RQ4):** The public documentation does not establish a complete traceability chain. This hypothesis is falsifiable: it would be refuted if a reviewed public document explicitly links a hazard-derived autonomy boundary to a specific decision/escalation rule and its corresponding verification property.

The study does not test causal relationships. It tests the presence or absence of documentary links.

### Foreknowledge of data or evidence

Authors have observed the data, but have not performed the proposed analyses. At least some of the data that will be used for this analysis plan has been accessed and observed by the authors. The authors have sufficiently observed relevant evidence to influence their analysis decisions or conclusions. However, the authors have not yet performed any of the proposed analyses in this plan and will not do so until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

The study is a documentary analysis. The documents reviewed (NASA requirements, safety data packages, technical presentations, and peer-reviewed papers) are publicly available. The author has read these documents for the v1.0.0 analysis. For this registration, the following steps have been taken to reduce the risk of unintended influences:

1. The eight-step traceability sequence was specified before the Phase II review.
2. The Phase II review is limited to the experimental pipeline (Phase II-bis, II-ter, II-quater, II-quinquies), not to the documentary analysis itself.
3. No code was modified during the Phase II review.
4. Three contradictions were resolved through code reading alone, without re-running experiments.
5. The seed invariance was established as structural (deterministic fault injection), not as an artifact of a fixed random seed.
6. A.3 remains NOT OPENED.
7. Pilot/Confirmatory remains not authorized.

The Phase II review is documented in `PHASE_II_CONSOLIDATED_REPORT.md` and in the `phase2bis_experimental/` artifacts. The review was conducted under signed mandates (`mandates/mandate_ii_quater.md`, `mandates/mandate_ii_quinquies.md`).

No data were generated for this registration. The registration documents a planned review of already-existing experimental artifacts.

---

## Research Design

### Study type

Descriptive study: Describing some features of a dataset or sample, but typically not for the purposes of informing a causal effect.

### Intention for causal interpretation

No causal relationship inferred: This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Additional blinding during research or analysis

No blinding is involved. The study is a documentary analysis; the documents are public, and the analyst's identity is known. The risk of unintended influence is mitigated through:

- The eight-step traceability sequence was specified before the analysis.
- The evidence-classification taxonomy was fixed before the analysis.
- The Phase II review was conducted under signed mandates.
- The contradictions were resolved through code reading alone, without re-running experiments.
- Seed invariance was established as structural, not as an artifact of a fixed seed.

### Study design

This is a documentary analysis. The unit of analysis is a set of 11 publicly available NASA Gateway documents (S1–S3, P1–P8). The design is descriptive and qualitative.

The analysis proceeds in three stages:

1. **Document coding.** Each document is read and coded against an eight-step traceability sequence (hazard → requirement → allocation → authority boundary → decision/escalation rule → formal property → verification evidence → operational response). Each step is coded as Documented, Partial, or Not established.
2. **Evidence classification.** Each document is classified into one or more of six evidence categories: Requirement, Architectural, Formal specification, Verification, Operational, Experimental.
3. **Phase II review (v1.1.0).** The experimental pipeline is reviewed across four sub-phases (II-bis, II-ter, II-quater, II-quinquies). The review produces 30 baseline records, 600 cycle-level records, and resolves three contradictions through code reading alone.

There is no randomization, no treatment, and no control group. The study does not test causal relationships. It tests the presence or absence of documentary links.

The design is fully specified in the manuscript (`paper/`) and in the Phase II Consolidated Report (`PHASE_II_CONSOLIDATED_REPORT.md`).

**Attached:** `README.md`, `CHANGELOG.md`, `NASA_Gateway_Traceability_Gap_Research_Paper_v1.0.0.pdf`

### Randomization

Not applicable. This is a documentary analysis, not a randomized study. There is no assignment of subjects to treatments or conditions.

The Phase II review uses fixed scenarios (S1, S2, S5) and deterministic fault injection. Seed invariance is structural: the fault injection does not use the random seed in the relevant branches (component_failure, shared_resource_failure). This is recorded in the Phase II Consolidated Report.

---

## Sampling

### Data collection procedures

This is a documentary analysis. The sample is a purposive sample of publicly available NASA Gateway documents. No new data were generated; the analysis relies on existing public documents.

**Inclusion criteria:**

- Documents that describe the MSM–VSM interface.
- Documents that describe safety-assurance activities (hazard analysis, safety requirements, autonomy allocation).
- Documents that describe formal-verification activities (Assume-Guarantee Contracts, R2U2, TLA+).
- Documents that are publicly accessible (NASA Technical Reports Server, conference proceedings, or peer-reviewed journals).

**Exclusion criteria:**

- Internal, controlled, or restricted NASA documents.
- Documents that do not address the MSM–VSM interface.
- Documents that are not publicly available.

The sample includes 11 documents:

- 3 NASA requirements/safety documents (S1–S3): DSG-RQMT-001, GLS-RQMT-001, GLS-006.
- 8 technical papers/presentations (P1–P8): When the Eyes Don't Have It (2020), Using AGCs for Operational Verification (2023), Gateway at the Crossroads (2023), Trustworthy Autonomy for VSM (2023), MAST (2019), Gateway Risk-Reduction (2022), Refueling Systems (2024), Stochastic Timeline Validation (2026).

**Data collection duration:** The documentary review was conducted between October and November 2026. The Phase II review (v1.1.0) was conducted in November 2026.

**Source:** The documents are available via the NASA Technical Reports Server (NTRS), conference proceedings (IAC, AIAA ASCEND), and peer-reviewed journals (Foundations and Trends in Electronic Design Automation).

No new data were generated for this registration. The Phase II review uses existing experimental artifacts (`phase2bis_experimental/`).

### Sample size

The unit of analysis is the document. The sample size is 11 documents:

- 3 NASA requirements/safety documents (S1–S3).
- 8 technical papers/presentations (P1–P8).

The sample size is not expected to vary across conditions, treatments, or clusters because the study is descriptive and does not have conditions or treatments.

For the Phase II review, the sample size is:

- 30 baseline records (S1, S2, S5 × 5 seeds × 2 conditions) — II-bis.
- 600 cycle-level records (JSONL) — II-ter.
- 3 contradictions (resolved through code reading) — II-quater and II-quinquies.

No multi-level or mixed design is used.

### Sample size rationale

No power analysis is applicable because the study is qualitative and documentary.

The sample size (11 documents) is determined by the availability of public documents that meet the inclusion criteria. No document was excluded on the basis of sample size.

The Phase II sample size (30 baseline records, 600 cycle-level records) is determined by the experimental design of the existing pipeline (S1, S2, S5 × 5 seeds × 2 conditions). The seeds are fixed, and the fault injection is deterministic in the relevant branches; therefore, the sample size is not a source of variance.

The sample size is recorded in the manuscript (Section 10) and in the Phase II Consolidated Report.

### Starting and stopping rules

This is a documentary analysis. There is no pilot testing and no data collection in the traditional sense.

**Starting rule:** The analysis began when the 11 documents were identified and retrieved (October 2026).

**Stopping rule:** The analysis stopped when all 11 documents were coded against the eight-step traceability sequence and the six evidence categories, and when the Phase II review resolved all three contradictions (November 2026).

The Phase II review has a fixed scope: II-bis, II-ter, II-quater, II-quinquies. The review stops when:

- II-bis produces 30 baseline records.
- II-ter produces 600 cycle-level records.
- II-quater resolves contradictions 1 and 3 (partial 2).
- II-quinquies resolves contradiction 2.

A.3 remains NOT OPENED. Pilot/Confirmatory remains not authorized.

No additional data will be generated for this registration.

---

## Variables

### Manipulated variables

None. This is a documentary analysis, not an experiment. There are no manipulated variables, no treatment arms, and no randomization.

The study does not assign subjects or documents to conditions. Each of the 11 documents is coded against the same eight-step traceability sequence and the same six evidence categories.

### Measured variables

The study measures two sets of coding variables. Both are descriptive and qualitative.

**Set 1: Traceability variables (8 steps)**

Each step is coded for each document:

- Documented: the step is explicitly stated in the reviewed public document.
- Partial: the step is partially stated or stated at a general level.
- Not established: the step is not established in the reviewed public document.

The eight steps are:

1. Hazard identified.
2. Safety requirement derived.
3. Function allocated.
4. Authority boundary defined.
5. Decision/escalation rule specified.
6. Formal property or mechanism.
7. Verification evidence.
8. Operational response to violation.

**Set 2: Evidence-classification variables (6 categories)**

Each document is classified into one or more of:

- Requirement.
- Architectural.
- Formal specification.
- Verification.
- Operational.
- Experimental.

**Set 3: Source verification status (3 levels)**

Each source is coded for how thoroughly it was read:

- A: full text read.
- B: public record located, details not re-read.
- C: cited as supplied, text not located.

**Set 4: Phase II review variables**

- Number of baseline records (30).
- Number of cycle-level records (600 JSONL rows).
- Number of contradictions (3).
- Resolution status (resolved / partial / not resolved).

No inferential statistics are used. The analysis is descriptive.

### Indices

Two indices are derived from the coding variables.

**Index 1: Traceability completeness index (TCI)**

The TCI is the number of steps coded as "Documented" divided by 8 (the total number of steps).

```

TCI = (number of steps with status "Documented") / 8

```

A TCI of 1.0 would indicate that all eight steps are documented. In this study, the TCI is recorded per document, and the aggregate TCI is recorded for the full sample.

The TCI is descriptive; it is not used for inferential statistics.

**Index 2: Phase II resolution index (PRI)**

The PRI is the number of contradictions resolved divided by the total number of contradictions identified.

```

PRI = (number of contradictions resolved) / 3

```

In this study, PRI = 3/3 = 1.0 (all three contradictions were resolved through code reading).

The PRI is descriptive; it is not used for inferential statistics.

No other indices are constructed. The study does not combine variables into composite scores beyond the two indices above.

---

## Analysis Plan

### Statistical models

No statistical models are used. This is a documentary analysis, not a quantitative study.

The analysis proceeds in three stages:

1. **Document coding.** Each of the 11 documents is read and coded against the eight-step traceability sequence and the six evidence categories. Coding is performed by the author.
2. **Traceability assessment.** For each step, the analysis records whether the step is documented, partial, or not established. A link is counted as established only if consecutive steps are tied together by the documents themselves (shared identifiers or explicit derivation), for a specific rule.
3. **Phase II review (v1.1.0).** The experimental pipeline is reviewed across four sub-phases:
   - II-bis: baseline records (30 summary rows).
   - II-ter: cycle-level records (600 JSONL rows, 780 log lines).
   - II-quater: code reading — three contradictions (resolved 1, 3; partial 2).
   - II-quinquies: code reading — remaining contradiction (resolved 2).

No inferential statistics are computed. No p-values, Bayes factors, or model fit indices are used. The analysis is descriptive and qualitative.

Positive controls, negative controls, and manipulation checks are not applicable. Convergence criteria and model assumption tests are not applicable.

### Transformations

No statistical transformations are performed.

Categorical variables are coded as follows:

- Traceability step status: Documented / Partial / Not established.
- Evidence category: Requirement / Architectural / Formal specification / Verification / Operational / Experimental.
- Source verification status: A (full text read) / B (public record located, details not re-read) / C (cited as supplied, text not located).

No centering, recoding, or numerical transformation is applied.

For the Phase II review:

- Contradiction status: Resolved / Partial / Not resolved.
- Record counts: 30 baseline records, 600 cycle-level records, 780 log lines.
- Seed invariance: Structural (deterministic fault injection), not a random-seed artifact.

These codings are descriptive and are recorded in the manuscript (Section 10) and in the Phase II Consolidated Report.

### Inference criteria

No inferential statistics are used. The study does not test hypotheses with p-values, Bayes factors, or model fit indices.

The inference criteria are qualitative:

1. **A traceability link is established** if and only if consecutive steps are tied together by the documents themselves (shared identifiers or explicit derivation), for a specific rule.
2. **A traceability link is partial** if the documents describe the step at a general level, without a specific rule or shared identifier.
3. **A traceability link is not established** if the reviewed public documents do not tie the step to the preceding or following step.

The central finding (RQ4) is a negative finding: the traceability chain is not established in public documentation. This finding is falsifiable: it would be refuted if a reviewed public document explicitly links a hazard-derived autonomy boundary to a specific decision/escalation rule and its corresponding verification property.

No one-tailed or two-tailed tests are used. No multiple-comparison correction is applied because no statistical comparisons are made.

### Data inclusion and exclusion

The inclusion and exclusion criteria are stated in the Sampling section.

**Inclusion criteria:**

- Documents that describe the MSM–VSM interface.
- Documents that describe safety-assurance activities (hazard analysis, safety requirements, autonomy allocation).
- Documents that describe formal-verification activities (AGCs, R2U2, TLA+).
- Documents that are publicly accessible.

**Exclusion criteria:**

- Internal, controlled, or restricted NASA documents.
- Documents that do not address the MSM–VSM interface.
- Documents that are not publicly available.

All 11 included documents are used. No observation is excluded after coding.

Outliers are not applicable because the study is descriptive and qualitative.

For the Phase II review, all 30 baseline records and all 600 cycle-level records are used. No record is excluded.

### Missing data

There is no missing data in the traditional sense.

The 11 documents are all available and were all coded. No document was partially available or missing.

For the Phase II review:

- The 30 baseline records are complete.
- The 600 cycle-level records are complete.
- The three contradictions are resolved (two fully, one partially). The partial resolution is documented as such, not as missing data.

No imputation is used. No data are discarded.

### Other planned analysis

No additional analyses are planned beyond those described above.

The study is limited to:

1. The eight-step traceability sequence.
2. The six evidence categories.
3. The Phase II review (four sub-phases).

No exploratory analyses, subgroup analyses, or secondary analyses are planned.

The limitations of the study are recorded in the manuscript (Threats to Validity, L1–L6) and are not treated as additional analyses.

---

## Other

### Context and additional information

**Phase II Independent Evidence Review (v1.1.0)**

Version 1.1.0 adds a four-phase independent review of the experimental pipeline. The review was conducted under signed mandates and did not modify any project code.

| Phase | Scope | Output | Status |
|---|---|---|---|
| II-bis | Baseline records (S1, S2, S5 × 5 seeds × 2 conditions) | 30 summary rows | Closed |
| II-ter | Cycle-level records with real seed | 600 JSONL rows, 780 log lines | Closed |
| II-quater | Code reading — three contradictions | Resolved 1, 3; partial 2 | Closed |
| II-quinquies | Code reading — remaining contradiction | Resolved 2 | Closed |

**Three contradictions resolved:**

1. `escalation_requested_at` is never populated in `_trace_scenario.py` (monitoring script defect, not engine).
2. `safe=1` in S5 is correct; `run_scenario` produces it via rule R5/R5c. `_trace_scenario.py` does not reproduce it due to a different `RuleView`.
3. `local_recovery_failures=0` while C2 remains unhealthy is consistent with `_execute_local_action` (contains only `pass`, no failure record).

**Seed invariance:** S1/S2/S5 are deterministic in fault injection. Seed variance is structurally impossible in these scenarios. This explains why all five seeds produced identical results in Phase II-bis, without invoking `0xA5A5` as an explanation.

**Code modification:** None.
**A.3:** NOT OPENED.
**Pilot/Confirmatory:** Not authorized.

---

**Scope of the finding**

The finding concerns **public documentation only**. It does not claim that any mechanism is absent from Gateway's implementation, and it never says NASA "lacks" a mechanism.

The central finding (RQ4) is a negative finding: the traceability chain is not established in public documentation. This finding is falsifiable: it would be refuted if a reviewed public document explicitly links a hazard-derived autonomy boundary to a specific decision/escalation rule and its corresponding verification property.

---

**What this repository does not claim**

- That NASA lacks a traceability mechanism in implementation.
- That Gateway autonomy is unsafe or deficient.
- That the documentary gap implies implementation failure.
- Any causal claim beyond the documentary analysis.
- A complete inventory of internal NASA artifacts.

---

**Links**

- Zenodo DOI: https://doi.org/10.5281/zenodo.24559255
- Figshare DOI: https://doi.org/10.6084/m9.figshare.35136991
- GitHub: https://github.com/gitdeeper16/NASA-GATEWAY
- Project Website: https://nasa-gateway.netlify.app

---

**Citation**

Baladi, S. (2026). *The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation* (Version 1.1.0). Zenodo. https://doi.org/10.5281/zenodo.24559255

---

## Metadata

### Contributors

Samir Baladi

### Resource type

No resource type

### Description

A documentary analysis of safety-derived autonomy boundaries and formal verification mechanisms at the MSM–VSM interface in NASA Gateway autonomous systems.

The study asks whether safety-derived boundaries of local autonomy can be traced, using public documents alone, to formally verifiable decision and escalation rules at the interface between Module System Managers (MSMs) and the Vehicle System Manager (VSM) in NASA Gateway.

Two engineering pathways are documented independently:

- Safety-assurance pathway: hazard analysis → safety requirements → autonomous functions → authority boundaries
- Formal-verification pathway: software requirements → assume-guarantee contracts (AGCs) → formal models → runtime verification (R2U2) → fault management

The study does not propose a new architecture. It audits the traceability of publicly documented mechanisms.

Version 1.1.0 adds a Phase II Independent Evidence Review (four sub-phases: II-bis, II-ter, II-quater, II-quinquies). The review produced 30 baseline records, 600 cycle-level records, and resolved three contradictions in the experimental pipeline through code reading alone. No code was modified. Seed invariance in S1/S2/S5 was established as structural (deterministic fault injection), not as an artifact of a fixed random seed.

The decision remains: the traceability chain is not established in public documentation. This finding is scope-limited to public documents.

Links:

- Zenodo DOI: https://doi.org/10.5281/zenodo.24559255
- Figshare DOI: https://doi.org/10.6084/m9.figshare.35136991
- GitHub: https://github.com/gitdeeper16/NASA-GATEWAY
- Project Website: https://nasa-gateway.netlify.app

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Date Created

Nov 28, 2026, 1:33 PM

### Date registered

Nov 28, 2026, 1:33 PM

### Subjects

- Aerospace Engineering
- Engineering
- Social and Behavioral Sciences
- Electrical and Computer Engineering
- Software Engineering
- Computer Sciences
- Science and Technology Studies
- Physical Sciences and Mathematics
- Systems and Communications

### Tags

- Autonomous Systems
- Formal Verification
- MSM-VSM Interface
- NASA Gateway
- Safety Assurance
- Traceability Gap

### Affiliated Institutions

No affiliated institutions

### Funder Names

No information

### Language

No language

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/FN2QW

---

## Citations

### APA

Baladi, S. (2026, November 28). NASA Gateway: A Traceability Gap in Public Documentation (v1.1.0). OSF. https://doi.org/10.17605/OSF.IO/FN2QW

### MLA

Baladi, Samir. "NASA Gateway: A Traceability Gap in Public Documentation (v1.1.0)." OSF, 28 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "NASA Gateway: A Traceability Gap in Public Documentation (v1.1.0)." OSF. November 28. doi:10.17605/OSF.IO/FN2QW.

### BibTeX

```bibtex
@misc{baladi2026nasagateway_osf,
  author       = {Baladi, Samir},
  title        = {{NASA Gateway: A Traceability Gap in Public Documentation (v1.1.0)}},
  year         = {2026},
  month        = nov,
  day          = {28},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/FN2QW},
  url          = {https://doi.org/10.17605/OSF.IO/FN2QW},
  note         = {OSF Preregistration}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-28
