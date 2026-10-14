# 🕷️ Dự Án: SPIDER NEWS RADAR (Tin Tức Quanh Ta)
> **Ý tưởng:** Trực quan hóa tiến trình quét & phân tích tin tức kinh tế - chính trị bằng "Nhện Thảo Mộc SVG 2D Layered + GSAP" (Làm màu có cơ sở kỹ thuật, AI thật - Dữ liệu thật, phong cách Botanical Ink).

---

## 📌 1. Bối Cảnh & Mục Tiêu

### 1.1. Bóc tách hiện tượng "Con nhện AI" trên TikTok
* **Bản chất video TikTok:** Là hoạt họa 3D/CGI dàn dựng (Render concept bằng Blender/Sora/Kling), sử dụng các bài báo giả tưởng (như *"GPT-6 September 2026"*) và các tên gọi hư cấu (*Laya, Clef-Flash, Jev*).
* **AI thực tế:** Chạy song song trên tensor/GPU trong vài phần nghìn giây, không "bò cơ học" trên trang giấy.
* **Mục tiêu của dự án này:** 
  * Biến ý tưởng thị giác hấp dẫn đó thành **một ứng dụng hoạt động thật 100%**.
  * Con nhện đóng vai trò là **Interactive Visual Cursor (Avatar đại diện)**: Bò trúng các thực thể, chỉ số, từ khóa kinh tế/chính trị do AI backend trích xuất thật từ các nguồn tin tức (RSS).

---

## 🏛️ 2. Kiến Trúc Hybrid Hai Tầng AI (System 1 + System 2)

```
[ NGUỒN TIN ĐA DẠNG ]
  ├─ Báo chí Đa Quốc Gia: Reuters, Bloomberg, FT, Nikkei, CaféF, VnExpress...
  └─ GitHub Radar: GitHub Trending, Repositories, Release Notes, READMEs
             │
             ▼
[ 1. Data Ingestion & Sanitizer ] (Cào & làm sạch dữ liệu đa ngôn ngữ)
             │
             ▼
[ 2. TẦNG 1: DECISION 3.0 LITE (System 1 - Gatekeeper & Diệt Giật Tít Siêu Tốc) ]
   - Model: vllm-sr/d3-lite (Nền tảng Qwen 3.5 0.85B Multimodal)
   - Chạy trên Docker local GPU RTX 3050 (Port 8000, image vllm-sr/d3-serve:latest)
   - Tốc độ: 150ms – 200ms / bài trên NVIDIA GPU (giá trị đo được, hiển thị latency trung bình trong app; ăn ~1.8GB VRAM)
   - Native Context: 32K – 128K tokens (Đọc trọn vẹn bài báo dài hàng nghìn chữ, không sợ tràn hay cắt cụt context)
   - Nhiệm vụ: 
     * Phân loại đề tài & đo lường tâm lý thị trường (Sentiment)
     * Bộ lọc Hải quan diệt giật tít: Đối chiếu Tiêu đề vs Nội dung thật, loại 80% tin rác/PR giúp tiết kiệm 80% tiền LLM
     * Đa phương thức: Đọc được cả ảnh bìa, biểu đồ nến kỹ thuật, infographic tài chính
     * Cấp tọa độ từ khóa cho Con Nhện giăng tơ
             │
             ▼
[ 3. Nhện Visualizer & Hàng Đợi (Queue) ]
   - Nhện bò trên bài viết / README repo, đánh dấu từ khóa, giọt nước loang mực
             │
             ▼  (Khi người dùng Click vào tin lẻ HOẶC bấm "Tổng Hợp Toàn Bộ")
[ 4. TẦNG 2: LLM SYNTHESIZER (System 2 - Chuyên Gia Phân Tích & Dịch Thuật) ]
   - Công nghệ: Gemini Flash API (Context 1 Triệu tokens) hoặc Qwen 2.5 Local
   - Nhiệm vụ:
     * Dịch chuẩn xác sang tiếng Việt văn phong tài chính / công nghệ chuyên sâu.
     * Deep Dive: Giải thích tác động vĩ mô / chính trị của 1 tin được chọn.
     * Executive Digest: Nối kết toàn bộ danh sách tin đã lọc thành 1 báo cáo tổng quan.
     * GitHub Insight: Đọc README tóm tắt repo này giải quyết bài toán gì, tại sao hot.
```


---

## ⚡ 3. Giải Pháp Tối Ưu Tốc Độ & Tài Nguyên Phần Cứng

### 3.1. Sự chênh lệch nhịp điệu: Độ trễ AI vs Nhịp độ Thị giác (Visual Pacing)
* **Độ trễ suy luận System 1 (đo trên NVIDIA GPU, hiển thị latency trung bình trong app):**
  * **Laya RL Agent: 30ms – 60ms** / bài (single-pass tensor, tổng HTTP roundtrip < **70ms**).
  * **Decision 3.0 Lite: 150ms – 200ms** / bài (giá trị đo được trên NVIDIA GPU).
* **Nhịp độ thị giác của Con nhện (Pacing Delay):**
  * *Chế độ Laya/D3 Sync (Mặc định):* **400ms – 600ms** cho mỗi bước nhảy từ khóa (nhện phóng vụt siêu tốc theo nhịp sự kiện).
  * *Chế độ Chill Mode (Thư giãn):* **1000ms – 1500ms** cho mỗi bước (bò thong thả để người đọc kịp theo dõi).
* **Kết luận:** AI phản xạ nhanh hơn mắt người gấp nhiều lần. Do đó, Backend gom toàn bộ kết quả của Decision 3 đẩy xuống SSE Queue, Frontend tự điều phối nhịp độ nhảy của nhện để không bao giờ bị đơ giao diện.

### 3.2. Ba Kỹ Thuật Tối Ưu Bắt Buộc & Cơ Chế Chống Miss Từ

1. **Hàng Đợi Hoạt Ảnh Tự Tiêu Thụ Tách Rời (Client-Side FIFO Animation Queue & Consumer):**
   * **Bản chất kỹ thuật:** Tách rời hoàn toàn tốc độ nhận tin của mạng (SSE stream từ Backend, ~40ms - 200ms) với tốc độ chuyển động vật lý của con nhện (`400ms`).
   * **Quy trình hoạt động:** Khi SSE gửi sự kiện `SpiderEvent` về, Client lập tức đưa vào hàng đợi `animationQueue`. Con nhện ở vai trò là một Consumer độc lập, dùng `gsap.timeline({ onComplete: processNextEvent })` để lấy từng từ ra bò lần lượt.
   * **Cam kết kỹ thuật:** **100% không bao giờ bị miss từ hay giật hình**, vì sự kiện mới không bao giờ ghi đè lên chuyển động đang chạy dở; bước nhảy tiếp theo chỉ được kích hoạt khi bước nhảy trước đã kết thúc trọn vẹn.

2. **Bộ Điều Tốc Tự Động 3 Cấp Chống Ứ Đọng Hàng Đợi (3-Tier Adaptive Pacing Engine):**
   * Khi tin tức dồn về nhiều cùng lúc, hệ thống tự động co giãn thời gian tween chuyển động dựa trên độ dài hàng đợi (`queue.length`):
     - **Cấp 1 - Bình thường (`queue.length <= 4`):** Nhện giữ đúng nhịp thơ mộng chuẩn **`400ms`** (hoặc `1200ms` nếu bật Chill Mode).
     - **Cấp 2 - Tăng tốc Sprint (`5 <= queue.length <= 12`):** Nhện tự động rút ngắn duration còn **`180ms – 220ms`** / từ. Chân guồng nhanh, lướt vút qua các từ khóa cực kỳ kịch tính và dứt khoát.
     - **Cấp 3 - Xả lũ Fast-Forward (`queue.length > 12`):** Nhện chỉ bò qua **3 từ khóa then chốt nhất**; các từ khóa phụ còn lại tự động phát sáng loang màu bằng CSS; nhện phóng tơ kết thúc bài và lướt sang bài tiếp theo để giữ độ trễ thời gian thực.

3. **Prefetching (Quét ngầm bài tiếp theo):**
   * Trong lúc con nhện đang biểu diễn ở bài báo số 1, Backend đã ngầm phân tích bài báo số 2.
   * Khi nhện diễn xong bài 1 $\rightarrow$ Dữ liệu bài 2 đã sẵn sàng ngay lập tức (Zero Latency).

### 3.3. Kiến Trúc Đa Mô Hình System 1 (System 1 Multi-Engine: Laya vs Decision 3.0 vs Mock)
Hệ thống hỗ trợ linh hoạt cả hai mô hình tiên tiến nhất phục vụ System 1, chia sẻ cùng giao thức kết nối Wire Format (`/v1/systemone` với payload `state` và `questions`), cho phép người dùng tự do lựa chọn theo nhu cầu:

#### 1. Bảng So Sánh Hai Động Cơ System 1:
| Tiêu Chí | **Laya RL Agent (`laya-serve`)** | **Decision 3.0 Lite (`d3-serve`)** | **Mock Engine (Dev/Test)** |
| :--- | :--- | :--- | :--- |
| **Bản chất mô hình** | RL Decision Agent đa ngôn ngữ | Qwen 3.5 0.85B Multimodal | Bộ luật từ khóa nội bộ (In-Memory) |
| **Nền tảng thực thi** | Docker GPU NVIDIA CUDA (`RTX 3050`) | Docker GPU / CPU | Không cần Docker / 0% VRAM |
| **Độ trễ thực tế** | **30ms – 60ms** (Siêu tốc) | **150ms – 200ms** (NVIDIA GPU) | **0.5ms** |
| **Cổng mặc định** | `http://127.0.0.1:8000` | `http://127.0.0.1:8000` (hoặc `8002`) | `local://mock` |
| **Khả năng đa phương thức** | Văn bản, chỉ số, mã nguồn | Đọc cả ảnh bìa, biểu đồ nến, infographic | Văn bản cơ bản |
| **Trọng số Checkpoint** | Checkpoint hash `7b928d828b...` | Trọng số `.safetensors` vllm-sr | Không áp dụng |

