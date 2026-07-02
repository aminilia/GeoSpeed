$ErrorActionPreference = "Stop"

function Test-MakeTarget {
    param([Parameter(Mandatory = $true)][string]$Target)

    if (-not (Test-Path "Makefile")) {
        return $false
    }

    return Select-String -Path "Makefile" -Pattern "^$([regex]::Escape($Target)):" -Quiet
}

if ((Get-Command make -ErrorAction SilentlyContinue) -and (Test-MakeTarget "ingest-sample") -and (Test-MakeTarget "release-report")) {
    make ingest-sample
    make release-report
    exit 0
}

$requiredFiles = @(
    "pipelines/ingest/ingest_osm_roads.py",
    "pipelines/transform/infer_speed_limits.py",
    "pipelines/validate/generate_release_report.py",
    "data/sample/roads.geojson",
    "data/sample/speed_limits.geojson",
    "data/sample/signs.geojson",
    "data/sample/observed_speeds.csv"
)

$missing = $requiredFiles | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
    throw "Cannot run sample pipeline. Missing: $($missing -join ', ')"
}

python pipelines/ingest/ingest_osm_roads.py --input data/sample/roads.geojson --output data/sample/normalized_roads.json
python pipelines/transform/infer_speed_limits.py --segments data/sample/roads.geojson --speeds data/sample/speed_limits.geojson --signs data/sample/signs.geojson --observed data/sample/observed_speeds.csv --output data/sample/release_candidate.geojson
python pipelines/validate/generate_release_report.py --input data/sample/release_candidate.geojson --output data/sample/release_report.md
