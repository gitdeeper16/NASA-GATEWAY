# Pilot results — Phase II

**Status:** Preserved as a diagnostic record after Addendum 002.

> **Note (2026-11-28):** These pilot results are preserved as a diagnostic
> record after Addendum 002 identified structural limitations in the Phase II
> design. They are not evidence for or against H1, H2, or H4. See
> `docs/ADDENDUM_002_2026-11-28.md` for the full analysis.

---

## What goes here

One JSONL file per (scenario, condition), produced by
`experiments/run_pilot.py`:

```

results/pilot/
├── S1_treatment.jsonl
├── S1_control.jsonl
├── S2_treatment.jsonl
├── S2_control.jsonl
├── S3_treatment.jsonl
├── S3_control.jsonl
├── S4_treatment.jsonl
├── S4_control.jsonl
├── S5_treatment.jsonl
└── S5_control.jsonl

```

Each line is one run. Total: 5 × 2 × 20 = **200 runs**.

## What pilot results are

**Descriptive only.** They characterise how the model behaves across the
five scenarios under both conditions. They are used to:

- confirm the model is not trivially safe (all zero violations) or
  trivially unsafe (all violations);
- calibrate fault magnitudes if the frozen values produce degenerate
  outcomes (this calibration must be recorded as a dated amendment
  *before* confirmatory, per `PREREGISTRATION.md` §5.3);
- inspect the distribution of outcome variables for the descriptive
  summary.

## What pilot results are NOT

- **Not** used for hypothesis testing (H1–H4). Those are tested on the
  confirmatory stage only.
- **Not** used to choose hypotheses, statistical tests, or falsification
  thresholds.
- **Not** mixed with confirmatory results. `tests/test_separation.sh`
  enforces this.

## Leakage rules

The pilot and confirmatory stages use disjoint seed sets:

- `experiments/seeds_pilot.txt` — 20 seeds, used here only.
- `experiments/seeds_confirmatory.txt` — 80 seeds, disjoint from the
  pilot seeds, used only in `results/confirmatory/`.

`tests/test_separation.sh` verifies:
1. the seed sets are disjoint;
2. no pilot seed appears in confirmatory results;
3. confirmatory analysis code does not read from `results/pilot/`;
4. no file in `results/confirmatory/` has the same SHA as a file in
   `results/pilot/`.

## Reproducibility

Each line in a JSONL file is uniquely determined by
`(scenario, seed, condition, model version)`. Two runs with the same
triple must produce identical output (H6 determinism, verified by
`tests/test_model_determinism.sh`).

## If a calibration is needed

Record it as `docs/ADDENDUM_NNN_YYYY-MM-DD.md`, dated **before** the
confirmatory stage begins. The amendment must not alter hypotheses or
falsification criteria; it may only record a change to fault magnitudes.
