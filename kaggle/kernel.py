from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
SOURCE_COMMIT = "SOURCE_COMMIT_PLACEHOLDER"
EMBEDDED_PROJECT_B64 = "PROJECT_B64_PLACEHOLDER"
BUNDLE = KERNEL_ROOT / "project.tar.gz"
WORKDIR = KERNEL_ROOT / "dijitalikiz"
PYTHON_ENV = KERNEL_ROOT / "dijitalikiz-py311"
TARGET_PYTHON = PYTHON_ENV / "bin" / "python"


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, env=env, check=True)


def output(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def ensure_python311() -> Path:
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    if current == "3.11":
        print(f"Using Kaggle launcher Python {sys.executable}", flush=True)
        return Path(sys.executable)

    if TARGET_PYTHON.is_file():
        detected = output(
            str(TARGET_PYTHON),
            "-c",
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
        )
        if detected == "3.11":
            print(f"Using existing Python 3.11 environment: {TARGET_PYTHON}", flush=True)
            return TARGET_PYTHON
        shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    # Prefer an already-installed 3.11 interpreter when Kaggle exposes one.
    candidates = [
        "python3.11",
        "/usr/bin/python3.11",
        "/opt/conda/bin/python3.11",
        "/opt/conda/envs/py311/bin/python",
    ]
    for candidate in candidates:
        executable = shutil.which(candidate) if not Path(candidate).is_absolute() else candidate
        if executable and Path(executable).is_file():
            try:
                if output(
                    executable,
                    "-c",
                    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
                ) == "3.11":
                    print(f"Creating isolated Python 3.11 venv from {executable}", flush=True)
                    run(executable, "-m", "venv", str(PYTHON_ENV))
                    return TARGET_PYTHON
            except (OSError, subprocess.CalledProcessError):
                shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    # Kaggle images historically include conda/mamba; use it when available.
    for manager in (
        "/opt/conda/bin/mamba",
        "/opt/conda/bin/conda",
        "mamba",
        "conda",
    ):
        executable = shutil.which(manager) if not Path(manager).is_absolute() else manager
        if executable and Path(executable).is_file():
            try:
                print(f"Creating isolated Python 3.11 conda environment with {executable}", flush=True)
                run(executable, "create", "-y", "--prefix", str(PYTHON_ENV), "python=3.11", "pip")
                return TARGET_PYTHON
            except (OSError, subprocess.CalledProcessError):
                shutil.rmtree(PYTHON_ENV, ignore_errors=True)

    # Final portable fallback: install uv in the bootstrap interpreter and let
    # uv provision CPython 3.11 without changing the Kaggle base environment.
    print("Provisioning Python 3.11 with uv", flush=True)
    run(sys.executable, "-m", "pip", "install", "--quiet", "uv")
    uv = shutil.which("uv")
    if not uv:
        candidate = Path(sys.executable).resolve().parent / "uv"
        uv = str(candidate) if candidate.is_file() else None
    if not uv:
        user_bin = Path.home() / ".local" / "bin" / "uv"
        uv = str(user_bin) if user_bin.is_file() else None
    if not uv:
        raise RuntimeError("Could not provision Python 3.11: neither conda/mamba nor uv is available.")
    run(uv, "venv", "--python", "3.11", "--seed", str(PYTHON_ENV))
    if not TARGET_PYTHON.is_file():
        raise RuntimeError(f"Python 3.11 venv was created but interpreter is missing: {TARGET_PYTHON}")
    return TARGET_PYTHON


# Kaggle's kernel package does not reliably expose arbitrary sidecar files.
# The GitHub Action therefore embeds the exact source archive into this
# launcher. Kaggle never needs credentials for the private GitHub repository.
if SOURCE_COMMIT == "SOURCE_COMMIT_PLACEHOLDER":
    raise RuntimeError("Frozen source commit was not embedded into the Kaggle launcher.")
if EMBEDDED_PROJECT_B64 == "PROJECT_B64_PLACEHOLDER":
    raise RuntimeError("Exact project source was not embedded into the Kaggle launcher.")

try:
    BUNDLE.write_bytes(
        base64.b64decode(EMBEDDED_PROJECT_B64.encode("ascii"), validate=True)
    )
except Exception as exc:
    raise RuntimeError("Embedded exact-source project archive is invalid.") from exc

print(f"Using embedded exact project source: {SOURCE_COMMIT}", flush=True)

target_python = ensure_python311()
target_version = output(
    str(target_python),
    "-c",
    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
)
if target_version != "3.11":
    raise RuntimeError(f"Frozen pilot requires Python 3.11, got {target_version}")

if WORKDIR.exists():
    shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True, exist_ok=True)

with tarfile.open(BUNDLE, "r:gz") as archive:
    archive.extractall(WORKDIR)

source_commit = SOURCE_COMMIT
pilot_dir = WORKDIR / "data" / "pilot"
pilot_dir.mkdir(parents=True, exist_ok=True)
(pilot_dir / "kaggle_source_commit.txt").write_text(
    source_commit + "\n", encoding="utf-8"
)

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
environment["source_commit_verified_from_embedded_bundle"] = True
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
