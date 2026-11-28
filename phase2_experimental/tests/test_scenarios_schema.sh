#!/usr/bin/env bash
# Phase II — Scenario contract test.
# Enforces scenarios/_schema.md and the anti-tautology rule:
#   - required keys present;
#   - can_fail_how >= 3;
#   - no outcome variable, statistical threshold, or NASA/Gateway
#     reference leaks into a scenario.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - << 'PY'
import sys
try:
    import yaml
except ImportError:
    print("❌ PyYAML required"); sys.exit(1)

REQUIRED = [
    "scenario_id", "version", "frozen_at", "preregistration_ref",
    "hypotheses_ref", "description", "initial_state", "fault_injection",
    "expected_rule", "treatment_property", "control_rule", "can_fail_how",
]
OUTCOME_VARS = [
    "safety_violations", "consistency", "escalations_total",
    "escalations_correct", "escalations_false", "escalations_missed",
    "secondary_damage", "safe_mode_reached", "time_to_resolution",
]
STAT_THRESH = ["p <", "p<", "cohen", "holm", "alpha", "α", "0.05"]
NASA_REFS = ["NASA", "Gateway", "L2-GW", "DSG-RQMT"]

fails = 0
for sid in ["S1", "S2", "S3", "S4", "S5"]:
    path = f"scenarios/{sid}.yaml"
    with open(path) as f:
        raw = f.read()
    d = yaml.safe_load(raw)

    missing = [k for k in REQUIRED if k not in d]
    if missing:
        print(f"❌ {sid}: missing {missing}"); fails += 1; continue

    if d["scenario_id"] != sid:
        print(f"❌ {sid}: scenario_id={d['scenario_id']} != {sid}"); fails += 1

    n = len(d["can_fail_how"])
    if n < 3:
        print(f"❌ {sid}: can_fail_how has {n} < 3"); fails += 1

    leaked = [v for v in OUTCOME_VARS if v in raw]
    if leaked:
        print(f"❌ {sid}: outcome vars leaked: {leaked}"); fails += 1

    leaked = [s for s in STAT_THRESH if s in raw]
    if leaked:
        print(f"❌ {sid}: stat thresholds leaked: {leaked}"); fails += 1

    leaked = [s for s in NASA_REFS if s in raw]
    if leaked:
        print(f"❌ {sid}: NASA refs leaked: {leaked}"); fails += 1

    if d["frozen_at"] != "2026-11-27":
        print(f"❌ {sid}: frozen_at != 2026-11-27"); fails += 1

    if d["initial_state"]["components"] > 4:
        print(f"❌ {sid}: components > MAX_COMPONENTS"); fails += 1
    if d["fault_injection"]["at_cycle"] > 20:
        print(f"❌ {sid}: at_cycle > MAX_CYCLES"); fails += 1
    pu = d["fault_injection"].get("persist_until")
    if pu is not None and pu > 20:
        print(f"❌ {sid}: persist_until > MAX_CYCLES"); fails += 1

    print(f"✅ {sid}: OK (can_fail_how={n}, expected={d['expected_rule']})")

sys.exit(1 if fails else 0)
PY

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ test_scenarios_schema: PASS"
else
  echo ""
  echo "❌ test_scenarios_schema: FAIL"
  exit 1
fi