#### 2. Cơ Chế Bật/Tắt Thủ Công Trên Duy Nhất Port 8000 (Không Chạy Song Song):
> **Nguyên tắc:** Hệ thống **TUYỆT ĐỐI KHÔNG CHẠY SONG SONG** cả hai container cùng lúc để tránh cạnh tranh VRAM GPU RTX 3050 và tránh xung đột cổng mạng. Người dùng hoàn toàn chủ động **bật/tắt thủ công** (Manual Toggle) mô hình mong muốn trên **duy nhất cổng `http://127.0.0.1:8000`**:

* **Kịch bản A: Khi muốn dùng Laya RL Agent (GPU CUDA 30-60ms):**
  - Trong Docker Desktop: Bấm nút **Play ▶** tại container `3085c6038321_laya-laya-serve-1` (hoặc chạy lệnh: `docker start 3085c6038321_laya-laya-serve-1`).
  - Đảm bảo container `d3-serve-1` đang TẮT (`Stop ⏹`).
* **Kịch bản B: Khi muốn dùng Decision 3.0 (vllm-sr/d3-serve):**
  - Tắt Laya: Bấm **Stop ⏹** tại container `3085c6038321_laya-laya-serve-1` (hoặc: `docker stop 3085c6038321_laya-laya-serve-1`).
  - Bật D3: Bấm nút **Play ▶** tại container `d3-serve-1` (hoặc: `docker start d3-serve-1`).
* **Kịch bản C: Khi TẮT CẢ HAI ĐỂ GIẢI PHÓNG VRAM / DEV OFFLINE:**
  - Tắt cả 2 container trong Docker Desktop.
  - Backend tự động kích hoạt **High-Fidelity Mock Engine (0ms)**: App vẫn mở mượt mà, con nhện vẫn bò và giăng tơ duyệt tin tức bình thường mà không bao giờ báo lỗi crash hay mất kết nối.

#### 3. Cơ Chế Tự Động Nhận Diện (Auto-Detect) Trong App & File Cấu Hình:
* **Cấu hình qua file `.env`:**
  ```env
  SYSTEM1_ENGINE=auto     # auto (mặc định - tự nhận diện container đang bật trên port 8000)
  SYSTEM1_BASE_URL=http://127.0.0.1:8000
  ```
* **Chọn trực tiếp trong Giao Diện App (Màn hình 6 - Settings / Control Center):**
  - Màn hình 6 cung cấp thẻ trạng thái System 1 trực quan:
    `[● Auto-Detect (Tự nhận diện container trên port 8000)]` `[○ Laya CUDA]` `[○ Decision 3.0]` `[○ Mock Mode]`.
   - Backend tự động ping `http://127.0.0.1:8000/health`. Nếu thấy Laya thì hiển thị nhãn *Laya RL Agent (CUDA 30-60ms)*; nếu thấy D3 thì hiển thị *Decision 3.0 (NVIDIA GPU 150-200ms)*; nếu tắt thì hiển thị *Mock Engine*.
  - Người dùng có thể click chọn cưỡng bức mô hình mong muốn, frontend gọi `POST /api/v1/system1/select` $\rightarrow$ lưu vào bảng `system_settings` trong SQLite.
* **Đo lường độ chính xác (Accuracy Benchmark):**
  - Cả hai mô hình đều dùng chung trọng số kiến trúc Decision 3.0 đa ngôn ngữ. Các bài test vừa qua chủ yếu đo tải và độ trễ phản hồi (Latency & Throughput).
  - Để so sánh độ chính xác khách quan (Accuracy %, F1-score), cần tập kiểm thử chuẩn 30 – 50 bài báo có gán nhãn thực tế (Head-to-head benchmark).


---

### 3.4. Cơ Chế Cào Tin 15 Phút/Lần & Cam Kết Không Bị Sót Tin (15-min Polling & Zero-Miss)

#### 1. Tính Khả Thi Của Chu Kỳ 15 Phút:
* Chu kỳ 15 phút là **chuẩn mực vàng (Industry Standard)** của các hệ thống News Aggregator toàn cầu (Google News, Bloomberg Wire, Feedly).
* Báo chí điện tử (CaféF, VnExpress, Tuổi Trẻ, Reuters) không ra tin dồn dập hàng trăm bài mỗi phút. Trung bình mỗi chuyên mục chỉ xuất bản 1–3 bài mới trong 15 phút.
* Mỗi tệp tin RSS XML chỉ nặng từ `30KB – 70KB` và chứa sẵn 20 – 50 bài gần nhất.
* Cào 15 nguồn tin cùng lúc qua `asyncio` tốn chưa đầy **1.2 giây mạng** và dưới **1MB dữ liệu**, hoàn toàn không gây chậm máy hay lag giao diện.

#### 2. Chiến Lược Đảm Bảo 100% Không Bị Bỏ Sót Tin:
1. **Cơ chế Catch-Up tức thì khi vừa mở App:** Ngay khi ứng dụng khởi động ở giây đầu tiên, hệ thống lập tức kích hoạt 1 lượt cào toàn diện ngay lập tức mà không cần đợi đủ 15 phút đầu tiên.
2. **Cổng bảo hiểm Google News RSS 24h:** Với các nguồn quốc tế biến động mạnh, hệ thống dùng cú pháp truy vấn thời gian thực của Google News:  
   `https://news.google.com/rss/search?q=when:24h+allinurl:{tên_miền}`  
   Cổng này lưu vết và trả về toàn bộ bài viết trong vòng 24 giờ của tờ báo đó, đảm bảo dù người dùng tắt máy cả đêm mở lại vẫn gom đủ 100% tin trong ngày.
3. **Khử trùng tuyệt đối bằng SHA-256 URL Hash:** URL gốc sau khi chuẩn hóa (cắt bỏ đuôi tracking `?utm_source=...`) được băm thành mã băm 64 ký tự. Chỉ bài viết có hash mới mới được ghi vào SQLite, ngăn chặn 100% việc trùng lặp hay cào lại bài cũ.

---

### 3.5. Chiến Lược Vượt Paywall Cho Các Hãng Thông Tấn Lớn (Bloomberg, FT, Reuters, WSJ, BBC...)

Hệ thống xử lý phân loại rõ ràng theo 3 nhóm rào cản kỹ thuật của các đầu báo quốc tế:

| Nhóm Báo Chí | Tên Báo Điển Hình | Đặc Điểm Kỹ Thuật | Phương Pháp Xử Lý Của Hệ Thống |
| :--- | :--- | :--- | :--- |
| **Nhóm Mở (Free/Open)** | The Guardian, BBC News, Politico, CaféF, VnExpress | RSS sạch, không paywall, không chặn bot | Cào trực tiếp 100% qua RSS chính thức và bóc tách toàn văn sạch. |
| **Nhóm Metered / Bot Detection** | Reuters, AP News, The New York Times, Washington Post | Bắt đăng ký tài khoản sau vài bài, kiểm tra User-Agent bot | Đi qua Google News RSS Gateway + đọc thẻ ngầm `<script type="application/ld+json">` (`articleBody`) theo Tầng 1 của §12.5. |
| **Nhóm Hard Paywall Gắt** | Bloomberg News, Financial Times, Wall Street Journal, The Economist | Khóa chặt sau paywall trả phí + Cloudflare / Akamai chống bot | Sử dụng kiến trúc 2 giai đoạn: **Quét nhện nhanh** vs **Đọc sâu toàn văn On-Demand**. |

#### Kiến Trúc 2 Giai Đoạn Bóc Tách:
* **Giai đoạn 1 (Lúc Nhện Quét Báo Cáo):** Chỉ lấy Tiêu đề + Extended Excerpt (3–5 đoạn tóm tắt vĩ mô qua Google News RSS & thẻ SEO). Đủ để System 1 phân loại chuẩn xác trong 40ms và cấp tọa độ cho nhện bò giăng tơ mà không tốn công vượt paywall.
* **Giai đoạn 2 (Khi Người Dùng Click Đọc Chi Tiết Hoặc Bấm Deep Dive):** Hệ thống kích hoạt **On-Demand Full Extraction** qua 4 cổng dự phòng:
  1. *Yahoo Finance / MSN Syndication Mirror:* 80-90% bài tài chính của Bloomberg/Reuters được phân phối bản quyền miễn phí toàn văn trên Yahoo Finance.
  2. *Reader Proxy Mode (`r.jina.ai`):* Gỡ bỏ các lớp che Javascript và trích xuất Markdown toàn bài.
  3. *JSON-LD ArticleBody Extraction:* Đọc thẳng văn bản 2.000 từ nằm ẩn trong mã nguồn HTML phục vụ SEO.
  4. *Bản in / AMP / Cached (Tầng 4 của §12.5):* Thử `<url>?output=1`, `<url>/amp`, Google News cache hoặc text mirror.

---

### 3.6. Mỹ Thuật Sân Đấu Nhện & Quỹ Đạo Zic-Zac (Spider Locomotion Aesthetics)
> **Giải quyết bài toán thẩm mỹ:** *"Nếu chỉ quét tóm tắt thì bài báo có bị ngắn quá làm con nhện không có chỗ chạy không?"*

