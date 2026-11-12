# Historical CCDG confirmatory archive

This directory is reserved for the historical 9 October 2026 CCDG confirmatory archive.

## Expected file

`confirmatory_artifact_2026-10-09.zip`

- Expected size: **292,742 bytes**
- Expected SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`
- Original Actions run: `37976682761`
- Original Actions artifact ID: `11640450681`

The original GitHub Actions artifact is no longer available through the Actions API. Five identical copies were recovered from the user's ChatGPT Library on 12 November 2026. Their ZIP CRC, 212 manifest-file hashes and sizes, and 160 unique run records were independently rechecked.

The verification report is in `confirmatory_archive_verification_2026-10-09.json`.

## Repository upload is still pending

The recovered ZIP is not yet committed to this repository. Do not treat the Actions history or this JSON report as a substitute for the archive bytes.

After uploading the ZIP to this directory, verify it:

```bash
sha256sum data/historical/confirmatory_artifact_2026-10-09.zip
python -m zipfile -t data/historical/confirmatory_artifact_2026-10-09.zip
```

The hash must exactly match the value above. Then rerun the historical archive integrity workflow.

## Scope separation

This is a legacy **CCDG** experiment archive (16 cases, 160 model runs: 80 Standard and 80 CCDG). It is retained for historical reproducibility only. It is **not** the evidence-abstention dataset and must not be used as confirmatory training or evaluation data for the new abstention research.

The Qwen2.5-3B-Instruct weights were used under the Qwen Research License. The archived run was non-commercial research; any redistribution of model materials or derivatives must comply with the governing license and attribution terms.
