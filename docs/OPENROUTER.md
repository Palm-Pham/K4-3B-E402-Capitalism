# Test with OpenRouter

Verified on 2026-09-18: 30 software tests passed. One real synthetic request to the exact model
completed in 27.1 seconds, returning MISSING_CONTEXT and asking for reproduction steps and environment.
Trace: `eval/private-traces/e12b7268a65d49f3a7596a203271ac5b.json`.
This single successful connection test is not a golden-set accuracy result.

In the repository `.env`, keep your existing key and add/update:

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_actual_openrouter_key
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

Never commit `.env`. Existing Discord settings can remain. `OPENROUTER_BASE_URL` is not used:
the code uses the fixed official endpoint `https://openrouter.ai/api/v1/chat/completions`.

Restart the Python process once after this code update (Ctrl+C, then `python -m codebase.server`).
Open http://127.0.0.1:8765 and refresh. The provider/model should show OpenRouter and the exact model above.
Subsequent `.env` edits are read on each request. Explicit shell environment variables override `.env`.

Try a synthetic input: `Em bị lỗi ModuleNotFoundError: No module named 'google'.`
The classifier should ask for missing context, never give a solution. See the returned trace ID in `eval/private-traces/`.

## What changed

- `codebase/agent.py`: provider selection, separate keys, OpenRouter Chat Completions transport, tool argument extraction; existing Python validation and fixed replies remain.
- `codebase/server.py`: provider-aware health endpoint; removed a duplicate class declaration that prevented startup.
- `codebase/index.html`: shows the actual provider/key setting instead of always saying OpenAI.
- `tests/test_openrouter.py`: request contract, parsing, rejection paths, key isolation and configuration reload tests.

The selected endpoint advertises tools and named tool choice, but not `response_format`.
The request therefore forces one `classify_context` tool call with the schema as its parameters.
This is only structured data extraction: no tool-generated code or command is executed.
`require_parameters=true` avoids providers silently ignoring tool parameters. Local validation is still mandatory;
tool calling does not guarantee semantic correctness or exact schema compliance.

## Errors

- `missing_api_key`: check `OPENROUTER_API_KEY` and provider selection.
- `provider_http_401`: invalid/revoked key or wrong provider key.
- `provider_http_429`: rate limit/capacity; wait before trying again.
- `provider_http_404` / `503`: exact model route or provider unavailable; the code does not silently switch models.
- `provider_not_completed`: response was incomplete/truncated; inspect the private trace.
- Invalid JSON/evidence/tool: safely returns UNCERTAIN and no student reply.

Use synthetic inputs for this free endpoint. NVIDIA's model page states that free-endpoint inputs are logged
for security and service improvement and asks users not to upload confidential/personal information.
Do not send the real-chatlog golden set to it without checking the hackathon's data restrictions.

Sources checked 2026-09-18:
- https://openrouter.ai/api/v1/models/nvidia/nemotron-3-ultra-550b-a55b:free/endpoints
- https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free/api
- https://openrouter.ai/docs/guides/features/structured-outputs
