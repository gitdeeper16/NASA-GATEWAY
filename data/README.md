# Data — Analytical Artifacts

This directory contains the analytical artifacts derived from the 
documentary analysis in the manuscript.

## Planned Contents

### 1. Traceability Matrix

**File:** `traceability_matrix.csv`

An eight-step traceability matrix that maps each analytical step 
(from hazard identification to verification evidence) to the 
specific public document(s) where evidence was found — and 
explicitly marks where evidence was NOT found.

**Structure:**

| Column | Description |
|--------|-------------|
| `step` | Traceability step number (1–8) |
| `step_name` | Description of the step |
| `evidence_found` | Yes / Partial / No |
| `source_document` | Document identifier(s) |
| `source_section` | Section or requirement number |
| `notes` | Analytical notes |

### 2. Evidence Classification Table

**File:** `evidence_classification.csv`

A six-category classification of every source document reviewed, 
recording the evidence type (requirement, architectural, formal 
specification, verification, operational, experimental).

**Structure:**

| Column | Description |
|--------|-------------|
| `document` | Document identifier |
| `evidence_type` | One of six categories |
| `contribution` | What this document contributes |
| `limitation` | What this document does NOT establish |

### 3. Requirement-to-Property Mapping

**File:** `requirement_to_property.csv`

A tentative mapping of the safety requirements cited in the 
manuscript to the formal properties or fault-management rules 
that they would need to correspond to — explicitly marking the 
mapping as not established in public documentation where applicable.

## Notes

- No data generated from closed or internal NASA systems is included.
- All artifacts are derived strictly from publicly available documents.
- Files in this directory are analytical, not empirical; they 
  represent documentary analysis, not measurement.

---

**NASA Gateway — Safety Assurance and Formal Verification v1.0.0**
