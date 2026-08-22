#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Uso: $0 <rama> <ruta>" >&2
  exit 2
fi
branch="$1"
path="$2"
git worktree add "$path" -b "$branch"
echo "Worktree creado. Los secretos NO se copian automáticamente."
