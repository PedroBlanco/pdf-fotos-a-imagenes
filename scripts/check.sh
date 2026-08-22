#!/usr/bin/env bash
set -euo pipefail
echo "Comprobaciones para pdf-fotos-a-imagenes (python)."
case "python" in
  generic)
    while IFS= read -r -d '' script_file; do bash -n "$script_file"; done < <(find scripts -type f -name '*.sh' -print0)
    ;;
  python)
    python -m compileall -q src tests
    python -m ruff check .
    python -m mypy src
    python -m pytest
    ;;
  node)
    node --check src/index.js
    npm run lint
    npm run format:check
    npm test
    ;;
  php)
    php -l src/App.php
    composer validate --strict
    vendor/bin/phpunit
    vendor/bin/phpstan analyse
    vendor/bin/php-cs-fixer fix --dry-run --diff
    ;;
esac
