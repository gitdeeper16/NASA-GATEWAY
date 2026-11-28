#!/usr/bin/env bash
# Phase II — pre-pilot test suite.
# Termux-compatible: no /tmp, no bash -c with multiline, no pipefail surprises.
set -u

PASS=0
FAIL=0

# Run a command, capture exit code, print its output.
# Usage: run_step <name> <expected_exit> <command...>
run_step() {
  local name="$1"
  local expect="$2"
  shift 2
  echo ""
  echo ">>> $name"
  echo "    cmd: $*"
  "$@"
  local rc=$?
  if [ "$rc" -eq "$expect" ]; then
    echo "✅ PASS: $name (exit $rc)"
    PASS=$((PASS+1))
  else
    echo "❌ FAIL: $name (exit $rc, expected $expect)"
    FAIL=$((FAIL+1))
  fi
}

# For commands whose expected exit is non-zero, we run them and capture,
# then compare. This avoids `set -e` entirely.
echo "=================================================="
echo " Phase II — pre-pilot test suite (Termux-safe)"
echo "=================================================="

# 1. Rules unit tests
run_step "1. Rules unit tests" 0 python3 model/test_rules.py

# 2. Scenario contract
run_step "2. Scenario contract" 0 bash tests/test_scenarios_schema.sh

# 3. Separation
run_step "3. Pilot/confirmatory separation" 0 bash tests/test_separation.sh

# 4. Determinism (H6)
echo ""
echo ">>> 4. Determinism (H6) across all scenarios"
DET_OK=1
for s in S1 S2 S3 S4 S5; do
  for c in treatment control; do
    if bash tests/test_model_determinism.sh "scenarios/$s.yaml" 42 "$c" >/dev/null 2>&1; then
      echo "  ✅ $s/$c"
    else
      echo "  ❌ $s/$c"
      DET_OK=0
    fi
  done
done
if [ "$DET_OK" -eq 1 ]; then
  echo "✅ PASS: 4. Determinism"
  PASS=$((PASS+1))
else
  echo "❌ FAIL: 4. Determinism"
  FAIL=$((FAIL+1))
fi

# 5. Addendum digest
run_step "5. Addendum digest" 0 sha256sum -c results/.addendum_001.sha256

# 6. Historical digest — expected: model_check.sh FAILED, nothing else.
# We capture the output first, then judge in shell (no pipes in conditions).
echo ""
echo ">>> 6. Historical freeze digest"
HIST_OUT=$(sha256sum -c results/.preregistration.sha256 2>&1)
echo "$HIST_OUT"
OTHER_FAILS=""
EXPECTED_FAIL_SEEN=0
# Parse line by line — robust on Termux
OLDIFS="$IFS"
IFS='
'
for line in $HIST_OUT; do
  case "$line" in
    *": FAILED"*)
      case "$line" in
        *model_check.sh*) EXPECTED_FAIL_SEEN=1 ;;
        *) OTHER_FAILS="$OTHER_FAILS$line
" ;;
      esac
      ;;
  esac
done
IFS="$OLDIFS"

if [ "$EXPECTED_FAIL_SEEN" -eq 1 ] && [ -z "$OTHER_FAILS" ]; then
  echo "✅ PASS: 6. Historical digest (only model_check.sh differs, as documented)"
  PASS=$((PASS+1))
elif [ "$EXPECTED_FAIL_SEEN" -eq 0 ] && [ -z "$OTHER_FAILS" ]; then
  echo "⚠️  model_check.sh matches the frozen SHA — was it restored?"
  echo "✅ PASS: 6. Historical digest (all OK)"
  PASS=$((PASS+1))
else
  echo "❌ FAIL: 6. Historical digest — unexpected failures:"
  echo "$OTHER_FAILS"
  FAIL=$((FAIL+1))
fi

# 7. TLA+ structural checks
echo ""
echo ">>> 7. TLA+ structural checks"
TLA_OK=1
tla_check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  ✅ $desc"
  else
    echo "  ❌ $desc"
    TLA_OK=0
  fi
}
tla_check "properties.tla ends with ====" \
  bash -c 'test "$(grep -c "^====" formal/properties.tla)" -eq 1'
tla_check "GatewayPhase2.tla ends with ====" \
  bash -c 'test "$(grep -c "^====" formal/GatewayPhase2.tla)" -eq 1'
tla_check "cfg has PROPERTIES" \
  bash -c 'test "$(grep -c "^PROPERTIES" formal/GatewayPhase2.cfg)" -eq 1'
tla_check "cfg has no INVARIANTS" \
  bash -c 'test "$(grep -c "^INVARIANTS" formal/GatewayPhase2.cfg)" -eq 0'
tla_check "EscalationCompletes present" \
  grep -q "EscalationCompletes" formal/properties.tla
tla_check "BoundedEscalation removed (no actual definition)" \
  bash -c '! grep -qE "^BoundedEscalation[[:space:]]*==" formal/properties.tla'
tla_check "FailLocalRecovery present" \
  grep -q "FailLocalRecovery" formal/GatewayPhase2.tla
tla_check "ConstraintConflict present" \
  grep -q "ConstraintConflict" formal/GatewayPhase2.tla
tla_check "TakeLocalAction present" \
  grep -q "TakeLocalAction" formal/GatewayPhase2.tla
tla_check "MaxEscalationDepth present" \
  grep -q "MaxEscalationDepth" formal/GatewayPhase2.tla

if [ "$TLA_OK" -eq 1 ]; then
  echo "✅ PASS: 7. TLA+ structural"
  PASS=$((PASS+1))
else
  echo "❌ FAIL: 7. TLA+ structural"
  FAIL=$((FAIL+1))
fi

# 8. Stub refuses TLC
run_step "8. Stub refuses TLC (expected exit 2)" 2 bash formal/model_check.sh --run-tlc

# 9. TLC PENDING
echo ""
echo ">>> 9. TLC runner reports PENDING without TLC"
TLA_JAR=/nonexistent bash formal/model_check_full.sh
rc=$?
if [ "$rc" -eq 2 ]; then
  echo "✅ PASS: 9. TLC PENDING (exit $rc)"
  PASS=$((PASS+1))
else
  echo "❌ FAIL: 9. TLC PENDING (exit $rc, expected 2)"
  FAIL=$((FAIL+1))
fi

echo ""
echo "=================================================="
echo " RESULTS: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  echo " ✅ ALL PHASE II PRE-PILOT TESTS PASSED"
else
  echo " ❌ SOME TESTS FAILED"
fi
echo "=================================================="

exit "$FAIL"
