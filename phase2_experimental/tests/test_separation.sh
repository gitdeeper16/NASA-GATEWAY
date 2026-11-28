#!/usr/bin/env bash
# Phase II — H6 supporting test: pilot/confirmatory separation.
#
# Enforces PREREGISTRATION.md §5.3 at the file level:
#   1. seed sets are disjoint;
#   2. confirmatory analysis code must not read from results/pilot/;
#   3. pilot results must not appear in results/confirmatory/.
set -euo pipefail
cd "$(dirname "$0")/.."

FAIL=0
note() { echo "  $*"; }

echo "== 1. Seed files exist and are disjoint =="
for f in experiments/seeds_pilot.txt experiments/seeds_confirmatory.txt; do
  if [ ! -f "$f" ]; then
    echo "❌ missing $f"; FAIL=1
  fi
done

PY_PILOT=$(grep -vE '^\s*#|^\s*$' experiments/seeds_pilot.txt | wc -l)
PY_CONF=$(grep -vE '^\s*#|^\s*$' experiments/seeds_confirmatory.txt | wc -l)
note "pilot seeds: $PY_PILOT (expected 20)"
note "confirmatory seeds: $PY_CONF (expected 80)"
[ "$PY_PILOT" -eq 20 ] || { echo "❌ pilot seed count != 20"; FAIL=1; }
[ "$PY_CONF" -eq 80 ] || { echo "❌ confirmatory seed count != 80"; FAIL=1; }

OVERLAP=$(python3 - << 'PY'
p = {int(l) for l in open("experiments/seeds_pilot.txt")
     if l.strip() and not l.startswith("#")}
c = {int(l) for l in open("experiments/seeds_confirmatory.txt")
     if l.strip() and not l.startswith("#")}
print(len(p & c))
PY
)
note "overlap: $OVERLAP (expected 0)"
[ "$OVERLAP" -eq 0 ] || { echo "❌ seed sets overlap"; FAIL=1; }

echo ""
echo "== 2. Pilot seeds must not appear in confirmatory results =="
if [ -d results/confirmatory ] && [ -n "$(ls -A results/confirmatory 2>/dev/null)" ]; then
  PILOT_SEEDS=$(grep -vE '^\s*#|^\s*$' experiments/seeds_pilot.txt | tr '\n' ' ')
  HITS=$(grep -rE "\"seed\"\s*:\s*(${PILOT_SEEDS})" results/confirmatory/ 2>/dev/null || true)
  if [ -n "$HITS" ]; then
    echo "❌ pilot seed found in confirmatory results:"
    echo "$HITS" | head -5
    FAIL=1
  else
    note "no pilot seed in confirmatory results ✅"
  fi
else
  note "(confirmatory/ empty — check skipped)"
fi

echo ""
echo "== 3. Confirmatory analysis code must not read from results/pilot =="
# Heuristic: search for 'results/pilot' in any confirmatory analysis script.
if [ -d experiments/confirmatory ] || [ -d results/confirmatory ]; then
  if grep -rn "results/pilot" experiments/confirmatory/ results/confirmatory/ 2>/dev/null; then
    echo "❌ confirmatory code references results/pilot"
    FAIL=1
  else
    note "no confirmatory→pilot reference ✅"
  fi
fi

echo ""
echo "== 4. Pilot results must not have leaked into confirmatory/ =="
if [ -d results/confirmatory ] && [ -d results/pilot ]; then
  # If any file in confirmatory/ has identical SHA to a file in pilot/,
  # that is a leak (same content in two stages).
  LEAK=0
  while IFS= read -r f; do
    h=$(sha256sum "$f" | awk '{print $1}')
    if grep -rq "$h" results/pilot/ 2>/dev/null; then
      echo "❌ $f has identical SHA to a file in results/pilot/"
      LEAK=1
    fi
  done < <(find results/confirmatory -type f 2>/dev/null)
  [ "$LEAK" -eq 0 ] && note "no content leak ✅"
  [ "$LEAK" -eq 0 ] || FAIL=1
else
  note "(pilot or confirmatory empty — leak check skipped)"
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "✅ test_separation: PASS"
else
  echo "❌ test_separation: FAIL"
  exit 1
fi