Để đảm bảo con nhện luôn có một **sân khấu biểu diễn kỳ vĩ, thoáng đãng và đậm chất nghệ thuật Thảo Mộc**:
1. **Dàn trang Bản Báo Cáo Học Thuật (Financial Paper Sheet):** Màn hình chính 1 (Spider Web Arena) chiếm 63% không gian (32% Vòng Cung System 1, 5% Bottom Telemetry Bar) (`1450px x 940px`). Văn bản hiển thị gồm: Tiêu đề lớn $\rightarrow$ Khung Metadata $\rightarrow$ Đoạn Tóm tắt điều hành $\rightarrow$ **Extended Excerpt (3–5 đoạn trích bối cảnh và số liệu then chốt)**, duy trì độ dài lý tưởng **150 – 300 từ**.
2. **Quỹ đạo di chuyển Zic-zac khắp mặt giấy (Diagonal Trajectory):** Các mốc từ khóa `<mark data-spider-index="...">` được phân bổ rải đều:
   - Từ khóa 1: Nằm ở Tiêu Đề trên đỉnh trang.
   - Từ khóa 2: Nằm ở Đoạn Tóm Tắt vĩ mô ở giữa.
   - Từ khóa 3 & 4: Nằm ở Đoạn Số Liệu & Tác Động Thị Trường phía dưới.
   - Từ khóa 5: Nằm ở Kết luận.
3. **Vũ đạo phóng tơ xuyên suốt màn hình:** Tại mỗi điểm dừng, nhện xoay thân và phóng một **sợi tơ mảnh 0.75px cong Bezier mềm mại** vút ngang màn hình sang Vòng Cung Quyết Định bên phải, tạo cảm giác chuyển động sống động và hoành tráng.
4. **Hiệu ứng lật trang (Page-Flip Transition):** Khi duyệt xong bài 1, tờ giấy báo trượt nhẹ với hiệu ứng mực loang, bài mới trượt vào, nhện lướt vút về đầu trang bắt đầu chu kỳ mới!



---

---

## 🛠️ 4. Công Nghệ Đề Xuất Tối Ưu (Tech Stack)

| Tầng | Công nghệ đề xuất | Lý do & Nhiệm vụ |
| :--- | :--- | :--- |
| **Desktop App Shell** | **Tauri v2 (Rust + WebView2)** | Đóng gói thành ứng dụng máy tính native (`.exe` ~15MB, RAM < 30MB), hỗ trợ System Tray, cửa sổ không viền (Frameless), thông báo Windows. |
| **Backend** | **Python (FastAPI + `httpx` async)** | Gọi Docker Decision 3 / Laya qua HTTP async chỉ mất vài mili-giây. Cào & làm sạch RSS báo chí bằng `feedparser` và `trafilatura`. |
| **AI Sơ Tuyển (System 1)** | **Laya RL Agent (`laya-laya-serve`) hoặc Decision 3.0 Lite (`vllm-sr/d3-lite`)** | System 1 trên Docker GPU port 8000 (0.85B Qwen 3.5 Multimodal), lọc sạch tin giật tít/PR rác, đọc trọn vẹn context 32K+, nhận diện hình ảnh biểu đồ. Độ trễ đo được trên NVIDIA GPU: **Laya 30–60ms / Decision 3.0 150–200ms**, hiển thị latency trung bình trong app. |
| **AI Tổng Hợp (System 2)** | **Gemini Flash API** hoặc **Qwen 2.5 Local** | Phân tích sâu, tổng hợp toàn bộ danh sách tin hoặc tin lẻ, dịch thuật chuẩn xác sang tiếng Việt văn phong tài chính/công nghệ. |
| **Frontend UI** | **TypeScript + Vite (React)** | Khởi động 0.1s, render 60 FPS mượt mà. Type-safe cho dữ liệu từ Laya và LLM. |
| **Hiệu ứng & Chuyển động** | **GSAP (GreenSock Animation Platform)** | Khai thác từ bộ `D:\code\skill_AI\gsap-skills`: Điều phối chuyển động con nhện, tia nước/mực, hiệu ứng gắp từ khóa qua `gsap.timeline()`. |
| **Nhện Asset (Visual)** | **SVG 2D Layered + GSAP (Chuẩn hóa duy nhất)** | Siêu nhẹ (vài KB), nét vẽ thơ mộng tinh tế, không tốn GPU/VRAM, ánh xạ 1:1 tọa độ DOM `getBoundingClientRect()`, loại bỏ hoàn toàn Three.js/Spline 3D. |

---

## 🌸 5. Định Hình Phong Cách: "Tạp Chí Kinh Tế Thơ Mộng" (Poetic Botanical)
> Dựa trên tài liệu gốc: `D:\code\skill_AI\canva_skill\references\18-poetic-botanical-ink.md` (Nhánh F. Wavy-Pastoral & G. Branch-Spine).

Thoát khỏi lối mòn "Cyberpunk / Hacker đen ngòm", dự án hướng tới một **Tạp chí Tri thức Kinh tế - Chính trị thanh nhã**:

### 5.1. Bảng màu & Typography (Chuẩn WCAG, Dịu Mắt)
* **Nền bài viết (`bg`):** Trắng ngà giấy dó `#FAF8F5` (Ấm áp, chống mỏi mắt).
* **Bề mặt phụ (`surface`):** Xanh non thảo mộc `#E8F5D8` hoặc be nhạt.
* **Màu chữ chính (`text`):** Xanh rừng sâu `#2D4A2B` (Tương phản cao 11.9:1, cực kỳ rõ và thanh lịch).
* **Màu sắc tâm lý thị trường (Sentiment Colors từ Laya):**
  * 🌸 **Tin tốt / Tăng trưởng:** Nhấn màu **Hồng đào san hô** (`#F8AFA6`) hoặc **Xanh ngọc bích**.
  * 🍂 **Tin rủi ro / Tiêu cực:** Nhấn màu **Nâu đất / Cam đất ấm** (`#C86D51`) (Thay cho màu đỏ chói gắt).
  * 🌾 **Tin chính sách vĩ mô:** Nhấn màu **Vàng hổ phách thảo mộc** (`#E5B869`).
* **Typography:**
  * Tiêu đề báo & Chỉ số: **Playfair Display** / **Fraunces** (Serif cổ điển, có chân sang trọng).
  * Nội dung chi tiết: **Be Vietnam Pro** (Sans-serif hiện đại, chuẩn tiếng Việt).

### 5.2. Chốt mẫu con nhện: "Làm sao để duyệt hình mẫu chính không đổi?"
1. **Bước 1: Khóa Concept Visual qua Canva AI / Prompt:**
   * Concept: *"Botanical Crystal Spider"* (Nhện giọt sương / thủy tinh / thảo mộc gốm sứ mộng mơ).
   * Khóa góc nhìn: **Top-down view (từ trên nhìn xuống)** để hiển thị rõ nhất trên mặt trang báo.
2. **Bước 2: Xuất Asset Vector cố định (SVG Layered):**
   * Vẽ lại thành file vector SVG cố định: Tách riêng thân (`#spider-body`) và 8 chân (`#leg-1` đến `#leg-8`).
   * Sử dụng GSAP điều khiển khớp chân bò tự nhiên như sinh vật sống.
   * Ưu điểm: Model cố định vĩnh viễn 100%, không bị biến dạng giữa các lần chạy, tải tức thì.

### 5.3. Vũ đạo nhịp nhàng (Choreography):
* Chân nhện chạm vào từ khóa tạo hiệu ứng **Gợn sóng nước (Water ripple)** hoặc **Giọt mực thủy mặc loang nhẹ**.
* Từ khóa được gắp sẽ uốn lượn bay (FLIP Animation) sang **Cột cành cây tri thức (Branch Spine Shelf)** bên phải màn hình.

### 5.4. Quy chuẩn Sợi Tơ Bắn Tới (Transient Web Filament - 4 Quy Tắc Chống Rối Mắt):
> **Bài toán "Visual Noise":** Nếu Laya xử lý quá nhanh mà sợi tơ nào bắn ra cũng nằm lì trên màn hình, chỉ sau vài giây trang báo sẽ biến thành một "đĩa mì spaghetti" rối rắm, che hết chữ và gây nhức mắt. Để giữ màn hình luôn thanh nhã, thoáng đãng đúng chất Thơ Mộng, hệ thống áp dụng **4 quy tắc thiết kế tơ nhện** sau:

1. **Cơ chế Tơ Tự Tiêu Biến (Fade-out Lifecycle / Tan vào giấy - 1.2s):**
   * Sợi tơ **KHÔNG BAO GIỜ tồn tại vĩnh viễn** trên màn hình.
   * *0.0s – 0.3s:* Nhện cắm chân $\rightarrow$ Sợi tơ phóng vút sang chiếc hộp bên phải (GSAP `drawSVG` / SVG Bezier).
   * *0.3s – 0.5s:* Chiếc hộp bên phải nhận tơ, chớp sáng nhẹ và nhảy số đếm (`+1`).
   * *0.5s – 1.2s:* Sợi tơ mờ dần (`opacity: 0.6 → 0`) và **biến mất hoàn toàn khỏi DOM**, tan vào nền giấy ngà như một vệt nước bốc hơi.
   * $\rightarrow$ **Kết quả:** Tại bất kỳ thời điểm nào, mắt người dùng chỉ nhìn thấy **1 đến 2 sợi tơ lướt qua**, màn hình luôn sạch sẽ!
2. **Độ mảnh như tơ nhện thật (Delicate Hairline 0.75px):**
   * Không dùng đường kẻ dày thô kệch. Độ dày nét vẽ: Bắt buộc **`0.75px – 1.0px`** (Hairline stroke).
   * Màu sắc: Bán trong suốt (`opacity: 0.6`, màu xanh ngọc `#A8D5BA`), đường cong uốn lượn mềm mại (Cubic Bezier curve), tạo cảm giác mỏng manh và tinh tế như sợi tơ sương mai buổi sáng.
3. **Giới hạn số tơ đồng thời (Max Concurrent Threads = 2):**
   * Dù Laya có phân tích ra 10 từ khóa cùng lúc trong 10 mili-giây, hệ thống **chỉ cho phép tối đa 2 sợi tơ xuất hiện đồng thời** (`max_active_filaments = 2`).
   * Các từ khóa tiếp theo nằm trong hàng đợi (Queue) và bắn ra tuần tự nhịp nhàng cách nhau `300ms – 400ms`. Nhện bắn "tách... tách... tách..." cực kỳ đã mắt và có nhịp điệu.
