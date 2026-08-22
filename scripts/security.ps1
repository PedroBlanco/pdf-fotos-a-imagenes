$ErrorActionPreference = 'Stop'
$failed = $false

if (Get-Command gitleaks -ErrorAction SilentlyContinue) {
    $hasGitHead = $false
    if (Get-Command git -ErrorAction SilentlyContinue) {
        & git rev-parse --is-inside-work-tree *> $null
        $insideGit = ($LASTEXITCODE -eq 0)

        if ($insideGit) {
            & git rev-parse --verify HEAD *> $null
            $hasGitHead = ($LASTEXITCODE -eq 0)
        }
    }

    if ($hasGitHead) {
        Write-Host '[info] Gitleaks: análisis del historial Git.'
        & gitleaks git --redact .
    } else {
        Write-Host '[info] Gitleaks: análisis del árbol de archivos (sin HEAD válido).'
        & gitleaks dir --redact .
    }

    if ($LASTEXITCODE -ne 0) { $failed = $true }
} else {
    Write-Warning "Gitleaks no está instalado; se omite el escaneo local."
}

if (Get-Command trivy -ErrorAction SilentlyContinue) {
    & trivy fs --scanners vuln,secret,misconfig --exit-code 1 .
    if ($LASTEXITCODE -ne 0) { $failed = $true }
} else {
    Write-Warning "Trivy no está instalado; se omite el escaneo local."
}

if ($failed) { exit 1 }
