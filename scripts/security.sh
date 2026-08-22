#!/usr/bin/env bash
set -euo pipefail

status=0
if command -v gitleaks >/dev/null 2>&1; then
  if command -v git >/dev/null 2>&1 \
    && git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    && git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "[info] Gitleaks: análisis del historial Git."
    gitleaks git --redact . || status=$?
  else
    echo "[info] Gitleaks: análisis del árbol de archivos (sin HEAD válido)."
    gitleaks dir --redact . || status=$?
  fi
else
  echo "[aviso] Gitleaks no está instalado; se omite el escaneo local."
fi

if command -v trivy >/dev/null 2>&1; then
  trivy fs --scanners vuln,secret,misconfig --exit-code 1 . || status=$?
else
  echo "[aviso] Trivy no está instalado; se omite el escaneo local."
fi

exit "$status"
