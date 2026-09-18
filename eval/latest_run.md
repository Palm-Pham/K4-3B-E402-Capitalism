# CP3 run — 20260918T082705Z

Nhãn hiện là bản nháp, chưa có hai thành viên chấm độc lập.

| Chỉ số | Kết quả |
|---|---|
| Case thử | 22 |
| Model hoàn tất | 0 |
| Đạt | 0 |
| Sai | 0 |
| Bị chặn / lỗi hạ tầng | 22 |
| Tỷ lệ đạt trên model hoàn tất | N/A — chưa đo |

## Phân tích từng case

| Case | Kết quả | Nguyên nhân |
|---|---|
| CP3-01 | BLOCKED | missing_api_key |
| CP3-02 | BLOCKED | missing_api_key |
| CP3-03 | BLOCKED | missing_api_key |
| CP3-04 | BLOCKED | missing_api_key |
| CP3-05 | BLOCKED | missing_api_key |
| CP3-06 | BLOCKED | missing_api_key |
| CP3-07 | BLOCKED | missing_api_key |
| CP3-08 | BLOCKED | missing_api_key |
| CP3-09 | BLOCKED | missing_api_key |
| CP3-10 | BLOCKED | missing_api_key |
| CP3-11 | BLOCKED | missing_api_key |
| CP3-12 | BLOCKED | missing_api_key |
| CP3-13 | BLOCKED | missing_api_key |
| CP3-14 | BLOCKED | missing_api_key |
| CP3-15 | BLOCKED | missing_api_key |
| CP3-16 | BLOCKED | missing_api_key |
| CP3-17 | BLOCKED | missing_api_key |
| CP3-18 | BLOCKED | missing_api_key |
| CP3-19 | BLOCKED | missing_api_key |
| CP3-20 | BLOCKED | missing_api_key |
| CP3-21 | BLOCKED | missing_api_key |
| CP3-22 | BLOCKED | missing_api_key |

## Giới hạn

Không tính fallback UNCERTAIN do lỗi API là dự đoán đúng. Unit test dùng test double không phải số đo AI. Chưa chấm độc lập, chưa có video gọi AI thật nếu model chưa hoàn tất. Case sai status: xem trace prompt/output; sai missing: đối chiếu thông tin đã có, trường cần thiết và nhãn TA. Không sửa nhãn để tăng điểm. Không suy ra chất lượng thực tế chỉ từ schema hợp lệ.