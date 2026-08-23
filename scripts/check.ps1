$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw 'PowerShell 7+ requerido para scripts/check.ps1.'
}

Write-Host 'Comprobaciones para pdf-fotos-a-imagenes.'

python -m compileall -q src tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m ruff check .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m mypy src
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m pytest
exit $LASTEXITCODE
