from __future__ import annotations

import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parent
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

