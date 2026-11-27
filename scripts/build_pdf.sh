#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
PAPER="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.md"
OUT="paper/NASA_Gateway_Safety_Assurance_and_Formal_Verification.pdf"
command -v pandoc &>/dev/null || { echo "❌ pandoc not installed"; exit 1; }
echo "▶ Building PDF..."
pandoc "$PAPER" -o "$OUT" --pdf-engine=xelatex 
  --metadata title="NASA Gateway — Safety Assurance and Formal Verification" 
  --metadata author="Samir Baladi" 
  --metadata date="2026-11-26" 
  -V geometry:margin=1in -V fontsize=11pt
[ -f "$OUT" ] && echo "✅ $OUT" || exit 1
