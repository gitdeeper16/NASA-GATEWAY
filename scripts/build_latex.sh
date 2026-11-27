#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
PAPER="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.md"
OUT="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.tex"
command -v pandoc &>/dev/null || { echo "❌ pandoc not installed"; exit 1; }
pandoc "$PAPER" -o "$OUT" -s 
  --metadata title="NASA Gateway — Safety Assurance and Formal Verification" 
  --metadata author="Samir Baladi"
echo "✅ $OUT"
