# Tests — Project Integrity Verification

This directory contains automated integrity tests for the NASA Gateway 
research project. Since this is a documentary study (not software), the 
tests verify project structure, metadata consistency, and data integrity 
— not code behavior.

## Test Categories

| Category | Purpose |
|----------|---------|
| **Structure tests** | Verify required files and directories exist |
| **Metadata tests** | Verify DOIs, usernames, and identifiers are consistent |
| **Data tests** | Verify CSV files are well-formed and complete |
| **Figure tests** | Verify all 6 figures exist and are referenced |
| **Content tests** | Verify forbidden strings are absent |

## How to Run

```bash
# Run all tests
bash tests/run_all.sh

# Run a specific test
bash tests/test_structure.sh
bash tests/test_metadata.sh
bash tests/test_data.sh
bash tests/test_figures.sh
bash tests/test_content.sh
```

Exit Codes

· 0 — All tests passed
· 1 — One or more tests failed

---

NASA Gateway — Safety Assurance and Formal Verification v1.0.0
