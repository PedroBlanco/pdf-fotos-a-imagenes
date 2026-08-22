[CmdletBinding()]
param([Parameter(Mandatory=$true, Position=0, ValueFromRemainingArguments=$true)][string[]]$Path)
foreach ($item in $Path) {
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $item
    "{0}  {1}" -f $hash.Hash.ToLowerInvariant(), $item
}
