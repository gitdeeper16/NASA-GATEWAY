"""S3 capacity transition tests.

The key assertion: the transition boundary(cycle 3) -> overflow(cycle 5)
is caused by the SECOND fault, not merely by the presence of two faults.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.engine import (
    _apply_primary_fault,
    _build_initial_state,
    _iter_faults,
    _update_state,
    would_violate,
)


S3 = yaml.safe_load(
    (Path(__file__).resolve().parent.parent / "scenarios" / "S3.yaml").read_text()
)


def _build_fault_schedule():
    schedule = {}
    for f in _iter_faults(S3):
        schedule.setdefault(f["at_cycle"], []).append(f)
    return schedule


def _step_to(state, scenario, cycle, schedule):
    state.cycle = cycle
    for f in schedule.get(cycle, ()):
        _apply_primary_fault(state, f, random.Random(0))
    _update_state(state, scenario)


def test_s3_initial_capacity():
    state = _build_initial_state(S3)
    assert state.available_capacity == 3.0
    assert state.required_recovery_capacity == 2.0
    assert would_violate("recover_local", state) == (False, None)


def test_s3_boundary_after_first_fault():
    state = _build_initial_state(S3)
    sched = _build_fault_schedule()
    for c in (0, 1, 2, 3):
        _step_to(state, S3, c, sched)
    assert state.available_capacity == 2.0
    assert state.required_recovery_capacity == 2.0
    assert would_violate("recover_local", state) == (False, None)


def test_s3_overflow_after_second_fault():
    state = _build_initial_state(S3)
    sched = _build_fault_schedule()
    for c in (0, 1, 2, 3, 4, 5):
        _step_to(state, S3, c, sched)
    assert state.available_capacity == 1.0
    assert would_violate("recover_local", state) == (True, "capacity_overflow")


def test_s3_transition_is_due_to_second_fault():
    """Prove the transition boundary->overflow is caused by the second
    fault specifically: capture state at cycle 4 (boundary), advance one
    cycle (second fault), capture state again. Only difference is fault 2."""
    state = _build_initial_state(S3)
    sched = _build_fault_schedule()
    for c in (0, 1, 2, 3, 4):
        _step_to(state, S3, c, sched)
    before = would_violate("recover_local", state)
    avail_before = state.available_capacity

    _step_to(state, S3, 5, sched)
    after = would_violate("recover_local", state)
    avail_after = state.available_capacity

    assert before == (False, None), f"pre-fault2 must be boundary, got {before}"
    assert after == (True, "capacity_overflow"), f"post-fault2 must be overflow, got {after}"
    assert (avail_before, avail_after) == (2.0, 1.0)


def test_s3_faults_are_at_distinct_cycles():
    cycles = sorted(f["at_cycle"] for f in _iter_faults(S3))
    assert len(cycles) == 2
    assert cycles[0] != cycles[1]


def test_s3_faults_target_distinct_components():
    targets = sorted(f["target"] for f in _iter_faults(S3))
    assert len(set(targets)) == 2
