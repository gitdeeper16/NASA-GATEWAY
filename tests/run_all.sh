#!/bin/bash
# Run all integrity tests

cd "$(dirname "$0")/.." || exit 1

TOTAL_FAIL=0
TESTS=(
  "tests/test_structure.sh"
  "tests/test_metadata.sh"
  "tests/test_data.sh"
  "tests/test_figures.sh"
  "tests/test_content.sh"
)

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  NASA Gateway Project — Full Test Suite              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

for t in "${TESTS[@]}"; do
  echo "▶ Running $t..."
  echo ""
  bash "$t"
  RESULT=$?
  echo ""
  echo ""
  if [ "$RESULT" -ne 0 ]; then
    TOTAL_FAIL=$((TOTAL_FAIL+1))
  fi
done

echo "╔═══════════════════════════════════════════════════════╗"
if [ "$TOTAL_FAIL" -eq 0 ]; then
  echo "║  ✅ ALL TESTS PASSED                                 ║"
else
  echo "║  ❌ $TOTAL_FAIL TEST FILE(S) FAILED                  ║"
fi
echo "╚═══════════════════════════════════════════════════════╝"

exit "$TOTAL_FAIL"
