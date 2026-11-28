"""Unit tests for would_violate — the four constraints, in isolation.

These are pure-function tests. No scenarios, no seeds, no runs.
They verify that each constraint is correctly defined and independent.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.engine import would_violate
from model.state import Component, SharedResource, SystemState


def fresh_state() -> SystemState:
    s = SystemState()
    s.components = {"C1": Component("C1"), "C2": Component("C2"), "C3": Component("C3")}
    s.shared_resources = {"SR1": SharedResource("SR1")}
    s.available_capacity = 3.0
    s.required_recovery_capacity = 0.5
    return s


# ─── authority_boundary ───

def test_authority_no_violation_when_delegated():
    s = fresh_state()
    s.msm_authority_delegated = True
    assert would_violate("recover_local", s) == (False, None)


def test_authority_violation_when_not_delegated():
    s = fresh_state()
    s.msm_authority_delegated = False
    assert would_violate("recover_local", s) == (True, "authority_boundary")


def test_authority_independent_of_vsm_authority():
    """authority_boundary depends on MSM, not VSM."""
    s = fresh_state()
    s.vsm_authority = "delegated"
    s.msm_authority_delegated = True
    assert would_violate("recover_local", s) == (False, None)


# ─── shared_resource ───

def test_shared_resource_no_violation_when_healthy():
    s = fresh_state()
    assert would_violate("recover_local", s) == (False, None)


def test_shared_resource_violation_when_unhealthy():
    s = fresh_state()
    s.shared_resources["SR1"].healthy = False
    assert would_violate("recover_local", s) == (True, "shared_resource")


# ─── active_constraint ───

def test_active_constraint_no_violation_when_false():
    s = fresh_state()
    s.constraint_conflict = False
    assert would_violate("recover_local", s) == (False, None)


def test_active_constraint_violation_when_true():
    s = fresh_state()
    s.constraint_conflict = True
    assert would_violate("recover_local", s) == (True, "active_constraint")


# ─── capacity_overflow ───

def test_capacity_no_violation_when_sufficient():
    s = fresh_state()
    s.available_capacity = 2.0
    s.required_recovery_capacity = 1.5
    assert would_violate("recover_local", s) == (False, None)


def test_capacity_violation_when_insufficient():
    s = fresh_state()
    s.available_capacity = 2.0
    s.required_recovery_capacity = 2.5
    assert would_violate("recover_local", s) == (True, "capacity_overflow")


def test_capacity_boundary_equal():
    """required == available is NOT a violation."""
    s = fresh_state()
    s.available_capacity = 2.0
    s.required_recovery_capacity = 2.0
    assert would_violate("recover_local", s) == (False, None)


# ─── Priority order ───

def test_priority_authority_first():
    """If multiple constraints violated, authority is reported first."""
    s = fresh_state()
    s.msm_authority_delegated = False
    s.shared_resources["SR1"].healthy = False
    s.constraint_conflict = True
    s.available_capacity = 0.0
    s.required_recovery_capacity = 5.0
    assert would_violate("recover_local", s) == (True, "authority_boundary")


def test_priority_shared_before_constraint():
    s = fresh_state()
    s.msm_authority_delegated = True
    s.shared_resources["SR1"].healthy = False
    s.constraint_conflict = True
    s.available_capacity = 0.0
    s.required_recovery_capacity = 5.0
    assert would_violate("recover_local", s) == (True, "shared_resource")


def test_priority_constraint_before_capacity():
    s = fresh_state()
    s.msm_authority_delegated = True
    s.shared_resources["SR1"].healthy = True
    s.constraint_conflict = True
    s.available_capacity = 0.0
    s.required_recovery_capacity = 5.0
    assert would_violate("recover_local", s) == (True, "active_constraint")


# ─── Non-local actions ───

def test_non_local_actions_never_violate():
    s = fresh_state()
    s.msm_authority_delegated = False
    s.shared_resources["SR1"].healthy = False
    s.constraint_conflict = True
    s.available_capacity = 0.0
    s.required_recovery_capacity = 5.0
    for action in ("escalate", "safe_mode", "noop"):
        assert would_violate(action, s) == (False, None)
