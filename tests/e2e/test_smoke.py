from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_sample_data_files_exist() -> None:
    expected_files = [
        "data/sample/roads.geojson",
        "data/sample/signs.geojson",
        "data/sample/speed_limits.geojson",
        "data/sample/observed_speeds.csv",
        "data/sample/release_candidate.geojson",
    ]

    missing = [path for path in expected_files if not (REPO_ROOT / path).is_file()]

    assert missing == []


def test_key_service_directories_exist() -> None:
    service_dirs = [
        "apps/web-dashboard/src",
        "apps/auto-headunit-simulator/src",
        "services/api-java/src",
        "services/partner-integration-java/src",
        "services/ml-python/app",
        "services/vehicle-signals-python/src/geospeed_vehicle",
        "services/matcher-cpp/src",
    ]

    missing = [path for path in service_dirs if not (REPO_ROOT / path).is_dir()]

    assert missing == []
