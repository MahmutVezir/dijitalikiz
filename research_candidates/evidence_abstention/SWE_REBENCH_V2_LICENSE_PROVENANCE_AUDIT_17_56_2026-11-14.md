# SWE-rebench V2 — Cohort rows 17–56 exact-base license and file-provenance audit

**Audit date:** 14 November 2026  
**Scope:** Primary cohort rows 17–56 (40 upstream PRs)  
**Status:** Exact-base repository license and diff-path review completed. This is not legal advice, a complete per-file rights clearance, an experimental case acceptance, or authorization to run model inference.

## 1. Frozen source and method

Primary dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`  
Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`  
Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`  
Frozen 96-row cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`  
CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`  
Manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`  
Cohort ZIP SHA-256: `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`  
ZIP CRC check: passed.

For each of rows 17–56, the audit:
1. Read the row's immutable `base_commit` and upstream PR number from the frozen cohort.
2. Retrieved the upstream PR metadata and compared `PR.base.sha` with the frozen `base_commit`.
3. Retrieved the Git tree at that exact base commit, recording the root license path and Git blob object ID.
4. Searched the exact-base tree for license, copying, notice, copyright, and third-party paths.
5. Enumerated all PR changed paths (all pages) and scanned patch additions for copyright/SPDX/license/third-party attributions.
6. Read the two root NOTICE files and selected nested license texts where the tree showed independent content licensing.

**Hash terminology:** Values in the license table are Git blob SHA-1 object IDs, not SHA-256 file digests. The cohort CSV, manifest, Parquet and ZIP digests above are SHA-256.

## 2. Cohort result

- PR base SHA matched the frozen cohort for **40/40** rows.
- Exact-base root `LICENSE` file or license symlink found for **40/40** rows.
- Root NOTICE present for **2/40**: Napalm (row 19) and Modin (row 22).
- PRs were checked across **151 changed-file paths**. No PR changed a root or nested path named `LICENSE`, `NOTICE`, `COPYING`, or `third_party`.
- Root-license distribution agrees with the cohort's declared license strata: **12 Apache-2.0**, **2 BSD-2-Clause**, **24 BSD-3-Clause**, **2 MIT**.
- **One material file-level provenance hold:** Napalm PR #2152 adds a Cisco NX-OS `show_version.txt` test fixture containing Cisco copyright and GPL/LGPL component notices. The repository's Apache-2.0 root license does not, by itself, establish the fixture's redistribution provenance.
- Several repositories contain nested third-party, dataset, documentation, icon, or generated-asset licenses. These are documented below. The corresponding PR changed paths did not directly overlap those nested license paths, but this does not prove all source-file provenance is cleared.

## 3. Exact-base root license manifest

The base SHA column below was verified against the upstream PR's `base.sha` at the time of this audit. Repository aliases were resolved to their current canonical names without changing the frozen commit.

