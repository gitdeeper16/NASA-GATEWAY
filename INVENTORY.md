# Project Inventory — NASA Gateway v1.0.0

**Project:** NASA Gateway — Safety Assurance & Formal Verification
**Version:** 1.0.0
**Date:** 2026-11-26
**Author:** Samir Baladi
**License:** CC-BY-4.0

---

## Identifiers

| Resource | Identifier |
|---|---|
| Zenodo DOI | `10.5281/zenodo.24559255` |
| Figshare DOI | `10.6084/m9.figshare.35136991` |
| GitHub | https://github.com/gitdeeper16/NASA-GATEWAY |
| Website | https://nasa-gateway.netlify.app |
| ORCID | 0009-0003-8903-0029 |

---

## Root files (14)

| # | File | Purpose |
|---|------|---------|
| 1 | `README.md` | Project guide and overview |
| 2 | `AUTHORS.md` | Author information |
| 3 | `CHANGELOG.md` | Version history |
| 4 | `CITATION.cff` | Machine-readable citation (CFF 1.2.0) |
| 5 | `CONTRIBUTING.md` | Contribution guidelines |
| 6 | `INVENTORY.md` | This file |
| 7 | `LICENSE` | CC-BY-4.0 |
| 8 | `PROJECT_SUMMARY.txt` | One-page summary |
| 9 | `ROADMAP.md` | Publication roadmap |
| 10 | `VERSION` | `1.0.0` |
| 11 | `manifest.json` | Machine-readable project metadata |
| 12 | `netlify.toml` | Netlify deployment config |
| 13 | `scientific_state.json` | Research state snapshot |
| 14 | `.gitignore` | Git ignore rules |

---

## Directories

| Directory | Contents |
|---|---|
| `paper/` | `NASA_Gateway_Safety_Assurance_and_Formal_Verification.md` + `NASA_Gateway_Traceability_Gap_Research_Paper_v1.0.0.pdf` |
| `figures/` | 6 PNG files (Fig1 … Fig6) |
| `sources/` | README + `.gitkeep` (external source links) |
| `data/` | 3 CSV + README + `.gitkeep` |
| `docs/` | `methodology_notes.md`, `figure_provenance.md`, `README.md` |
| `scripts/` | `validate.py`, `build_pdf.sh`, `build_latex.sh`, `README.md` |
| `tests/` | `run_all.sh` + 5 test files + `README.md` (49 tests) |

---

## Figures

| # | File | Size | Paper section |
|---|------|------|---------------|
| 1 | `Fig1_Traceability_Chain_Gap.png` | 152K | Section 5.3 |
| 2 | `Fig2_Two_Pathways_Interface.png` | 220K | Section 5.1 |
| 3 | `Fig3_MSM_VSM_Architecture.png` | 144K | Section 4.1 |
| 4 | `Fig4_Evidence_Classification_Taxonomy.png` | 124K | Section 3.4 |
| 5 | `Fig5_Gateway_Lunar_Orbit.png` | 240K | Section 1 |
| 6 | `Fig6_Assurance_Case_GSN_Structure.png` | 176K | Section 5.3 |

---

## Data artifacts

| File | Rows | Purpose |
|---|:-:|---|
| `data/traceability_matrix.csv` | 8 | 8-step traceability sequence analysis |
| `data/evidence_classification.csv` | 11 | 11 documents with evidence categories |
| `data/requirement_to_property.csv` | 8 | Requirements mapped to expected properties |

---

## Tests (49 total, all passing)

| File | Count | Purpose |
|---|:-:|---|
| `tests/test_structure.sh` | 22 | File and directory existence |
| `tests/test_metadata.sh` | 5 | DOI, author, absence of legacy identifiers |
| `tests/test_data.sh` | 4 | CSV integrity |
| `tests/test_figures.sh` | 8 | 6 figures + references |
| `tests/test_content.sh` | 10 | No legacy text + core concepts present |
| **Total** | **49** | **All passing** |

---

## External mirrors

| Platform | DOI / URL | Contents |
|---|---|---|
| Zenodo | `10.5281/zenodo.24559255` | Primary archival record (manuscript) |
| Figshare | `10.6084/m9.figshare.35136991` | Full file bundle (PDF + metadata + figures) |
| GitHub | `github.com/gitdeeper16/NASA-GATEWAY` | Source files, scripts, tests |
| Netlify | `nasa-gateway.netlify.app` | Project website |

---

## Version history

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-11-26 | Phase I complete: documentary analysis, 6 figures, 3 CSVs, 49 tests |
