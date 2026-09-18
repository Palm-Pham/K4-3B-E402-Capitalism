# §2 · THIẾT KẾ & SPEC *(CP1 → CP4 · spec.md chốt tại hạn chốt spec: 21:00 18/9, tại CP4)*

## 2.1 Các câu hỏi phải tự trả lời

1. Người khác đã giải bài này thế nào — mình học gì, né gì, khác gì?
2. AI nên **tự làm đến đâu** — và nếu nó sai thì ai chịu gì, sửa đắt hay rẻ?
3. Sản phẩm sẽ **hành xử thế nào khi sai / khi không chắc** — cụ thể nói gì, hiện gì, cho user làm gì tiếp?
4. **"Tốt" nghĩa là gì, đo bằng gì** — và bar của nhóm là bao nhiêu %?

## 2.2 Nghiên cứu giải pháp tương tự *(express — chia người, 15'/người)*

Mỗi thành viên dùng thử 1 sản phẩm gần giống (ChatGPT study mode · Khanmigo · NotebookLM · Duolingo · Quizlet AI...) và trả lời đúng 4 câu: ① họ giải job này bằng flow nào? ② một điều đáng học (quan sát cụ thể — "NotebookLM luôn cite nguồn cạnh câu trả lời", không phải "giao diện đẹp")? ③ một điều đáng né? ④ mình sẽ khác gì ở lát cắt này? → gom vào spec §3.

## 2.3 Chọn mức automation theo cost-of-error

| Mức | Khi nào đúng | Ví dụ trong khoá |
|---|---|---|
| **Augment** — AI gợi ý, người quyết | Sai thì đắt (kiến thức sai đến học viên, điểm số) | Quiz AI sinh, giảng viên duyệt từng câu |
| **Conditional** — AI tự làm case chắc, chuyển người case mơ hồ | Đa số case lành, số ít hiểm | Trợ lý trả lời khi có căn cứ trong tài liệu; không có → chuyển TA |
| **Automate** — AI tự làm | Sai thì rẻ, user tự thấy và sửa được | Sinh chapter/timestamp cho video |

Lý do trong spec viết theo cost-of-error: *sai thì ai chịu gì, sửa đắt hay rẻ* — không viết "vì tiện".

*Đọc thêm — PAIR chương 1.2 "Balance automation & augmentation"* (`further-reading/pair-guidebook-digest.md`): tự động hoá hợp khi việc vượt kỹ năng người dùng, lặp/chán, ít rủi ro; **tăng cường** hợp khi người dùng *thích* làm việc đó, *chịu trách nhiệm* hậu quả, hoặc nhu cầu mơ hồ/đối thoại. Hậu quả càng lớn càng cần người giám sát (automation complacency). Với AI sinh, PAIR 1.3 gợi ý viết ba câu vào spec: *"AI luôn phải {…}"* · *"AI không được {…} kể cả khi user vô tình yêu cầu"* · *"Nếu AI dự đoán yếu, user không phiền {sửa nhỏ} miễn là {điều kiện}"*.

## 2.4 Nguyên tắc HAX/PAIR — chọn ≥4, khai trong spec §4b, mỗi cái trỏ vào chỗ cụ thể

*(Đủ 18 nguyên tắc HAX kèm câu tự kiểm và ví dụ trong khoá: `further-reading/hax-guidelines.md`; PAIR theo chương: `further-reading/pair-guidebook-digest.md`. Bản gốc: microsoft.com/haxtoolkit · pair.withgoogle.com/guidebook. Mỗi nguyên tắc khai báo phải chỉ ra được vị trí áp dụng cụ thể trong prototype — TA kiểm tra tại CP4.)*

**Nhóm khởi đầu (chọn ≥1):**
- **G1 — Làm rõ hệ thống làm được gì.** Câu đầu tiên user thấy có nói đúng phạm vi không? (Tutor chào bằng cả đoạn văn — có ai đọc?)
- **G2 — Làm rõ nó làm tốt đến đâu.** User biết khi nào nên tin, khi nào nên kiểm lại? ("Trả lời dựa trên tài liệu buổi 2; ngoài tài liệu mình sẽ nói rõ.")

