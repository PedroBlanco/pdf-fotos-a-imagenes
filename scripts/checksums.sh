#!/usr/bin/env bash
set -euo pipefail
if [[ $# -eq 0 ]]; then
  echo "Uso: $0 <archivo> [archivo...]" >&2
  exit 2
fi
sha256sum "$@"