4. **Vết tích để lại gọn gàng (Clean Residual Anchor):**
   * Sau khi sợi tơ biến mất: Từ khóa trên bài báo chỉ giữ lại một **vệt highlight pastel mờ nhẹ** (hoặc dấu chấm tròn nhỏ); chiếc hộp bên phải chỉ giữ lại **số đếm và một thẻ tag nhỏ** ở khay lưu trữ.
   * Khoảng không gian giữa hai bên hoàn toàn thông thoáng để người dùng đọc chữ.


---

## 🔗 6. Dây Chuyền Phối Hợp 4 Skill Có Sẵn

1. **`D:\code\skill_AI\canva_skill`:**
   * Tham chiếu các file `01-layout.md`, `03-color.md`, `18-poetic-botanical-ink.md` để thiết kế bố cục 3 cột và xuất các asset hoa văn/dây leo.
2. **`D:\code\skill_AI\.agents\skills\ui-ux-design-system`:**
   * Chuẩn hóa Design Tokens (CSS Variables, màu sắc, spacing, typography) thống nhất.
3. **`D:\code\skill_AI\frontend-design`:**
   * Ứng dụng `taste-skill-ReactBits.md` và `scroll_design` để làm hiệu ứng cuộn báo Parallax, Card Overlapping êm ái.
4. **`D:\code\skill_AI\gsap-skills`:**
   * Dùng `gsap-timeline`, `gsap-react` điều phối toàn bộ chuyển động bước chân nhện và hiệu ứng gắp dữ liệu.

---

---

## 📡 7. Nguồn Cấp Tin Đa Dạng: Vĩ Mô, Chứng Khoán, Vàng, Crypto & GitHub

Hệ thống được thiết kế mở, chia thành các chuyên mục rõ ràng và **cho phép người dùng tùy ý thêm/bớt/bật/tắt nguồn tin**:

### 7.1. Danh Mục Nguồn Mặc Định (Chuyên Sâu & Thời Gian Thực)
* **📈 1. Thị Trường Chứng Khoán (Stocks & Equities):**
  * *Trong nước:* CaféF Chứng khoán (`https://cafef.vn/thi-truong-chung-khoan.rss`), Vietstock Tin nhanh (`https://vietstock.vn/rss/chung-khoan.rss`), Tin Nhanh Chứng Khoán Đầu Tư.
  * *Quốc tế:* CNBC Stock Markets RSS, Yahoo Finance Top News, MarketWatch.
  * *Chỉ số theo dõi:* VN-Index, HNX, UPCoM, S&P 500, Nasdaq, Dow Jones.
* **🥇 2. Thị Trường Vàng & Kim Loại Quý (Gold & Commodities):**
  * *Trong nước:* Bản tin giá vàng SJC, DOJI, Vàng nhẫn 9999 (bóc từ CaféF Vàng / 24h Vàng).
  * *Quốc tế:* Kitco Gold News RSS (`https://www.kitco.com/rss/gold.xml`), World Gold Council Insights, Bloomberg Commodities.
  * *Chỉ số theo dõi:* XAU/USD (Spot Gold), Dầu thô Brent/WTI.
* **🪙 3. Tiền Mã Hóa & Web3 (Crypto & Blockchain):**
  * *Quốc tế:* CoinDesk Wire (`https://www.coindesk.com/arc/outboundfeeds/rss/`), Cointelegraph RSS (`https://cointelegraph.com/rss`), Decrypt News.
  * *Chủ đề:* Bitcoin (BTC ETF, Halving), Ethereum, Solana, chính sách quản lý tài sản số của SEC và các chính phủ.
* **🌐 4. Kinh Tế Vĩ Mô & Địa Chính Trị (Macro & Geopolitics):**
  * *Việt Nam:* CaféF Vĩ Mô (`https://cafef.vn/kinh-te-vi-mo.rss`), VnExpress Kinh Doanh (`https://vnexpress.net/rss/kinh-doanh.rss`), SBV (Ngân hàng Nhà nước).
  * *Quốc tế:* AP News Wire (`https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com`), Reuters Markets Query, Financial Times, Bloomberg.
  * *Chủ đề:* Lãi suất FED, ECB, lạm phát CPI, tỷ giá USD/VND, chuỗi cung ứng, bầu cử, chiến sự.
* **🐙 5. Chế Độ "GitHub Radar Only" (Dành Riêng Cho Developer & Kỹ Sư AI):**
  * Backend quét qua **GitHub Trending API** và Release Notes (topics: `ai`, `llm`, `agent`, `quant`, `machine-learning`, `rust`, `python`).
  * Con nhện bò trực tiếp trên `README.md` / Code blocks của repo để gắp tag công nghệ, commit mới và số stars ⭐.
  * LLM System 2 giải thích: Repo này đột phá ở đâu, giải quyết bài toán gì, sẵn sàng ứng dụng thực tế chưa.

### 7.2. Trung Tâm Quản Lý Nguồn Động (Dynamic Feed Manager & Custom RSS Settings)
> Người dùng không bị bó buộc vào danh sách cứng của hệ thống, mà có toàn quyền quản trị nguồn tin:

* **Tùy biến Thêm/Bớt Nguồn Tức Thì (CRUD Feeds):**
  * Tại Màn hình Cài đặt (Settings), người dùng có thể bấm **"+ Thêm Nguồn Tin Mới"**:
    - Nhập Tên nguồn (ví dụ: *"Báo Đầu Tư Chứng Khoán"*).
    - Nhập RSS URL (ví dụ: `https://baodautu.vn/rss/chung-khoan.rss`).
    - Chọn Chuyên mục: `[Chung_khoan]`, `[Vang]`, `[Crypto]`, `[Kinh_te]`, `[Chinh_tri]`, `[Tuy_chon]`.
    - Chọn Chu kỳ quét: 5 phút, 15 phút, 30 phút, 60 phút.
* **Kiểm tra tính hợp lệ tự động (RSS Health Validator):**
  * Khi bấm Lưu, Backend tự động gửi ping request kiểm tra URL RSS có phản hồi hợp lệ không (HTTP 200, đúng cấu trúc XML RSS/Atom). Nếu hợp lệ mới lưu vào SQLite và bắt đầu cào tự động.
* **Công tắc Bật/Tắt Từng Kênh (Toggle Switch ON/OFF):**
  * Người dùng có thể tạm tắt một kênh (ví dụ: tắt bớt Crypto nếu chỉ muốn tập trung đọc Vàng và Chứng khoán). Hệ thống sẽ lập tức dừng cào nguồn đó mà không cần khởi động lại app.
* **Tabs Lọc Động Trên Màn Hình Chính (Main Radar):**
  * Thanh điều hướng trên cùng tự động cập nhật các nút chọn lọc:
    `[Tất cả]` • `[📈 Chứng khoán]` • `[🥇 Vàng]` • `[🪙 Crypto]` • `[🌐 Vĩ mô & Chính trị]` • `[🐙 GitHub Tech]`.

### 7.3. Cơ Chế Chủ Đề Tra Cứu & Watchlist Động (Zero-Code Topic Watchlists & FTS5 Instant Search)
> **Giải đáp bài toán linh động:** *"Nếu muốn thêm chủ đề tra cứu mới như Chiến tranh Trung Đông, Giá dầu Brent, Bán dẫn... thì có phải sửa code chính không?"*  
> 👉 **TRẢ LỜI: KHÔNG CẦN SỬA MỘT DÒNG CODE NÀO! HỆ THỐNG ĐỘNG 100%!**

Hệ thống được thiết kế theo mô hình **Data-Driven Dynamic Registry**:
1. **Quản Lý Chủ Đề Qua Bảng `topic_watchlists` (Zero-Code):**
   * Người dùng có thể thêm bất kỳ chủ đề mới nào trên màn hình Cài đặt (ví dụ: Tên: *"Giá Dầu & Năng Lượng"*, Icon: `🛢️`, Từ khóa: `["dầu brent", "wti", "opec", "khí đốt"]`, Màu tơ: `#D97706`).
   * **Phía Frontend (Spider Web Arena):** Tự động mọc thêm một Node mới mang tên `🛢️ Node Giá Dầu` trên Vòng Cung Quyết Định bên phải màn hình.
   * **Phía Backend (Laya System 1):** Backend không fix cứng câu hỏi, mà đọc danh sách các topics đang active từ database để tự động ghép vào trường `criteria` gửi sang Laya:
     ```json
     "criteria": {
       "gia_dau": "biến động giá dầu mỏ thế giới, sản lượng OPEC, khủng hoảng năng lượng",
       "chien_tranh": "xung đột vũ trang, không kích, tên lửa, chiến sự leo thang"
     }
     ```
   * Khi bài báo có nội dung dầu khí $\rightarrow$ Laya nhận diện $\rightarrow$ Nhện lập tức **phóng tơ vút sang `🛢️ Node Giá Dầu`**! Tất cả vận hành tự động theo dữ liệu database!

2. **Tra Cứu Nhanh Mọi Từ Khóa Qua SQLite FTS5 (Full-Text Search 5):**
   * Ngay cả khi người dùng **chưa kịp tạo chủ đề trong Watchlist**, chỉ cần gõ bất kỳ từ khóa nào vào thanh tìm kiếm (ví dụ: *"Hormuz"*, *"chiến sự"*, *"Nvidia"*):
   * Bộ máy tìm kiếm toàn văn ảo `articles_fts` của SQLite sẽ quét toàn bộ tiêu đề và nội dung của hàng chục nghìn bài báo đã lưu với tốc độ **dưới 2 mili-giây**!