**Khi không chắc / khi sai (G10 bắt buộc + ≥1 trong G8/G9/G11):**
- **G10 — Thu hẹp phạm vi khi nghi ngờ.** Không chắc → hỏi lại một câu, hoặc trả lời kèm giới hạn — không làm liều.
- **G8 — Gạt bỏ dễ dàng.** User bỏ qua câu trả lời/gợi ý có dễ không, hay bị chặn flow?
- **G9 — Sửa dễ dàng.** User sửa/hỏi lại được ngay trên output không?
- **G11 — Giải thích vì sao.** "Vì đoạn bạn chọn ở trang 6 nói về X" — giải thích gắn với hành động tiếp theo.

**Nhóm nâng cao (tự chọn nếu hợp):** **G5** hợp chuẩn mực xã hội (giọng có hợp học viên VN gõ "cái chi dợ"?) · **G12** nhớ tương tác gần · **G13/G14** học từ hành vi, thay đổi thận trọng · **G15** mời feedback chi tiết (👍👎 kèm "sai chỗ nào?") · **G17** quyền kiểm soát tổng.

**PAIR — tra theo chương:** *Mental Models* (đặt kỳ vọng thấp hơn khả năng một chút, đừng ngược lại) · *Explainability + Trust* (tin đúng mức > tin tối đa — hiển thị căn cứ để user tự kiểm) · *Feedback + Control* (thu feedback ngay trong flow; user luôn bỏ qua AI được) · *Errors + Graceful Failure* (lỗi-do-giới-hạn ≠ lỗi-do-hiểu-nhầm-ngữ-cảnh — mỗi loại một đường lui).

## 2.5 Bốn lớp chỗ khó + kịch bản rủi ro *(≥8 kịch bản — TA soát tại CP4)*

Tự cụ thể hoá 4 lớp cho lát cắt của mình bằng 4 câu hỏi (đối chiếu với **bốn nguồn lỗi của PAIR chương 6**: lỗi dữ liệu/dự đoán · lỗi input & kỳ vọng · lỗi chất lượng/độ liên quan output · lỗi hệ thống nhiều tầng — `further-reading/pair-guidebook-digest.md` §6.2):
- ① **Nguồn sự thật** — chỗ nào AI bịa được? Không có căn cứ thì làm gì?
- ② **Mơ hồ / thiếu thông tin** — input không đủ chắc: hỏi lại, đoán có báo, hay từ chối?
- ③ **Ngoài phạm vi / thẩm quyền** — user sẽ đòi gì mà feature không được phép làm?
- ④ **Đặc thù domain** — sai cái gì thì học viên học sai kiến thức / mất điểm / mất niềm tin ngay?

Chạy **HAX Playbook** (github.com/microsoft/HAXPlaybook — trả lời bộ câu hỏi config → nhận kịch bản lỗi) → chốt ≥8 kịch bản, mỗi kịch bản một dòng: `tình huống cụ thể | lớp | hành vi mong muốn (nói gì, hiện gì, cho user làm gì tiếp) | nguyên tắc áp (G../PAIR)`. Tự kiểm: **kịch bản nào làm nhóm sợ nhất khi demo?** Chưa có cái nào đáng sợ = chưa đủ hiểm. Mỗi lớp phải có ≥2 case tương ứng trong golden set (§2.6).

## 2.6 Định nghĩa "tốt" + golden set + quality bar *(phải xong lượt đo đầu tại CP3)*

*Khung để chọn chiều chất lượng — PAIR 2.3 "Evolve AI with evaluation"*: Coverage (trả lời đủ mọi phần yêu cầu) · Relevance (đúng yêu cầu) · Diversity · Sensitivity (đổi input nhỏ, output đổi hợp lý) · Realism · **Factuality** (có căn cứ, không bịa) · Quality (mạch lạc). Chọn 2–3 chiều hợp lát cắt, mỗi chiều một định nghĩa kiểm chứng được; làm ngược từ *"đủ tốt" với người dùng là gì*. Chi tiết: `further-reading/pair-guidebook-digest.md` §2.3.

