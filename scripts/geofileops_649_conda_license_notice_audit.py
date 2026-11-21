from __future__ import annotations

import bz2
import concurrent.futures
import hashlib
import io
import json
import os
import re
import tarfile
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
ARTIFACT_ID = 14711502949
EXPECTED_ARTIFACT_SHA256 = "b4b408170b3fcae7c305d060f0cc283fcf912e964403a9eb1015b1209e60553f"
OUT = Path(os.environ.get("RUNNER_TEMP", ".")) / "geofileops-649-conda-license-audit"
NOTICES = OUT / "package-notices"
OUT.mkdir(parents=True, exist_ok=True)
NOTICES.mkdir(parents=True, exist_ok=True)

class StripAuthorizationOnExternalRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None:
            target_host = urllib.parse.urlparse(newurl).hostname
            if target_host != "api.github.com":
                redirected.remove_header("Authorization")
                redirected.remove_header("authorization")
        return redirected


def request_bytes(url: str, *, headers: dict[str, str] | None = None, timeout: int = 180) -> bytes:
    request = urllib.request.Request(url, headers=headers or {"User-Agent": "MahmutVezir-research-audit/1.0"})
    opener = urllib.request.build_opener(StripAuthorizationOnExternalRedirect())
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            with opener.open(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt == 4:
                break
            time.sleep(min(2 ** attempt, 16))
    assert last_error is not None
    raise last_error

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def safe_relpath(name: str) -> Path:
    parts = [p for p in PurePosixPath(name).parts if p not in ("", ".", "..", "/")]
    return Path(*parts) if parts else Path("unnamed-license-file")

def is_notice_path(name: str) -> bool:
    normalized = name.replace("\\", "/").lower()
    base = normalized.rsplit("/", 1)[-1]
    if normalized.startswith("info/licenses/"):
        return True
    return bool(re.search(r"(^|/)(license|licence|copying|notice|copyright|patents?)([._-].*)?$", normalized)) or base in {
        "license.txt", "licence.txt", "copying.txt", "notice.txt", "copyright.txt"
    }

def extract_tar_files(tar_bytes: bytes, *, prefix: str, package_key: str, found: dict[str, dict]) -> None:
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
        for member in tf:
            if not member.isfile() or not is_notice_path(member.name):
                continue
            if member.size > 10 * 1024 * 1024:
                found[f"{prefix}:{member.name}"] = {"path": member.name, "status": "skipped_over_10MiB", "size": member.size}
                continue
            extracted = tf.extractfile(member)
            if extracted is None:
                continue
            data = extracted.read()
            rel = safe_relpath(member.name)
            target = NOTICES / package_key / prefix / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            found[f"{prefix}:{member.name}"] = {
                "path": member.name,
                "artifact_path": str(target.relative_to(OUT)),
                "size": len(data),
                "sha256": sha256_bytes(data),
            }

def audit_conda_package(package: dict) -> dict:
    url = package["url"]
    expected_md5 = package["expected_md5"]
    filename = package["filename"]
    package_key = f'{package["name"]}-{package["version"]}-{package["build"]}'
    raw = request_bytes(url)
    actual_md5 = hashlib.md5(raw).hexdigest()
    if actual_md5 != expected_md5:
        raise ValueError(f"{filename}: explicit-lock MD5 mismatch: expected {expected_md5}, got {actual_md5}")
    actual_sha = sha256_bytes(raw)
    notice_files: dict[str, dict] = {}
    about: dict = {}
    index: dict = {}
    info_members: list[str] = []
    payload_members: list[str] = []
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        info_names = [n for n in archive.namelist() if n.startswith("info-") and n.endswith(".tar.zst")]
        pkg_names = [n for n in archive.namelist() if n.startswith("pkg-") and n.endswith(".tar.zst")]
        if len(info_names) != 1 or len(pkg_names) != 1:
            raise ValueError(f"{filename}: expected one info and one pkg zstd tar, found info={info_names}, pkg={pkg_names}")
        import zstandard
        info_tar = zstandard.ZstdDecompressor().decompress(archive.read(info_names[0]))
        with tarfile.open(fileobj=io.BytesIO(info_tar), mode="r:") as tf:
            for member in tf:
                if not member.isfile():
                    continue
                if member.name == "info/about.json":
                    item = tf.extractfile(member)
                    if item:
                        about = json.loads(item.read().decode("utf-8"))
                if member.name == "info/index.json":
                    item = tf.extractfile(member)
                    if item:
                        index = json.loads(item.read().decode("utf-8"))
                if member.name.startswith("info/licenses/") or is_notice_path(member.name):
                    if member.size > 10 * 1024 * 1024:
                        notice_files[f"info:{member.name}"] = {"path": member.name, "status": "skipped_over_10MiB", "size": member.size}
                        continue
                    item = tf.extractfile(member)
                    if item is None:
                        continue
                    data = item.read()
                    rel = safe_relpath(member.name.removeprefix("info/"))
                    target = NOTICES / package_key / "info" / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    notice_files[f"info:{member.name}"] = {
                        "path": member.name,
                        "artifact_path": str(target.relative_to(OUT)),
                        "size": len(data),
                        "sha256": sha256_bytes(data),
                    }
                info_members.append(member.name)
        # Stream the payload tar to inventory license/notice/copyright files without extracting package contents.
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            import zstandard
            payload_stream = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(archive.read(pkg_names[0])))
            try:
                with tarfile.open(fileobj=payload_stream, mode="r|") as tf:
                    for member in tf:
                        if not member.isfile():
                            continue
                        payload_members.append(member.name)
                        if is_notice_path(member.name) and not any(v.get("path") == member.name for v in notice_files.values()):
                            if member.size > 10 * 1024 * 1024:
                                notice_files[f"pkg:{member.name}"] = {"path": member.name, "status": "skipped_over_10MiB", "size": member.size}
                                continue
                            item = tf.extractfile(member)
                            if item is None:
                                continue
                            data = item.read()
                            rel = safe_relpath(member.name)
                            target = NOTICES / package_key / "pkg" / rel
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(data)
                            notice_files[f"pkg:{member.name}"] = {
                                "path": member.name,
                                "artifact_path": str(target.relative_to(OUT)),
                                "size": len(data),
                                "sha256": sha256_bytes(data),
                            }
            finally:
                payload_stream.close()
    index_identity = {
        "name": index.get("name"),
        "version": index.get("version"),
        "build": index.get("build"),
        "build_number": index.get("build_number"),
        "subdir": index.get("subdir"),
    }
    expected_identity = {
        "name": package["name"],
        "version": package["version"],
        "build": package["build"],
    }
    for key, expected in expected_identity.items():
        if index_identity.get(key) != expected:
            raise ValueError(
                f"{filename}: info/index.json {key} mismatch; "
                f"lock={expected!r}, package={index_identity.get(key)!r}"
            )
    return {
        **package,
        "info_index_identity": index_identity,
        "downloaded_bytes": len(raw),
        "archive_md5": actual_md5,
        "archive_sha256": actual_sha,
        "about_json": about,
        "license": about.get("license"),
        "license_family": about.get("license_family"),
        "license_file": about.get("license_file"),
        "notice_file_count": len(notice_files),
        "notice_files": list(notice_files.values()),
        "info_member_count": len(info_members),
        "payload_member_count": len(payload_members),
    }

