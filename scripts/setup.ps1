$ErrorActionPreference = "Stop"

function Invoke-InDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][scriptblock]$Command
    )

    Push-Location $Path
    try {
        & $Command
    }
    finally {
        Pop-Location
    }
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue) -and (Test-Path "C:\Program Files\nodejs")) {
    $env:Path = "C:\Program Files\nodejs;$env:Path"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm was not found on PATH. Install Node.js before running frontend setup."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "python was not found on PATH. Install Python before running backend setup."
}

Invoke-InDirectory "apps/web-dashboard" {
    npm install
}

Invoke-InDirectory "apps/auto-headunit-simulator" {
    npm install
}

Invoke-InDirectory "services/ml-python" {
    python -m pip install -r requirements-dev.txt
}

Invoke-InDirectory "services/vehicle-signals-python" {
    python -m pip install -e ".[dev]"
}

Invoke-InDirectory "pipelines" {
    python -m pip install -r requirements-dev.txt
}
