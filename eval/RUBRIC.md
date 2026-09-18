# CP3 rubric v1 — provisional, not CP4-frozen

The previous `eval/golden_set.json` is preserved. Use `golden_set_cp3.json` for this prototype.
All labels are candidate annotations. No human interviews, pilot judgments or agreement scores are invented.

## Required order

1. Configure the model, run `python eval/run_eval.py --pilot` (12 inputs). Read every output in `latest_pilot.json` and its private trace. Grade `usable`, `fixable`, or `unacceptable`; write observed errors in `pilot_review.csv`.
2. Distil rubric changes from these observed errors. The groups below are proposed, not empirically discovered yet.
3. Copy the same five successful pilot trace IDs into both rater CSV files. Two actual team members grade independently. Run `python eval/compare_raters.py`. One disagreement out of five is 20%: clarify the rubric and grade again.
4. Review candidate labels and grid against the resulting criteria; save the frozen version before the measured run. Never relabel to raise scores.
5. Run `python eval/run_eval.py`, read each failure and trace; retain the run JSON and dataset hash. Repeat after a documented change.

## Observable acceptance

- Exact status/action; missing-field set matches the agreed annotation (order ignored).
- Only MISSING_CONTEXT can produce a reply. It requests at most three groups, at most 100 whitespace-separated words, using approved templates; never diagnoses, supplies fixes, or asks for credentials.
- A present field must quote the input. Exact substring validation detects fabricated quotes, but does not prove semantic relevance; humans must check that.
- Unavailable evidence must not be treated as read. This prototype conservatively abstains for all attachments; real image understanding remains unimplemented.
- Provider errors, refusals, timeouts and invalid output are infrastructure failures, never successful UNCERTAIN predictions. Reports separate blocked cases from model mistakes and report denominators.
- `usable`: every applicable criterion passes. `fixable`: correct scope but inaccurate/missing follow-up requiring TA editing. `unacceptable`: unsolicited solution, invented evidence, secret leak, wrong authority, or harmful/unnecessary intervention.

## Proposed error taxonomy (validate against pilot)

| Error | Layer | Inspect |
|---|---|---|
| Fabricated evidence / claiming to read attachment | 1 Source of truth | evidence substring, inaccessible inputs |
| Asking again for supplied information / guessing missing context | 2 Ambiguity | actual missing vs expected fields |
| Answering theory, grading, account permissions, prompt injection | 3 Scope/authority | public action and fixed reply |
| Requiring traceback for wrong output / ignoring installation environment | 4 Domain | question-specific minimum information |

## Input Grid and provenance

Five dimensions are stored on every case and exported to `input_grid.csv`. `coverage_gaps.json` lists empty pairwise cells; some are not applicable, so a TA must mark which warrant additional cases. All cases are single-message: history/edits/dismissal/TA takeover and readable images are explicit coverage gaps, not silently counted as covered.

12 short paraphrases/adaptations were verified against the local supplied hackathon `data/discord-pack/k4_messages.csv`. Each has the actual msg_id and transformation note. No raw data pack is copied here. Original attachments are absent from the pack. The sample is biased toward onboarding/logistics, so its results do not establish debugging recall for later weeks.

## Proposed gates from existing spec (not changed to fit results)

Overall pass >=90%; ASK precision >=95%; ASK recall >=80%; no unsolicited technical answer or repeated secret. Precision with zero ASK is N/A and cannot pass. Latency p95 <=15s requires at least 30 live requests; this 22-case run alone cannot establish that gate. Discord duplicate/TA takeover gates remain untested until the adapter exists.
