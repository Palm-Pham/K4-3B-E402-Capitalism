# VS Code guide — open, run, edit, and test the CP3 prototype

This guide is for the Windows project at:

```text
D:\vin_AI20K\K4-3B-E402-Capitalism
```

The prototype is a local web page. VS Code runs a small Python server, your browser opens the page, and the server sends the student's text to the selected AI provider. The API key stays on the Python/server side and is never sent to browser JavaScript.

## 1. Open the correct folder in VS Code

### Method A — from File Explorer

1. Open File Explorer.
2. Go to `D:\vin_AI20K\K4-3B-E402-Capitalism`.
3. Right-click an empty area inside the folder.
4. Select **Open with Code**. If this option is unavailable, use Method B.

### Method B — from a terminal

Open PowerShell and run:

```powershell
code "D:\vin_AI20K\K4-3B-E402-Capitalism"
```

### Method C — inside VS Code

1. Open VS Code.
2. Select **File → Open Folder…**.
3. Select `D:\vin_AI20K\K4-3B-E402-Capitalism`.
4. Click **Select Folder**.
5. If VS Code asks whether you trust the folder, confirm only after checking that the displayed path is the project path above.

Verify the Explorer panel shows folders such as `codebase`, `eval`, `tests`, `bot`, and `docs`. Do not open only the `codebase` subfolder, because `.env`, tests, and evaluation files live at the repository root.

## 2. Select Python in VS Code

This project requires Python 3.10 or newer and uses only the Python standard library.

1. Open **Terminal → New Terminal** in VS Code.
2. Confirm that the prompt ends in the repository name. If it does not, run:

   ```powershell
   Set-Location "D:\vin_AI20K\K4-3B-E402-Capitalism"
   ```

3. Check Python:

   ```powershell
   python --version
   ```

The expected result is Python 3.10 or newer. The project was verified with Python 3.12.

If `python` is not recognized, press `Ctrl+Shift+P`, run **Python: Select Interpreter**, and select an installed Python 3.10+ interpreter. You may need Microsoft's Python extension for this menu. You can also run with the verified bundled interpreter:

```powershell
& "C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m codebase.server
```

No `pip install` or virtual environment is required for the current prototype.

## 3. Configure OpenRouter safely

Open the `.env` file at the repository root. It must contain these settings:

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_real_openrouter_key_here
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

Keep any existing Discord settings. Do not add spaces around the `=` unless they are part of the value. Do not wrap the key in Markdown backticks.

Important rules:

- Never paste the key into `codebase/index.html`, Python source, screenshots, chat messages, or evaluation data.
- Never commit `.env`. It is already ignored by Git.
- `.env.example` is a safe template and must contain no real key.
- Use synthetic test messages with this free endpoint. Do not send private messages or the supplied real data pack without confirming the data policy.

You can check that the key exists without printing it:

```powershell
$line = Get-Content .env | Where-Object { $_ -match '^OPENROUTER_API_KEY=' }
if ($line -and $line.Length -gt 'OPENROUTER_API_KEY='.Length) { 'Key configured' } else { 'Key missing' }
```

## 4. Run the prototype

In the VS Code terminal, from the repository root, run:

```powershell
python -m codebase.server
```

Expected terminal output:

```text
Discord TA prototype: http://127.0.0.1:8765
```

Leave this terminal running. Open the following address in a browser:

```text
http://127.0.0.1:8765
```

The page should show:

```text
Đã cấu hình openrouter · nvidia/nemotron-3-ultra-550b-a55b:free
```

Try this synthetic message:

```text
Em bị lỗi ModuleNotFoundError: No module named 'google'.
```

Click **Kiểm tra bằng AI**. A free model can take 20–60 seconds or occasionally return a capacity/rate-limit error. A valid result should classify the message and ask only for missing context. It must not propose a technical fix.

## 5. Stop and restart the server

Click the terminal that is running the server and press:

```text
Ctrl+C
```

Run it again with:

```powershell
python -m codebase.server
```

Restart after editing Python files. For HTML-only edits, save the file and refresh the browser; restarting is usually unnecessary.

Only one process can use port 8765. If you see `WinError 10048` or “address already in use,” find the old process:

