$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"

Push-Location $projectRoot

try {
    docker compose down

    $cachePaths = @(
        (Join-Path $projectRoot ".pytest_cache"),
        (Join-Path $projectRoot ".ruff_cache")
    )

    foreach ($cachePath in $cachePaths) {
        if (Test-Path $cachePath) {
            Remove-Item $cachePath -Recurse -Force
        }
    }

    $pythonCaches = @(
        Get-ChildItem -Path $projectRoot -Directory -Recurse -Force |
            Where-Object {
                $_.Name -eq "__pycache__" -and
                -not $_.FullName.StartsWith($venvPath)
            }
    )

    foreach ($pythonCache in $pythonCaches) {
        Remove-Item $pythonCache.FullName -Recurse -Force
    }

    Write-Host "RetailPulse local services stopped and caches removed."
}
finally {
    Pop-Location
}
