#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
exec bash tests/run_all.sh