1. **Bắt đầu từ output thật, không từ tiêu chí trừu tượng.** Chạy tay 10-20 input qua prototype (hoặc ChatGPT/Claude với prompt nháp), đọc từng output, ghi thô: dùng được / sửa được / không chấp nhận được. Tiêu chí tốt được *chưng cất từ lỗi đã thấy*. *(Hamel Husain — "Your AI Product Needs Evals": "look at your data" là bước một; Anthropic docs — "Create strong empirical evaluations".)*
2. **Đặt tên cho lỗi.** Gom output tệ thành nhóm lỗi có tên (bịa nguồn / lạc trình độ / cite sai trang / đoán khi thiếu thông tin / vượt thẩm quyền...), đối chiếu 4 lớp để không sót. Mỗi lỗi: trigger → biểu hiện → hậu quả. *(HAX Playbook; Aman Khan — "Beyond vibe checks", Lenny's Newsletter.)*
3. **Biến mỗi chiều chất lượng thành định nghĩa kiểm chứng được.** "Trả lời tốt" không đo được. Tách chiều (đúng-có-căn-cứ / đúng cỡ-đúng giọng / an toàn), mỗi chiều: pass/fail ("mọi thông tin trace được về transcript") hoặc thang có mô tả mức (1 = sai kiến thức; 3 = đúng nhưng dài gấp đôi cần; 5 = đúng, đúng cỡ, có trích dẫn). *(HAX G2.)*
4. **Test độ rõ bằng người thứ hai.** Hai thành viên chấm độc lập cùng 5 output → so. Lệch = định nghĩa mơ hồ → viết lại; lệch từ ~20% số case trở lên (ví dụ khác nhau 2/5 case) thì định nghĩa chưa đủ rõ để dùng. Trong nhóm còn chấm khác nhau thì không dùng chấm được ai. *(Ngưỡng đồng thuật người chấm theo lab AI Evaluation — Day 21 khoá AI20k.)*
5. **Golden set ≥20 case nhóm tự xây**: ≥2 case cho mỗi lớp chỗ khó + 8-10 case thường + 2-4 case hiếm; trong đó **≥10 case lấy hoặc phát triển từ chatlog thật** (nhóm dùng promptfoo nên mở rộng lên 30+). Lưu file trong `eval/` và **chốt quality bar trước khi đo**: "Đạt khi ≥ __% qua bộ, và [điều kiện cứng]" — chốt tại hạn chốt spec của khoá và giữ nguyên sau đó. Không đạt quality bar nhưng phân tích được nguyên nhân vẫn được tính đủ điểm; số liệu bị chỉnh sửa sẽ không được tính. *(Bài giảng Ship/Limited/Hold.)*

6. **Phủ case bằng User Input Grid, không thêm case theo cảm giác.** Liệt kê 3-5 chiều mà đổi giá trị thì câu trả lời đúng phải đổi theo — ví dụ: ai hỏi · loại câu hỏi · mức thiếu/mơ hồ của input · sai thì đắt cỡ nào · hành vi mong đợi (trả lời / hỏi lại / từ chối). Mỗi case trong golden set gắn vào một tổ hợp chiều; ô trống = lỗ hổng coverage. Giữ một tổ hợp khi: có khả năng xảy ra thật · làm AI dễ sai · sai thì đắt · nhóm chưa chắc ranh giới. **Chia việc người–máy:** người thiết kế coverage và viết case từ chatlog; LLM chỉ paraphrase biến thể câu chữ — bộ case do LLM tự sinh nguyên khối thường đồng nhất, toàn happy path (50 dòng sinh tự động có khi chỉ tương đương 3 case thật).

*(Nguồn: bài giảng và lab AI Evaluation khoá AI20k — Day 19–21.)*

## 2.7 Trước CP4 tự soát

Spec đủ §1-§9 theo `03-ai-spec-template.md` · evidence đạt chuẩn A/B có log · bảng impact ≥3 ứng viên + ứng viên loại · ≥4 nguyên tắc có "áp vào đâu" · 4 lớp + ≥8 kịch bản · quality bar bằng % · kế hoạch cho LEC 6 + LAB 6 (ai validate, ai dry run). **Commit spec.md trước hạn chốt spec (21:00 18/9, tại CP4) — quality bar chốt từ thời điểm này.**

---