| Row | Current repository / PR | Frozen base SHA (also PR base SHA) | Exact-base root license path — Git blob SHA-1 | License identified |
|---:|---|---|---|---|
| 17 | `skypilot-org/skypilot` [#5985](https://github.com/skypilot-org/skypilot/pull/5985) | `60a6c930feeb8c48511f74c25bc2d7e12b290dd6` | `LICENSE` — `aad27dddb0055248d9ceb93ac287898fc1d25b29` | Apache-2.0 |
| 18 | `SQLMesh/sqlmesh` [#3654](https://github.com/SQLMesh/sqlmesh/pull/3654) | `ab6bc178cf4317388e560730ae27004af07645de` | `LICENSE` — `eabfad022ad332261ed5df4b0d17b8410af5897e` | Apache-2.0 |
| 19 | `napalm-automation/napalm` [#2152](https://github.com/napalm-automation/napalm/pull/2152) | `d0d2a3e70d21d0556de71ab0462bd71a1450f820` | `LICENSE` — `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | Apache-2.0; root NOTICE present |
| 20 | `terrapower/armi` [#2121](https://github.com/terrapower/armi/pull/2121) | `1636d23787671a91e240eaae24740a7e2e7e979e` | `LICENSE.md` — `71d363f18a2ebe782d950fce2d543a865ec11a07` | Apache-2.0 |
| 21 | `PyThaiNLP/pythainlp` [#1046](https://github.com/PyThaiNLP/pythainlp/pull/1046) | `188904f22c4c80fd7406706850c798f611690a4a` | `LICENSE` — `8dada3edaf50dbc082c9a125058f25def75e625a` | Apache-2.0 |
| 22 | `modin-project/modin` [#7554](https://github.com/modin-project/modin/pull/7554) | `1817ae423ba86c467f5a737817a8c00653be75cb` | `LICENSE` — `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | Apache-2.0; root NOTICE present |
| 23 | `CrossGL/crosstl` [#201](https://github.com/CrossGL/crosstl/pull/201) | `2e6ede3fc697cf110938bfd6df6074504906e2a2` | `LICENSE` — `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | Apache-2.0 |
| 24 | `MarketSquare/robotframework-robocop` [#1374](https://github.com/MarketSquare/robotframework-robocop/pull/1374) | `271e73253a70710cc80374128efa9eabb549b5f2` | `LICENSE` — `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | Apache-2.0 |
| 25 | `CTFd/CTFd` [#2767](https://github.com/CTFd/CTFd/pull/2767) | `61d2bddaed393ce5be5a1e911be09522bebaf523` | `LICENSE` — `e852f622caf17e13982790b2399867b67900c805` | Apache-2.0 |
| 26 | `meltano/sdk` [#3091](https://github.com/meltano/sdk/pull/3091) | `ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2` | `LICENSE` — `564273905d22b60a0deb1155ece4281c0b855cbc` | Apache-2.0 |
| 27 | `capitalone/datacompy` [#404](https://github.com/capitalone/datacompy/pull/404) | `5ab81a14c59728c7ed338a855d1a94c7c1425259` | `LICENSE` — `7a4a3ea2424c09fbe48d455aed1eaa94d9124835` | Apache-2.0 |
| 28 | `jax-ml/jax` [#25650](https://github.com/jax-ml/jax/pull/25650) | `44d67e1379f931d730575a6db7691d58993ea5cd` | `LICENSE` — `d645695673349e3947e8e5ae42332d0ac3164cd7` | Apache-2.0 |
| 29 | `sparckles/Robyn` [#1002](https://github.com/sparckles/Robyn/pull/1002) | `deea29aec9348a96d4e2d4c9207c7a2ceb0bdbce` | `LICENSE` — `40c504a7176c9c6ef7fa9009483fb7e56c73b605` | BSD-2-Clause |
| 30 | `amaranth-lang/amaranth` [#1519](https://github.com/amaranth-lang/amaranth/pull/1519) | `8c5ed4051dd74a6347af8d52f8e397eb53218ac4` | `LICENSE.txt` — `cb522426f79b987ad57f265b639a3f6c28214e04` | BSD-2-Clause |
| 31 | `cta-observatory/ctapipe` [#2732](https://github.com/cta-observatory/ctapipe/pull/2732) | `287e7685e0e963f3fb44d92832ca97ac8c265c40` | `LICENSE` — `7d85dda24fa481e24c4b33dd98dbc13245ee1fd2` | BSD-3-Clause |
| 32 | `pallets/werkzeug` [#2956](https://github.com/pallets/werkzeug/pull/2956) | `40319f91dbbae0a780526eab037a009b1a7e4d36` | `LICENSE.txt` — `c37cae49ec77ad6ebb25568c1605f1fee5313cfb` | BSD-3-Clause |
| 33 | `pallets/click` [#2788](https://github.com/pallets/click/pull/2788) | `380008389b32ca2b7de7c73f670a9eee1562004e` | `LICENSE.txt` — `d12a849186982399c537c5b9a8fd77bf2edd5eab` | BSD-3-Clause |
| 34 | `Kozea/WeasyPrint` [#2416](https://github.com/Kozea/WeasyPrint/pull/2416) | `1b24ad91323c8444e398b75ed40ad54cf678ea0d` | `LICENSE` — `5b460bb52be9552ca2aa999642c6d66da9589fb3` | BSD-3-Clause |
| 35 | `python-control/python-control` [#1145](https://github.com/python-control/python-control/pull/1145) | `dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113` | `LICENSE` — `fbfc42c670132862f4d6998add25451214023574` | BSD-3-Clause |
| 36 | `stfc/PSyclone` [#2767](https://github.com/stfc/PSyclone/pull/2767) | `a33a99b7953130220ed7d3ad38d358c1124276af` | `LICENSE` — `9152f9670259384b1fe362f8461ced92fcea13ae` | BSD-3-Clause |
| 37 | `skrub-data/skrub` [#1445](https://github.com/skrub-data/skrub/pull/1445) | `3869319e82d307f7faa51a98800a10b980dfce22` | `LICENSE.txt` — `d6ac581db9e74bf99400052ea4658f14093cedf9` | BSD-3-Clause |
| 38 | `cogent3/cogent3` [#2050](https://github.com/cogent3/cogent3/pull/2050) | `7cf9ba361be9822e92989476c5fb690351481a3a` | `LICENSE` — `7941fa935f4b9dd97bf54cf4e1750d762763efe0` | BSD-3-Clause |
| 39 | `qutip/qutip` [#2694](https://github.com/qutip/qutip/pull/2694) | `b821b1aa8c98a00f58014e7ec02cc9cbef701ce4` | `LICENSE.txt` — `bb2d6131bb8f4820a2e29714fb4ce1792e0215b6` | BSD-3-Clause |
| 40 | `mpmath/mpmath` [#902](https://github.com/mpmath/mpmath/pull/902) | `04d79bd34c0543f023314960dd17e6440ee374c3` | `LICENSE` — `7a1328aab269b65f504ce42fd244a5db3262053a` | BSD-3-Clause |
| 41 | `astropy/ccdproc` [#901](https://github.com/astropy/ccdproc/pull/901) | `e793d77023ddfb62c4a1e7ca822e5a03a10b1776` | `LICENSE.rst` — `43e7424f276a51e3ab00133407641023098a5b2b` | BSD-3-Clause |
| 42 | `pybamm-team/PyBaMM` [#4465](https://github.com/pybamm-team/PyBaMM/pull/4465) | `1b6ef033646d7d89a0bebe12732a1d84ffee6739` | `LICENSE.txt` — `9937766a582491e7c9ea639b5d1095e44cec0c06` | BSD-3-Clause |
| 43 | `asdf-format/asdf` [#1907](https://github.com/asdf-format/asdf/pull/1907) | `74fdcd96540049e4824b4da2bbe3ffdf42d23cfc` | `LICENSE` — `62a4e1a84cf19b924d36cfcf56cb8a5fa8eddb84` | BSD-3-Clause |
| 44 | `msgspec/msgspec` [#772](https://github.com/msgspec/msgspec/pull/772) | `148f9a17e04915dcb50be96efc6a3e6732340a5a` | `LICENSE` — `9aae71ed462e08e3e0d955063e7d6679fd38207e` | BSD-3-Clause |
| 45 | `pallets/jinja` [#2033](https://github.com/pallets/jinja/pull/2033) | `1dc04bccf9384cced4262d7ca7157638b0ebd970` | `LICENSE.txt` — `c37cae49ec77ad6ebb25568c1605f1fee5313cfb` | BSD-3-Clause |
| 46 | `scikit-rf/scikit-rf` [#1282](https://github.com/scikit-rf/scikit-rf/pull/1282) | `6b92669854505b6ef73aa1e5e75669489adbd568` | `LICENSE.txt` — `ddfd40848d4b5d3e7c4e129f514e6d41c8322546` | BSD-3-Clause |
| 47 | `jsonpickle/jsonpickle` [#565](https://github.com/jsonpickle/jsonpickle/pull/565) | `9a6822734ea5d06967c0c514db3c5d577d6c1dc2` | `LICENSE` — `2e0bab72e2107889340676307d1867cde58137b8` | BSD-3-Clause |
| 48 | `scikit-activeml/scikit-activeml` [#504](https://github.com/scikit-activeml/scikit-activeml/pull/504) | `8bc5882a47ad9a9600c5806ea56987c2892167cb` | `LICENSE.txt` — `d137567ed81338e647e6aa6ffc2ea37edc454aeb` | BSD-3-Clause |
| 49 | `geofileops/geofileops` [#649](https://github.com/geofileops/geofileops/pull/649) | `f7f8a4cf49b1278f3e9e5f4157718de441a21b57` | `LICENSE.txt` — `ecf40d7a30bd534ebd781bca089abd3168bc13a1` | BSD-3-Clause |
| 50 | `lektor/lektor` [#1214](https://github.com/lektor/lektor/pull/1214) | `c22e224ec56620c2a1d90016d74518970b1dd578` | `LICENSE` — `b7ddaf0a1fd8cbfae2750f342404c23251552181` | BSD-3-Clause |
| 51 | `cuthbertLab/music21` [#1736](https://github.com/cuthbertLab/music21/pull/1736) | `e05fc53dfef7b2c9ac974c0cacb8b85e9c4d4605` | `LICENSE` symlink to `music21/license.txt`; symlink blob `10429f7ad70659ae5f4f21286c4ec9e25e85f56d`; target blob `d9e81a163d2ba817d5d5e9c785f626de43527dd1` | BSD-3-Clause for Python files |
| 52 | `geopandas/geopandas` [#3591](https://github.com/geopandas/geopandas/pull/3591) | `c36eba059f6170715b63a9aa065817c64025d263` | `LICENSE.txt` — `028603be2080134aa4817ed691fec3f449ffa609` | BSD-3-Clause |
| 53 | `python-babel/babel` [#1141](https://github.com/python-babel/babel/pull/1141) | `f1c8633a7d765f07b94e0a6097b3f0c7912b955f` | `LICENSE` — `83b6e513d40f78480c86ed03d6a2e6823774d589` | BSD-3-Clause |
| 54 | `gammapy/gammapy` [#5525](https://github.com/gammapy/gammapy/pull/5525) | `cff9ae2c54c38cc664967ff1cd2ef41457c2c6b8` | `LICENSE.rst` — `82a9b4334e9f31b6619b3fe005971d26bf25d939` | BSD-3-Clause |
| 55 | `joshuadavidthomas/django-bird` [#219](https://github.com/joshuadavidthomas/django-bird/pull/219) | `6641de58a71e94689fb96c09a3aca25aab8efc25` | `LICENSE` — `c159dcad5e8808651d43e7faf1c0e79dac7b322e` | MIT |
| 56 | `vacanza/holidays` [#2106](https://github.com/vacanza/holidays/pull/2106) | `60966eaeca137cf2e08826a2b3e08fe6f5af7b36` | `LICENSE` — `9bfa781d404b068ea21a586100de953f366dfacb` | MIT |

## 4. Root NOTICE files

### Row 19 — Napalm

Exact-base root NOTICE blob: `362d9d34c0a4fc9985f247b52d65e97d4d07e719`.

It attributes the project to Spotify AB (copyright 2015) and says the project includes software developed at Spotify AB, alongside contributions by other individuals. Preserve this notice with any use or redistribution that requires it.

**Additional file-level hold:** PR [#2152](https://github.com/napalm-automation/napalm/pull/2152) adds `test/nxos_ssh/mocked_data/test_get_facts/issue2151/show_version.txt`. The 50-line fixture begins with `Copyright (C) 2002-2017, Cisco and/or its affiliates` and states that certain components are licensed under GPL-2.0, GPL-3.0, LGPL-2.1 or LGPL-2.0. Issue [#2151](https://github.com/napalm-automation/napalm/issues/2151) includes a separate raw `show version` output in its comments. The issue output says Cisco copyright 2002–2024, Nexus9000 C93180YC-FX3, serial ABC12345DE, uptime 1 day 1 hour 11 minutes 11 seconds, and System version 10.2(6). The PR fixture says copyright 2002–2017, Nexus 3048, serial TM6012EC74B, uptime 50 days 5 hours 9 minutes 7 seconds, and System version 7.0(3)I4(7). Both contain the critical line `NXOS: version 10.3(5) [Maintenance Release]`, so the fixture may still exercise the same parser branch; however, it is not demonstrated to be the same raw device output. Its source and redistribution basis remain unestablished, and the issue-to-test provenance link is incomplete.

This does **not** prove that the fixture itself is GPL/LGPL, nor that Cisco's output is not reusable. It does mean the root Apache-2.0 file is insufficient evidence for the fixture's origin and redistribution terms. Keep row 19 on legal/provenance and test-identity hold until the source, applicable terms, and redistribution basis for this exact fixture are established. Do not copy this fixture into a benchmark packet merely because the upstream repository root is Apache-2.0. Prefer a minimal synthetic regression fixture containing only the relevant version line, if it reproduces the base failure and fixed pass.

### Row 22 — Modin

Exact-base root NOTICE blob: `77a9b8402671f140659c8956a98b3dc05d62eea0`.

It identifies Modin and states copyright 2018–2024 Modin Developers. The root also contains `LICENSE_HEADER` (blob `cae6413e55965df9ec6507a51c539412831726e7`) in addition to the Apache-2.0 `LICENSE`. Preserve the NOTICE attribution where applicable.

## 5. Nested and file-level license inventory

The tree scan found these relevant paths at the frozen base commits. The corresponding PR changed paths did not directly modify these license files or directories. They remain important when choosing which repository files, tests, fixtures, or data to include in a case packet.

| Row | Exact-base nested or special provenance paths | Relevance / treatment |
|---:|---|---|
| 17 | `llm/vicuna/LICENSE`; `sky/skylet/LICENSE` | Additional component licenses are present. PR #5985 changes Kubernetes/SSH/provisioning/resource code and tests, not these license paths. |
| 21 | `docs/notes/license.rst`; `pythainlp/corpus/corpus_license.md` | Corpus metadata says project corpora/datasets/docs are CC0 and language models CC BY 4.0. PR #1046 changes syllable utility code/tests, not corpus assets. Do not infer corpus or model license from the root code license. |
| 22 | `LICENSE_HEADER`; root `NOTICE` | Keep header and NOTICE attribution alongside the Apache-2.0 root file. |
| 25 | `CTFd/themes/core-beta/LICENSE` | The bundled core-beta theme has a separate license file. PR #2767 changes API flag handling and tests, not theme assets. |
| 26 | `cookiecutter/mapper-template/.../LICENSE`; `cookiecutter/tap-template/.../LICENSE`; `cookiecutter/target-template/.../LICENSE`; `samples/sample_tap_dummy_json/LICENSE` | Template/sample subprojects carry their own license files. PR #3091 changes Singer SDK schema code and tests, not these template/sample trees. |
| 28 | `jax/_src/third_party/scipy/LICENSE.txt`; `jax/experimental/jax2tf/examples/tf_js/quickdraw/third_party/zaidalyafeai.github.io/LICENSE`; `jaxlib/tools/LICENSE.txt`; `tests/third_party/scipy/LICENSE` | JAX includes third-party and test-derived material with separate license texts (including SciPy and MIT-licensed QuickDraw material). PR #25650 changes dtypes/array methods and tests, not those third-party paths. |
| 32 | `docs/license.rst`; `src/werkzeug/debug/shared/ICON_LICENSE.md` | The icon file identifies the Silk icon set and CC-BY-2.5 or CC-BY-3.0. PR #2956 changes HTTP authorization parsing and tests, not the icon. |
| 33 | `docs/license.rst` | Documentation carries a separate license note; PR #2788 changes Click argument handling and tests, not documentation assets. |
| 37 | `skrub/_reporting/_data/templates/icons/LICENSE`; `skrub/_reporting/_data/templates/pure-3.0.0/LICENSE` | Template assets include Bootstrap MIT and Yahoo BSD license notices. PR #1445 changes expression code/tests, not reporting templates. |
| 38 | `doc/COGENT3_LICENSE.rst`; `doc/licenses.rst` | Documentation explicitly says licenses for other code sources are left in place. PR #2050 changes core tree code/tests, not documentation or vendored source. |
| 39 | `doc/LICENSE_cc-by-3.0.txt`; `doc/copyright.rst` | QuTiP documentation has CC-BY-3.0 attribution separate from the BSD-3-Clause software license. PR #2694 changes coefficient code/tests and a changelog, not docs. |
| 41 | `docs/license.rst`; `licenses/README.rst` | The `licenses` directory is described as holding license/credit information for derived/distributed works and datasets. PR #901 also adds one contributor to `AUTHORS.rst`; it changes ccdproc image-collection code/tests, not the license directory. |
| 43 | `asdf/_jsonschema/COPYING`; `asdf/_jsonschema/json/LICENSE`; `licenses/JSONSCHEMA_LICENSE`; `licenses/JSON_LICENSE` | JSON Schema / JSON components have separate license records. PR #1907 changes YAML utilities/tests, not these nested third-party paths. |
| 45 | `docs/license.rst` | Documentation license note; PR #2033 changes sandbox code/tests, not docs. |
| 46 | `doc/source/examples/LICENSE.txt`; `doc/source/license.rst`; `doc/sphinxext/LICENSE.txt` | Example and Sphinx extension content have separate license files. PR #1282 changes scikit-rf source code/tests, not documentation extensions. |
| 47 | `jsonpickleJS/LICENSE` | JavaScript distribution has a separate license. PR #565 changes Python unpickling code/tests, not `jsonpickleJS`. |
| 50 | `example/themes/lektor-theme-nix/LICENSE.md`; `tests/demo-project/content/icc-profile-test/LICENSE.txt`; `tests/demo-project/content/icc-profile-test/license.txt` | Example theme and ICC profile test content have separate licensing. PR #1214 changes builder/utils code and tests, not these paths. |
| 51 | `LICENSE` is a symlink to `music21/license.txt`; also `music21/corpus/license.txt`, `music21/corpus/essenFolksong/license.txt`, `music21/scale/scala/scl/license.txt` | `music21/license.txt` explicitly applies BSD-3-Clause to all Python files, but excludes corpus content. The Essen folksong notice allows non-commercial distribution/use; Scala scale files may have non-commercial or other restrictions. PR #1736 changes Python source/tests only, not corpus or scale assets. |
| 53 | `babel/locale-data/LICENSE.unicode`; `docs/_themes/LICENSE`; `docs/license.rst` | Unicode locale data has a separate Unicode License V3. PR #1141 changes date-format code/tests, not locale data or documentation theme. |
| 56 | `tests/third_party/test_numpy.py` | A third-party test path exists; PR #2106 changes US holiday data, a snapshot and country tests, not this file. |

The table is a targeted tree inventory, not an exhaustive legal review of every dependency or every source line. A complete case packet must still preserve any applicable per-file copyright headers, license files, NOTICE files, and attribution accompanying files actually used.

## 6. Diff-level source and attribution check

Across the 40 PRs, the changed-path inventory returned **151 files** in total. No changed path was named `LICENSE`, `NOTICE`, `COPYING`, or a `third_party` path. The patch-addition scan produced these material observations:

- Row 19: new Cisco NX-OS `show_version.txt` fixture with Cisco copyright and GPL/LGPL component notices — **provenance hold**, as detailed above.
- Row 41: `AUTHORS.rst` adds contributor `Evelyn Montes Sobal`; this is contributor attribution, not a new software license.
- Row 29: an OpenAPI configuration adds a `license` metadata field; it is API-description metadata, not a source-file license change.
- Other keyword matches were normal code/documentation wording, not added license headers or third-party source declarations.

This static scan cannot establish that every pre-existing source line was authored by the upstream project. It only reports that no additional license/NOTICE path was changed in these PRs and records the one clear external copyright-bearing fixture found in the added lines.

## 7. Decision and remaining gates

### Closed for this narrow audit

- Exact PR/base SHA parity: **40/40**.
- Exact-base root license file: **40/40**.
- Root license strata: 12 Apache-2.0, 2 BSD-2-Clause, 24 BSD-3-Clause, 2 MIT.
- Root NOTICE inventory: **2/40**, Napalm and Modin, both recorded above.
- Repository aliases resolved: `TobikoData/sqlmesh` now resolves to `SQLMesh/sqlmesh`; `jcrist/msgspec` now resolves to `msgspec/msgspec`. In both cases the frozen PR base SHA still matches the cohort row.

### Still open

1. Row 19 Napalm fixture: verify the Cisco output's source and the applicable permission/redistribution basis, or exclude the fixture/case from any redistributed evidence packet.
2. For any selected case, inspect the actual changed source/test files at both buggy and fixed commits for copyright notices, embedded snippets, generated code, vendor-derived material, and data assets.
3. Preserve root NOTICE files and all applicable nested licenses when constructing case packets. Music21 corpus assets and PyThaiNLP corpus/model material must not be treated as covered by the root source-code license.
4. Complete equivalent nested/file-level review for the other cohort ranges; a root license file is not a substitute for that review.
5. Run exact-base fail-to-pass reproductions and obtain independent human root-cause adjudication before accepting any case.

**No row in 17–56 is promoted to an accepted confirmatory case by this license audit.** The case registry remains intentionally unchanged. No upstream tests, model inference, fine-tuning, or training were performed as part of this audit.