### 7.4. Cơ chế Chống Đọc Trùng Tin Tuyệt Đối (Deduplication)
* Băm mã hash `SHA-256(clean_url)` lưu vào cột `url_hash UNIQUE` trong SQLite.
* Sử dụng `INSERT OR IGNORE`: Bài viết/Repo nào đã quét trong ngày sẽ bị SQLite bỏ qua ngay trong 0.01ms, đảm bảo nhện không bao giờ bò lại tin cũ.

---

## 🧠 8. Chiến Lược Dịch Thuật & LLM System 2: Tối Ưu Chi Phí & Bảo Toàn Cấu Trúc

### 8.1. Ba Nguyên Tắc Bất Biến Về Dịch Thuật & Hiển Thị
1. **Con Nhện bò trên 100% BẢN BÁO GỐC (Original Language Arena):**
   * Tại màn hình chính (Spider Web Arena), bài báo hiển thị nguyên bản ngôn ngữ gốc (tiếng Anh nếu từ Bloomberg/Reuters/GitHub, tiếng Việt nếu từ CaféF/VnExpress).
   * Con nhện bò trực tiếp trên các thẻ từ khóa gốc `<mark>` (*"Federal Reserve"*, *"Interest Rates"*, *"Lãi suất"*, *"VN-Index"*).
   * Decision 3.0 đọc văn bản gốc và định vị tọa độ từ khóa gốc $\rightarrow$ Khớp 1:1 tuyệt đối, không có sai lệch do dịch thuật, nhện diễn mượt mà 60 FPS.
2. **Dịch Lười Theo Nhu Cầu (On-Demand / Lazy Translation):**
   * **Tuyệt đối không dịch hàng loạt khi cào tin:** Cào 100 tin về máy chỉ lưu văn bản gốc và chạy Decision 3 lọc rác. 0% CPU/mạng bị lãng phí cho việc dịch trước.
   * **Chỉ dịch duy nhất 1 bài khi người dùng Click mở xem chi tiết:** Khi người dùng click vào bài và gạt công tắc `[● 🇻🇳 Tiếng Việt]`, hệ thống mới kích hoạt dịch đúng bài đó theo từng đoạn văn bản.
3. **Dịch Chuyên Dụng 0đ & Bảo Toàn Cấu Trúc (Giống Cốc Cốc / Google Chrome):**
   * **Bỏ hoàn toàn việc dùng LLM để dịch toàn văn:** LLM sinh text dài vừa tốn tiền token khủng khiếp, vừa tự ý viết lại làm vỡ cấu trúc thẻ HTML và mất dấu vị trí từ khóa.
   * **Bỏ qua các model dịch local như NLLB-200:** NLLB-200 ngốn thêm 1.5GB – 2GB VRAM, sẽ làm tràn VRAM của card RTX 3050 (4GB) khi chạy cùng Decision 3.0.
   * **Sử dụng Engine Dịch Máy Chuyên Dụng (`deep-translator` qua web endpoint):**
     * **Chi phí: 0 ĐỒNG** (Hoàn toàn miễn phí, không cần API key).
     * **Ăn đúng 0% VRAM:** Chạy nhẹ nhàng qua HTTP async, không tốn tài nguyên GPU.
     * **Bảo toàn 100% cấu trúc DOM:** Dịch theo từng đoạn `<p>` và giữ nguyên thẻ tiêu đề, danh sách gạch đầu dòng, code block, tọa độ thẻ `<mark>`.

### 8.2. Chiến Lược Cache Bản Dịch: "In-Memory Session Cache" (Chống Nặng Database SQLite)
> **Bài toán:** *"Lưu toàn bộ bản dịch vào SQLite có làm phình to database quá nhanh không?"*

* **Đánh giá:** Người dùng đọc tin tức có tính thời sự ngắn, sau vài ngày hầu như không bao giờ mở lại tin cũ. Lưu vĩnh viễn mọi bản dịch vào đĩa SQLite là thừa thãi và gây rác dữ liệu.
* **Quy chuẩn giải pháp (Giống trình duyệt Cốc Cốc / Chrome 100%):**
  * **Lưu tạm thời trên RAM Giao Diện (React State / In-Memory Cache):**
    * Khi người dùng bấm xem chi tiết và dịch bài $\rightarrow$ Bản dịch được giữ trong RAM của phiên làm việc hiện tại.
    * Người dùng gạt qua lại giữa `[🇻🇳 Tiếng Việt]` và `[🌐 Bản Gốc]` tráo đổi tức thì trong 0ms.
    * Chuyển qua bài khác rồi quay lại bài này vẫn xem được ngay mà không cần gọi mạng dịch lại.
    * **Khi tắt ứng dụng:** RAM tự động giải phóng sạch sẽ. Database SQLite hoàn toàn không bị phình to 1 byte nào!
  * **Ngoại lệ duy nhất (Persistent Bookmark Exception):**
    * Chỉ khi người dùng bấm nút **⭐ Bookmark (Lưu vào Tech Vault)** để lưu trữ lâu dài, bản dịch mới được ghi cố định vào SQLite để phục vụ đọc offline vĩnh viễn.

### 8.3. Phân Công Nhiệm Vụ Cho LLM System 2 (Gemini Flash)
Thay vì làm "thợ dịch cửu vạn", LLM System 2 được giải phóng để làm đúng vai trò "Chuyên gia phân tích cấp cao":
* **Deep Dive Tin Lẻ:** Chỉ nhận ~300 từ cốt lõi, xuất bản nhận định tình báo tài chính:
  1. *Tóm tắt 3 gạch đầu dòng cô đọng (`vietnamese_summary`).*
  2. *Đánh giá tác động vĩ mô thị trường Việt Nam & dòng tiền (`macro_impact`).*
  $\rightarrow$ Tốn chỉ 200–300 tokens, siêu nhanh (< 1s) và tiết kiệm 95% chi phí API.
* **Executive Digest (Tạp chí vĩ mô tổng hợp):** Nối kết toàn bộ 20–30 tin tinh hoa trong ngày thành 1 bức tranh toàn cảnh vĩ mô mạch lạc.

### 8.4. Quy Chuẩn Xử Lý Đa Ngôn Ngữ Phần Chìm (Multilingual Underwater Pipeline)
Dù trên giao diện hiển thị 100% bằng **Tiếng Việt chuẩn mực**, phần chìm (underwater) của hệ thống xử lý đa ngôn ngữ theo 6 nguyên tắc kỹ thuật đồng bộ:
1. **Phát Hiện Ngôn Ngữ Tự Động (Language Tagger < 0.2ms):**
   * Khi crawler cào tin về, hàm `detect_language()` gắn tag ISO (`en`, `vi`, `zh`, `ja`) lưu vào cột `language` của bảng `articles`.
2. **Tiêu Chí Phân Loại Song Ngữ Cho Laya System 1 (Bilingual Criteria Prompting):**
   * Laya đánh giá ngữ nghĩa (30–60ms, D3 150–200ms trên NVIDIA GPU). Cột `criteria_prompt` trong `topic_watchlists` luôn lưu song ngữ Anh-Việt (ví dụ: `"interest rate hikes, inflation, central bank policy / tăng lãi suất, lạm phát, chính sách tiền tệ"`). Nhờ đó, bất kể bài báo gốc là tiếng Anh hay tiếng Việt, Laya đều lọc chính xác mà không tốn thời gian dịch trước.
3. **Ánh Xạ Tơ Nhện Sang Node Quyết Định (Spider Keyword Mapping):**
   * Trên bài viết gốc: Nhện bò và cắm chân vào từ khóa nguyên bản (ví dụ: `Federal Reserve`, `interest rates`).
   * Phóng tơ sang cột phải: Sợi tơ nối thẳng sang Node tiếng Việt đã định danh (ví dụ: `🏛️ Ngân Hàng Trung Ương` / `Node Kinh Tế & Dòng Tiền`). Người dùng vừa thấy nguyên văn vừa hiểu ngay ý nghĩa phân loại.
4. **Dịch Thuật Chuyên Biệt Tài Chính & Kỹ Thuật (System 2 Translation):**
   * Prompt hệ thống yêu cầu: Gãy gọn, bảo toàn thuật ngữ quốc tế (`Fed`, `S&P 500`, `VN-Index`, `OPEC+`, `EBITDA`, `P/E`, `USD/VND`, `Docker`, `LLM`), không dịch ngô nghê từng từ.
5. **Tìm Kiếm Không Phân Biệt Dấu Tiếng Việt (FTS5 Accent-Insensitive):**
   * Bảng ảo `articles_fts` cấu hình `tokenize='unicode61 remove_diacritics 2'`. Người dùng gõ `dau brent`, `lai suat fed`, hay `chien su` đều khớp chính xác các bài có `dầu Brent`, `lãi suất FED`, `chiến sự` trong 1–2ms.
6. **Công Tắc Chuyển Đổi Song Ngữ Trên Màn Hình (Bilingual View Switcher):**
   * Bố trí widget nút gạt nhỏ ngay cạnh nguồn tin: `[● 🇻🇳 Tiếng Việt (Bản tóm tắt AI)] [○ 🌐 Bản Gốc (Tiếng Anh/Quốc tế)]`.
   * Chuyển đổi trạng thái tức thì trong 0.05 giây mà không gọi lại mạng vì dữ liệu bản gốc và bản tóm tắt đều đã được lưu trữ sẵn trong cơ sở dữ liệu SQLite.

---

## 🎵 9. Thiết Kế Âm Thanh (SFX Foley) & Tương Tác Người Dùng

### 9.1. Âm thanh mộng mơ (Thư giãn, không chói tai)
* 💧 **Water Droplet (Giọt nước rơi):** Phát ra khi chân nhện chạm vào từ khóa kinh tế/chính trị.
* 📜 **Paper Rustle (Lật trang giấy):** Phát ra nhẹ nhàng khi chuyển bài báo mới.
* 🎐 **Wind Chime / Harp (Chuông gió thanh mảnh):** Kêu khẽ khi Laya phát hiện tin biến động lớn (Breaking News).
* *Tích hợp sẵn công tắc Mute / Unmute trên góc giao diện.*

