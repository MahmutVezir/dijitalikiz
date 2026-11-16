# attrs 24.3.0 — missing wheel license metadata resolution for Nox #919

**Distribution:** `attrs==24.3.0`  
**PyPI release page:** https://pypi.org/project/attrs/24.3.0/  
**Exact upstream source:** https://github.com/python-attrs/attrs/tree/24.3.0  
**Source commit:** `598494a618410490cfbe0c896b7a544f6d23e0d9`  
**Source LICENSE blob:** `2bd6453d255e19b973f19b128596a8b6dd65b2c3`  
**Source pyproject.toml blob:** `0b598099fdd945dcb75f3145909a9b4a85a93972`

## Finding

The pinned attrs 24.3.0 PyPI release page shows no license value and no license classifier in the release metadata displayed for this version. The source tag is independently pinned. Its `pyproject.toml` declares `license = "MIT"` and `license-files = ["LICENSE"]`; the exact-tag `LICENSE` file contains the MIT License and is identified by the Git blob above.

This resolves the ambiguity for this exact distribution version by checking its upstream source tag, rather than inferring a license from the package name. The decision is restricted to attrs 24.3.0; a different version must pass its own source-identity and license check.

## Workflow condition

When installed metadata for `attrs` has neither `License`, `License-Expression`, nor license classifier, the Nox #919 pre-execution inventory may record `MIT` only when:
1. installed distribution version equals `24.3.0`;
2. source repository is checked out at `598494a618410490cfbe0c896b7a544f6d23e0d9`;
3. `git rev-parse HEAD:LICENSE` equals `2bd6453d255e19b973f19b128596a8b6dd65b2c3`;
4. `git rev-parse HEAD:pyproject.toml` equals `0b598099fdd945dcb75f3145909a9b4a85a93972`;
5. the project metadata at that commit declares the MIT license and includes the LICENSE file.

Any mismatch remains a hard stop before Nox source import or tests.

## Scope

This is a documentary package-license resolution to unblock the exact pinned test environment. It is not legal advice, does not clear other attrs versions, optional packages, or redistribution of the package, and does not establish the license status of the entire Nox ecosystem.
