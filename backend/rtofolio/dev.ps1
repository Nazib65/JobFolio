$ErrorActionPreference = "Stop"

$backendRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendRoot

# Run with the venv interpreter to avoid accidentally using global Python packages.
& "$backendRoot\\venv\\Scripts\\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

