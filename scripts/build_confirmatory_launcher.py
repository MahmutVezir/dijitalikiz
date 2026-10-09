from __future__ import annotations

import argparse
import base64
import hashlib
import tarfile
from pathlib import Path


def validate_source_bundle(bundle: Path) -> None:
    root_name = ""
    with tarfile.open(bundle, "r:gz") as archive:
        members = archive.getmembers()
        if not members:
            raise ValueError("The source bundle is empty.")
        for member in members:
            if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                raise ValueError(f"Unsupported source-bundle entry: {member.name!r}")
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe source-bundle path: {member.name!r}")
            root_name = member.name
    if not root_name:
        raise ValueError("The source bundle did not contain any files.")


def build_kernel_source(bundle_bytes: bytes, source_commit: str, runner_source: str) -> str:
    if len(source_commit) != 40 or any(
        char not in "0123456789abcdef" for char in source_commit.lower()
    ):
        raise ValueError("source_commit must be a full 40-character Git SHA.")
    if not bundle_bytes:
        raise ValueError("Source bundle bytes are empty.")

    bundle_sha256 = hashlib.sha256(bundle_bytes).hexdigest()
    bundle_b64 = base64.b64encode(bundle_bytes).decode("ascii")
    runner_b64 = base64.b64encode(runner_source.encode("utf-8")).decode("ascii")

    return f'''from __future__ import annotations

import base64
import hashlib
from pathlib import Path

BUNDLE_B64 = {bundle_b64!r}
EXPECTED_BUNDLE_SHA256 = {bundle_sha256!r}
FROZEN_SOURCE_COMMIT = {source_commit!r}
RUNNER_SOURCE_B64 = {runner_b64!r}


def main() -> None:
    kernel_root = Path("/kaggle/working")
    bundle_path = kernel_root / "project.tar.gz"
    commit_path = kernel_root / "source_commit.txt"

    bundle_bytes = base64.b64decode(BUNDLE_B64, validate=True)
    actual_sha256 = hashlib.sha256(bundle_bytes).hexdigest()
    if actual_sha256 != EXPECTED_BUNDLE_SHA256:
        raise RuntimeError(
            f"Embedded confirmatory source checksum mismatch: "
            f"expected {{EXPECTED_BUNDLE_SHA256}}, got {{actual_sha256}}"
        )

    bundle_path.write_bytes(bundle_bytes)
    commit_path.write_text(FROZEN_SOURCE_COMMIT + "\\n", encoding="utf-8")

    runner_source = base64.b64decode(RUNNER_SOURCE_B64, validate=True).decode("utf-8")
    exec(compile(runner_source, "kaggle/confirmatory_kernel.py", "exec"), {{
        "__name__": "__main__",
        "__file__": "kaggle/confirmatory_kernel.py",
    }})


if __name__ == "__main__":
    main()
'''


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a self-contained Kaggle kernel for the frozen confirmatory run."
    )
    parser.add_argument("--bundle", required=True, help="Exact-source .tar.gz bundle.")
    parser.add_argument("--source-commit", required=True, help="Full 40-character Git SHA.")
    parser.add_argument("--runner", default="kaggle/confirmatory_kernel.py")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    bundle = Path(args.bundle)
    runner = Path(args.runner)
    output_dir = Path(args.output_dir)
    if not bundle.is_file():
        raise SystemExit(f"Source bundle not found: {bundle}")
    if not runner.is_file():
        raise SystemExit(f"Confirmatory runner not found: {runner}")
    try:
        validate_source_bundle(bundle)
    except (OSError, tarfile.TarError, ValueError) as exc:
        raise SystemExit(f"Invalid source bundle: {exc}") from exc

    source = build_kernel_source(
        bundle.read_bytes(),
        args.source_commit,
        runner.read_text(encoding="utf-8"),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    kernel_path = output_dir / "kernel.py"
    kernel_path.write_text(source, encoding="utf-8")
    print(f"Generated self-contained launcher: {kernel_path} ({len(source):,} characters)")
    print(f"Source commit: {args.source_commit}")
    print(f"Source bundle SHA-256: {hashlib.sha256(bundle.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
