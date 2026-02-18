function Get-LargePythonFiles {
    param (
        [int]$Limit = 10
    )

    Get-ChildItem .\src -Recurse -Filter *.py |
    ForEach-Object {
        $lineCount = [System.IO.File]::ReadLines($_.FullName).Count
        if ($lineCount -gt $Limit) {
            [PSCustomObject]@{
                File      = $_.FullName.Replace("$PWD\", "")
                LineCount = $lineCount
            }
        }
    } | Sort-Object LineCount -Descending
}
