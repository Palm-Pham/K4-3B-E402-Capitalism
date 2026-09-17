# Canvas CP1: Trợ lý Discord cho TA

| # | Dòng | Nội dung |
|---|---|---|
| 1 | **Track + đề** | Track B · Trợ lý Discord cho TA — Tự động sàng lọc câu hỏi thiếu ngữ cảnh và yêu cầu bổ sung thông tin. |
| 2 | **Job executor** | TA đang trực kênh hỏi đáp kỹ thuật (`#q-and-a`) trên Discord, vừa nhận được một tin nhắn báo lỗi từ sinh viên. |
| 3 | **Pain một câu** | TA đang trực kênh giải đáp, gặp phải sinh viên hỏi lỗi nhưng không cung cấp log hoặc hình ảnh code; TA tốn thời gian gõ thủ công để hỏi lại thông tin, làm gián đoạn mạch làm việc và khiến sinh viên khác phải chờ đợi lâu hơn. |
| 4 | **Bằng chứng đầu** | Phỏng vấn 1 TA, các học viên lv 2-3 cap màn hình và hỏi các lỗi trên terminal, các câu hỏi về môi trường, bug, trace back.... cần AI có thể trả lời nhanh, hỏi lại học viên để bổ sung thông tin để đủ context |
| 5 | **Lát cắt MỘT CÂU** | Sinh viên gõ câu hỏi báo lỗi vào kênh chung · TA cần vào hỗ trợ · AI tự động đọc tin nhắn/ hình ảnh để quyết định xem câu hỏi đã đủ thông tin (có log/code/context) hay chưa · nếu thiếu, AI tự động reply nhắc sinh viên bổ sung theo template; nếu đủ, AI không can thiệp để TA vào xử lý. |
| 6 | **AI tự làm đến đâu** | *Tự làm:* Phân loại tin nhắn có đủ context không và bot-reply xin thêm log. *Không tự làm:* Không tự động trả lời kiến thức kỹ thuật thay TA. *Lý do:* Sinh viên cung cấp thiếu context thì AI cũng dễ "hallucinate" sinh ra đáp án sai, làm sinh viên đi sai hướng; TA vẫn phải là người chốt đáp án cuối cùng.<br>**Willing users:** `[Bùi Quốc Việt]`, `[Văn Thành Huy]`, `[Nguyễn Đức Đông]`. |
| 7 | **Phân công có tên** | `[Phạm Đình Bảo Khôi]` — phụ trách xử lý data pack, mining bằng chứng & prompt thiết lập tiêu chí "đủ context" · `[Phạm Thị Thùy Linh]` — làm bot Discord, backend gọi model AI · `[Nguyễn Thị Lê Na]` — tạo golden set, chạy test (eval) · `[Nguyễn Thùy Linh]` — spec, demo · `[Hoài Lam]` — user test với các TA, lấy feedback. |
