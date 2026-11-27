#!/bin/bash
# Structure tests — verify required files and directories exist

cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0

check_file() {
  if [ -f "$1" ]; then
    echo "  ✅ FILE: $1"
    PASS=$((PASS+1))
  else
    echo "  ❌ MISSING FILE: $1"
    FAIL=$((FAIL+1))
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    echo "  ✅ DIR:  $1/"
    PASS=$((PASS+1))
  else
    echo "  ❌ MISSING DIR:  $1/"
    FAIL=$((FAIL+1))
  fi
}

echo "═══════════════════════════════════════════════════════"
echo " Test 1: Required root files"
echo "═══════════════════════════════════════════════════════"

for f in README.md AUTHORS.md CHANGELOG.md CITATION.cff CONTRIBUTING.md \
         INVENTORY.md LICENSE PROJECT_SUMMARY.txt ROADMAP.md VERSION \
         manifest.json netlify.toml scientific_state.json .gitignore; do
  check_file "$f"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 2: Required directories"
echo "═══════════════════════════════════════════════════════"

for d in paper figures sources data docs tests scripts; do
  check_dir "$d"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo " Test 3: Manuscript"
echo "═══════════════════════════════════════════════════════"

PAPER="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.md"
if [ -f "$PAPER" ]; then
  WC=$(wc -w < "$PAPER")
  echo "  ✅ Manuscript exists ($WC words)"
  if [ "$WC" -gt 5000 ]; then
    echo "  ✅ Word count sufficient (>5000)"
    PASS=$((PASS+1))
  else
    echo "  ⚠️  Word count below 5000"
    FAIL=$((FAIL+1))
  fi
else
  echo "  ❌ Manuscript missing"
  FAIL=$((FAIL+1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo " RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
