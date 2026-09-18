# Software verification — 2026-09-18

- 22 Python unit tests passed (`python -m unittest discover -s tests -v`). Test doubles were used to exercise model-response handling; this is **not AI accuracy**.
- Checks include grounded evidence, malformed/refused/incomplete provider output, missing credentials, timeouts, three-field limit, fixed templates, secret redaction before transmission, safe trace-write failure, and excluding infrastructure failures from model accuracy.
- 12 source IDs were verified against the original local Discord pack, including original attachment counts; see `provenance_audit.json`.
- 22 candidate cases: 10 common, 8 hard, 4 rare. At least two cases cover each of the four difficult layers; see `input_grid.csv` and `coverage_gaps.json`.
- Browser interaction tested: entered a synthetic debugging question, submitted it, and observed `missing_api_key`, `Chưa gọi API`, no student reply, and a trace identifier. No successful model call was claimed.
- Initial sandbox test failures were caused by denied access to Windows temporary folders. The same unmodified tests passed after an authorized run outside the sandbox.

Pending: API-backed pilot and evaluation, human label review, two independent reviewers, live 30-second recording. Live Discord and vision are not implemented in this local text prototype.
