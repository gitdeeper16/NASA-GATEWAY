#!/bin/bash
# Data tests — verify CSV files are well-formed

cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0

check_csv() {
  local file="$1"
  local min_rows="$2"

  if [ ! -f "$file" ]; then
    echo "  ❌ MISSING: $file"
    FAIL=$((FAIL+1))
    return
  fi

  local rows=$(($(wc -l < "$file") - 1))
  local header=$(head -1 "$file")

  echo "  ✅ $file"
  echo "     Header: $header"
  echo "     Data rows: $rows"

  if [ -n "$min_rows" ] && [ "$rows" -lt "$min_rows" ]; then
    echo "     ❌ Expected at least $min_rows rows, got $rows"
    FAIL=$((FAIL+1))
  else
    PASS=$((PASS+1))
  fi
}

echo "═══════════════════════════════════════════════════════"
echo " Test 1: traceability_matrix.csv (8 steps)"
echo "═══════════════════════════════════════════════════════"
check_csv "data/traceability_matrix.csv" 8

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 2: evidence_classification.csv (≥6 documents)"
echo "═══════════════════════════════════════════════════════"
check_csv "data/evidence_classification.csv" 6

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 3: requirement_to_property.csv"
echo "═══════════════════════════════════════════════════════"
check_csv "data/requirement_to_property.csv" 5

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 4: Requirement IDs referenced"
echo "═══════════════════════════════════════════════════════"

REQ_COUNT=$(grep -c "L2-GW\|L3-GLS" data/requirement_to_property.csv 2>/dev/null)
echo "  Requirement IDs in CSV: $REQ_COUNT"
if [ "$REQ_COUNT" -ge 5 ]; then
  echo "  ✅ Sufficient requirement coverage"
  PASS=$((PASS+1))
else
  echo "  ⚠️  Low requirement coverage"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
