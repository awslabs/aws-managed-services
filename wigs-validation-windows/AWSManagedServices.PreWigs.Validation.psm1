Get-ChildItem -Path $PSScriptRoot -Recurse -Include *.ps1 -Exclude *.Tests.ps1 | ForEach-Object {
    . $_.FullName
    Export-ModuleMember -Function $_.BaseName -Alias *
}