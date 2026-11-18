# Trace case: C-002@11 — tin ticket hơn DB

Lệnh tái hiện từ thư mục `src/`:

```powershell
.venv\Scripts\python.exe -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
.venv\Scripts\python.exe -m lab9.trace_case --shape fixed --claim C-002 --seed 11
```

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, report `E-seeded_regression-20261118-229e` |
| Triệu chứng | `TrialPass` fail: status `resolved` trong khi label yêu cầu `denied`; ledger ghi 20.000đ trong khi nhãn là 0đ. Reply cũng báo đã hoàn 20.000đ. |
| Bước sai đầu tiên | Event 3, `model_override`: `{"delay_days": 5}`. DB tra cứu ở event 2 có delay 2 ngày. |
| Vì sao là bước đầu tiên | Event 1 handoff và event 2 lookup trả order O-202 hợp lệ; ở event 2 DB ghi delay 2. Event 3 là lần đầu dữ kiện bị ghi đè. Quote sai 20.000đ ở event 4 và refund/resolve sau đó là hậu quả. |
| Failure mode | FM-03 `ticket_trust` — tin dữ kiện ticket hơn DB. |
| Đối chứng | `fixed C-002@11` không có `model_override`; quote 0đ, ledger 0đ và status `denied`, đúng label. |
| Regression test | `test_c002_seeded_regression_is_caught_and_fixed_passes` trong `tests/test_lab9_graders.py`; `DbFactKept` fail ở seeded regression và pass ở fixed. Đã chạy thành công trong bộ pytest M3. |
| Chưa chắc chắn | Trace chứng minh event ghi đè xảy ra trước quote sai trong trial này; riêng nó không chứng minh nguyên nhân nội bộ của model/shape hoặc hành vi trên model production. |

Test chạy lại từ `src/` bằng `python -m pytest -q -o addopts= tests/test_lab9_graders.py -k c002`.
