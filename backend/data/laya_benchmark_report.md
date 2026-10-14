# Báo Cáo Đo Lường Tốc Độ Phản Hồi Model Laya RL Agent (System 1)
*Thời gian thực hiện: 2026-10-12 23:29:43*
## 1. Bảng Tổng Hợp Chi Tiết (Benchmark Matrix)
| Kịch bản (Scenario) | C | Mẫu | Trung bình (ms) | Median P50 (ms) | P90 (ms) | Server Time (ms) | RPS | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `01_Laya_Warm_SteadyState` | 1 | 5 | 80.2 | 41.1 | 236.2 | 76.7 | 12.46 | 100% |
| `02_Len_Headline (~15 words)` | 1 | 3 | 40.3 | 40.5 | 40.7 | 36.8 | 24.74 | 100% |
| `02_Len_Abstract (~70 words)` | 1 | 3 | 43.3 | 43.5 | 43.6 | 39.6 | 23.02 | 100% |
| `02_Len_Article (~250 words)` | 1 | 3 | 53.2 | 52.8 | 55.0 | 49.5 | 18.76 | 100% |
| `03_Q_Single_Choice (1 Q)` | 1 | 3 | 46.8 | 35.5 | 71.6 | 43.7 | 21.35 | 100% |
| `03_Q_Two_Choices (2 Qs)` | 1 | 3 | 42.4 | 42.4 | 42.9 | 38.9 | 23.52 | 100% |
| `03_Q_Three_Hybrid (3 Qs)` | 1 | 3 | 68.9 | 49.8 | 107.9 | 65.7 | 14.49 | 100% |
| `04_Concurrency_C=1` | 1 | 5 | 42.5 | 42.2 | 43.7 | 39.2 | 23.50 | 100% |
| `04_Concurrency_C=2` | 2 | 5 | 74.7 | 81.7 | 85.5 | 39.8 | 24.14 | 100% |
| `04_Concurrency_C=4` | 4 | 5 | 113.4 | 122.6 | 161.4 | 38.4 | 24.96 | 100% |
| `05_Spider_Radar_RealWorld (8 Feeds)` | 1 | 8 | 46.9 | 42.7 | 80.0 | 43.6 | 21.28 | 100% |
| `06_Reuters_News_Articles (3 Links)` | 1 | 3 | 177.1 | 205.5 | 205.7 | 173.6 | 5.64 | 100% |

## 2. Nhận Xét & So Sánh Kỹ Thuật
- **Tốc độ Steady-State:** Laya đạt độ trễ ổn định ~350-380ms trong môi trường Docker CPU.
- **Phân loại Ngôn ngữ:** Tích hợp bộ định tuyến `convaiinnovations/laya/multilingual`, tự động nhận diện tiếng Việt và ký tự Latin.
- **Đồng bộ Con Nhện:** Thời gian ~360ms hoàn toàn nằm dưới ngưỡng Pacing Delay 400ms của Con Nhện trên Frontend.
