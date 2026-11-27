# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-11-26

### Added

- Initial public release of **NASA Gateway — Safety Assurance & Formal Verification**.
- Manuscript (~6,829 words): *The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation*.
- Six figures (Fig1 … Fig6) under `figures/`.
- Three analytical data files under `data/`:
  - `traceability_matrix.csv` (8-step sequence)
  - `evidence_classification.csv` (11 documents)
  - `requirement_to_property.csv` (8 requirements)
- Documentation under `docs/`:
  - `methodology_notes.md`
  - `figure_provenance.md`
- Scripts under `scripts/`:
  - `validate.py`
  - `build_pdf.sh`
  - `build_latex.sh`
- Test suite under `tests/` (49 tests, all passing).
- Root metadata files: `README.md`, `AUTHORS.md`, `CITATION.cff`, `CONTRIBUTING.md`, `INVENTORY.md`, `LICENSE`, `PROJECT_SUMMARY.txt`, `ROADMAP.md`, `VERSION`, `manifest.json`, `netlify.toml`, `scientific_state.json`, `.gitignore`, `.gitattributes`.

### Identifiers

- Zenodo DOI: `10.5281/zenodo.24559255` — https://doi.org/10.5281/zenodo.24559255
- Figshare DOI: `10.6084/m9.figshare.35136991` — https://doi.org/10.6084/m9.figshare.35136991
- GitHub: https://github.com/gitdeeper16/NASA-GATEWAY
- Website: https://nasa-gateway.netlify.app
- ORCID: 0009-0003-8903-0029

### Notes

- The central finding concerns **public documentation only**. It makes no claim about the absence of mechanisms in implementation.
- Phase II (simulation / executable artefacts) is **not** part of v1.0.0.

---

## [Unreleased]

### Planned

- Phase II: illustrative reference model of the MSM–VSM interface (not a Gateway model).
- Phase III: independent community review of the documentary method.
- Ongoing: expand the source register if new public documents are located.

---

[1.0.0]: https://doi.org/10.5281/zenodo.24559255
