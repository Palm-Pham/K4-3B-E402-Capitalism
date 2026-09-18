# CP3 pilot — 20260918T082705Z

Nhãn hiện là bản nháp, chưa có hai thành viên chấm độc lập.

| Chỉ số | Kết quả |
|---|---|
| Case thử | 12 |
| Model hoàn tất | 0 |
| Đạt | 0 |
| Sai | 0 |
| Bị chặn / lỗi hạ tầng | 12 |
| Tỷ lệ đạt trên model hoàn tất | N/A — chưa đo |

## Phân tích từng case

| Case | Kết quả | Nguyên nhân |
|---|---|
| PILOT-01 | BLOCKED | missing_api_key |
| PILOT-02 | BLOCKED | missing_api_key |
| PILOT-03 | BLOCKED | missing_api_key |
| PILOT-04 | BLOCKED | missing_api_key |
| PILOT-05 | BLOCKED | missing_api_key |
| PILOT-06 | BLOCKED | missing_api_key |
| PILOT-07 | BLOCKED | missing_api_key |
| PILOT-08 | BLOCKED | missing_api_key |
| PILOT-09 | BLOCKED | missing_api_key |
| PILOT-10 | BLOCKED | missing_api_key |
| PILOT-11 | BLOCKED | missing_api_key |
| PILOT-12 | BLOCKED | missing_api_key |

## Giới hạn

Không tính fallback UNCERTAIN do lỗi API là dự đoán đúng. Unit test dùng test double không phải số đo AI. Chưa chấm độc lập, chưa có video gọi AI thật nếu model chưa hoàn tất. Case sai status: xem trace prompt/output; sai missing: đối chiếu thông tin đã có, trường cần thiết và nhãn TA. Không sửa nhãn để tăng điểm. Không suy ra chất lượng thực tế chỉ từ schema hợp lệ.