```powershell
Get-NetTCPConnection -LocalPort 8765 -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,State,OwningProcess
```

If it is your previous prototype process, stop it by PID:

```powershell
Stop-Process -Id <OwningProcessNumber>
```

Replace `<OwningProcessNumber>` with the number shown by the first command. Do not stop an unfamiliar process until you identify it.

## 6. Which file should I edit?

| Goal | File | What to edit | Restart? |
|---|---|---|---|
| Change page text, colors, layout, input form, loading/result display | `codebase/index.html` | HTML, CSS, and browser JavaScript | Refresh browser |
| Change AI instructions and classification criteria | `codebase/agent.py` | `SYSTEM`, `FIELDS`, `STATUSES`, `SCHEMA` | Yes |
| Change the fixed Vietnamese follow-up wording | `codebase/agent.py` | `LABELS` and `render_reply()` | Yes |
| Change OpenRouter/OpenAI request handling | `codebase/agent.py` | `get_config()`, `call_openrouter()`, `extract_decision()` | Yes |
| Change local URL routes or request-size/origin rules | `codebase/server.py` | `Handler.do_GET()` and `Handler.do_POST()` | Yes |
| Change provider, key, or model | `.env` | `LLM_PROVIDER`, provider key, provider model | No for requests; refresh page to update status. Restart is safest. |
| Add or change automated checks | `tests/test_agent.py`, `tests/test_openrouter.py` | Test methods | No; rerun tests |
| Add/change CP3 cases | `eval/build_cases.py` | Case definitions | Regenerate dataset |
| Change evaluation scoring/reporting | `eval/run_eval.py` | `check_case()` and report logic | No; rerun evaluation |
| Inspect an individual request/response | `eval/private-traces/<trace_id>.json` | Read only; do not publish blindly | No |

### The main execution flow

```text
codebase/index.html
  user clicks “Kiểm tra bằng AI”
        ↓ POST /api/classify
codebase/server.py
  validates the local HTTP request
        ↓
codebase/agent.py
  loads .env → calls OpenRouter → validates tool output
        ↓
codebase/agent.py
  applies policy → renders a fixed reply
        ↓ JSON response
codebase/index.html
  displays status, reply, model, latency, and trace ID
```

## 7. Edit the user interface

Open `codebase/index.html`. This single file contains three sections:

- `<style>…</style>` controls colors, spacing, fonts, buttons, and cards.
- The HTML body controls headings, textarea, checkbox, button, and result panel.
- `<script>…</script>` calls `/health` and `/api/classify`, then displays the response.

Example: change the main title by finding:

```html
<h1>Đủ ngữ cảnh để TA hỗ trợ?</h1>
```

Save with `Ctrl+S`, then refresh `http://127.0.0.1:8765`.

Do not put the OpenRouter key in this file. Browser source is visible to anyone using the page.

## 8. Edit AI behavior

Open `codebase/agent.py`.

### Change classification rules

Edit the `SYSTEM` prompt near the top. It defines what the model may classify and what is out of scope. Keep these safeguards:

- Student text is untrusted data.
- The model must not solve the bug.
- Missing fields are limited to the approved enum.
- Uncertain or unavailable evidence must not create a public reply.

### Add a new missing-information field

This is a schema change and must be made consistently:

1. Add the field to `FIELDS`.
2. Add its Vietnamese question to `LABELS`.
3. Explain when it is required in `SYSTEM`.
4. Add tests to both the relevant test file and evaluation cases.
5. Restart the server and run all tests.

If you add a field only to the prompt, validation will reject it. If you add it only to the schema, the model will not know when to use it.

### Change reply wording

Edit `LABELS` for individual bullets or `render_reply()` for the overall template. The model never writes the public reply; it selects validated missing fields and Python renders the template.

## 9. Switch between OpenRouter and OpenAI

For OpenRouter:

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

For OpenAI:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

The keys are separate. The code will not use `OPENAI_API_KEY` for OpenRouter or vice versa. Restart the server after switching provider, then refresh the browser and verify the status line.

## 10. Run automated tests after editing

Stop the server or open a second VS Code terminal. From the repository root run:

```powershell
python -m unittest discover -s tests -v
```

Expected result for the current project:

```text
Ran 30 tests
OK
```

