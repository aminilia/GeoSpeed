from pathlib import Path

from geospeed_pipeline.validate_samples import validate_synthetic_signs


def test_validate_synthetic_signs() -> None:
    sample_path = Path(__file__).resolve().parents[2] / "sample-data" / "synthetic_sign_observations.csv"

    assert validate_synthetic_signs(sample_path) == 3

