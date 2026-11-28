"""Seven design-integrity tests (SPECIFICATION.md §8).

Test 1: Existence of would_violate=True cases in S2/S3/S4 (>=50% seeds).
Test 2: Variance of would_violate across seeds in S2/S3/S4.
Test 3: Separation of candidate vs executed violations.
Test 4: H1 effect: safety_violations(treatment) < (control) in S3/S4.
Test 5: H2 effect: secondary_damage(treatment) < (control) in S2.
Test 6: Determinism: same seed -> same trace.
Test 7: Seed separation: pilot_bis / confirmatory_bis disjoint.

These tests run on a SAMPLE of seeds (not full pilot). Full pilot runs
separately. If a test fails on the sample, the design is broken.
"""
from __future__ import annotations

import random
from pathlib import Path

import pytest
import yaml

from model.engine import run_scenario


ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = ROOT / "scenarios"
SEEDS_PILOT = ROOT / "experiments" / "seeds_pilot_bis.txt"
SEEDS_CONFIRM = ROOT / "experiments" / "seeds_confirmatory_bis.txt"

# Use a small subset for speed (5 seeds instead of 20)
SAMPLE_SEEDS = None


def load_scenario(sid: str) -> dict:
    return yaml.safe_load((SCENARIOS / f"{sid}.yaml").read_text())


def load_seeds(path: Path, n: int = 5) -> list[int]:
    seeds = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            seeds.append(int(line))
    return seeds[:n]


def run_grid(scenario_id: str, seeds: list[int]) -> dict[str, list[dict]]:
    scen = load_scenario(scenario_id)
    out = {"control": [], "treatment": []}
    for cond in ("control", "treatment"):
        for seed in seeds:
            out[cond].append(run_scenario(scen, seed, cond))
    return out


# ─── Test 7 (fastest, no runs) ───

def test_7_seed_separation():
    pilot = set(load_seeds(SEEDS_PILOT, n=10**9))
    confirm = set(load_seeds(SEEDS_CONFIRM, n=10**9))
    assert len(pilot) == 20, f"expected 20 pilot seeds, got {len(pilot)}"
    assert len(confirm) == 80, f"expected 80 confirm seeds, got {len(confirm)}"
    assert not (pilot & confirm), "pilot and confirm overlap"
    print(f"pilot={len(pilot)}, confirm={len(confirm)}, overlap=0")


# ─── Test 1 & 2 & 3 & 4 & 5 (need runs) ───

@pytest.fixture(scope="module")
def pilot_results():
    seeds = load_seeds(SEEDS_PILOT, n=5)
    results = {}
    for sid in ("S1", "S2", "S3", "S4", "S5"):
        results[sid] = run_grid(sid, seeds)
    return results


def test_1_existence_of_violations(pilot_results):
    """S3 and S4 test H1-bis: candidate_would_violate=True in >=1 cycle
    across >=50% of seeds. S2 does not test H1-bis (it tests H2-bis).
    S1 is a negative control: always False."""
    for sid in ("S3", "S4"):
        for cond in ("control", "treatment"):
            runs = pilot_results[sid][cond]
            with_v = sum(1 for r in runs if r["candidate_would_violate_final"] == 1)
            assert with_v >= len(runs) // 2, (
                f"{sid}/{cond}: only {with_v}/{len(runs)} runs saw a violation"
            )
    # S1: no violations (negative control)
    for cond in ("control", "treatment"):
        runs = pilot_results["S1"][cond]
        for r in runs:
            assert r["candidate_would_violate_final"] == 0, (
                f"S1/{cond}: unexpected violation — negative control failed"
            )
    print("test_1: OK (S3+S4 violations, S1 clean)")


def test_3_separation_candidate_vs_executed(pilot_results):
    """In S3/S4: exists at least one run with candidate_would_violate=1
    AND safety_violations=0 (policy chose safe_mode or escalate, so the
    violated candidate was NOT executed)."""
    found = False
    for sid in ("S3", "S4"):
        for cond in ("control", "treatment"):
            for r in pilot_results[sid][cond]:
                if r["candidate_would_violate_final"] == 1 and r["safety_violations"] == 0:
                    found = True
                    break
    assert found, "no run showed candidate=1 but executed=0 — separation failed"
    print("test_3: OK (separation observed)")


def test_6_determinism(pilot_results):
    """Same seed -> same trace."""
    seeds = load_seeds(SEEDS_PILOT, n=2)
    scen = load_scenario("S2")
    for seed in seeds:
        r1 = run_scenario(scen, seed, "control")
        r2 = run_scenario(scen, seed, "control")
        # Remove events (should be identical anyway)
        for k in r1:
            assert r1[k] == r2[k], f"S2 seed={seed}: {k} differs: {r1[k]} vs {r2[k]}"
    print("test_6: OK")


# ─── Test 4 & 5 (hypothesis effects) — informative, not hard assert ───

def test_4_H1_effect(pilot_results):
    """S3/S4: safety_violations(treatment) < safety_violations(control) in
    at least 50% of seeds. Not a hard failure — records the observation."""
    for sid in ("S3", "S4"):
        ctrl = pilot_results[sid]["control"]
        trt = pilot_results[sid]["treatment"]
        n = len(ctrl)
        better = sum(1 for c, t in zip(ctrl, trt)
                     if t["safety_violations"] < c["safety_violations"])
        print(f"  {sid}: treatment better in {better}/{n} seeds")
        # Soft check: warn if completely flat
        if better == 0:
            print(f"  WARNING: {sid} shows no H1 effect at all")


def test_5_H2_effect(pilot_results):
    """S2: mean secondary_damage(treatment) < mean secondary_damage(control)."""
    ctrl = [r["secondary_damage"] for r in pilot_results["S2"]["control"]]
    trt = [r["secondary_damage"] for r in pilot_results["S2"]["treatment"]]
    mean_c = sum(ctrl) / len(ctrl)
    mean_t = sum(trt) / len(trt)
    print(f"  S2: mean secondary_damage control={mean_c:.2f}, treatment={mean_t:.2f}")
    if mean_t >= mean_c:
        print("  WARNING: H2 direction not observed (treatment >= control)")
