"""Independent file-mode reproducer for Lektor issue #1213 / PR #1214."""
from __future__ import annotations

import os
import stat


def test_new_artifact_mode_matches_normally_created_file(tmp_path, builder):
    previous_umask = os.umask(0o022)
    try:
        normal_file = tmp_path / "ordinary-file.txt"
        normal_file.write_text("ordinary", encoding="utf-8")
        normal_mode = stat.S_IMODE(normal_file.stat().st_mode)

        build_state = builder.new_build_state()
        artifact = build_state.new_artifact("permission-regression", sources=())
        with artifact.update(), artifact.open("w", encoding="utf-8") as fp:
            fp.write("artifact")

        artifact_mode = stat.S_IMODE(os.stat(artifact.dst_filename).st_mode)
    finally:
        os.umask(previous_umask)

    assert artifact_mode == normal_mode, (
        f"artifact mode={oct(artifact_mode)}; "
        f"normal file mode={oct(normal_mode)}"
    )
