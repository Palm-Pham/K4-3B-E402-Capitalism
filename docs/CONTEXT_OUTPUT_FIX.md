# Why the short error report produced no reminder

## Evidence inspected

The screenshot input was `biến môi trường bị lỗi`. Its selected model was
`nvidia/nemotron-3.5-content-safety:free`, different from the model previously tested.
The trace `12d954f4d376420f9d635708c05244b1.json` contains OpenRouter's HTTP 404 error:
`No endpoints found that support tool use.` The request was rejected while filtering
providers for tool compatibility. It never produced a context classification.

A separate earlier trace, `f2730db875424bf48d8186037bca16a6.json`, used
`nvidia/nemotron-3-ultra-550b-a55b:free`. It classified a similar report as
MISSING_CONTEXT but put `problem_description` in both `missing` and `evidence`.
The Python validator rejected that contradiction as `ungrounded_evidence`.

Both failures kept the initial safe state `UNCERTAIN / NO_AUTO_REPLY / reply=null`.
The browser then displayed `Không gửi lời nhắc. TA tiếp tục xử lý.` for any null reply,
including API failures. That generic display hid the distinction between a valid
decision to stay silent and a request that could not be classified.

## Changes

| Location | Before | After |
|---|---|---|
| `.env`, `OPENROUTER_MODEL` | Content-safety model rejected tool requests | Restored previously requested Nemotron 3 Ultra free model |
| `codebase/agent.py`, `SYSTEM` | Generic missing-context instructions | Explicit guidance for short technical error reports, disjoint present/missing fields, and function-call output |
| `codebase/agent.py`, `PROMPT_VERSION` | `cp3-v1` | `cp3-v2-vague-error-context` for trace comparison |
| `codebase/agent.py`, `render_reply()` | General request for missing fields | Explicit “Thiếu ngữ cảnh” plus a fill-in template for the selected missing fields |
| `codebase/agent.py`, `error_message()` and exception handling | Machine-readable error only | Safe explanation of model/tool incompatibility, validation failures and common API errors |
| `codebase/index.html`, result rendering | Any null reply displayed as TA handoff | API errors display their cause; only valid silent decisions display the TA handoff text |
| `codebase/index.html`, health text | Key presence could imply model readiness | States that a key was found but model access has not been verified |
| `tests/test_context_regression.py` | No targeted regressions for this report | Tests template, word limit, recorded contradiction and unsupported tool routing |

No API error is converted into a fabricated MISSING_CONTEXT result. The central decision
still comes from a real model response and passes the existing schema/evidence checks.
The template requests only fields the model identified as missing, rather than asking
again for every field regardless of what the student already provided.

## Expected successful response

For a vague environment-variable error report, the reply now starts:

```text
Thiếu ngữ cảnh. Vui lòng cung cấp thông tin lỗi theo mẫu dưới đây:

- Thông báo lỗi hoặc traceback (đã che thông tin riêng tư).
  [Điền thông tin tại đây]
- Lệnh hoặc các bước ngay trước khi xảy ra lỗi.
  [Điền thông tin tại đây]
- Môi trường liên quan: hệ điều hành, công cụ và phiên bản.
  [Điền thông tin tại đây]
```

The exact missing fields can vary with supplied context. A provider outage or invalid
model response is still shown as an error, not claimed as a successful AI classification.

## Verification

- All 34 software tests passed, including the original contradictory model response and HTTP 404 tool mismatch.
- A real request for `biến môi trường bị lỗi` with the final prompt completed in 13.633 seconds:
  MISSING_CONTEXT / ASK_FOR_CONTEXT; missing error_log, reproduction and environment.
- Trace: `eval/private-traces/479cad62c9624a7ab4a112013c50719e.json`.
- Summary: `eval/context_fix_verification.json`.
- An intermediate prompt produced malformed text rather than a tool call, and a separate earlier request was stopped after waiting over two minutes. These are not counted as passing runs. The final prompt explicitly requires the named tool call.
- One successful live regression is evidence that this input now works; it does not establish reliability of every free-endpoint request or golden-set accuracy.