def main() -> int:
    api_url = f"https://api.github.com/repos/{REPO}/actions/artifacts/{ARTIFACT_ID}/zip"
    artifact_zip = request_bytes(api_url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "MahmutVezir-research-audit/1.0",
    })
    artifact_sha = sha256_bytes(artifact_zip)
    if artifact_sha != EXPECTED_ARTIFACT_SHA256:
        raise SystemExit(f"Source artifact SHA-256 mismatch: {artifact_sha}")
    with zipfile.ZipFile(io.BytesIO(artifact_zip)) as zf:
        lock = zf.read("conda-explicit.txt").decode("utf-8")
        lock_sha = hashlib.sha256(lock.encode("utf-8")).hexdigest()
    packages = []
    for line in lock.splitlines():
        if not line.startswith("https://"):
            continue
        url, sep, expected_md5 = line.partition("#")
        parsed = urllib.parse.urlparse(url)
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 3 or parts[0] != "conda-forge":
            raise ValueError(f"Unexpected channel URL: {url}")
        subdir, filename = parts[-2], parts[-1]
        if subdir not in ("linux-64", "noarch"):
            raise ValueError(f"Unexpected subdir: {subdir}")
        if not sep or not re.fullmatch(r"[0-9a-f]{32}", expected_md5):
            raise ValueError(f"Missing/invalid MD5 lock fragment: {line}")
        stem = filename.removesuffix(".conda").removesuffix(".tar.bz2")
        components = stem.split("-")
        # The package name ld_impl_linux-64 contains a numeric name component;
        # do not mistake that component for the version.
        if components[:2] == ["ld_impl_linux", "64"]:
            version_idx = 2
        else:
            # Package version starts at the first component beginning with a digit.
            version_idx = next((i for i, c in enumerate(components) if c and c[0].isdigit()), None)
        if version_idx is None or version_idx == 0 or version_idx >= len(components) - 1:
            raise ValueError(f"Cannot parse name/version/build from {filename}")
        packages.append({
            "name": "-".join(components[:version_idx]),
            "version": components[version_idx],
            "build": "-".join(components[version_idx + 1:]),
            "subdir": subdir,
            "filename": filename,
            "url": url,
            "expected_md5": expected_md5,
        })
    if len(packages) != 105 or len({p["filename"] for p in packages}) != 105:
        raise SystemExit(f"Expected 105 unique lock packages; got {len(packages)}")

    records: list[dict] = []
    errors: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(audit_conda_package, p): p for p in packages}
        for future in concurrent.futures.as_completed(futures):
            package = futures[future]
            try:
                records.append(future.result())
            except Exception as exc:
                errors.append({"filename": package["filename"], "error": f"{type(exc).__name__}: {exc}"})

    records.sort(key=lambda r: r["filename"])
    summary = {
        "record_type": "geofileops_649_exact_conda_package_license_notice_audit",
        "created_utc": os.environ.get("GITHUB_RUN_STARTED_AT", "not_supplied"),
        "repository": REPO,
        "source_artifact_id": ARTIFACT_ID,
        "source_artifact_sha256_verified": artifact_sha,
        "conda_explicit_sha256": lock_sha,
        "locked_package_count": len(packages),
        "downloaded_and_md5_verified_count": len(records),
        "failed_package_count": len(errors),
        "license_metadata_present_count": sum(bool(r.get("license")) for r in records),
        "license_metadata_missing_count": sum(not bool(r.get("license")) for r in records),
        "license_file_metadata_present_count": sum(bool(r.get("license_file")) for r in records),
        "license_family_metadata_present_count": sum(bool(r.get("license_family")) for r in records),
        "packages_with_notice_files": sum(r["notice_file_count"] > 0 for r in records),
        "notice_files_extracted_count": sum(r["notice_file_count"] for r in records),
        "total_package_bytes_downloaded": sum(r["downloaded_bytes"] for r in records),
        "errors": errors,
        "package_archive_identity_checked_against_info_index": True,
        "all_exact_package_archives_verified_against_frozen_lock_md5": len(records) == len(packages) and not errors,
        "legal_clearance": False,
        "interpretation": "Package-level metadata and notice-file presence inventory only. Not legal advice, not a license compatibility opinion, and not a final acceptance decision.",
    }
    (OUT / "package-license-inventory.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "audit-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "source-conda-explicit.txt").write_text(lock, encoding="utf-8")
    with zipfile.ZipFile(OUT / "package-notices-and-inventory.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(OUT / "package-license-inventory.json", "package-license-inventory.json")
        archive.write(OUT / "audit-summary.json", "audit-summary.json")
        archive.write(OUT / "source-conda-explicit.txt", "source-conda-explicit.txt")
        for file in NOTICES.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(OUT).as_posix())
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if errors or len(records) != 105 else 0

if __name__ == "__main__":
    raise SystemExit(main())
