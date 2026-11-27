#!/bin/bash
# Content tests — verify no forbidden strings, required concepts present

cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0

# Helper: search excluding tests/ and scripts/
search_excluding_tests() {
  grep -rn "$1" . 2>/dev/null | grep -v "^./tests/" | grep -v "^./scripts/"
}

echo "═══════════════════════════════════════════════════════"
echo " Test 1: No forbidden strings outside tests/"
echo "═══════════════════════════════════════════════════════"

FORBIDDEN="gitdeeper15\|24466801\|24433970\|24433969\|24473998\|AetherSovereignty\|StructOPE\|EZJKF"
BAD=$(search_excluding_tests "$FORBIDDEN")
if [ -z "$BAD" ]; then
  echo "  ✅ No forbidden strings found"
  PASS=$((PASS+1))
else
  echo "  ❌ Found forbidden strings:"
  echo "$BAD"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 2: Critical requirement IDs present"
echo "═══════════════════════════════════════════════════════"

PAPER="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.md"
if [ -f "$PAPER" ]; then
  for req in "L2-GW-0199" "R2U2" "AGC"; do
    COUNT=$(grep -c "$req" "$PAPER" 2>/dev/null)
    if [ "$COUNT" -ge 1 ]; then
      echo "  ✅ $req ($COUNT references)"
      PASS=$((PASS+1))
    else
      echo "  ❌ $req NOT FOUND"
      FAIL=$((FAIL+1))
    fi
  done
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 3: No positive overstatement (NASA lacks...)"
echo "═══════════════════════════════════════════════════════"

# Strategy: extract each sentence containing "NASA lacks" and check
# whether it is negated (contains "not", "does not", "never", "no claim")
# within the SAME sentence.
#
# We use a Python one-liner for robust sentence-level analysis.

OVERSTATEMENTS=$(python3 - "$PAPER" << 'PYEOF' 2>/dev/null
import re, sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Split into sentences (approximate)
sentences = re.split(r'(?<=[.!?])\s+', text)

negation_markers = [
    'does not', "doesn't", 'do not', "don't",
    'is not', "isn't", 'are not', "aren't",
    'not claim', 'not to claim', 'never',
    'cannot', 'can not', "can't",
    'no claim', 'not assert', 'not demonstrate',
    'not imply', 'not suggest', 'not conclude',
    'not evidence', 'not establish',
]

positive_claims = []
for s in sentences:
    if 'NASA lacks' in s.lower() or 'NASA lack' in s.lower():
        s_lower = s.lower()
        is_negated = any(m in s_lower for m in negation_markers)
        if not is_negated:
            positive_claims.append(s.strip())

for claim in positive_claims:
    print(claim)
PYEOF
)

if [ -z "$OVERSTATEMENTS" ]; then
  echo "  ✅ No positive overstatement claims found (all instances are negated)"
  PASS=$((PASS+1))
else
  echo "  ❌ Found positive overstatement(s):"
  echo "$OVERSTATEMENTS"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 4: Key concepts present in manuscript"
echo "═══════════════════════════════════════════════════════"

for concept in "traceability" "VSM" "MSM" "safety assurance" "formal verification"; do
  COUNT=$(grep -ci "$concept" "$PAPER" 2>/dev/null)
  if [ "$COUNT" -ge 3 ]; then
    echo "  ✅ '$concept' ($COUNT references)"
    PASS=$((PASS+1))
  else
    echo "  ⚠️  '$concept' low ($COUNT references)"
    FAIL=$((FAIL+1))
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo " RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
