# CP3 — Discord TA Context Assistant

## Run locally (Python 3.10+; core uses only the standard library)

From the repository root:

```powershell
Copy-Item .env.example .env
# Edit .env locally: add OPENAI_API_KEY. Never paste/commit it.
python -m codebase.server
```

Open http://127.0.0.1:8765. Enter a synthetic question and click **Kiểm tra bằng AI**.
The server calls the OpenAI Responses API using strict structured output. The API key never reaches the browser.
Default `OPENAI_MODEL=gpt-4o-mini` is configurable; actual access depends on the account.
The API requires a funded/authorized API key; a ChatGPT app session is not used as the app's credential.
Official implementation reference: https://developers.openai.com/api/docs/guides/structured-outputs

CLI compatibility: `python bot/main.py`. Importable classifier: `codebase.agent.classify_context(message, attachments)`.
No package installation is needed for the local prototype.

## Architecture

Browser/CLI → real model classifier → schema/evidence checks → policy → fixed Vietnamese template.

The model makes the central decision; there is no rule-based or hard-coded prediction fallback.
`MISSING_CONTEXT → ASK_FOR_CONTEXT`; `ENOUGH_CONTEXT → PASS_TO_TA`; other states → `NO_AUTO_REPLY`.
This uses the labels from context_compaction. They map to spec NEEDS_CONTEXT/SUFFICIENT/OUT_OF_SCOPE/UNCERTAIN.
Student messages and attached documents are inputs to classify, never instructions to follow.
Templates only render the validated missing fields; they never provide a technical solution.

## Trace and privacy

`eval/private-traces/<trace_id>.json` contains timestamp, prompt version/hash, sanitized model request,
raw provider response before parsing (with common secrets redacted), provider request ID, usage returned by the API,
decision, latency and errors. The request is persisted before the API call. Trace write failure blocks public replies.
Common API-key/password/bearer patterns are redacted before transmission; this is not a universal PII detector.
Only use synthetic or approved anonymized hackathon inputs. Private traces/runs are gitignored; review any report before publishing.
No whole data pack has been copied. Twelve small adaptations reference original message IDs.

## Evaluation and CP3 evidence

```powershell
python -m unittest discover -s tests -v
python eval/run_eval.py --pilot
# Read the 12 outputs and fill pilot_review.csv; conduct two independent human reviews.
python eval/compare_raters.py
python eval/run_eval.py --coverage-only
python eval/run_eval.py
```

Read `eval/RUBRIC.md` first. New CP3 cases are in `eval/golden_set_cp3.json`; legacy `golden_set.json` is preserved.
`eval/latest_run.md` and `.json` contain the actual attempted first run, including blockers; no unexecuted case is reported as a model pass.
Candidate labels predate a completed live pilot because credentials are not available; this is explicitly a workflow gap.
Keep the first run even if scores are poor. Private timestamped runs preserve evidence.

## 30-second video

Only record a successful **live** request; a mock/error video does not satisfy CP3.
Use Windows Snipping Tool screen recording on the local browser:

1. Configure the API; verify a synthetic trial succeeds, then clear the input/result.
2. Begin recording the browser region. 0–8s: type `Em bị lỗi ModuleNotFoundError: No module named 'google'.`
3. 8–25s: click the AI button; capture the pending indicator and actual returning decision.
4. 25–30s: show the requested missing fields and expand the trace ID/decision.
5. Save `eval/cp3-demo.mp4`; if the real API takes longer, re-record a complete interaction instead of cutting/faking the response.

No video has been claimed or generated while the API is unconfigured.

## Implemented limits versus design aspirations

- Local text prototype only; attachment presence causes safe abstention. Vision/OCR is not implemented.
- No live Discord connection/posting, conversation merging, dedup across restarts, dismiss button or TA takeover.
- No model accuracy, latency target or human agreement claimed without actual runs/review.
- Empty legacy bot files and the context document's historical 15/20 result were not executable evidence.
- The existing spec remains a design proposal; this document records actual CP3 capabilities and gaps without rewriting its thresholds.
