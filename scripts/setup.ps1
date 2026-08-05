$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$envFile = Join-Path $projectRoot ".env"
$envExample = Join-Path $projectRoot ".env.example"

function Test-Python312 {
    param(
        [string]$Executable,
        [string[]]$PrefixArguments = @()
    )

    $argumentList = @($PrefixArguments) + @(
        "-c",
        "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)"
    )

    & $Executable @argumentList
    return $LASTEXITCODE -eq 0
}

function Find-Python312 {
    $pyCommand = Get-Command py -ErrorAction SilentlyContinue |
        Select-Object -First 1

    if (
        $null -ne $pyCommand -and
        (Test-Python312 -Executable $pyCommand.Source -PrefixArguments @("-3.12"))
    ) {
        return @{
            Executable = $pyCommand.Source
            PrefixArguments = @("-3.12")
        }
    }

    foreach ($commandName in @("python", "python3")) {
        $commands = @(
            Get-Command $commandName -All -ErrorAction SilentlyContinue
        )

        foreach ($command in $commands) {
            if ($command.Source -match '[\\/]\.venv[\\/]') {
                continue
            }

            if (Test-Python312 -Executable $command.Source) {
                return @{
                    Executable = $command.Source
                    PrefixArguments = @()
                }
            }
        }
    }

    throw "Python 3.12 was not found. Install Python 3.12 and run setup again."
}

Push-Location $projectRoot

try {
    if (-not (Test-Path $venvPython)) {
        $python312 = Find-Python312
        $venvArguments = @($python312.PrefixArguments) + @(
            "-m",
            "venv",
            $venvPath
        )

        & $python312.Executable @venvArguments

        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython)) {
            throw "Python virtual environment creation failed."
        }
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
