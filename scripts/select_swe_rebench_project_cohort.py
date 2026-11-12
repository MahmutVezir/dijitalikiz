#!/usr/bin/env python3
"""Build a deterministic project-stratified metadata-only review cohort."""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

INPUT_SHA256 = "805559607aa5711a2d527e2429733d85e267f592e95609a27e54872bc0f91e14"
EXPECTED_INPUT_ROWS = 347
DATASET_ID = "PrimeIntellect/SWE-rebench-V2-Filtered-Verified"
DATASET_FILE_REVISION = "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
DATASET_FILE_SHA256 = "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
SEED = "tubitak-2204a-evidence-abstention-cohort-v1-2026-11-12"
TARGET_PROJECTS = 96
ALLOWED_LICENSES = frozenset({"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "MIT-0"})
EXPOSED_REPOSITORIES = frozenset({
    "keras-team/keras",
    "pandas-dev/pandas",
    "scrapy/scrapy",
    "tornadoweb/tornado",
})
REQUIRED_COLUMNS = {
    "instance_id", "repo", "base_commit", "created_at_utc", "language",
    "license", "fail_to_pass_count", "screen_status",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
OUTPUT_COLUMNS = [
    "selection_role", "license_stratum", "stratum_project_quota", "project_rank",
    "case_rank_within_project", "instance_id", "repo", "base_commit",
    "created_at_utc", "language", "license", "fail_to_pass_count", "screen_status",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rank_hash(*parts: str, seed: str = SEED) -> str:
    payload = "\0".join((seed, *parts)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_candidate_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Input CSV missing columns: {sorted(missing)}")
        return list(reader)


def hamilton_quotas(project_counts: dict[str, int], target: int) -> dict[str, int]:
    total = sum(project_counts.values())
    if target <= 0 or target > total:
        raise ValueError(f"Target {target} must be in [1, {total}]")
    base = {lic: target * n // total for lic, n in project_counts.items()}
    remaining = target - sum(base.values())
    order = sorted(
        project_counts,
        key=lambda lic: (-(target * project_counts[lic] % total), lic),
    )
    for lic in order[:remaining]:
        base[lic] += 1
    if sum(base.values()) != target:
        raise AssertionError("Hamilton allocation did not sum to target")
    return dict(sorted(base.items()))


def _normalize_and_filter(rows: list[dict[str, str]], seed: str):
    ids = [str(row.get("instance_id", "")).strip() for row in rows]
    if any(not x for x in ids):
        raise ValueError("Input contains an empty instance_id")
    duplicates = [k for k, n in Counter(ids).items() if n > 1]
    if duplicates:
        raise ValueError(f"Duplicate instance_id values in input: {duplicates[:10]}")

    excluded = Counter()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for raw in rows:
        row = {k: str(v or "").strip() for k, v in raw.items()}
        repo = row["repo"]
        license_name = row["license"]
        if row["screen_status"] != "metadata_candidate_unreviewed":
            excluded["not_metadata_candidate"] += 1
            continue
        if row["language"].casefold() != "python":
            excluded["not_python"] += 1
            continue
        if license_name not in ALLOWED_LICENSES:
            excluded["license_not_in_pre_screen_allowlist"] += 1
            continue
        if repo in EXPOSED_REPOSITORIES:
            excluded["previously_exposed_repository"] += 1
            continue
        if not repo or "/" not in repo:
            excluded["invalid_repository_identifier"] += 1
            continue
        if not SHA_RE.fullmatch(row["base_commit"]):
            excluded["invalid_base_commit"] += 1
            continue
        if not row["created_at_utc"].endswith("Z"):
            excluded["invalid_created_at"] += 1
            continue
        try:
            dt = datetime.fromisoformat(row["created_at_utc"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Invalid created_at_utc for {row['instance_id']}") from exc
        cutoff = datetime(2024, 9, 20, tzinfo=timezone.utc)
        if dt.tzinfo is None or dt.astimezone(timezone.utc) < cutoff:
            excluded["date_before_cutoff_or_naive"] += 1
            continue
        try:
            n_fail = int(row["fail_to_pass_count"])
        except ValueError:
            n_fail = 0
        if n_fail <= 0:
            excluded["empty_fail_to_pass"] += 1
            continue
        grouped[repo].append(row)

    for repo, project_rows in grouped.items():
        licenses = {r["license"] for r in project_rows}
        if len(licenses) != 1:
            raise ValueError(f"Repository has mixed license metadata: {repo}: {sorted(licenses)}")
        project_rows.sort(key=lambda r: rank_hash("CASE", repo, r["instance_id"], seed=seed))
    return grouped, excluded


def build_cohort(rows: list[dict[str, str]], target: int = TARGET_PROJECTS, seed: str = SEED):
    grouped, excluded = _normalize_and_filter(rows, seed)
    if not grouped:
        raise ValueError("No eligible repositories after metadata filters")
    project_by_license: dict[str, list[str]] = defaultdict(list)
    for repo, candidates in grouped.items():
        project_by_license[candidates[0]["license"]].append(repo)
    project_counts = {lic: len(repos) for lic, repos in project_by_license.items()}
    quotas = hamilton_quotas(project_counts, target)

    selected_repos = set()
    project_rank_by_repo = {}
    for lic, repos in project_by_license.items():
        ordered = sorted(repos, key=lambda repo: rank_hash("PROJECT", lic, repo, seed=seed))
        for rank, repo in enumerate(ordered, start=1):
            project_rank_by_repo[repo] = rank
        selected_repos.update(ordered[:quotas[lic]])

    primary, project_reserves, within_project_alternates = [], [], []
    for lic in sorted(project_by_license):
        ordered = sorted(
            project_by_license[lic],
            key=lambda repo: rank_hash("PROJECT", lic, repo, seed=seed),
        )
        for repo in ordered:
            candidates = grouped[repo]
            role = "primary" if repo in selected_repos else "project_reserve"
            representative = candidates[0].copy()
            representative.update({
                "selection_role": role,
                "license_stratum": lic,
                "stratum_project_quota": quotas[lic],
                "project_rank": project_rank_by_repo[repo],
                "case_rank_within_project": 1,
            })
            if role == "primary":
                primary.append(representative)
            else:
                project_reserves.append(representative)
            for case_rank, row in enumerate(candidates[1:], start=2):
                alt = row.copy()
                alt.update({
                    "selection_role": "within_project_alternate",
                    "license_stratum": lic,
                    "stratum_project_quota": quotas[lic],
                    "project_rank": project_rank_by_repo[repo],
                    "case_rank_within_project": case_rank,
                })
                within_project_alternates.append(alt)

    sort_key = lambda r: (r["license_stratum"], int(r["project_rank"]), r["repo"], r["instance_id"])
    primary.sort(key=sort_key)
    project_reserves.sort(key=sort_key)
    within_project_alternates.sort(key=sort_key)

    if len(primary) != target or len({r["repo"] for r in primary}) != target:
        raise AssertionError("Primary cohort is not exactly one case per target project")
    if set(r["repo"] for r in primary) & set(r["repo"] for r in project_reserves):
        raise AssertionError("Primary and project reserve repositories overlap")

    summary = {
        "record_type": "deterministic_metadata_only_project_cohort",
        "dataset_id": DATASET_ID,
        "dataset_file_revision": DATASET_FILE_REVISION,
        "dataset_file_sha256": DATASET_FILE_SHA256,
        "metadata_candidate_input_sha256": INPUT_SHA256,
        "selection_seed": seed,
        "selection_algorithm": "SHA-256 rank by license stratum and repository; one candidate instance per repository; Hamilton proportional allocation over project counts.",
        "target_primary_projects": target,
        "eligible_metadata_candidates_after_rechecks": sum(len(v) for v in grouped.values()),
        "eligible_distinct_projects": len(grouped),
        "allowlisted_licenses": sorted(ALLOWED_LICENSES),
        "previously_exposed_repositories_excluded": sorted(EXPOSED_REPOSITORIES),
        "project_counts_by_license": dict(sorted(project_counts.items())),
        "primary_quota_by_license": quotas,
        "primary_cases": len(primary),
        "primary_distinct_projects": len({r["repo"] for r in primary}),
        "project_reserve_cases": len(project_reserves),
        "project_reserve_distinct_projects": len({r["repo"] for r in project_reserves}),
        "within_project_alternate_cases": len(within_project_alternates),
        "within_project_alternate_projects": len({r["repo"] for r in within_project_alternates}),
        "excluded_metadata_rows_by_reason": dict(sorted(excluded.items())),
        "accepted_confirmatory_cases": 0,
        "upstream_tests_executed": False,
        "human_adjudication_completed": False,
        "model_loaded": False,
        "model_inference_performed": False,
        "fine_tuning_performed": False,
        "status": "CANDIDATE_COHORT_ONLY_NOT_ACCEPTED_CASES",
    }
    return primary, project_reserves, within_project_alternates, summary


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run(input_path: Path, output_dir: Path, target: int = TARGET_PROJECTS,
        seed: str = SEED, verify_input: bool = True):
    digest = sha256_file(input_path)
    if verify_input and digest != INPUT_SHA256:
        raise ValueError(f"Candidate CSV SHA-256 mismatch: expected {INPUT_SHA256}, got {digest}")
    rows = read_candidate_csv(input_path)
    if verify_input and len(rows) != EXPECTED_INPUT_ROWS:
        raise ValueError(f"Candidate CSV row count mismatch: expected {EXPECTED_INPUT_ROWS}, got {len(rows)}")
    primary, reserves, alternates, summary = build_cohort(rows, target, seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "primary": output_dir / "SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv",
        "project_reserves": output_dir / "SWE_REBENCH_V2_PROJECT_RESERVES_2026-11-12.csv",
        "within_project_alternates": output_dir / "SWE_REBENCH_V2_WITHIN_PROJECT_ALTERNATES_2026-11-12.csv",
    }
    write_csv(files["primary"], primary)
    write_csv(files["project_reserves"], reserves)
    write_csv(files["within_project_alternates"], alternates)
    summary["candidate_csv_observed_sha256"] = digest
    summary["files"] = {
        name: {"path": path.name, "sha256": sha256_file(path), "bytes": path.stat().st_size}
        for name, path in files.items()
    }
    summary_path = output_dir / "SWE_REBENCH_V2_COHORT_96_MANIFEST_2026-11-12.json"
    summary["manifest_excludes_solution_bearing_content"] = True
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary["manifest_sha256"] = sha256_file(summary_path)
    return summary, summary_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target", type=int, default=TARGET_PROJECTS)
    parser.add_argument("--seed", default=SEED)
    parser.add_argument("--allow-unpinned-fixture", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        summary, manifest_path = run(
            args.input, args.output_dir, args.target, args.seed,
            verify_input=not args.allow_unpinned_fixture,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"manifest_path={manifest_path}")
        return 0
    except (OSError, ValueError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
