from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_expected_workspace_folders_exist() -> None:
    expected_paths = [
        "apps/web-dashboard",
        "apps/auto-headunit-simulator",
        "services/api-java",
        "services/partner-integration-java",
        "services/ml-python",
        "services/vehicle-signals-python",
        "services/matcher-cpp",
        "pipelines",
        "infra/docker",
        "infra/k8s",
        "docs/product",
        "docs/engineering",
    ]

    missing = [path for path in expected_paths if not (REPO_ROOT / path).is_dir()]

    assert missing == []


def test_core_project_files_exist() -> None:
    expected_files = [
        "README.md",
        "Makefile",
        "docker-compose.yml",
        ".github/workflows/ci.yml",
    ]

    missing = [path for path in expected_files if not (REPO_ROOT / path).is_file()]

    assert missing == []
