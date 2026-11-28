#!/usr/bin/env bash
# Phase II — TLC runner (Addendum 001).
# NOT in the original freeze digest. SHA recorded in
# results/.addendum_001.sha256.
#
# What a successful run means: the MODEL satisfies the stated properties
# within the frozen bounds. It does NOT mean that NASA's operational
# Gateway is safe. See PREREGISTRATION.md §12.
set -euo pipefail
cd "$(dirname "$0")"

MAX_COMPONENTS=4
MAX_CYCLES=20
MAX_ESCALATION_DEPTH=2
MAX_MESSAGES_IN_FLIGHT=3

echo "State space (from frozen stub):"
echo "  MAX_COMPONENTS=$MAX_COMPONENTS"
echo "  MAX_CYCLES=$MAX_CYCLES"
echo "  MAX_ESCALATION_DEPTH=$MAX_ESCALATION_DEPTH"
echo "  MAX_MESSAGES_IN_FLIGHT=$MAX_MESSAGES_IN_FLIGHT"

TLA_JAR="${TLA_JAR:-tla2tools.jar}"
if [ ! -f "$TLA_JAR" ]; then
  echo ""
  echo "❌ tla2tools.jar not found at $TLA_JAR"
  echo "   H5 is PENDING until TLC is available."
  echo "   Set TLA_JAR=/path/to/tla2tools.jar and retry."
  echo "   This is not a failure of H5; it is an unexecuted verification."
  exit 2
fi

LOG="results/tlc_run_$(date -u +%Y-%m-%dT%H-%M-%SZ).log"
mkdir -p results
{
  echo "TLC run log"
  echo "  date:        $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "  TLA_JAR:     $TLA_JAR"
  echo "  cfg:         GatewayPhase2.cfg"
  echo "  tla:         GatewayPhase2.tla properties.tla"
  echo "  state space: MAX_COMPONENTS=$MAX_COMPONENTS MAX_CYCLES=$MAX_CYCLES MAX_ESCALATION_DEPTH=$MAX_ESCALATION_DEPTH MAX_MESSAGES_IN_FLIGHT=$MAX_MESSAGES_IN_FLIGHT"
  echo "  SHAs:"
  sha256sum GatewayPhase2.tla properties.tla GatewayPhase2.cfg | sed 's/^/    /'
  echo ""
} > "$LOG"

java -cp "$TLA_JAR" tlc2.TLC \
    -config GatewayPhase2.cfg \
    -workers auto \
    -deadlock \
    GatewayPhase2.tla 2>&1 | tee -a "$LOG"

echo ""
echo "Log saved to $LOG"
