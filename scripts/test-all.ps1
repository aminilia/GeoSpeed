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

function Invoke-MavenTest {
    param([Parameter(Mandatory = $true)][string]$Path)

    Invoke-InDirectory $Path {
        if (Get-Command mvn -ErrorAction SilentlyContinue) {
            mvn test
        }
        elseif (Test-Path ".\mvnw.cmd") {
            cmd.exe /c mvnw.cmd test
        }
        else {
            throw "No mvn executable or mvnw.cmd found in $Path."
        }
    }
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue) -and (Test-Path "C:\Program Files\nodejs")) {
    $env:Path = "C:\Program Files\nodejs;$env:Path"
}

Invoke-InDirectory "apps/web-dashboard" {
    npm test -- --run
    npm run build
}

Invoke-InDirectory "apps/auto-headunit-simulator" {
    npm test
    npm run build
}

Invoke-InDirectory "services/ml-python" {
    python -m pytest
}

Invoke-InDirectory "services/vehicle-signals-python" {
    python -m pytest
}

Invoke-InDirectory "pipelines" {
    python -m pytest
}

Invoke-MavenTest "services/api-java"
Invoke-MavenTest "services/partner-integration-java"

docker compose config
