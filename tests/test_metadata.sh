#!/bin/bash
# Metadata tests — verify DOIs, usernames, identifiers

cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0

# Helper: search excluding tests/
search_excluding_tests() {
  grep -rn "$1" . 2>/dev/null | grep -v "^./tests/" | grep -v "^./scripts/"
}

echo "═══════════════════════════════════════════════════════"
echo " Test 1: Correct DOI present (10.5281/zenodo.24559255)"
echo "═══════════════════════════════════════════════════════"

DOI_COUNT=$(search_excluding_tests "24559255" | wc -l)
echo "  References containing DOI: $DOI_COUNT"
if [ "$DOI_COUNT" -ge 5 ]; then
  echo "  ✅ DOI present in sufficient files"
  PASS=$((PASS+1))
else
  echo "  ❌ DOI not widely present (expected ≥5)"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 2: Correct GitHub username (gitdeeper16)"
echo "═══════════════════════════════════════════════════════"

GH_COUNT=$(search_excluding_tests "gitdeeper16" | wc -l)
echo "  References containing gitdeeper16: $GH_COUNT"
if [ "$GH_COUNT" -ge 4 ]; then
  echo "  ✅ Username present"
  PASS=$((PASS+1))
else
  echo "  ❌ Username not widely present"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 3: No old username (gitdeeper15) outside tests/"
echo "═══════════════════════════════════════════════════════"

OLD_GH=$(search_excluding_tests "gitdeeper15")
if [ -z "$OLD_GH" ]; then
  echo "  ✅ No gitdeeper15 found outside tests/"
  PASS=$((PASS+1))
else
  echo "  ❌ Found gitdeeper15:"
  echo "$OLD_GH"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 4: No old DOIs outside tests/"
echo "═══════════════════════════════════════════════════════"

OLD_DOI=$(search_excluding_tests "24466801\|24433970\|24433969\|24473998")
if [ -z "$OLD_DOI" ]; then
  echo "  ✅ No old DOIs found outside tests/"
  PASS=$((PASS+1))
else
  echo "  ❌ Found old DOIs:"
  echo "$OLD_DOI"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 5: Correct website (nasa-gateway.netlify.app)"
echo "═══════════════════════════════════════════════════════"

WEBSITE_COUNT=$(search_excluding_tests "nasa-gateway.netlify.app" | wc -l)
echo "  References containing website: $WEBSITE_COUNT"
if [ "$WEBSITE_COUNT" -ge 2 ]; then
  echo "  ✅ Website present"
  PASS=$((PASS+1))
else
  echo "  ❌ Website not present"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
