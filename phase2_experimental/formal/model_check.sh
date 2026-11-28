#!/usr/bin/env bash
# Phase II — TLC state space, fixed at PREREGISTRATION freeze 2026-11-27.
# The state space below is FROZEN. Expanding it after freeze to avoid a
# counterexample invalidates H5 (see docs/METHODOLOGICAL_REVIEW.md §5).
#
# This file is a STUB at freeze: it declares the state-space bounds that
# the TLA+ model must respect. It does NOT run TLC. The TLC runner is
# formal/model_check_full.sh, which is recorded in Addendum 001 and is not
# part of the original freeze digest.
#
# The original stub (SHA f13fc1b2...) was lost during implementation and
# was reconstructed here. See docs/ADDENDUM_001_2026-11-27.md §3.2.

set -euo pipefail

MAX_COMPONENTS=4
MAX_CYCLES=20
MAX_ESCALATION_DEPTH=2
MAX_MESSAGES_IN_FLIGHT=3

if [ "${1:-}" = "--run-tlc" ]; then
  echo "❌ This is the frozen stub, not the TLC runner."
  echo "   Use formal/model_check_full.sh for TLC."
  echo "   H5 remains PENDING until a reproducible TLC run is logged."
  exit 2
fi

echo "Frozen state space:"
echo "  MAX_COMPONENTS=$MAX_COMPONENTS"
echo "  MAX_CYCLES=$MAX_CYCLES"
echo "  MAX_ESCALATION_DEPTH=$MAX_ESCALATION_DEPTH"
echo "  MAX_MESSAGES_IN_FLIGHT=$MAX_MESSAGES_IN_FLIGHT"
