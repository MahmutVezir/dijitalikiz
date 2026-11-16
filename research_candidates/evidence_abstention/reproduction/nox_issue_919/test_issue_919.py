"""Independent reproducer for wntrblm/nox#919 (broken pyenv uv shim)."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import unittest

_fake_bin = Path(tempfile.mkdtemp(prefix="nox-919-uv-shim-"))
_fake_uv = _fake_bin / "uv"
_fake_uv.write_text(
    "#!/usr/bin/env python3\n"
    "import sys\n"
    "sys.stderr.write('pyenv: uv: command not found\\n')\n"
    "sys.exit(127)\n",
    encoding="utf-8",
)
_fake_uv.chmod(0o755)
os.environ["PATH"] = str(_fake_bin) + os.pathsep + os.environ.get("PATH", "")
sys.modules["uv"] = None

import nox.virtualenv as nox_virtualenv  # noqa: E402


class NoxIssue919Regression(unittest.TestCase):
    def test_broken_pyenv_uv_shim_is_not_detected_as_available(self) -> None:
        self.assertFalse(nox_virtualenv.HAS_UV)


if __name__ == "__main__":
    unittest.main(verbosity=2)
