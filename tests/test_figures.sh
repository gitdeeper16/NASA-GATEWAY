#!/bin/bash
# Figure tests — verify all 6 figures exist

cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0

EXPECTED_FIGURES=(
  "Fig1_Traceability_Chain_Gap.png"
  "Fig2_Two_Pathways_Interface.png"
  "Fig3_MSM_VSM_Architecture.png"
  "Fig4_Evidence_Classification_Taxonomy.png"
  "Fig5_Gateway_Lunar_Orbit.png"
  "Fig6_Assurance_Case_GSN_Structure.png"
)

echo "═══════════════════════════════════════════════════════"
echo " Test 1: All 6 expected figures exist"
echo "═══════════════════════════════════════════════════════"

for f in "${EXPECTED_FIGURES[@]}"; do
  if [ -f "figures/$f" ]; then
    SIZE=$(du -h "figures/$f" | cut -f1)
    echo "  ✅ $f ($SIZE)"
    PASS=$((PASS+1))
  else
    echo "  ❌ MISSING: $f"
    FAIL=$((FAIL+1))
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 2: No unexpected PNG files"
echo "═══════════════════════════════════════════════════════"

EXTRA=$(ls figures/*.png 2>/dev/null | grep -v -E "Fig[1-6]_" || true)
if [ -z "$EXTRA" ]; then
  echo "  ✅ No unexpected PNG files"
  PASS=$((PASS+1))
else
  echo "  ⚠️  Extra PNG files found:"
  echo "$EXTRA"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 3: All figures referenced in docs/figure_provenance.md"
echo "═══════════════════════════════════════════════════════"

PROV="docs/figure_provenance.md"
if [ -f "$PROV" ]; then
  MISSING_REFS=""
  for f in "${EXPECTED_FIGURES[@]}"; do
    if ! grep -q "$f" "$PROV"; then
      MISSING_REFS="$MISSING_REFS $f"
    fi
  done
  if [ -z "$MISSING_REFS" ]; then
    echo "  ✅ All figures referenced in provenance doc"
    PASS=$((PASS+1))
  else
    echo "  ⚠️  Missing references:$MISSING_REFS"
    FAIL=$((FAIL+1))
  fi
else
  echo "  ⚠️  $PROV not found"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
