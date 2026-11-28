#!/usr/bin/env bash
# Phase II — H6 determinism test.
# Two runs with the same scenario, seed, and condition must produce
# byte-identical traces (excluding the "events" list ordering, which is
# already deterministic by construction).
set -euo pipefail
cd "$(dirname "$0")/.."

SCEN="$1"
SEED="${2:-42}"
COND="${3:-treatment}"

A=$(python3 -m model.run --scenario "$SCEN" --seed "$SEED" --condition "$COND")
B=$(python3 -m model.run --scenario "$SCEN" --seed "$SEED" --condition "$COND")

if [ "$A" = "$B" ]; then
  echo "✅ deterministic: $SCEN seed=$SEED condition=$COND"
else
  echo "❌ non-deterministic: $SCEN seed=$SEED condition=$COND"
  diff <(echo "$A") <(echo "$B") || true
  exit 1
fi
