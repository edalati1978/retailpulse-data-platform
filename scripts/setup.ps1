$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$envFile = Join-Path $projectRoot ".env"
$envExample = Join-Path $projectRoot ".env.example"

Push-Location $projectRoot

try {
    if (-not (Test-Path $venvPython)) {
        py -3.12 -m venv $venvPath
    }

    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install pytest==9.1.1 ruff==0.16.1

    if (-not (Test-Path $envFile)) {
        Copy-Item $envExample $envFile
    }

    docker compose up -d

    $services = @("postgres", "airflow")
    $deadline = (Get-Date).AddSeconds(120)
    $allHealthy = $false

    while ((Get-Date) -lt $deadline) {
        $allHealthy = $true

        foreach ($service in $services) {
            $containerId = docker compose ps -q $service

            if ([string]::IsNullOrWhiteSpace($containerId)) {
                $allHealthy = $false
                break
            }

            $health = docker inspect --format '{{.State.Health.Status}}' $containerId

            if ($health -ne "healthy") {
                $allHealthy = $false
                break
            }
        }

        if ($allHealthy) {
            break
        }

        Start-Sleep -Seconds 5
    }

    docker compose ps

    if (-not $allHealthy) {
        throw "Docker services did not become healthy within 120 seconds."
    }

    Write-Host "RetailPulse setup completed successfully."
}
finally {
    Pop-Location
}
