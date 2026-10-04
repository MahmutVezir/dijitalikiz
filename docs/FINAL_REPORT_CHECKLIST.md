# TÜBİTAK 2204-A Final Report Checklist

## Research framing
- [ ] Official title and research question unchanged.
- [ ] Testable hypotheses stated.
- [ ] Independent/dependent variables defined.
- [ ] Software case is the experimental unit.
- [ ] Seed repetitions are not independent cases.

## Dataset and provenance
- [ ] Source URL and publication date recorded.
- [ ] Root cause and fix independently verified.
- [ ] CCDG edges evidence-backed.
- [ ] Pilot/confirmatory inclusion rule documented.
- [ ] Contamination audit completed.
- [ ] No case selected because of model success.

## Experimental controls
- [ ] Exact model ID/revision and quantization recorded.
- [ ] Prompt/context hashes recorded.
- [ ] Generation parameters and seeds recorded.
- [ ] Equivalent base evidence used.
- [ ] Ground truth absent from both contexts.
- [ ] Output schema and matcher frozen.

## Statistics
- [ ] Five seeds aggregated with frozen 3/5 majority.
- [ ] Exact two-sided McNemar test used.
- [ ] Alpha = 0.05.
- [ ] Power/sample-size assumption fixed before confirmatory inference.
- [ ] Discordant pairs and CCDG-minus-Standard effect reported.
- [ ] Parse failures/missing runs reported.
- [ ] Secondary metrics labeled descriptive unless pre-specified.

## Reproducibility
- [ ] Raw outputs archived.
- [ ] Code commit SHA recorded.
- [ ] Dependency/environment versions recorded.
- [ ] Exact commands recorded.
- [ ] No secrets committed.

## Interpretation
- [ ] Claims limited to sampled domain.
- [ ] Limitations explicit.
- [ ] Contamination uncertainty discussed.
- [ ] Model-size/quantization limitations discussed.
- [ ] Negative results reported without selective exclusion.
