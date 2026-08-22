$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw 'PowerShell 7+ requerido para scripts/check.ps1.'
}

function Resolve-CompatibleBash {
    if ($env:BASH_EXE) {
        $configured = [Environment]::ExpandEnvironmentVariables($env:BASH_EXE)
        if (-not (Test-Path -LiteralPath $configured -PathType Leaf)) {
            throw "BASH_EXE no apunta a un ejecutable existente: $configured"
        }
        return (Resolve-Path -LiteralPath $configured).Path
    }

    $candidates = [System.Collections.Generic.List[string]]::new()
    foreach ($commandName in @('bash', 'bash.exe')) {
        @(Get-Command $commandName -CommandType Application -All -ErrorAction SilentlyContinue) |
            ForEach-Object {
                if ($_.Source) { $candidates.Add($_.Source) }
            }
    }

    if ($env:OS -eq 'Windows_NT') {
        $known = @(
            $(if ($env:ProgramFiles) { Join-Path $env:ProgramFiles 'Git\bin\bash.exe' }),
            $(if ($env:ProgramFiles) { Join-Path $env:ProgramFiles 'Git\usr\bin\bash.exe' }),
            $(if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'Programs\Git\bin\bash.exe' }),
            $(if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'Programs\Git\usr\bin\bash.exe' }),
            'C:\msys64\usr\bin\bash.exe',
            'C:\mingw64\bin\bash.exe'
        )
        foreach ($candidate in $known) {
            if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
                $candidates.Add($candidate)
            }
        }
    }

    foreach ($candidate in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
        if ($env:OS -eq 'Windows_NT') {
            if ($candidate -match '(?i)\\Windows\\(?:System32|Sysnative)\\bash\.exe$') { continue }
            if ($candidate -match '(?i)\\WindowsApps\\bash\.exe$') { continue }
        }
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
    }
    return $null
}

function Convert-ToBashPath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$BashExe
    )

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if ($env:OS -ne 'Windows_NT') {
        return $fullPath
    }

    $bashDir = Split-Path -Parent $BashExe
    $bashParent = Split-Path -Parent $bashDir
    $cygpathCandidates = @(
        (Join-Path $bashDir 'cygpath.exe'),
        (Join-Path $bashParent 'usr\bin\cygpath.exe')
    )

    foreach ($cygpath in ($cygpathCandidates | Select-Object -Unique)) {
        if (-not (Test-Path -LiteralPath $cygpath -PathType Leaf)) {
            continue
        }

        $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
        $startInfo.FileName = $cygpath
        $startInfo.UseShellExecute = $false
        $startInfo.RedirectStandardOutput = $true
        $startInfo.RedirectStandardError = $true
        $startInfo.ArgumentList.Add('-u')
        $startInfo.ArgumentList.Add('--')
        $startInfo.ArgumentList.Add($fullPath)

        $process = [System.Diagnostics.Process]::new()
        $process.StartInfo = $startInfo
        [void]$process.Start()
        $stdout = $process.StandardOutput.ReadToEnd().Trim()
        $stderr = $process.StandardError.ReadToEnd().Trim()
        $process.WaitForExit()

        if ($process.ExitCode -eq 0 -and $stdout) {
            return $stdout
        }

        Write-Verbose "cygpath falló ($cygpath): $stderr"
    }

    if ($fullPath -match '^([A-Za-z]):[\\/](.*)$') {
        $drive = $Matches[1].ToLowerInvariant()
        $rest = $Matches[2] -replace '\\', '/'
        return "/$drive/$rest"
    }

    return ($fullPath -replace '\\', '/')
}

function Invoke-BashSyntaxCheck {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$BashExe,

        [Parameter(Mandatory)]
        [string]$FilePath
    )

    $bashPath = Convert-ToBashPath -Path $FilePath -BashExe $BashExe

    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $BashExe
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.ArgumentList.Add('-n')
    $startInfo.ArgumentList.Add('--')
    $startInfo.ArgumentList.Add($bashPath)

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    [void]$process.Start()
    $stdout = $process.StandardOutput.ReadToEnd().Trim()
    $stderr = $process.StandardError.ReadToEnd().Trim()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        $details = @(
            "Sintaxis Bash inválida: $FilePath"
            "Bash: $BashExe"
            "Ruta entregada a Bash: $bashPath"
            "Código de salida: $($process.ExitCode)"
        )
        if ($stdout) { $details += "stdout:`n$stdout" }
        if ($stderr) { $details += "stderr:`n$stderr" }
        throw ($details -join [Environment]::NewLine)
    }
}
Write-Host "Comprobaciones para pdf-fotos-a-imagenes (python)."
switch ('python') {
    'generic' {
        $BashExe = Resolve-CompatibleBash
        if ($BashExe) {
            Get-ChildItem scripts -Filter *.sh -Recurse | ForEach-Object {
                Invoke-BashSyntaxCheck -BashExe $BashExe -FilePath $_.FullName
            }
        } else {
            Write-Warning 'Bash compatible no disponible; se omite la sintaxis Bash.'
        }
    }
    'python' {
        python -m compileall -q src tests
        python -m ruff check .
        python -m mypy src
        python -m pytest
    }
    'node' {
        node --check src/index.js
        npm run lint
        npm run format:check
        npm test
    }
    'php' {
        php -l src/App.php
        composer validate --strict
        & vendor/bin/phpunit
        & vendor/bin/phpstan analyse
        & vendor/bin/php-cs-fixer fix --dry-run --diff
    }
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
