# Frozen Confirmatory Experiment Results — 2026-10-09

## Execution and provenance

The frozen confirmatory run completed successfully.

- GitHub Actions run: [37976682761](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761), workflow run #95.
- Confirmatory source commit: `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`.
- GitHub artifact ID: `11640450681`.
- GitHub artifact archive SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`; this matched the downloaded ZIP hash.
- The artifact's internal manifest declares 212 files and 160 inference records. Independent rechecking found 212/212 listed files present, with no unlisted files, size mismatches or SHA-256 mismatches.
- 160 unique run files: 16 cases × 2 conditions × 5 seeds. All records cite the same source commit, all raw-output checksums matched, and all 160 outputs parsed as JSON. There were no parse failures or duplicate parsed-output groups.
- Runtime metadata records Python 3.11.17, PyTorch 2.2.1+cu121, Transformers 4.43.2 and two NVIDIA Tesla T4 devices.

## Frozen primary endpoint and results

The frozen primary endpoint is root-cause correctness under a predeclared, case-specific string-alias rubric. A case passes a condition only when at least 3 of 5 seed-level outputs match an alias under the exact normalization/contiguous-phrase rule. The statistical unit is the independent software case.

| Metric | Standard Context | CCDG Context |
|---|---:|---:|
| Inference records | 80/80 | 80/80 |
| JSON parse failures | 0 | 0 |
| Primary endpoint passes | 0/80 (0%) | 0/80 (0%) |
| Cases passing the 3-of-5 majority rule | 0/16 (0%) | 0/16 (0%) |
| Legacy complete-diagnostic passes | 0/80 (0%) | 0/80 (0%) |

The case-level paired contingency table is:

| | CCDG passes | CCDG fails |
|---|---:|---:|
| Standard passes | 0 | 0 |
| Standard fails | 0 | 16 |

- Exact two-sided McNemar test: **p = 1.00**.
- Observed paired risk difference (CCDG minus Standard): **0.00**.
- 95% paired risk-difference interval as computed by the frozen analysis: **[-0.1936, 0.1936]**.
- Discordant pairs: Standard-only = 0; CCDG-only = 0.
- The predeclared decision rule does not reject the null hypothesis at α = 0.05.

## Interpretation: a floor effect, not evidence of equivalence

The execution and artifact checks passed, but the measured primary endpoint has a severe floor effect: every one of the 160 outputs failed the frozen alias matcher, so all 16 cases tie as failures across the two conditions. The p-value of 1.00 follows from zero discordant case outcomes. It **does not** establish equivalence and it **does not** prove that CCDG has no effect.

The alias checker is explicitly a deterministic contiguous-string matcher, not a semantic judge. For example, a CLOSURE-14 output explains that `ControlFlowAnalysis` misclassifies an exception path through a `finally` block and labels it `UNCOND` rather than `ON_EX`; the ground truth describes an exception path mislabeled as an unconditional edge. This is close in meaning but is not necessarily a contiguous match to any fixed alias phrase. This example demonstrates why zero string matches cannot be interpreted as a validated finding that every diagnosis was semantically wrong. It does not justify changing the frozen endpoint after seeing results.

The experiment therefore answers a narrower question: **under the frozen literal-alias operationalization, the study detected no difference because both conditions had zero case-level passes. The intended scientific question—whether CCDG improves semantic root-cause diagnosis—remains unresolved by this endpoint.**

## Contamination and limitations

All 16 cases carry a **high public-exposure contamination-risk label**. This means the defects/fixes are publicly exposed and could have appeared in model training data; it is not evidence that the model definitely saw any case during training. The finding should be reported as a limitation.

The scoring amendment was documented on 2026-10-09 after pilot-output diagnostics and before any confirmatory outputs were examined. Case selection did not consult model outputs. The final TÜBİTAK report must transparently disclose this chronology rather than describing the primary endpoint as fully preregistered before any model output had been seen.

## Next scientific decision

1. Preserve this confirmatory artifact, frozen rubric, and reported analysis unchanged.
2. Do not add aliases or alter scoring on the basis of these 160 outputs and then report the modified score as confirmatory.
3. Any semantic review of these existing outputs must be labeled exploratory, with condition labels concealed from reviewers where possible and adjudication rules specified before the review.
4. To test the intended semantic hypothesis confirmatorily, define and validate the scoring instrument before outcomes are inspected, then preregister a new independent confirmatory sample and power plan. Do not reuse a post hoc re-score of this same visible result as a new confirmatory result.

## Reproduction

The delivered archive is `dijitalikiz-confirmatory-e1e083f5400432b98143bdb35ff2c5b435ea8f6e.zip`, available from GitHub Actions run #95 as artifact `11640450681`. Its internal `artifact_manifest.json` records hashes and sizes for all 212 delivered files. The repository's independent audit utility is `scripts/audit_confirmatory_artifact.py`.
