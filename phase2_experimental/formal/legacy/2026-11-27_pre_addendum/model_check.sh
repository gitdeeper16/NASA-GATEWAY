#!/usr/bin/env bash
# Phase II — TLC model checker runner.
# State space frozen at PREREGISTRATION freeze 2026-11-27.
# Fails LOUDLY if TLC is unavailable; H5 cannot be claimed without TLC.
set -euo pipefail
cd "$(dirname "$0")"

MAX_COMPONENTS=4
MAX_CYCLES=20
MAX_ESCALATION_DEPTH=2
MAX_MESSAGES_IN_FLIGHT=3

echo "Frozen state space:"
echo "  MAX_COMPONENTS=$MAX_COMPONENTS"
echo "  MAX_CYCLES=$MAX_CYCLES"
echo "  MAX_ESCALATION_DEPTH=$MAX_ESCALATION_DEPTH"
echo "  MAX_MESSAGES_IN_FLIGHT=$MAX_MESSAGES_IN_FLIGHT"

TLA_JAR="${TLA_JAR:-tla2tools.jar}"
if [ ! -f "$TLA_JAR" ]; then
  echo "❌ tla2tools.jar not found at $TLA_JAR"
  echo "   H5 is PENDING until TLC is available."
  echo "   Set TLA_JAR=/path/to/tla2tools.jar and retry."
  exit 2
fi

java -cp "$TLA_JAR" tlc2.TLC \
    -config GatewayPhase2.cfg \
    -workers auto \
    -deadlock \
    GatewayPhase2.tla
