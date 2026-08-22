#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo "Uso: $0 <ruta>" >&2
  exit 2
fi
git worktree remove "$1"
git worktree prune
