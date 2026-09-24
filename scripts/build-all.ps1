$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DetectionRoot = Join-Path $RepoRoot "detections"

$Files = Get-ChildItem -Path $DetectionRoot -Recurse -Filter *.bicep

if (-not $Files) {
    throw "No Bicep detection files found under $DetectionRoot"
}

foreach ($File in $Files) {
    Write-Host "Building $($File.FullName)"
    az bicep build --file $File.FullName

    if ($LASTEXITCODE -ne 0) {
        throw "Bicep build failed: $($File.FullName)"
    }
}

Write-Host "All detection Bicep files compiled successfully."
