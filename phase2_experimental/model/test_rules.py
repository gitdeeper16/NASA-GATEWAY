"""
Unit tests for rules.py. Run before building the engine.

These tests do NOT test hypotheses H1–H6. They test that the rules are
well-formed: pure, total (always return bool), and capable of returning
False. Hypothesis testing is done by the engine on frozen scenarios.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.rules import (
    RuleView,
    R1_local_containable, R2_shared_resource, R3_local_recovery_failed,
    R4_constraint_conflict, R5_comm_lost,
    R1_control, R2_control, R3_control, R4_control, R5_control,
    R3_TREATMENT_N, CONTROL,
)


def _view(**kw):
    defaults = dict(cycle=0, local_fault_count=0, local_recovery_failures=0,
                    local_containable=True, shared_resource_affected=False,
                    shared_resource_severity=0.0,
                    constraint_violated_by_local_action=False,
                    comm_lost=False, comm_silence_cycles=0)
    defaults.update(kw)
    return RuleView(**defaults)


def test_rules_are_total():
    """Every rule must return a bool for a minimal view."""
    v = _view()
    for fn in [R1_local_containable, R2_shared_resource, R3_local_recovery_failed,
               R4_constraint_conflict, R5_comm_lost,
               R1_control, R2_control, R3_control, R4_control, R5_control]:
        assert isinstance(fn(v), bool), fn.__name__


def test_every_rule_can_be_false():
    """If a rule can never be False, hypotheses using it are unfalsifiable."""
    v = _view()
    assert R1_local_containable(v) is False
    assert R2_shared_resource(v) is False
    assert R3_local_recovery_failed(v) is False
    assert R4_constraint_conflict(v) is False
    assert R5_comm_lost(v) is False
    assert R1_control(v) is False
    assert R2_control(v) is False
    assert R3_control(v) is False
    assert R4_control(v) is False
    assert R5_control(v) is False


def test_every_rule_can_be_true():
    """And each must be able to fire."""
    assert R1_local_containable(_view(local_fault_count=1)) is True
    assert R2_shared_resource(_view(shared_resource_affected=True,
                                     shared_resource_severity=0.5)) is True
    assert R3_local_recovery_failed(_view(local_recovery_failures=R3_TREATMENT_N)) is True
    assert R4_constraint_conflict(_view(constraint_violated_by_local_action=True)) is True
    assert R5_comm_lost(_view(comm_lost=True)) is True
    assert R1_control(_view(local_fault_count=CONTROL["R1_control_threshold"])) is True
    assert R3_control(_view(local_recovery_failures=CONTROL["R3_control_threshold"])) is True
    assert R4_control(_view(cycle=CONTROL["R4_control_threshold"])) is True
    assert R5_control(_view(comm_silence_cycles=CONTROL["R5_control_threshold"])) is True


def test_purity():
    """Rules must not mutate their view."""
    import copy
    v = _view(local_fault_count=2)
    snapshot = copy.deepcopy(v)
    R1_local_containable(v); R2_shared_resource(v); R3_local_recovery_failed(v)
    R4_constraint_conflict(v); R5_comm_lost(v)
    R1_control(v); R2_control(v); R3_control(v); R4_control(v); R5_control(v)
    assert v == snapshot


def test_r4_control_is_blind_to_safety():
    """The control for R4 must NOT look at constraint_violated_by_local_action.
    Otherwise the control is not structurally distinct from the treatment."""
    v_no_conflict = _view(cycle=10, constraint_violated_by_local_action=False)
    v_conflict    = _view(cycle=10, constraint_violated_by_local_action=True)
    # Same cycle -> same control decision, regardless of the safety signal.
    assert R4_control(v_no_conflict) == R4_control(v_conflict)


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"✅ {t.__name__}")
    print(f"\n{len(tests)} rule tests passed.")