### 9.2. Tính năng tương tác & Điều khiển Tốc độ Nhện (User Controls)
* **⚡ Mặc định: Chế độ "Laya/D3 Sync" (`pacing_delay_ms = 400`):**
   * System 1 suy luận trong **30ms – 60ms** (Laya, HTTP roundtrip < 70ms) hoặc **150ms – 200ms** (D3 trên NVIDIA GPU). SSE Queue đẩy sự kiện xuống Frontend, nhện nhận xung và phóng tới từ khóa tiếp theo với nhịp **400ms/bước** với gia tốc mượt mà (`ease: "expo.out"`), cắm chân tạo giọt sương rồi tiếp tục săn tin. Cảm giác như một chú nhện cơ khí siêu linh hoạt săn tin theo nhịp xung thần kinh của AI.
* **☕ Dự phòng: Chế độ "Chill Mode" (`pacing_delay_ms = 1200`):**
  * Gạt công tắc sang **Chill Mode (1.2s/bước)** để nhện bò thong thả thư giãn, vừa uống cà phê vừa đọc tin.
* **Nút Skip / Next:** Bấm để nhện giật mình nhảy vụt sang bài tiếp theo.
* **Bộ lọc nguồn:** Tabs chọn: `[Tất cả]`, `[Kinh tế VN]`, `[Vĩ mô Quốc tế]`, `[🐙 GitHub Only]`.
* **Nút "Tổng Hợp Bằng Tiếng Việt":** Kích hoạt LLM System 2 tóm tắt tức thì.


---

## 🖥️ 10. Danh Sách Các Màn Hình Chuẩn (Screen Architecture & Sitemap)

Ứng dụng được thiết kế gồm **7 màn hình / chế độ xem** kết hợp hoàn hảo giữa tính giải trí trực quan và giá trị thông tin thực tế. Đặc tả chi tiết từng nút bấm, Design Token và component mapping: [`DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md`](./DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md).

### 1. 🕷️ Màn hình 1: SPIDER WEB ARENA (Bản Đồ Giăng Tơ & Sân Khấu Nhện Độc Lập)
* **Cảm hứng trực tiếp:** Trend *"Anh IT họ Lào - Prompt Spider // Mỗi hàm, một ngã rẽ"* trên TikTok.
* **Bố cục Sân Đấu Tự Do (Split Layout 63% – 32% + Bottom Telemetry Bar 5%):**
  * **Cột trái (63% - Paper & Code Arena):** Không gian mênh mông trên nền giấy ngà `#FAF8F5`, chữ và code trải dài thoáng đãng. Con nhện tự do bay nhảy, cắm chân tạo gợn sóng nước và **phóng tơ vút dài 300px** sang bên phải. Cột danh sách tin được tích hợp dạng **Slide-over Drawer (ngăn kéo bên trái)** có thể bật/tắt để không chiếm diện tích sân khấu.
  * **Cột phải (32% - Neural Routing Arc):** Vòng cung các Node Quyết Định của System 1 (`Node Kinh Tế & Dòng Tiền`, `Node Chứng Khoán`, `Node Giá Vàng`, `Node Crypto`, `Node Breaking News`). Khi nhận tơ từ nhện, node chớp sáng và nhảy số đếm (`+1`).
  * **Thanh đáy (Bottom Telemetry Bar - 5%):** Hiển thị `[Độ trễ System 1 trung bình: 45ms]` • `[Tơ đã giăng: 6/14]` • `[Ma trận Token Đã Đọc: ●●●●●●○○○○○○○○]` • `[FPS: 60.0]`.
  * **Top Header:** Nút chuyển đổi View + Nút Mute SFX + Thanh Pacing.

### 2. 📑 Màn hình 2: Curated Feeds & Bilingual Reader (Dòng Tin Đã Lọc & Trình Đọc Song Ngữ)
* **Bố cục Master-Detail 3 vùng:** Sidebar lọc `240px` (FTS5 + ngưỡng Score) → Master Feed List `560px` → Bilingual Reader `1060px`.
* **Master Feed List:** Danh sách bài đã được System 1 sàng lọc, mỗi thẻ hiển thị badge thể loại, tiêu đề, nguồn/thời gian, badge định tuyến kèm latency thực tế (`⚡ ROUTED: 45ms • ON-DEMAND TRANSLATE (0đ)`) và nút ghim `★` vào Tech Vault.
* **Bilingual Reader:** Công tắc `[● 🇻🇳 Tiếng Việt]` / `[○ 🌐 Bản Gốc]`. Bản gốc giữ nguyên ngôn ngữ nguồn (con nhện ở Màn hình 1 luôn bò trên 100% bản gốc này); bản dịch kích hoạt On-Demand theo từng `<p>` bằng `deep-translator`, cache In-Memory RAM để hoán đổi trong 0ms.

### 3. 📰 Màn hình 3: Executive Intelligence Digest (Bản Tin Tổng Hợp Vĩ Mô Điều Hành)
* **Kích hoạt:** Khi người dùng bấm *"⚡ Tổng hợp tin hôm nay"*.
* **Bố cục Hero + 2:** Sidebar lịch sử bản tin `240px` (kèm Chỉ số Tâm Lý Thị Trường) → Hero Macro Panel full-width + 2 cột phân tích chuyên sâu bên dưới.
* **Nội dung:** LLM System 2 gom toàn bộ danh sách 20-50 tin nóng đã được System 1 lọc thành một **Bản Tin Tạp Chí Vĩ Mô mạch lạc bằng tiếng Việt**:
  * *1. Xu hướng kinh tế thế giới & Chính sách (FED, Chiến sự, Tỷ giá).*
  * *2. Thị trường tài chính & Dòng tiền (VN-Index, Giá vàng SJC, Crypto Bitcoin).*
  * *3. Điểm tin công nghệ AI & GitHub nổi bật.*
* **Hành động:** Nút `📥 Xuất Báo Cáo PDF`, `📋 Sao Chép Bản Tin`.

### 4. 🐙 Màn hình 4: GitHub Tech Radar (Chế độ chuyên sâu cho Dev / AI Engineers)
* **Kích hoạt:** Khi bật tab `[🐙 GitHub Only]`.
* **Bố cục 3 vùng:** Tech Trends Sidebar `240px` (lọc ngôn ngữ/chủ đề, repo trending) → Code & README Inspector `1040px` (tab `README.md` / Kiến trúc mã nguồn / Cài đặt Docker) → Tech Arc Column `580px` (điểm kỹ thuật, độ trễ P50/P95, tương thích phần cứng).
* **Giao diện:** Trình đọc `README.md` và cấu trúc Repo. Nhện bò gắp số Stars ⭐, Forks, Tech Stack lõi.
* **Khung phân tích của LLM System 2:**
  * *Repo giải quyết bài toán gì? Có điểm gì đột phá? Đã sẵn sàng dùng cho thực tế chưa?*

### 5. 🌳 Màn hình 5: Trend Vault & Knowledge Graph (Kho Lưu Trữ & Xu Hướng)
* **Dữ liệu:** Tra cứu lại dữ liệu tin bài đã ghim từ SQLite trong 7 hoặc 30 ngày qua; miễn trừ chính sách TTL 30 ngày.
* **Cây Tri Thức Thảo Mộc (SVG 2D - `BotanicalTree.tsx`):** Thân cây đại diện dòng thời gian, cành Bezier tỏa ra 3 cụm chủ đề (Kinh Tế `#2D4A2B`, Địa Chính Trị `#C86D51`, Công Nghệ AI `#4A6B82`), node lá dạng pill tương tác bằng GSAP.
* **Keyword Heatmap:** Thống kê tần suất xuất hiện của các từ khóa nóng (*"Thuế quan"*, *"Lãi suất"*, *"Vàng nhẫn"*, *"Bitcoin ETF"*, *"Bán dẫn"*...).
* **Tìm kiếm nâng cao:** Lọc lại tin cũ theo sentiment, danh mục hoặc mã cổ phiếu. Xuất trích dẫn BibTeX.

### 6. ⚙️ Màn hình 6: Settings & Data Retention Management (Cài Đặt & Quản Trị Dữ Liệu)
* **Nguyên tắc Progressive Disclosure:** Section 2 (Feeds Manager) **mở sẵn**; Section 1 (Động Cơ AI) và Section 3 (Watchlists & TTL) **thu gọn mặc định**.
* **Quản Lý Nguồn RSS Động (Feed Manager):**
  * Bảng danh sách nguồn tin: Tên nguồn, URL RSS, Chuyên mục (`chung_khoan`, `vang`, `crypto`, `kinh_te`, `chinh_tri`, `github`), Chu kỳ quét, Trạng thái (Bật/Tắt).
  * Nút **"+ Thêm Nguồn RSS Mới"**: Modal nhập tên + URL RSS + chuyên mục $\rightarrow$ tự động kiểm tra cú pháp RSS (Health Check) trước khi lưu.
  * Nút Xóa / Tạm dừng (Toggle ON/OFF) từng nguồn độc lập.
* **Monitor Docker System 1:** Hiển thị trạng thái kết nối `http://127.0.0.1:8000/health`, **latency trung bình**, tải RAM/CPU/VRAM. Bộ chọn động cơ: `Auto-Detect`, `Laya GPU CUDA`, `Decision 3.0`, `Mock Engine`.
* **Cấu hình LLM System 2:** Cài đặt API Key (Gemini, OpenRouter, DeepSeek) hoặc địa chỉ Ollama Local.
* **Vòng đời dữ liệu:** Quota quét 500 bài/ngày, chính sách TTL 30 ngày (bảo vệ tuyệt đối Tech Vault), nút `🧹 Dọn Dẹp Ngay` và `💾 Thu Hồi Đĩa VACUUM`.
* **Tùy biến Thẩm mỹ Nhện:** Chọn skin nhện (Thủy tinh trong suốt, Giọt sương, Cơ khí thảo mộc).

