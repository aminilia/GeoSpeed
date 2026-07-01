from __future__ import annotations

import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from ingest.ingest_sign_observations import main


if __name__ == "__main__":
    main()
