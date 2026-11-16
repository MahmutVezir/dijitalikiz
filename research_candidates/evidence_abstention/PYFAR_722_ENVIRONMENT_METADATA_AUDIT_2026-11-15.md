# pyfar #722 — exact-row environment metadata extraction audit

**Date:** 15 November 2026  
**Status:** `PASS_METADATA_EXTRACTION / ENVIRONMENT_NOT_FROZEN / NO_UPSTREAM_EXECUTION`

## 1. Exact source and extraction

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet: `data/train-00000-of-00001.parquet`
- Expected/observed size: `226272977` bytes
- Expected/observed SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Expected/observed rows: `6272`
- Reader: `pyarrow==19.0.1`
- Exact row locator: `instance_id=pyfar__pyfar-722`
- Extracted repository/base: `pyfar/pyfar` / `648dda4c60c5a6f74acf335f7808c590c9d23929`

The dedicated GitHub Actions run [43751492697](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43751492697) succeeded end-to-end: pinned reader install, extraction utility tests, exact dataset download and SHA/byte validation, unique row extraction, and artifact upload.

## 2. Preserved output

The exact extracted record is committed alongside this audit as `PYFAR_722_ENVIRONMENT_METADATA_2026-11-15.json`.

- GitHub Actions artifact ID: `14175749025`
- Artifact name: `pyfar-722-environment-metadata-43751492697-1`
- ZIP bytes: `1147`
- ZIP SHA-256: `9e4c3a8e706a6b8f76dbae80916bb82ccc835cccd51d6dc2b8ea39d795e5a047`
- Extracted JSON bytes: `2470`
- Extracted JSON SHA-256: `6811f95d3b473b6d90e1ca7551d1e71614ebdaf2ea41456eec0e94b609567072`
- Canonical selected-metadata SHA-256 (as reported by extractor): `734cb8eb136585afb129ad0bb614c9cd5c9ae224978b46a59a1bd76e7db697e8`

The extracted row reports:
- image: `prime/primeintellect/pyfar-pyfar:722-648dda4`;
- base image: `python_base_310`;
- system install: `apt-get update` followed by installation of `libsndfile1`;
- Python install: `pip install -q -e ".[tests]"`;
- target command: `pytest --no-header -rA --tb=line --color=no -p no:cacheprovider -W ignore::DeprecationWarning tests/test_dsp_normalize.py`.

## 3. Static packaging review — unresolved install ambiguity

The exact upstream base commit's packaging files were inspected without checking out, installing, building, or testing the upstream project:

- `setup.py` at base commit `648dda4c60c5a6f74acf335f7808c590c9d23929` defines ordinary `install_requires` and a legacy `tests_require` list. It does not declare `extras_require={"tests": ...}`.
- `setup.cfg` has no `[options.extras_require]` section.
- `pyproject.toml` has no `[project.optional-dependencies]` section.
- `requirements_dev.txt` contains development/test tools, including pytest, but the dataset's recorded install command does not install that file.
- The `docker_specs.python_version` field is null; `python_base_310` indicates a Python 3.10 base image family but not a fully specified micro-version.
- The recorded image is a tag, not a container digest in the dataset row.

Setuptools documents `extras_require` (or `project.optional-dependencies`) as the mechanism that declares installable extras. It documents `tests_require` as a deprecated legacy mechanism associated with the old setuptools test command, not a replacement for an installable extra. References: [setuptools keywords](https://setuptools.pypa.io/en/latest/references/keywords.html) and [dependency management](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html).

**Interpretation:** the dataset's `pip install -e ".[tests]"` instruction must not be assumed to install the test dependency set. The image may already contain required test tools, but this was not checked or inferred. The exact image digest, Python micro-version, OS package versions, installed distribution snapshot, and package resolver outcomes still need to be captured in the intended environment before a controlled base/fix reproduction can be authorized.

## 4. Execution boundary and next gate

This workflow did not:
- clone or checkout the upstream pyfar repository;
- install pyfar or any dependency from its install configuration;
- execute a test, build, or reproduction;
- load a model, run inference, or fine-tune.

The record is metadata provenance only. It does not prove a base-fail/fix-pass result, accept the case, establish the environment lock, or authorize any upstream execution. Keep pyfar row 90 in `STRONG_STATIC_DEFECT_CANDIDATE` status until the runtime ambiguity and human role/approval gates are resolved.

