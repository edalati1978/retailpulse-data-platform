$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

function Assert-LastExitCode {
    param([string]$StepName)

    if ($LASTEXITCODE -ne 0) {
        throw "$StepName failed with exit code $LASTEXITCODE."
    }
}

Push-Location $projectRoot

try {
    if (-not (Test-Path $venvPython)) {
        throw "Python environment not found. Run scripts\setup.ps1 first."
    }

    Write-Host "Running Python tests..."
    & $venvPython -m pytest
    Assert-LastExitCode "Pytest"

    Write-Host "Running Ruff..."
    & $venvPython -m ruff check .
    Assert-LastExitCode "Ruff"

    Write-Host "Validating Docker Compose..."
    docker compose config --quiet
    Assert-LastExitCode "Docker Compose validation"

    Write-Host "Testing PostgreSQL..."
    docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -tA -c "SELECT CASE WHEN EXISTS (SELECT 1 FROM smoke_check WHERE id = 1) THEN 1 ELSE 0 END;" | grep -qx "1"'
    Assert-LastExitCode "PostgreSQL smoke test"

    Write-Host "Testing Airflow DAG..."
    docker compose exec -T airflow airflow dags test retailpulse_smoke
    Assert-LastExitCode "Airflow smoke DAG"

    Write-Host "All RetailPulse tests passed."
}
finally {
    Pop-Location
}
