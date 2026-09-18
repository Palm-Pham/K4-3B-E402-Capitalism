# Project Context — Discord TA Assistant

Tôi đang làm **Checkpoint 2 (CP2)** cho project:

**Track B · Trợ lý Discord cho TA — Tự động sàng lọc câu hỏi thiếu ngữ cảnh và yêu cầu bổ sung thông tin.**

## 1. Bối cảnh bài toán

TA đang trực kênh hỏi đáp kỹ thuật `#q-and-a` trên Discord.

Pain chính:

Sinh viên thường gửi câu hỏi kỹ thuật nhưng thiếu:

* error log / traceback
* đoạn code liên quan
* lệnh hoặc bước tái hiện lỗi
* environment
* expected behavior
* actual behavior

TA phải hỏi lại thủ công, làm gián đoạn flow hỗ trợ và khiến các sinh viên khác phải chờ lâu hơn.

Bằng chứng ban đầu:

* Đã phỏng vấn ít nhất 1 TA.
* Các học viên level 2–3 thường chụp màn hình terminal hoặc hỏi lỗi về environment, bug, traceback.
* Nhu cầu là AI giúp sàng lọc nhanh và yêu cầu bổ sung context trước khi TA vào xử lý.

## 2. Lát cắt sản phẩm

Flow chính:

```text
Student gửi message / ảnh
        ↓
Discord bot nhận message
        ↓
Context checker
        ↓
Phân loại:
MISSING_CONTEXT
ENOUGH_CONTEXT
OUT_OF_SCOPE
UNCERTAIN
        ↓
Action
```

Quy tắc:

### `MISSING_CONTEXT`

Bot tự động hỏi sinh viên bổ sung đúng phần còn thiếu.

### `ENOUGH_CONTEXT`

Bot không reply, để TA xử lý.

### `OUT_OF_SCOPE`

Bot không reply.

Ví dụ:

* câu hỏi deadline
* phòng học
* câu hỏi kiến thức thuần lý thuyết

### `UNCERTAIN`

Bot không auto-reply.

Nguyên tắc:

* Khi không chắc, ưu tiên không can thiệp.
* Không để AI đoán hoặc spam sinh viên.

---

# 3. AI được làm và không được làm

## AI được làm

* Detect xem câu hỏi kỹ thuật có đủ context hay không.
* Xác định missing fields.
* Reply yêu cầu sinh viên bổ sung context.

## AI không được làm

* Không tự giải bug.
* Không trả lời kỹ thuật thay TA.
* Không tự kết luận nguyên nhân lỗi.
* Không xử lý general assistant / logistics.
* Không auto-reply khi confidence thấp.

Lý do:

Nếu context thiếu mà AI vẫn cố giải bug thì nguy cơ hallucination cao. TA vẫn là người đưa ra hướng giải quyết cuối cùng.

---

# 4. Context fields hiện tại

Các field đang xét:

```text
problem_description
error_log
relevant_code
reproduction
environment
expected_behavior
actual_behavior
```

Không yêu cầu tất cả field cho mọi câu hỏi.

Requirement phụ thuộc loại câu hỏi.

Ví dụ:

## Runtime / Error

Ưu tiên:

```text
problem_description
error_log
reproduction hoặc relevant_code
```

## Environment / Installation

Ưu tiên:

```text
problem_description
environment
installation_command
error_log
```

## Code behavior

Ưu tiên:

```text
relevant_code
expected_behavior
actual_behavior
```

---

# 5. Decision contract

Output chuẩn của classifier:

```json
{
  "status": "MISSING_CONTEXT",
  "missing": [
    "error_log",
    "relevant_code",
    "environment"
  ],
  "action": "ASK_FOR_CONTEXT"
}
```

Case đủ context:

```json
{
  "status": "ENOUGH_CONTEXT",
  "missing": [],
  "action": "PASS_TO_TA"
}
```

Case ngoài scope:

```json
{
  "status": "OUT_OF_SCOPE",
  "missing": [],
  "action": "NO_AUTO_REPLY"
}
```

Case không chắc:

```json
{
  "status": "UNCERTAIN",
  "missing": [
    "expected_behavior"
  ],
  "action": "NO_AUTO_REPLY"
}
```

Bot reply nên được tạo từ template trong code, không để LLM tự generate hoàn toàn.

Kiến trúc mong muốn:

```text
AI/classifier
    ↓
status + missing fields
    ↓
template code
    ↓
Discord reply
```

---

# 6. Ví dụ hành vi mong muốn

## Case 1 — thiếu context

Input:

```text
Anh ơi code em lỗi rồi, xem giúp em với ạ.
```

Expected:

```text
MISSING_CONTEXT
```

Missing:

```text
error_log
relevant_code
environment
```

Bot reply yêu cầu bổ sung.

---

## Case 2 — có error nhưng vẫn thiếu

Input:

```text
Em bị lỗi ModuleNotFoundError: No module named 'google'.
```

Expected:

```text
MISSING_CONTEXT
```

Missing:

```text
reproduction
environment
```

Bot không được hỏi lại error log vì student đã cung cấp.

---

## Case 3 — đủ context

Input:

