#!/usr/bin/env bash
set -euo pipefail

echo "Comprobaciones para pdf-fotos-a-imagenes."
python -m compileall -q src tests
python -m ruff check .
python -m mypy src
python -m pytest
