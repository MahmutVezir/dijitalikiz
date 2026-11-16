# dependency-groups 1.3.0 — manual license metadata resolution

**Purpose:** resolve the missing wheel METADATA license field encountered by the Nox #919 dependency-license gate.

- Installed distribution: dependency-groups==1.3.0
- PyPI release page: https://pypi.org/project/dependency-groups/1.3.0/
- PyPI source-distribution SHA-256: 5b9751d5d98fbd6dfd038a560a69c8382e41afcbf7ffdbcc28a2a3f85498830f
- PyPI wheel SHA-256: 1abf34d712deda5581e80d507512664d52b35d1c2d7caf16c85e58ca508547e0
- PyPI attested source repository: sirosen/dependency-groups
- Exact source commit for 1.3.0: 1c99d4a6e50504354ef501e5f8543a22830c788d
- Exact source tag: refs/tags/1.3.0
- Exact source pyproject.toml declares license = { text = "MIT" }.
- Exact source LICENSE.txt blob SHA (Git blob identity): b9723b85ed7adb32f8c2b4ee880c06ec3061da50
- LICENSE.txt contents identify the MIT License and copyright Stephen Rosen (2024-present).

## Decision

The distribution metadata gate must not silently infer a license from the package name. For this exact version only, the workflow may record MIT when all of the following pass:

1. Installed version is exactly 1.3.0.
2. The upstream source repository is checked out at commit 1c99d4a6e50504354ef501e5f8543a22830c788d.
3. git rev-parse HEAD:LICENSE.txt equals b9723b85ed7adb32f8c2b4ee880c06ec3061da50.
4. The exact pyproject.toml contains license = { text = "MIT" }.

Any version or source-identity mismatch remains a hard stop. This manual resolution is limited to the Nox reproduction environment and does not imply that all package metadata gaps may be waived.

## Scope limitation

This is a documentary source-license screen for a test dependency. It is not legal advice and is not a blanket clearance for redistribution or optional extras.