```text
Em dùng Windows 11, PowerShell, đã activate .venv.

Em chạy:
pip install google-genai

Sau đó chạy:
python chatbot.py

Lỗi:
ModuleNotFoundError: No module named 'google'
```

Expected:

```text
ENOUGH_CONTEXT
```

Action:

```text
PASS_TO_TA
```

Bot không reply.

---

## Case 4 — ngoài scope

Input:

```text
Deadline assignment 2 là mấy giờ vậy mọi người?
```

Expected:

```text
OUT_OF_SCOPE
```

Bot không reply.

---

## Case 5 — ambiguous

Input:

```text
Em train model được accuracy 52%, có phải code của em bị lỗi không ạ?
```

Expected:

```text
UNCERTAIN
```

Bot không auto-reply.

---

# 7. CP2 requirement

CP2 chưa cần bot production hoàn chỉnh.

Mục tiêu chính:

```text
Student message
→ context checker
→ status
→ reply/pass
```

CP2 được phép dùng:

* mock data
* rule-based classifier
* hard-coded logic

CP3 mới thay phần quyết định trung tâm bằng AI call thật.

CP2 cần demo ít nhất 4 đường:

1. Missing toàn bộ context
2. Có một phần context nhưng vẫn thiếu
3. Enough context
4. Out-of-scope hoặc uncertain

---

# 8. Phân công nhóm

## Phạm Đình Bảo Khôi

Phụ trách:

* data pack
* mining evidence
* sample messages
* annotated samples
* định nghĩa “đủ context”
* prompt/context criteria

Việc CP2:

* đọc khoảng 30–50 message
* tìm pattern
* annotate data
* thống kê các missing fields phổ biến

---

## Phạm Thị Thùy Linh

Phụ trách:

* Discord bot
* backend
* classifier integration

CP2:

* bot nhận message
* gọi mock classifier
* nếu missing → reply
* nếu enough/out-of-scope/uncertain → không reply

CP3:

* thay mock classifier bằng AI call thật

---

## Nguyễn Thị Lê Na

Phụ trách:

* golden set
* evaluation

CP2:

* tạo `eval/golden_set.json`
* tạo `eval/test_golden_set.py`
* bắt đầu với ≥20 test cases

Golden set cần có:

* normal cases
* hard cases
* edge cases
* image cases
* out-of-scope
* uncertain

Trước CP3/CP4 phải có ít nhất 10 case lấy hoặc phát triển từ chatlog thật đã ẩn danh.

---

## Nguyễn Thùy Linh

Phụ trách:

* spec
* system flow
* demo

Các file:

* `spec.md`
* `docs/flow.md`
* `docs/cp2-demo.md`

---

## Hoài Lam

Phụ trách:

* user test với TA
* lấy feedback

Không hỏi kiểu:

```text
Anh/chị có thích bot này không?
```

Nên hỏi:

```text
Lần gần nhất bạn gặp sinh viên gửi câu hỏi thiếu context là khi nào?
Bạn phải hỏi lại gì?
```

Sau đó cho TA thử prototype và ghi:

* hành vi
* quote
* issue
* severity

---

# 9. Repo hiện tại

Repo mẫu đang dùng:

```text
discord-ta-assistant-cp2/
│
├── README.md
├── spec.md
├── .gitignore
│
├── bot/
│   ├── main.py
│   ├── classifier.py
│   └── templates.py
│
├── data/
│   ├── sample_messages.json
│   └── annotated_samples.json
│
├── eval/
│   ├── golden_set.json
│   └── test_golden_set.py
│
├── docs/
│   ├── flow.md
│   ├── cp2-demo.md
│   ├── team-checklist.md
│   ├── evidence-mining.md
│   ├── risk-scenarios.md
│   └── impact-table.md
│
└── validation/
    └── feedback_log.md
```

---

# 10. Data hiện tại

Đã tạo:

```text
data/sample_messages.json
```

với khoảng 30 sample messages.

Các loại case bao gồm:

* Python runtime error
* installation/environment
* API error
* image/screenshot
* ML training
* SQL
* Git
* Jupyter
* logistics
* concept questions
* ambiguous questions

Đã tạo:

```text
data/annotated_samples.json
```

Mỗi sample có annotation:

```json
{
  "status": "MISSING_CONTEXT",
  "missing": [
    "error_log",
    "relevant_code",
    "environment"
  ],
  "action": "ASK_FOR_CONTEXT"
}
```

---

# 11. Golden set hiện tại

File:

```text
eval/golden_set.json
```

Có 20 test cases.

Schema:

```json
{
  "id": "case_001",
  "source_message_id": "msg_001",
  "source_type": "mock_cp2_replace_with_real_chatlog_when_available",
  "category": "runtime_error",
  "difficulty": "easy",
  "input": {
    "message": "...",
    "attachments": []
  },
  "expected": {
    "status": "MISSING_CONTEXT",
    "missing": [],
    "action": "ASK_FOR_CONTEXT"
  },
  "reason": "..."
}
```

Hiện tại đây chủ yếu là mock cases.

Sau này cần thay/phát triển ít nhất 10 case từ chatlog thật.

---

