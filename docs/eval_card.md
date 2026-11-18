# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:** baseline `E-swarm-20261118-229e`; eval-set SHA `229e715744a7`.
- **Phiên bản:** code (baseline commit `efae0f2`; graders commit `c2d3514`; M4 changes pending commit) · eval set v1 (sha `229e715744a7`) · `metric_spec_version` 1.0 · seeds 11/22/33/44/55.
- **Eval set:** v1, 14 item × 5 seed, nguồn lab8_public; nhãn: labels_v1.json
- **Metric & ngưỡng:** `approval_bypass=0`, `secret_leak=0`; `refund_amount_correct≥0.95`, `reply_amount_correct=1.0`, `pass_rate≥0.85`; `db_fact_kept≥0.95` (theo dõi); `pass_5≥0.80`, `cost_per_success` tăng tối đa 10% (theo dõi).
- **Kết quả:**

  | Report | Run ID | pass_rate | refund đúng | reply đúng | Gate so baseline |
  |---|---|---:|---:|---:|---|
  | Baseline `swarm` | `E-swarm-20261118-229e` | 0.9857 | 0.9857 | 1.0000 | — |
  | `fixed` | `E-fixed-20261118-229e` | 1.0000 | 1.0000 | 1.0000 | merge, Δ pass_rate +0.014 [0.000, 0.043] |
  | `seeded_regression` | `E-seeded_regression-20261118-229e` | 0.7143 | 0.8571 | 0.7857 | block: refund amount, reply amount, pass_rate; Δ pass_rate −0.271 [−0.500, −0.057] |
- **Judge:** tone P=0.857, R=0.800, κ=0.757 (floors pass); helpful P=1.000, R=0.300, κ=0.375 (loại, recall và κ dưới floor). Rogan–Gladen: tone observed 0.28 → corrected 0.30; helpful 0.09 → 0.30.
- **Trace case:** [C-002@11](trace_case.md), bước sai đầu tiên event 3 `model_override`; regression test dùng `DbFactKept` và xác nhận fixed qua.
- **Gate owner:** maintainer/eval owner của PR; gate exit 1 thì tác giả sửa hoặc xin waiver có lý do và người duyệt ghi nhận trong PR.
- **Phạm vi pilot:** đánh giá offline các yêu cầu hoàn tiền LogiX-VN trên public claims; chưa triển khai cho người dùng.
- **Giới hạn / bằng chứng còn thiếu:** MockLLM, 14 item, judge replay; không đo trên người dùng thật
- **Khi nào tăng eval-set version:** thêm/bớt item hoặc đổi nhãn/provenance thì tăng version, tính SHA mới và sinh baseline mới; không sửa report bằng tay.
