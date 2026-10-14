from __future__ import annotations

"""Compatibility entry point retained for the existing Kaggle launcher.

All model/runtime checks are centralized in compatibility_gate.py. The legacy
--require-cuda flag is consumed here so the launcher remains backward compatible.
"""

import sys

from compatibility_gate import main


if __name__ == "__main__":
    sys.argv = [sys.argv[0]]
    raise SystemExit(main())
