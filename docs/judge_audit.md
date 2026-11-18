# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng giới hạn cho kiểm tra tone; không dùng chấm tiền/chính sách. |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại khỏi gate; recall thấp, bỏ sót nhiều reply sai. |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người | “em … nha” quá suồng sã với khách; judge nhầm thân thiện là phù hợp. Bổ sung ví dụ về xưng hô vào rubric. |
| 2 | H-017 | PASS | FAIL | Người | “bạn ơi” không phù hợp với khách lớn tuổi; thêm kiểm tra xưng hô theo ngữ cảnh. |
| 3 | H-029 | PASS | FAIL | Người | “không cần nhắn thêm” mang giọng ra lệnh; rubric cần phân biệt lời hướng dẫn với lời áp đặt. |
| 4 | H-042 | FAIL | PASS | Người | Câu ngắn vẫn đủ số tiền và thời gian; không bắt buộc lời xin lỗi ở mọi reply. |
| 5 | H-051 | FAIL | PASS | Người | “refund” được LogiX cho phép; không phạt từ tiếng Anh này nếu nội dung rõ và đúng. |

## Kết luận
- `tone_ok` đạt cả ba floor. Ma trận nhầm lẫn: TP=24, FP=4, FN=6, TN=66. Tỉ lệ fail quan sát là 0.280; Rogan–Gladen hiệu chỉnh thành 0.300 với sensitivity 0.800 và specificity 66/70. Chỉ dùng cho tone, có audit mẫu; tiền và approval vẫn do code chấm.
- `helpful` bị loại làm gate: TP=9, FP=0, FN=21, TN=70. Precision 1.000 nhưng recall 0.300, κ=0.375; judge bỏ sót 21/30 lỗi theo nhãn người. Tỉ lệ fail quan sát 0.090 hiệu chỉnh thành 0.300 với sensitivity 0.300 và specificity 1.000. Precision cao không bù được recall dưới floor.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