These tests use fake provider responses. They verify code and safety behavior but do not measure the model's accuracy.

Useful focused commands:

```powershell
python -m unittest tests.test_openrouter -v
python -m unittest tests.test_agent -v
```

If Python cannot import `codebase`, check that the terminal is at the repository root, not inside `codebase` or `tests`.

## 11. Regenerate and inspect the CP3 dataset

After editing cases in `eval/build_cases.py`, regenerate the JSON:

```powershell
python eval/build_cases.py
python eval/run_eval.py --coverage-only
```

This updates:

- `eval/golden_set_cp3.json`
- `eval/input_grid.csv`
- `eval/coverage_gaps.json`

Review the Git diff before accepting generated changes. Do not modify expected labels merely to improve the score.

## 12. Run a live pilot or evaluation

The current free OpenRouter endpoint states that prompts may be logged for service improvement. Use only synthetic inputs unless the data policy explicitly permits the selected provider.

Run the synthetic pilot:

```powershell
python eval/run_eval.py --pilot
```

Run the 22-case measured set only after confirming that sending those adapted cases is allowed:

```powershell
python eval/run_eval.py
```

Results appear in `eval/latest_pilot.*`, `eval/latest_run.*`, and ignored timestamped private runs. Infrastructure errors are reported as blocked cases, not counted as correct `UNCERTAIN` predictions.

## 13. Inspect traces without exposing credentials

Every request creates a file under:

```text
eval\private-traces\<trace_id>.json
```

Open the result panel in the browser to find its `trace_id`, then find the matching file in VS Code. It contains the sanitized request, raw provider response, parsed decision, latency, model, and provider response ID.

The trace directory is Git-ignored. Redaction handles common secret patterns but is not a universal privacy filter. Read a trace before sharing it and never publish the entire directory.

## 14. Use the console version

For a terminal-only demonstration:

```powershell
python bot/main.py
```

Type a question and press Enter. Type `/quit` to exit. The console imports the same classifier as the web prototype; it is not a separate model implementation.

## 15. Common errors

### The page says the key is missing

- Confirm `.env` is in the repository root.
- Confirm `LLM_PROVIDER=openrouter`.
- Confirm `OPENROUTER_API_KEY=` has a value.
- Restart the server and refresh the page.

### `provider_http_401`

The key is invalid, revoked, or belongs to a different provider. Create/check the key in OpenRouter and update only `.env`.

### `provider_http_429`

The free endpoint is rate-limited or at capacity. Wait and try one synthetic request again. Do not loop rapidly.

### `provider_http_404` or `provider_http_503`

The exact free model route may be unavailable. Check the model ID spelling and OpenRouter model status. The application intentionally does not silently switch to another model.

### `provider_not_completed`

The output was interrupted or truncated. Inspect its private trace. Retry once after capacity stabilizes.

### `missing_structured_output_or_refusal` or `unexpected_tool_call`

The model did not return the required `classify_context` tool call. The application safely returns `UNCERTAIN` and sends no student reply.

### Browser cannot connect

- Confirm the terminal still shows the running server.
- Use exactly `http://127.0.0.1:8765`.
- Check for a Python traceback in the terminal.
- Stop and restart the server.

### Changes do not appear

- Save the file with `Ctrl+S`.
- HTML change: refresh with `Ctrl+R`; use `Ctrl+F5` if cached.
- Python change: stop and restart the server.
- `.env` change: requests reload the file, but restart and refresh to make the visible status unambiguous.

## 16. Before committing code

Run:

```powershell
python -m unittest discover -s tests -v
git status --short
git diff --check
git diff
```

Confirm that `.env`, private traces, API keys, raw data packs, and personal information are absent from the staged files. A safe status check should never list `.env`.

## Quick daily workflow

1. Open `D:\vin_AI20K\K4-3B-E402-Capitalism` in VS Code.
2. Check `.env` provider/model without revealing the key.
3. Run `python -m codebase.server`.
4. Open `http://127.0.0.1:8765`.
5. Test with synthetic input.
6. Edit `index.html` for UI or `agent.py` for AI behavior.
7. Save; restart for Python changes.
8. Run all 30 tests.
9. Inspect the trace and Git diff before sharing or committing.
