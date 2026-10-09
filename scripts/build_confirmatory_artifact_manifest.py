from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_FINAL_FILES = (
    Path("environment.json"),
    Path("confirmatory_evaluation.json"),
    Path("case_level_analysis.json"),
    Path("primary_analysis.json"),
    Path("confirmatory_qa_report.json"),
    Path("confirmatory_records.jsonl"),
    Path("benchmark_manifest.json"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_payload(
    root: Path,
    runs: Path,
    output: Path,
    case_ids: list[str],
    conditions: list[str],
    seeds: list[int],
) -> dict:
    root = root.resolve()
    runs = runs.resolve()
    output = output.resolve()

    if not runs.is_relative_to(root):
        raise RuntimeError("Confirmatory run records must live inside the artifact root.")
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise RuntimeError("Confirmatory case IDs must be non-empty and unique.")
    if not conditions or len(conditions) != len(set(conditions)):
        raise RuntimeError("Confirmatory conditions must be non-empty and unique.")
    if not seeds or len(seeds) != len(set(seeds)):
        raise RuntimeError("Confirmatory seeds must be non-empty and unique.")

    expected_names = {
        f"{case_id}__{condition}__seed{seed}.json"
        for case_id in case_ids
        for condition in conditions
        for seed in seeds
    }
    records = sorted(path for path in runs.glob("*.json") if path.is_file())
    actual_names = {path.name for path in records}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise RuntimeError(
            "Confirmatory run set differs from the frozen design; "
            f"missing={missing}, unexpected={unexpected}"
        )

    missing_required = [
        str(root / relative)
        for relative in REQUIRED_FINAL_FILES
        if not (root / relative).is_file()
    ]
    if missing_required:
        raise RuntimeError(f"Missing finalized confirmatory artifacts: {missing_required}")

    # Hash every file delivered as evidence, not just the headline reports.
    # The manifest cannot hash itself without becoming recursive.
    files = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and path.resolve() != output
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    if not files:
        raise RuntimeError("Confirmatory artifact root contains no files.")

    relative_paths = [path.relative_to(root).as_posix() for path in files]
    if len(relative_paths) != len(set(relative_paths)):
        raise RuntimeError("Duplicate relative paths found in confirmatory artifact.")

    expected_record_count = len(expected_names)
    payload = {
        "version": "0.2",
        "root": "data/benchmark",
        "finalization_gate": {
            "expected_run_record_count": expected_record_count,
            "required_final_files": [str(path) for path in REQUIRED_FINAL_FILES],
            "status": "complete",
        },
        "files": [
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in files
        ],
        "run_record_count": len(records),
    }
    payload["file_count"] = len(payload["files"])
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build checksums for every delivered confirmatory artifact."
    )
    parser.add_argument("--runs-dir", default="data/benchmark/runs")
    parser.add_argument("--output", default="data/benchmark/artifact_manifest.json")
    args = parser.parse_args()

    root = Path("data/benchmark")
    runs = Path(args.runs_dir)
    manifest = json.loads((root / "benchmark_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "frozen":
        raise RuntimeError("Confirmatory benchmark manifest must be frozen.")
    pilot_manifest = json.loads(
        Path("data/pilot/pilot_manifest.json").read_text(encoding="utf-8")
    )
    conditions = list(pilot_manifest["conditions"])
    seeds = list(pilot_manifest["generation"]["seeds"])

    payload = build_payload(
        root,
        runs,
        Path(args.output),
        list(manifest["case_ids"]),
        conditions,
        seeds,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "run_record_count": payload["run_record_count"],
                "file_count": payload["file_count"],
                "output": str(output_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
