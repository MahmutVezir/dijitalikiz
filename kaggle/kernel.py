from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
SOURCE_DATASET = "mahmutvezir/dijitalikiz-frozen-source"
BUNDLE = KERNEL_ROOT / "project.tar.gz"
WORKDIR = KERNEL_ROOT / "dijitalikiz"
PYTHON_ENV = KERNEL_ROOT / "dijitalikiz-py311"
TARGET_PYTHON = PYTHON_ENV / "bin" / "python"


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, env=env, check=True)


def output(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def ensure_kagglehub() -> None:
    try:
        import kagglehub  # noqa: F401
        return
    except Exception:
        run(sys.executable, "-m", "pip", "install", "--quiet", "kagglehub")


def ensure_python311() -> Path:
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    if current == "3.11":
        return Path(sys.executable)

    if TARGET_PYTHON.is_file():
        detected = output(
            str(TARGET_PYTHON),
            "-c",
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
        )
        if detected == "3.11":
            return TARGET_PYTHON
        shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    candidates = (
        "python3.11",
        "/usr/bin/python3.11",
        "/opt/conda/bin/python3.11",
        "/opt/conda/envs/py311/bin/python",
    )
    for candidate in candidates:
        executable = shutil.which(candidate) if not Path(candidate).is_absolute() else candidate
        if executable and Path(executable).is_file():
            try:
                version = output(
                    executable,
                    "-c",
                    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
                )
                if version == "3.11":
                    run(executable, "-m", "venv", str(PYTHON_ENV))
                    return TARGET_PYTHON
            except (OSError, subprocess.CalledProcessError):
                shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    for manager in (
        "/opt/conda/bin/mamba",
        "/opt/conda/bin/conda",
        "mamba",
        "conda",
    ):
        executable = shutil.which(manager) if not Path(manager).is_absolute() else manager
        if executable and Path(executable).is_file():
            try:
                run(executable, "create", "-y", "--prefix", str(PYTHON_ENV), "python=3.11", "pip")
                return TARGET_PYTHON
            except (OSError, subprocess.CalledProcessError):
                shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    run(sys.executable, "-m", "pip", "install", "--quiet", "uv")
    uv = shutil.which("uv")
    if not uv:
        candidate = Path(sys.executable).resolve().parent / "uv"
        uv = str(candidate) if candidate.is_file() else None
    if not uv:
        user_bin = Path.home() / ".local" / "bin" / "uv"
        uv = str(user_bin) if user_bin.is_file() else None
    if not uv:
        raise RuntimeError("Could not provision Python 3.11.")
    run(uv, "venv", "--python", "3.11", "--seed", str(PYTHON_ENV))
    if not TARGET_PYTHON.is_file():
        raise RuntimeError(f"Python 3.11 interpreter is missing: {TARGET_PYTHON}")
    return TARGET_PYTHON


ensure_kagglehub()
import kagglehub

dataset_dir = Path(kagglehub.dataset_download(SOURCE_DATASET))
bundle_source = dataset_dir / "project.tar.gz"
commit_source = dataset_dir / "source_commit.txt"

if not bundle_source.is_file():
    raise RuntimeError(f"Frozen source bundle missing from Kaggle Dataset: {bundle_source}")
if not commit_source.is_file():
    raise RuntimeError(f"Frozen source commit marker missing from Kaggle Dataset: {commit_source}")

source_commit = commit_source.read_text(encoding="utf-8").strip()
if len(source_commit) != 40 or any(ch not in "0123456789abcdef" for ch in source_commit.lower()):
    raise RuntimeError(f"Invalid frozen source commit marker: {source_commit!r}")

shutil.copy2(bundle_source, BUNDLE)
print(f"Using versioned Kaggle source bundle for commit {source_commit}", flush=True)

if WORKDIR.exists():
    shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True, exist_ok=True)

with tarfile.open(BUNDLE, "r:gz") as archive:
    archive.extractall(WORKDIR)

pilot_dir = WORKDIR / "data" / "pilot"
pilot_dir.mkdir(parents=True, exist_ok=True)
(pilot_dir / "kaggle_source_commit.txt").write_text(
    source_commit + "\n", encoding="utf-8"
)

target_python = ensure_python311()
target_version = output(
    str(target_python),
    "-c",
    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
)
if target_version != "3.11":
    raise RuntimeError(f"Frozen pilot requires Python 3.11, got {target_version}")

run(
    str(target_python),
    "-m",
    "pip",
    "install",
    "-r",
    "requirements-pilot.txt",
    cwd=WORKDIR,
)

env = dict(os.environ)
env["PYTHONPATH"] = str(WORKDIR)

run(str(target_python), "scripts/capture_environment.py", cwd=WORKDIR, env=env)
environment_path = pilot_dir / "environment.json"
environment = json.loads(environment_path.read_text(encoding="utf-8"))
environment["source_commit"] = source_commit
environment["source_commit_verified_from_kaggle_dataset"] = True
environment_path.write_text(
    json.dumps(environment, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

run(str(target_python), "scripts/pilot_preflight.py", "--require-cuda", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/model_load_preflight.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/audit_pilot_integrity.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/run_pilot.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/finalize_pilot.py", cwd=WORKDIR, env=env)

output_dir = KERNEL_ROOT / "pilot-output"
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

for item in pilot_dir.iterdir():
    destination = output_dir / item.name
    if item.is_dir():
        shutil.copytree(item, destination)
    else:
        shutil.copy2(item, destination)

required = (
    output_dir / "pilot_records.jsonl",
    output_dir / "pilot_evaluation.json",
    output_dir / "case_level_analysis.json",
    output_dir / "pilot_qa_report.json",
    output_dir / "artifact_manifest.json",
)
missing = [str(path) for path in required if not path.is_file()]
if missing:
    raise RuntimeError(
        "Pilot finalized but required artifacts are missing: " + ", ".join(missing)
    )

print(f"Kaggle pilot completed for source commit {source_commit}.", flush=True)
print(f"Pilot artifacts staged at {output_dir}.", flush=True)