### 7. 📊 Màn hình 7: Macro Analytics & Quantitative Chart Metrics (Thống Kê Định Lượng Vĩ Mô)
* **Bố cục Bento Grid 4-Card (2x2, gap 16):** Analytics Sidebar `240px` (Time Horizon `24h/7d/30d/90d`, phân khúc, Quick KPI Summary) → 4 thẻ biểu đồ `1640px`:
  1. **Chỉ Số Tâm Lý Thị Trường 30 Ngày** (Sentiment Step-Curve + Event Callout Pins).
  2. **Phân Phối Độ Trễ Suy Luận System 1** (Latency Histogram, P50/P95) — nguồn dữ liệu từ `laya_decisions.latency_ms`.
  3. **Cơ Cấu Chủ Đề Vĩ Mô Trọng Điểm** (Stacked Horizontal Ratio Bar + Momentum).
  4. **Ma Trận Nhiệt Từ Khóa Trọng Điểm 4x3** (Keyword Co-occurrence Heatmap).
* **Chỉ Số Định Lượng Tiết Kiệm Chi Phí:** So sánh mô hình thuần Cloud vs Hybrid Dual-System (token tiết kiệm, chi phí API/tháng).

---

## 📂 11. Cấu Trúc Thư Mục Dự Án Thực Tế (Project Scaffolding)

```
D:\code_tienich_forme\tintuc_quanhta\
├── backend/                  # Python FastAPI Service
│   ├── app.py                # Server chính & SSE Stream tọa độ
│   ├── rss_crawler.py        # Module cào RSS báo chí đa quốc gia
│   ├── github_crawler.py     # Module cào GitHub Trending & README
│   ├── laya_client.py        # Client async gọi Laya Docker port 8000 (System 1)
│   ├── llm_synthesizer.py    # Client gọi LLM tổng hợp & dịch tiếng Việt (System 2)
│   ├── database.py           # SQLite lưu bài báo, repo & hash chống trùng
│   └── requirements.txt
├── frontend/                 # Vite + React + TypeScript + GSAP + Tauri v2
│   ├── src/
│   │   ├── components/       # Bố cục 3 cột (Feed - Reader - Shelf & LLM Summary)
│   │   ├── spider/           # SVG Nhện Thảo Mộc + Bộ điều khiển GSAP
│   │   ├── audio/            # Âm thanh giọt nước, lật giấy (SFX)
│   │   └── tokens/           # Bảng màu Poetic Botanical (#FAF8F5, #2D4A2B...)
│   ├── src-tauri/            # Cấu hình Desktop Native (Rust + Tauri v2)
│   │   ├── tauri.conf.json   # Cấu hình cửa sổ không viền, System Tray, kích thước
│   │   └── Cargo.toml        # Rust dependencies cho Tauri v2
│   └── package.json
├── HUONG_DAN_KIEN_TRUC_SPIDER_RADAR.md
├── HUONG_DAN_CANVA_AI_VE_MAN_HINH.md
├── KE_HOACH_THIET_KE_DATABASE.md
└── README.md
```

---

## ⚡ 12. Chiến Lược Vận Hành Kỹ Thuật (Operational & Scraping Strategy)

### 12.1. Giao thức Truyền Tải: SSE (Server-Sent Events) + REST API
* **SSE (`/api/stream/spider-events`):** Backend đẩy một chiều dữ liệu tọa độ nhện bò, từ khóa mới, sự kiện âm thanh (`water_drop`) và sentiment xuống Frontend. Tự động kết nối lại khi rớt mạng, cực nhẹ và chuẩn HTTP.
* **REST API:** Dùng cho các tương tác rời rạc của người dùng (nút Skip, chọn lọc chủ đề, yêu cầu LLM System 2 dịch bài).

### 12.2. Chuẩn Hóa Biến Môi Trường (`.env`) Đa Nền Tảng
Hỗ trợ mọi nhà cung cấp LLM bên thứ 3 (OpenAI-compatible):
```ini
LAYA_BASE_URL=http://127.0.0.1:8000
LLM_PROVIDER=openrouter            # gemini, deepseek, groq, ollama
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your_api_key_here
LLM_MODEL_NAME=google/gemini-2.5-flash
GITHUB_TOKEN=your_github_token
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36
```

### 12.3. Đóng Gói Thành Desktop App Native Bằng Tauri v2
Chính thức lựa chọn **Tauri v2 (Rust + WebView2)** thay vì chạy trên trình duyệt web:
* **Siêu nhẹ:** File cài đặt `.exe` chỉ nặng khoảng **10MB – 15MB**, tiêu tốn chưa tới **30MB RAM**.
* **Trải nghiệm Desktop cao cấp:**
  * **Cửa sổ không viền (Frameless Window):** Tạo cảm giác một chiếc "bàn đọc tin tạp chí nổi" trên màn hình máy tính.
  * **Khay hệ thống (System Tray):** Thu nhỏ radar xuống góc phải màn hình, tự động bật thông báo Windows khi phát hiện Breaking News.
  * **Bảo mật tuyệt đối:** Giao tiếp giữa giao diện và hệ thống bằng Rust IPC an toàn.

### 12.4. Luật An Toàn Tuyệt Đối Cho Git / GitHub
* `.gitignore` bắt buộc loại trừ: `.env`, `.env.*`, `backend/data/*.db`, `*.log`, `target/` (Rust Tauri build).
* Tạo sẵn file mẫu `.env.example` an toàn với các khóa rỗng.
* Thiết lập Pre-commit hook chặn commit nếu phát hiện khóa bí mật (`sk-...`).

### 12.5. Chiến Lược Thu Thập Nguồn Tin & Vượt Paywall (Waterfall Pipeline 4 Tầng)
Hệ thống sử dụng cơ chế **Phễu Thác Nước 4 Tầng (Waterfall Ingestion Pipeline)** để đảm bảo: **Lấy tin sớm nhất - Đầy đủ nhất - Không bao giờ crash backend** (đồng bộ với AGENTS.md §2.4 — Plan A RSS chính đạo, Plan B 4 tầng dự phòng):

* **Tier 1 (Chính Đạo - Tốc Độ Chớp Nhoáng < 50ms):**
  * Ưu tiên số 1: Quét RSS / Atom Feeds trực tiếp từ các nguồn mở miễn phí, không yêu cầu đăng nhập hay giải mã:
    * *Kinh tế / Vĩ mô VN:* CaféF (`https://cafef.vn/kinh-te-vi-mo.rss`), VnExpress Kinh Doanh (`https://vnexpress.net/rss/kinh-doanh.rss`), Tuổi Trẻ Thế Giới (`https://tuoitre.vn/rss/the-gioi.rss`).
    * *Vĩ mô Toàn Cầu:* AP News Wire (`https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com`), CNBC Markets RSS, Trading Economics.
    * *GitHub Radar:* GitHub Trending Repositories & Release Feeds.
  * *Ưu điểm:* Ổn định 99.9%, độ trễ cực thấp, không tốn tài nguyên, không rủi ro bị chặn IP.

* **Tầng 1 - JSON-LD (Móc Thẻ Ngầm Qua SEO Backdoor < 200ms):**
  * Kích hoạt khi bài báo chỉ có link tóm tắt hoặc bị che nội dung:
    1. *Móc thẻ ngầm `JSON-LD`:* Trích xuất trực tiếp trường `articleBody` từ thẻ `<script type="application/ld+json">` trong HTML gốc (chỉ mất vài mili-giây regex, không cần render DOM).
    2. *Stateless Fetching:* Request không gửi Cookie, xóa sạch session tracking để vượt qua bộ đếm đọc thử 3–5 bài/tháng.

* **Tầng 2 - Proxy Đọc Sạch (< 800ms):** Kích hoạt khi Tầng 1 trả về HTTP 403/401/402 hoặc nội dung quá ngắn (< 100 từ): gọi *Jina Reader Engine* `https://r.jina.ai/{article_url}` để lấy Markdown sạch toàn văn, tự động lột bỏ toàn bộ paywall JS, pop-up quảng cáo.
* **Tầng 3 - Giả Mạo User-Agent Thân Thiện:** Gửi lại request với header trình duyệt thật `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36`, kèm `Accept: text/html,application/xhtml+xml`, `Accept-Language: vi,en-US;q=0.9`, `Referer` trang chủ nguồn tin.
* **Tầng 4 - Bản In / AMP / Cached:** Thử biến thể `<url>?output=1`, `<url>/amp`, rồi Google News cache hoặc text mirror.

* **Graceful Fallback (An Toàn Tuyệt Đối):**
  * Nếu cả 4 tầng trên đều không lấy được nội dung toàn văn: Lưu tiêu đề + mô tả tóm tắt ban đầu từ RSS, đánh dấu trạng thái `content_status = 'summary_only'`, ghi log `status = 'skipped'` kèm HTTP status và lý do.
  * **Tuyệt đối không để crash Scraper hay ngắt luồng SSE.** Nhện vẫn bò trên tiêu đề và mô tả có sẵn!

### 12.6. Quản Lý Quota Quét, Chống Quá Tải & Vòng Đời Dọn Dẹp Dữ Liệu (System Load Safeguards & Data Retention Policy)
> **Giải quyết triệt để bài toán:** *"Lượng tin cào mỗi ngày có bị quá tải không? Tin cũ lưu vào đâu và dọn dẹp như thế nào để không phình ổ đĩa hay tràn RAM?"*

Hệ thống thiết lập cơ chế kiểm soát tải đa tầng từ Ingestion đến Storage:

