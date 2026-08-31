$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "=== RetailPulse Phase 1 Demo ==="
Write-Host ""

Write-Host "1. Active data contracts"
Get-ChildItem ".\docs\data-contracts\*.yaml" |
    Where-Object { $_.Name -ne "contract-template.yaml" } |
    Select-Object -ExpandProperty Name

Write-Host ""
Write-Host "2. TPC-DS sample validation"
python -m pytest .\tests\test_tpcds.py -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "3. Event contract validation"
python -m pytest .\tests\test_events.py -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "4. Open-Meteo fixture and client validation"
python -m pytest .\tests\test_open_meteo.py -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "5. PostgreSQL OLTP integration"
docker compose up -d --wait postgres
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

try {
    $env:RUN_POSTGRES_INTEGRATION = "1"
    python -m pytest .\tests\test_postgres_integration.py -q
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Remove-Item Env:RUN_POSTGRES_INTEGRATION -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "6. Data contract validation"
python -m pytest .\tests\test_contracts.py -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=== Phase 1 demo completed successfully ==="