# 12. Eval hiện tại

Chạy:

```bash
python eval/test_golden_set.py
```

Classifier CP2 đang rule-based.

Kết quả hiện tại:

```text
15/20 passed
75%
```

Đây là baseline mock, chưa phải performance của AI.

Một số failure hiện tại là có chủ đích để sau này:

* phân tích lỗi
* cải thiện classifier
* so sánh với AI ở CP3

Không được chỉ sửa golden label để tăng accuracy.

---

# 13. Mock classifier

File:

```text
bot/classifier.py
```

CP2 classifier dùng heuristic/rule:

* keyword detection
* error signal
* code signal
* environment signal
* out-of-scope signal
* uncertain signal

Flow:

```python
classify_context(message, attachments)
```

trả về:

```python
{
    "status": ...,
    "missing": [...],
    "action": ...
}
```

---

# 14. Template reply

File:

```text
bot/templates.py
```

Bot không để model tự viết reply tự do.

Ví dụ:

```text
Mình chưa thấy đủ thông tin để TA kiểm tra nhanh vấn đề này.
Bạn bổ sung giúp:

- error message / traceback
- đoạn code liên quan
- môi trường đang chạy

Bạn có thể dán log bằng code block hoặc gửi ảnh rõ nội dung lỗi.
```

---

# 15. CP2 demo

Chạy:

```bash
python bot/main.py
```

Sau đó nhập message student.

Ví dụ:

```text
Anh ơi code em lỗi rồi
```

Bot sẽ:

* classify
* tạo reply nếu missing
* in debug result

Khi đủ context:

```text
BOT: no auto reply
```

---

# 16. Success criteria đang đề xuất

Một prediction được xem là đúng khi:

1. `status` đúng.
2. Nếu `MISSING_CONTEXT`, bot chỉ hỏi phần thực sự thiếu.
3. Không hỏi lại dữ liệu student đã cung cấp.
4. `OUT_OF_SCOPE` không auto-reply.
5. `UNCERTAIN` không auto-reply.
6. Bot không giải kỹ thuật thay TA.

Quality bar đề xuất để nhóm chốt:

```text
≥85% status accuracy trên golden set
100% OUT_OF_SCOPE → NO_AUTO_REPLY
100% UNCERTAIN → NO_AUTO_REPLY
```

Đây mới là proposal, chưa phải evidence-based target cuối cùng.

---

# 17. Risk scenarios

Các case cần chú ý:

1. Student chỉ nói “code em lỗi”.
2. Có traceback nhưng không có code.
3. Có screenshot nhưng ảnh mờ/cắt mất lỗi.
4. Concept question.
5. Logistics question.
6. ML result bất thường nhưng chưa chắc là bug.
7. Student paste API key/token.
8. Bot đánh giá đủ nhưng TA vẫn phải hỏi lại.
9. Bot hỏi lại field student đã cung cấp.
10. Message có nhiều vấn đề cùng lúc.

Nguyên tắc quan trọng:

```text
When uncertain → NO_AUTO_REPLY
```

---

# 18. Evidence work còn phải làm

Mock data hiện tại không thay thế evidence thật.

Khôi cần:

* đọc 30–50 Discord messages thật
* định nghĩa rule trước
* đếm tỷ lệ câu hỏi thiếu context
* thống kê missing fields
* giữ ít nhất khoảng 5 ví dụ nguyên văn đã ẩn danh

Evidence summary nên có:

```text
Total messages read:
Technical debugging questions:
Missing-context questions:
TA had to ask follow-up:
Top missing fields:
```

---

# 19. User test còn phải làm

Hoài Lam cần test prototype với TA/willing users.

Willing users hiện tại:

```text
Bùi Quốc Việt
Văn Thành Huy
Nguyễn Đức Đông
```

Cần ghi:

* task
* observed behavior
* direct quote
* severity
* change decided

Không dùng feedback chung chung kiểu “ổn”, “hay”.

---

# 20. Nguyên tắc khi tiếp tục hỗ trợ project này

Khi tôi hỏi tiếp trong chat mới:

* Hãy giữ nguyên scope hẹp hiện tại.
* Không tự động mở rộng thành chatbot giải bug.
* Không thêm RAG/dashboard nếu chưa cần.
* Ưu tiên CP2 end-to-end flow trước.
* Nếu sửa code, giữ tương thích cấu trúc repo trên.
* Nếu tạo data/eval, dùng cùng schema.
* Nếu đề xuất AI ở CP3, classifier phải trả structured output theo decision contract.
* Khi đánh giá model, dùng golden set thay vì demo cảm tính.
* Phân biệt rõ mock data và evidence thật.
* Khi có ambiguity, ưu tiên `UNCERTAIN + NO_AUTO_REPLY`.

## Mục tiêu tiếp theo

Tiếp tục hoàn thiện CP2 theo thứ tự:

```text
1. Replace mock samples bằng chatlog thật đã ẩn danh
2. Review annotation
3. Review golden set
4. Nối mock classifier vào Discord bot thật
5. Chạy end-to-end demo
6. User test với TA
7. Ghi evidence + feedback
8. Chuẩn bị CP3 AI classifier
```
