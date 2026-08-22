[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Branch,
    [Parameter(Mandatory=$true)][string]$Path
)
$ErrorActionPreference = 'Stop'
git worktree add $Path -b $Branch
Write-Host "Worktree creado. Los secretos NO se copian automáticamente."