1. **Kiểm Soát Hạn Mức Cào Tin (Daily Ingestion Quota & Throttling):**
   * **Lọc trùng lặp cấp 1 (SHA-256 URL Hash):** Mọi URL bài viết được băm SHA-256 thành mã duy nhất (`url_hash` UNIQUE). Nếu URL đã tồn tại trong SQLite, server bỏ qua ngay lập tức trong 0.01ms mà không tải lại nội dung hay gọi AI.
   * **Hạn mức cào tin hàng ngày (Daily Quota):** Mặc định khống chế trần `MAX_ARTICLES_PER_DAY = 500 bài / ngày`.
   * **Giới hạn chu kỳ nguồn tin:** Mỗi nguồn RSS/API chỉ lấy tối đa 20 bài mới nhất mỗi chu kỳ 15 phút.
    * **Lọc rác siêu tốc Decision 3.0 Lite (Triage & Anti-Clickbait):** Các bài báo giật gân, quảng cáo hoặc không khớp tiêu chí Watchlist sẽ bị Decision 3 gán nhãn `status = 'skipped'` ngay tại tầng tensor GPU (< 50ms), hoàn toàn không gửi sang LLM System 2, tiết kiệm 100% chi phí token và điện toán.

2. **Cơ Chế Chống Tràn Hàng Đợi & Tiết Kiệm RAM (Queue Overflow & Buffer Policy):**
   * **Backend SSE Queue:** Sử dụng `asyncio.Queue(maxsize=100)`. Khi người dùng tạm ngưng đọc hoặc mạng lag khiến queue đạt 100 sự kiện, chính sách `drop_oldest` tự động loại bỏ các sự kiện cũ nhất để nhường chỗ cho tin mới nhất.
   * **Frontend DOM & Silk Filaments:**
     - Giới hạn đồng thời tối đa **2 sợi tơ nhện** trên màn hình (`max_active_filaments = 2`). Mỗi sợi tơ tự tiêu biến sau chu kỳ 1.2s.
     - Danh sách bài báo ở màn hình đọc tin áp dụng phân trang (Pagination 20 bài/trang) và Virtual Scrolling, giữ vững hiệu năng **60.0 FPS** và RAM chỉ dao động **20MB – 30MB**.

3. **Chiến Lược Lưu Trữ SQLite WAL & Dự Toán Dung Lượng:**
   * Cơ sở dữ liệu duy nhất: `backend/data/spider_radar.db` kích hoạt chế độ `PRAGMA journal_mode=WAL;`.
   * Vì hệ thống chỉ lưu text thuần túy đã khử HTML và metadata JSON, dung lượng trung bình chỉ **~3 KB / bài viết**.
   * Với 500 bài/ngày $\rightarrow$ Tốn ~1.5 MB/ngày $\rightarrow$ 1 tháng (15.000 bài) chỉ tốn **~45 MB**. Cực kỳ gọn nhẹ.

4. **Vòng Đời Xoay Vòng & Dọn Dẹp Tin Cũ Tự Động (TTL 30 Days Purging Lifecycle):**
   * **Chính sách 30 ngày:** Tin tức thông thường sau 30 ngày sẽ hết giá trị thời sự và tự động được dọn dẹp.
   * **Cron Job tự động chạy lúc 03:00 AM hàng ngày:**
     ```sql
     DELETE FROM articles 
     WHERE crawled_at < datetime('now', '-30 days') 
       AND is_bookmarked = 0;
     ```
   * **Ngoại lệ an toàn (Safe Bookmark Exception):** Các bài báo được người dùng nhấn **⭐ Bookmark / Lưu vào Tech Vault** (`is_bookmarked = 1`) sẽ **được giữ lại vĩnh viễn**, không bao giờ bị xóa.
   * **Thu hồi dung lượng đĩa (Incremental Vacuuming):**
     - Kích hoạt `PRAGMA auto_vacuum = INCREMENTAL;`.
     - Sau khi xóa tin cũ, chạy lệnh `PRAGMA incremental_vacuum;` để hoàn trả các megabyte đĩa trống cho Windows mà không khóa database.

---

## 🗺️ 13. Lộ Trình Phát Triển (Roadmap)

- [ ] **Giai đoạn 1: Core Data & Decision 3.0 Backend + LLM Synthesizer**
  - [x] Đóng gói thành công Docker container `vllm-sr/d3-serve:latest` (port 8000) trên GPU RTX 3050 CUDA 12.4.
  - [x] Lưu trữ vĩnh viễn 1.61 GB trọng số `vllm-sr/d3-lite` tại `D:\docker_data\d3-serve\model` và thiết lập `restart: "no"`.
  - [ ] Viết script FastAPI Python cào RSS kinh tế/chính trị & GitHub Trending (Tích hợp Waterfall Pipeline 4 tầng).
  - [ ] Tích hợp Decision 3 `/v1/systemone` cho bước lọc sơ tuyển và diệt giật tít.
  - [ ] Tích hợp LLM System 2 (Gemini Flash / OpenRouter) cho bước tổng hợp & dịch tiếng Việt.
  - [ ] Thiết lập SQLite lưu bài, kiểm tra trùng tin và Cron Job dọn dẹp TTL 30 ngày.
- [ ] **Giai đoạn 2: Khóa Asset Nhện & Concept Giao Diện**
  - [x] Tạo layout mẫu phong cách Poetic Wavy-Pastoral trong `spider_radar.pen` và xuất bộ ảnh 7 màn hình chi tiết.
  - [ ] Xuất file SVG nhện giọt sương / thảo mộc (tách layer chân và thân).
- [ ] **Giai đoạn 3: Frontend Vite React + GSAP Animation & Đóng Gói Tauri v2**
  - [ ] Dựng giao diện đọc tin phong cách Tạp chí ngà (`#FAF8F5`).
  - [ ] Lập trình GSAP cho nhện bò theo tọa độ DOM `getBoundingClientRect()`.
  - [ ] Kết nối luồng stream SSE `/api/stream/spider-events`.
  - [ ] Tích hợp và build Desktop App Native qua **Tauri v2** (`src-tauri/`).
- [ ] **Giai đoạn 4: Hoàn thiện Event Queue & Prefetching**
  - [ ] Kết nối luồng tin thời gian thực mượt mà, không giật lag.

---

## 📝 14. Nhật Ký Cập Nhật (Changelog & Notes)
* **2026-10-12 (10:55):** Nâng cấp đột phá công nghệ **System 1 từ Laya sang Decision 3.0 Lite (`vllm-sr/d3-lite`, 0.85B Qwen 3.5 Multimodal)**:
  - Khắc phục triệt để nguy cơ tràn context của Laya (Nâng native context từ 1,024 lên **32K+ tokens**).
  - Bổ sung **Bộ lọc Hải quan Chống Giật Tít (Anti-Clickbait & Substance Filter)**: Đối chiếu Title vs Body, loại bỏ 80% tin rác giúp tiết kiệm 80% chi phí gọi LLM System 2.
  - Hỗ trợ đa phương thức **Multimodal** (đọc hiểu cả biểu đồ nến, infographic, ảnh bìa).
  - Đóng gói Docker `vllm-sr/d3-serve:latest` chạy trực tiếp trên GPU **RTX 3050 (4GB VRAM)**, ăn ~1.8GB VRAM, phản hồi 30-60ms. Cấu hình `restart: "no"` để người dùng tự chủ bật/tắt thủ công (`docker start/stop d3-serve-1`).
  - Chuẩn hóa **Kiến trúc Cache 3 Tầng** (SHA-256 Hash -> SQLite Persistence -> Triton GPU Autotune & SafeTensors mmap).
* **2026-10-10 (00:15):** Định vị thành công Docker container `laya-laya-serve-1` (port 8000) và phân tích cấu trúc request Jev/System 1.
* **2026-10-10 (00:28):** Bổ sung phong cách Poetic Botanical Ink (từ `canva_skill/references/18-poetic-botanical-ink.md`), quy trình khóa asset nhện qua SVG/GSAP, và sơ đồ phối hợp 4 skill UI/UX.
* **2026-10-10 (00:30):** Bổ sung nguồn tin RSS cụ thể, thiết kế âm thanh giọt nước/lật giấy (SFX Foley), tính năng tương tác người dùng, và cấu trúc cây thư mục chi tiết.
* **2026-10-10 (00:34):** Nâng cấp kiến trúc **Hybrid AI System 1 (Laya) + System 2 (LLM Synthesizer dịch & tổng hợp tiếng Việt)**, mở rộng nguồn tin Đa Quốc Gia và bổ sung chế độ **"GitHub Radar Only"** cho Developer.
* **2026-10-10 (00:39):** Bổ sung đặc tả kiến trúc **5 màn hình chuẩn** (Main Radar, Executive Digest, GitHub Radar, Trend Vault, Settings Telemetry).
* **2026-10-10 (00:52):** Bổ sung giao thức truyền tải SSE, chuẩn cấu hình `.env` cho LLM bên thứ 3, luật bảo mật Git và chiến lược cào tin 4 tầng (§12.5).
* **2026-10-10 (00:56):** Chốt hạ giải pháp **Tauri v2 (Rust + WebView2)** làm Desktop App Shell chính thức (cửa sổ không viền, System Tray, file `.exe` ~15MB, RAM < 30MB).
* **2026-10-11 (23:55):** Hoàn thành thiết kế & đồng bộ toàn bộ hệ thống **7 màn hình** trong [`spider_radar.pen`](./spider_radar.pen) và ban hành bản đặc tả kỹ thuật chi tiết:
  - Xuất bộ ảnh 7 màn hình chuẩn độ phân giải cao vào thư mục [`pencil_exports/`](./pencil_exports/) (từ `01_...png` đến `07_macro_analytics_charts.png`).
  - Ban hành tài liệu [`DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md`](./DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md): Đặc tả chi tiết từng pixel, nút bấm, ma trận API, sự kiện client/server, 6 cụm biểu đồ định lượng và cây component React TypeScript phục vụ AI tự động sinh frontend.








