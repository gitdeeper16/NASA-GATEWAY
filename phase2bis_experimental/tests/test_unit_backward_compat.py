"""Backward compatibility: single-fault scenarios behave as before."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.engine import _iter_faults


SCEN_DIR = Path(__file__).resolve().parent.parent / "scenarios"


def _load(sid):
    return yaml.safe_load((SCEN_DIR / f"{sid}.yaml").read_text())


def test_single_fault_s1():
    assert len(_iter_faults(_load("S1"))) == 1


def test_single_fault_s2():
    assert len(_iter_faults(_load("S2"))) == 1


def test_single_fault_s4():
    assert len(_iter_faults(_load("S4"))) == 1


def test_multi_fault_s3():
    assert len(_iter_faults(_load("S3"))) == 2


def test_single_fault_shape_is_unchanged():
    """_iter_faults must return the original dict, not a copy."""
    s1 = _load("S1")
    faults = _iter_faults(s1)
    assert faults[0] is s1["fault_injection"]
