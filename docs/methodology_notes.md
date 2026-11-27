# Methodology Notes — Extended

**Companion to:** Section 3 (Research Scope and Methodology) of the manuscript
**Date:** 2026-11-26
**Author:** Samir Baladi

---

## 1. Purpose of These Notes

These notes extend the methodology section of the manuscript with 
additional detail on the documentary research process, so that a 
reader can reproduce or critique the analysis.

## 2. Document Retrieval

### 2.1 Search strategy

Public NASA documents were identified through:

- NASA Technical Reports Server (NTRS): https://ntrs.nasa.gov
- NASA Gateway Program public documentation
- IEEE Xplore and AIAA databases for peer-reviewed technical papers
- NASA public technical presentation archives

### 2.2 Search terms

The following search terms were used:

- "Gateway Vehicle System Manager" OR "VSM"
- "Module System Manager" OR "MSM"
- "Assume-Guarantee Contract" AND "Gateway"
- "R2U2" AND "NASA"
- "Gateway fault management" OR "FDIR"
- "L2-GW-0199"
- "GLS-RQMT-001"

### 2.3 Inclusion criteria

A document was included if it:

1. Was publicly available at the time of writing (2026-11-26).
2. Addressed Gateway architecture, safety, autonomy, or verification.
3. Provided sufficient detail to support or contradict the traceability chain.

### 2.4 Exclusion criteria

A document was excluded if it:

1. Required access credentials or was subject to ITAR restrictions.
2. Addressed only peripheral subsystems not relevant to the MSM–VSM interface.
3. Was not identifiable in public repositories.

## 3. Version Control of Sources

NASA documents are periodically revised. The manuscript cites the 
specific versions available at the time of writing. Future revisions 
may alter requirement numbers or wording; the analysis in the 
manuscript should be read as applying to the versions cited.

## 4. The Eight-Step Traceability Sequence

The eight-step sequence used in the analysis (Section 3.3 of the 
manuscript) was developed specifically for this study. It is an 
analytical instrument, not an asserted NASA process. The choice of 
these eight steps reflects the minimal traceability chain from 
hazard identification to verification evidence; other chains could 
be constructed with more or fewer steps.

## 5. Treatment of Negative Findings

The manuscript uses "not established in public documentation" as 
a distinct epistemic status, separate from:

- "Established in public documentation"
- "Contradicted by public documentation"
- "Absent from implementation"

This distinction is important because the absence of a documented 
chain is not evidence of the absence of a mechanism.

## 6. Limitations of the Method

See Section 7 of the manuscript for the full limitations discussion. 
Key limitations:

- Access to DSG-SPEC-VSM-003, the complete MSM ICD, DSG-RQMT-011, 
  and DSG-RPT-001 was not available.
- Requirements establish obligations, not implementations.
- Experimental evidence (MAST, risk-reduction) is not evidence of 
  operational deployment.
- Module-specific requirements (GLS-RQMT-001) cannot be generalized.

---

**NASA Gateway — Safety Assurance and Formal Verification v1.0.0**
