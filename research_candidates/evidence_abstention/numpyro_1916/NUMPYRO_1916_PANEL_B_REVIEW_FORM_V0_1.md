# Panel B — coded evidence-packet review form

**Form version:** 0.1 draft  
**Use:** One completed copy per coded packet per reviewer. Do not write the case name, issue/PR, hidden tier, or suspected gold cause.

## Reviewer declaration

- Reviewer code:
- Date/time (UTC):
- Conflict-of-interest screen completed: YES / NO
- Prior access to source/issue/PR/patch/fix: NO / YES (if YES, stop; do not rate)
- External search performed: NO / YES (if YES, stop and disclose)
- Packet code:
- Review order position:
- Reviewer confirms no discussion with other raters before lock: YES / NO

## A. Technical readability

- Can the visible packet be interpreted without hidden context? YES / PARTLY / NO
- Are any terms or references materially ambiguous? NO / YES
- Ambiguity details:
- Any suspected missing context? Describe without searching externally.

## B. Free-form causal mechanisms

List each distinct causal explanation that remains consistent with the visible packet. Do not guess what the hidden answer is.

| Mechanism code | Mechanism stated in your own words | Evidence item IDs and exact supporting excerpt | Status |
|---|---|---|---|
| M1 |  |  | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M2 |  |  | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M3 |  |  | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M4 |  |  | PLAUSIBLE / EXCLUDED / UNRESOLVED |

Add rows as needed. Do not collapse distinct explanations merely because they produce the same observed error.

## C. Evidence-to-causality assessment

For each mechanism you listed:
- Does the packet establish a causal link, or merely show a compatible symptom/call-site?
- What exact visible item supports the link?
- What plausible alternative does the evidence fail to rule out?
- What evidence would discriminate the remaining alternatives?

## D. Overall packet judgment

Select exactly one:

- [ ] One causal mechanism is uniquely supported by the visible evidence.
- [ ] Multiple distinct mechanisms remain plausible.
- [ ] No causal mechanism can be assessed from this packet.
- [ ] Unscorable; explain why.

Number of distinct mechanisms you regard as still plausible:

- [ ] 0
- [ ] 1
- [ ] 2
- [ ] 3
- [ ] 4 or more
- [ ] Cannot determine

Does the packet eliminate at least one plausible alternative? YES / NO / UNCLEAR

Does the packet contain enough evidence to justify a definitive root-cause diagnosis? YES / NO / UNCLEAR

Rationale (must cite item IDs and explain the causal inference):

## E. Missing/discriminating evidence

What is the smallest additional observable evidence needed to distinguish the remaining mechanisms?

## F. Reviewer confidence and identity check

- Confidence in this rating: LOW / MODERATE / HIGH
- Did you recognize the project, issue, PR, or codebase? NO / POSSIBLY / YES
- Did you access any external material? NO / YES
- If recognized or external material accessed, explain:
- Any reason your rating should be excluded from blinded adjudication?

## G. Lock record

- I confirm this is my independent first rating: YES / NO
- I have not seen the other reviewer's scores: YES / NO
- Signed reviewer code:
- Timestamp:
- Immutable form SHA-256 (filled by custodian after receipt):
