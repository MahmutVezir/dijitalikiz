from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
BUNDLE_SOURCE = KERNEL_ROOT / "project.tar.gz"
SOURCE_COMMIT_FILE = KERNEL_ROOT / "source_commit.txt"

# Kaggle exports files left in /kaggle/working. Source code, wheels and the
# Python environment therefore stay in /tmp; only final research artifacts
# are copied back to KERNEL_ROOT.
RUNTIME_ROOT = Path("/tmp/dijitalikiz-confirmatory-runtime")
BUNDLE = RUNTIME_ROOT / "project.tar.gz"
WORKDIR = RUNTIME_ROOT / "dijitalikiz"
PYTHON_ENV = RUNTIME_ROOT / "dijitalikiz-py311"
TARGET_PYTHON = PYTHON_ENV / "bin" / "python"
OUTPUT_DIR = KERNEL_ROOT / "confirmatory-output"


def run(
    *args: str,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, env=env, check=True)


def output(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def ensure_python311() -> Path:
    """Provision the pinned Python minor version in an isolated /tmp env."""
    if TARGET_PYTHON.is_file():
        detected = output(
            str(TARGET_PYTHON),
            "-c",
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
        )
        if detected == "3.11":
            return TARGET_PYTHON
        shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    for manager in (
        "/opt/conda/bin/mamba",
        "/opt/conda/bin/conda",
        "mamba",
        "conda",
    ):
        executable = (
            shutil.which(manager)
            if not Path(manager).is_absolute()
            else manager
        )
        if executable and Path(executable).is_file():
            try:
                run(
                    executable,
                    "create",
                    "-y",
                    "--prefix",
                    str(PYTHON_ENV),
                    "python=3.11",
                    "pip",
                )
                if TARGET_PYTHON.is_file():
                    return TARGET_PYTHON
            except (OSError, subprocess.CalledProcessError):
                shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    shutil.rmtree(PYTHON_ENV, ignore_errors=True)
    run(sys.executable, "-m", "pip", "install", "--quiet", "uv")
    uv = shutil.which("uv")
    if not uv:
        candidate = Path(sys.executable).resolve().parent / "uv"
        if candidate.is_file():
            uv = str(candidate)
    if not uv:
        candidate = Path.home() / ".local" / "bin" / "uv"
        if candidate.is_file():
            uv = str(candidate)
    if not uv:
        raise RuntimeError("Could not provision uv for Python 3.11.")

    run(uv, "venv", "--python", "3.11", "--seed", str(PYTHON_ENV))
    if not TARGET_PYTHON.is_file():
        raise RuntimeError(f"Python 3.11 interpreter is missing: {TARGET_PYTHON}")
    return TARGET_PYTHON


def extract_source_bundle(bundle: Path, destination: Path) -> None:
    """Reject absolute paths, traversal and links in the exact-source archive."""
    destination_resolved = destination.resolve()
    with tarfile.open(bundle, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            if member.islnk() or member.issym() or not (member.isfile() or member.isdir()):
                raise RuntimeError(f"Unsupported source-archive entry: {member.name!r}")
            target = (destination / member.name).resolve()
            if target != destination_resolved and destination_resolved not in target.parents:
                raise RuntimeError(f"Unsafe source-archive path: {member.name!r}")
        archive.extractall(destination, members=members)


def main() -> None:
    if not BUNDLE_SOURCE.is_file():
        raise RuntimeError("Exact-source confirmatory project bundle is missing.")
    if not SOURCE_COMMIT_FILE.is_file():
        raise RuntimeError("Exact source commit file is missing.")

    source_commit = SOURCE_COMMIT_FILE.read_text(encoding="utf-8").strip()
    if len(source_commit) != 40 or any(c not in "0123456789abcdef" for c in source_commit.lower()):
        raise RuntimeError("Source commit must be a full 40-character Git SHA.")

    # Move inputs away from Kaggle's export directory before extracting or
    # installing packages, so they cannot inflate the downloaded artifact.
    if RUNTIME_ROOT.exists():
        shutil.rmtree(RUNTIME_ROOT)
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BUNDLE_SOURCE, BUNDLE)
    source_bundle_sha256 = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
    BUNDLE_SOURCE.unlink()
    SOURCE_COMMIT_FILE.unlink()

    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    WORKDIR.mkdir(parents=True, exist_ok=True)
    extract_source_bundle(BUNDLE, WORKDIR)
    BUNDLE.unlink()

    benchmark = WORKDIR / "data" / "benchmark"
    benchmark.mkdir(parents=True, exist_ok=True)
    (benchmark / "kaggle_source_commit.txt").write_text(
        source_commit + "\n", encoding="utf-8"
    )

    python = ensure_python311()
    py_version = output(
        str(python),
        "-c",
        "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
    )
    if py_version != "3.11":
        raise RuntimeError(f"Confirmatory run requires Python 3.11, got {py_version}")

    run(str(python), "-m", "pip", "install", "--upgrade", "pip", cwd=WORKDIR)
    run(
        str(python),
        "-m",
        "pip",
        "install",
        "-r",
        "requirements-pilot.txt",
        cwd=WORKDIR,
    )
    run(str(python), "-m", "pip", "check", cwd=WORKDIR)

    env = dict(os.environ)
    env["PYTHONPATH"] = str(WORKDIR)

    run(
        str(python),
        "scripts/capture_environment.py",
        "--output",
        "data/benchmark/environment.json",
        cwd=WORKDIR,
        env=env,
    )
    env_path = benchmark / "environment.json"
    environment = json.loads(env_path.read_text(encoding="utf-8"))
    environment["source_commit"] = source_commit
    environment["source_commit_verified_from_bundle"] = True
    environment["source_bundle_sha256"] = source_bundle_sha256
    environment["runtime_root"] = str(RUNTIME_ROOT)
    environment_path = benchmark / "environment.json"
    environment_path.write_text(
        json.dumps(environment, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # All fail-closed checks must complete before the first confirmatory call.
    run(
        str(python),
        "scripts/pilot_preflight.py",
        "--require-cuda",
        cwd=WORKDIR,
        env=env,
    )
    run(str(python), "scripts/model_load_preflight.py", cwd=WORKDIR, env=env)
    run(
        str(python),
        "scripts/audit_confirmatory_integrity.py",
        cwd=WORKDIR,
        env=env,
    )
    run(str(python), "scripts/run_confirmatory.py", cwd=WORKDIR, env=env)

    manifest = json.loads(
        (benchmark / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    run(
        str(python),
        "scripts/finalize_confirmatory.py",
        "--runs-dir",
        "data/benchmark/runs",
        "--case-ids",
        *manifest["case_ids"],
        cwd=WORKDIR,
        env=env,
    )

    # Validate checksums before staging anything in Kaggle's exported directory.
    run(
        str(python),
        "scripts/validate_confirmatory_artifact_manifest.py",
        "--artifact-root",
        "data/benchmark",
        "--manifest",
        "data/benchmark/artifact_manifest.json",
        cwd=WORKDIR,
        env=env,
    )

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for item in benchmark.iterdir():
        destination = OUTPUT_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)

    required = (
        "environment.json",
        "confirmatory_evaluation.json",
        "case_level_analysis.json",
        "primary_analysis.json",
        "confirmatory_qa_report.json",
        "confirmatory_records.jsonl",
        "artifact_manifest.json",
        "benchmark_manifest.json",
    )
    missing = [str(OUTPUT_DIR / name) for name in required if not (OUTPUT_DIR / name).is_file()]
    if missing:
        raise RuntimeError(
            "Confirmatory run finalized but required artifacts are missing: "
            + ", ".join(missing)
        )

    print(f"Confirmatory experiment completed for source commit {source_commit}.", flush=True)
    print(f"Only final research artifacts are staged at {OUTPUT_DIR}.", flush=True)


if __name__ == "__main__":
    main()
