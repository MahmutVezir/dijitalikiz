from __future__ import annotations

"""Backward-compatible entry point for the single fail-closed compatibility gate."""

from compatibility_gate import main


if __name__ == "__main__":
    raise SystemExit(main())
