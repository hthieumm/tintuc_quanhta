# AGENTS.md — Hợp Đồng Kỹ Thuật Bất Biến Cho AI (Machine-Actionable Contract)

> **Mục tiêu:** Bản đặc tả kỹ thuật chuẩn xác, không chứa văn phong định tính, loại bỏ hoàn toàn mơ hồ, phục vụ AI Coding Agents (Claude Code, Cursor, Antigravity, Roo-Code) thực thi tự động.  
> **Nguyên tắc:** Single Source of Truth. Mọi bước thực thi đều phải kết thúc bằng **Tiêu chí nghiệm thu nhị phân (Pass/Fail Gate)** chạy được qua CLI.

---

## 1. RÀNG BUỘC KỸ THUẬT BẤT BIẾN (HARD INVARIANTS)

1. **Thị giác Con Nhện (Visual Engine):**
   * **Bắt buộc dùng SVG 2D Layered + GSAP.** Tuyệt đối không dùng Three.js hay WebGL 3D (tránh lỗi chiếu ma trận camera và cạnh tranh VRAM).
2. **Độ trễ & Pacing (Latency vs Visual Contract):**
   * **System 1 Inference Latency (đo trên NVIDIA GPU, hiển thị latency trung bình trong app):** `Laya RL Agent: 30ms – 60ms` (single-pass tensor, HTTP roundtrip < `70ms`) và `Decision 3.0 Lite: 150ms – 200ms` (NVIDIA GPU).
   * **Visual Pacing Delay:** Mặc định `pacing_delay_ms = 400` (Chế độ Laya/D3 Sync) và `pacing_delay_ms = 1200` (Chế độ Chill Mode).
3. **Phân Định Cổng Mạng (Port Allocation) & Hỗ Trợ Đa Động Cơ System 1:**
   * Port `8000`: Dành riêng cho Docker System 1 (`http://127.0.0.1:8000/v1/systemone`). Người dùng **bật/tắt thủ công** (Manual Toggle) giữa **Laya RL Agent** (`laya-laya-serve:latest`, chạy GPU CUDA, phản hồi 30ms – 60ms) hoặc **Decision 3.0** (`d3-serve-1`, chạy GPU NVIDIA, phản hồi 150ms – 200ms), không chạy song song để tránh xung đột cổng và tiết kiệm tối đa VRAM GPU. Payload gửi lên bắt buộc dùng trường `"state"` (chuỗi văn bản/tiêu đề + tóm tắt) và `"questions"` (typed choice/null).
   * Port `8001`: Dành riêng cho FastAPI Backend (`http://127.0.0.1:8001`).
   * Hệ thống hỗ trợ biến môi trường `SYSTEM1_ENGINE=auto|laya|d3|mock` và 2 REST endpoint điều khiển động: `GET /api/v1/system1/status`, `POST /api/v1/system1/select` (lưu cấu hình vào SQLite `system_settings`). Khi cả 2 container đều tắt, hệ thống tự động fallback sang High-Fidelity Mock Engine (0ms).
4. **Cơ Sở Dữ Liệu & Ràng Buộc Khóa (Database Integrity):**
   * File SQLite: `backend/data/spider_radar.db` (chế độ `PRAGMA journal_mode=WAL;`).
   * Bảng `llm_syntheses` bắt buộc có ràng buộc:
     `CHECK ((synthesis_type = 'single_deep_dive' AND (article_id IS NOT NULL OR repo_id IS NOT NULL)) OR (synthesis_type = 'executive_digest'))`
   * Bảng `laya_decisions` bắt buộc có ràng buộc:
     `CHECK (article_id IS NOT NULL OR repo_id IS NOT NULL)`
5. **Desktop App Framework:**
   * Bắt buộc dùng **Tauri v2** (`frontend/src-tauri`). Cấm dùng Electron.
6. **Bảo Mật Git:**
   * Cấm commit `.env`, `backend/data/*.db`, `*.log`, `frontend/src-tauri/target/`.
   * Pre-commit hook phải chặn mọi commit chứa regex: `(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})`.

---

## 2. ĐẶC TẢ CHI TIẾT CÁC THÀNH PHẦN TRUNG TÂM (CORE SPECS)

### 2.1. Hợp đồng tọa độ Con Nhện (Spider Coordinate Contract)
> **Nguyên tắc:** Server **KHÔNG** tính toán tọa độ pixel (vì không biết kích thước màn hình client). Server chỉ gửi định danh từ khóa; Frontend tự đo bằng `getBoundingClientRect()`.

```python
# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class SpiderEvent(BaseModel):
    event_id: str                          # UUIDv4
    article_id: int
    target_word: str                       # Từ khóa cần highlight (vd: "Lãi suất")
    target_index: int                      # Vị trí thứ tự của từ trong bài (0, 1, 2...)
    category: Literal["kinh_te", "chung_khoan", "vang", "crypto", "chinh_tri", "github", "quoc_te"]
    sentiment: Literal["positive", "negative", "neutral"]
    sentiment_color: Literal["#F8AFA6", "#C86D51", "#E5B869"]
    sfx_trigger: Literal["water_drop", "paper_rustle", "wind_chime"]
    pacing_delay_ms: int = 400             # Thời gian nhện dừng lại trước khi sang từ tiếp theo
```

* **Frontend DOM Binding & Hiệu Ứng Bắn Tơ (`frontend/src/components/SpiderCanvas.tsx`):**
  * **Bố cục SPIDER WEB ARENA:** Màn hình chính chia tỉ lệ **63%** (Không gian bài báo/Code) và **32%** (Vòng cung quyết định System 1), 5% còn lại là Bottom Telemetry Bar (Độ trễ trung bình, Tơ đã giăng, Token Matrix). Cột danh sách Feeds được thu vào ngăn kéo trượt (Slide-over Drawer) bên trái.
  * Mỗi từ khóa được render trong thẻ HTML: `<mark data-spider-index="0" data-word="Lãi suất">Lãi suất</mark>`.
  * **Hợp Đồng Hàng Đợi Hoạt Ảnh Tự Tiêu Thụ (FIFO Animation Queue & Anti-Miss Contract):**
    - Client tách rời hoàn toàn luồng nhận SSE và luồng diễn hoạt của nhện: Mọi `SpiderEvent` được đẩy vào `animationQueue` FIFO.
    - Nhện hoạt động như một Consumer độc lập, sử dụng `gsap.timeline({ onComplete: processNextEvent })`. Tuyệt đối không gọi `gsap.to()` rời rạc đè lên nhau gây giật lag hoặc miss từ khóa.
    - **Adaptive Pacing Engine (Bộ điều tốc 3 cấp tự thích ứng theo độ dài hàng đợi):**
      + `queue.length <= 4`: Giữ nhịp chuẩn `400ms` (hoặc `1200ms` Chill Mode).
      + `5 <= queue.length <= 12` (Sprint Mode): Tự động tăng tốc, rút ngắn duration còn `180ms – 220ms` / từ.
      + `queue.length > 12` (Fast-Forward): Nhện chỉ bò qua 3 từ then chốt, các từ phụ tự loang màu bằng CSS, nhện lướt sang bài tiếp theo.
  * **Quy chuẩn Sợi Tơ Tự Tiêu Biến (Transient Filament Lifecycle - Chống Rối Mắt):**
    - Độ dày nét tơ: Bắt buộc `stroke-width: 0.75px` đến `1.0px`, bán trong suốt `opacity: 0.6`.
    - Đường dẫn: Đường cong SVG Bezier nối từ chân nhện sang hộp đích bên phải.
    - Animation chu kỳ 1.2s: Phóng tơ (0.3s) $\rightarrow$ Hộp đích nhận xung chớp sáng $\rightarrow$ Tơ tự động mờ dần và remove khỏi DOM (`opacity: 0` trong 0.8s).
    - Giới hạn đồng thời: Tối đa **2 sợi tơ** cùng tồn tại trên màn hình (`max_active_filaments = 2`).
  * **Công Tắc Song Ngữ & Nguyên Tắc Con Nhện (Bilingual View Switcher Contract):**
    - **Sân Đấu Nhện (Spider Arena):** Hiển thị **100% bằng NGÔN NGỮ GỐC** để con nhện bò chuẩn xác trên thẻ từ khóa gốc `<mark>` do Decision 3.0 trích xuất.
    - **Dịch Lười Theo Yêu Cầu (On-Demand Translation):** Chỉ khi người dùng click mở bài và gạt nút `[● 🇻🇳 Tiếng Việt]`, hệ thống mới kích hoạt dịch máy theo từng đoạn (`<p> by <p>`) bằng `deep-translator` (0đ API, 0% VRAM), bảo toàn 100% cấu trúc HTML DOM.
    - **In-Memory RAM Cache:** Bản dịch toàn văn chỉ giữ trong RAM của Giao diện (React State) trong phiên làm việc, không lưu vào SQLite (trừ khi bài viết được Bookmark `is_bookmarked = 1`). Tráo đổi tức thì giữa `[🇻🇳 Tiếng Việt]` và `[🌐 Bản Gốc]` trong 0ms.


### 2.2. Hợp đồng Hàng đợi & SSE (Queue & SSE Contract)
* **Hàng đợi Backend:** `asyncio.Queue(maxsize=100)`.
* **Chính sách tràn hàng đợi (Overflow Policy):** Nếu queue đạt 100 phần tử, tự động loại bỏ phần tử cũ nhất (`drop_oldest`) để nhường chỗ cho tin mới nhất.
* **Header SSE:**
  * `Content-Type: text/event-stream`
  * `Cache-Control: no-cache`
  * `Connection: keep-alive`
* **Heartbeat:** Server tự động gửi comment `: ping\n\n` mỗi 15 giây để duy trì kết nối.
* **Phục hồi kết nối (Reconnection):** Server duy trì Ring Buffer 50 sự kiện gần nhất; hỗ trợ header `Last-Event-ID` để phát lại các sự kiện bị lỡ khi client mất mạng.

### 2.3. Hợp đồng REST API cho LLM System 2
Ngoài luồng SSE một chiều, Backend cung cấp 2 REST endpoint phục vụ người dùng tương tác:

1. **Deep Dive Tin Lẻ:**
   * `POST /api/v1/synthesize/article`
   * Body: `{"article_id": 12}`
   * Response 200:
     ```json
     {
       "article_id": 12,
       "vietnamese_title": "string",
       "vietnamese_summary": "string",
       "macro_impact": "string",
       "confidence_score": 0.95
     }
     ```
2. **Bản Tin Tổng Hợp Vĩ Mô Đa Khung (Modular Executive Digest):**
   * `POST /api/v1/synthesize/digest`
   * Body: `{"date": "2026-10-10", "category": "all"}`
   * Response 200:
     ```json
     {
       "digest_date": "2026-10-10",
       "total_articles": 42,
       "market_sentiment_score": 0.65,
       "macro_economy_panel": {
         "title": "Toàn Cảnh Kinh Tế & Dòng Tiền",
         "highlights": ["FED giữ lãi suất", "Tỷ giá USD/VND hạ nhiệt"],
         "narrative_markdown": "Phân tích vĩ mô chi tiết..."
       },
       "geopolitics_panel": {
         "title": "Toàn Cảnh Chính Trị & Địa Chính Trị",
         "highlights": ["Chính sách thương mại EU", "Bầu cử"],
         "narrative_markdown": "Phân tích chính sách..."
       },
       "github_tech_panel": {
         "title": "Đột Phá Công Nghệ AI & GitHub",
         "top_repos": ["NandhaKishorM/laya"],
         "narrative_markdown": "Phân tích công nghệ mã nguồn mở..."
       },
       "chart_metrics": {
         "category_ratio": {"kinh_te": 0.45, "chinh_tri": 0.30, "github": 0.25},
         "sentiment_sparkline": [0.2, 0.4, 0.5, 0.65]
       }
     }
     ```


3. **Quản Lý Nguồn Tin Động (Dynamic Feed Manager Endpoints):**
   * `GET /api/v1/sources`: Lấy danh sách toàn bộ nguồn tin kèm trạng thái `is_active`, số bài đã cào và lần cập nhật cuối.
   * `POST /api/v1/sources`: Thêm nguồn RSS mới (`{"name": "...", "url": "...", "category": "chung_khoan|vang|crypto|kinh_te"}`). Server bắt buộc tự động kiểm tra tính hợp lệ của RSS (Validate HTTP 200 & XML format) trước khi ghi vào SQLite.
   * `PATCH /api/v1/sources/{source_id}/toggle`: Bật/Tắt quét một nguồn (`is_active = 0/1`).
   * `DELETE /api/v1/sources/{source_id}`: Xóa hẳn một nguồn tin khỏi hệ thống.

4. **Quản Lý Chủ Đề Watchlists Động (Zero-Code Dynamic Watchlists):**
   * `GET /api/v1/watchlists`: Lấy danh sách các chủ đề đang active (Chiến tranh, Giá dầu, Vàng, Bán dẫn...).
   * `POST /api/v1/watchlists`: Thêm chủ đề mới kèm danh sách từ khóa và prompt tiêu chí Laya (`{"topic_code": "gia_dau", "display_name": "...", "keywords": [...], "criteria": "..."}`). Lập tức tự sinh Node trên frontend và criteria cho Laya mà không cần sửa code.
   * `DELETE /api/v1/watchlists/{id}`: Xóa hoặc tạm ẩn một chủ đề.

5. **Tìm Kiếm Toàn Văn Toàn Bộ Kho Tin (Instant FTS5 Search):**
   * `GET /api/v1/search?q={query}`: Tra cứu toàn văn bất kỳ từ khóa ngẫu nhiên nào qua SQLite FTS5, trả về kết quả trong < 2ms.


### 2.4. Chính sách Cào Tin: Plan A (Chính Đạo) vs Plan B (Dự Phòng)
* **Plan A (Mặc định bắt buộc):** Chỉ cào RSS công khai sạch không yêu cầu đăng nhập:
  * CaféF Vĩ Mô (`https://cafef.vn/kinh-te-vi-mo.rss`)
  * VnExpress Kinh Doanh (`https://vnexpress.net/rss/kinh-doanh.rss`)
  * Tuổi Trẻ Thế Giới (`https://tuoitre.vn/rss/the-gioi.rss`)
  * AP News Top Stories (`https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com`)
* **Plan B (Chỉ kích hoạt khi Plan A trả về HTTP 403/401/402, Cloudflare challenge, hoặc nội dung < 100 từ):**
  1. **Tầng 1 - JSON-LD:** Thử cào thẻ ngầm `<script type="application/ld+json">`.
  2. **Tầng 2 - Proxy đọc sạch:** Thử gọi `https://r.jina.ai/{url}`.
  3. **Tầng 3 - Giả mạo User-Agent thân thiện:** Gửi lại request với header trình duyệt thật
     `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36`,
     kèm `Accept: text/html,application/xhtml+xml`, `Accept-Language: vi,en-US;q=0.9`, `Referer` trang chủ nguồn tin.
  4. **Tầng 4 - Bản in / AMP / Cached:** Thử biến thể `<url>?output=1`, `<url>/amp`, rồi `Google News` cache hoặc text mirror.
  5. **Nếu cả 4 tầng thất bại:** Ghi log `status = 'skipped'` kèm HTTP status và lý do, **TUYỆT ĐỐI KHÔNG CRASH BACKEND**.

---

## 3. CÔNG THỨC THỰC THI & CÁC GATE KIỂM TRA TỰ ĐỘNG (CLI VERIFIABLE GATES)

AI Agent phải tuân thủ nghiêm ngặt 7 Gate dưới đây. Mỗi Gate bắt buộc phải có lệnh kiểm tra nhị phân (Exit code 0 = PASS; khác 0 = FAIL):

### 📍 GATE 1: Khởi Tạo Dự Án & Kiểm Tra Secret Guardrails
* **Tác vụ:** Tạo cấu trúc thư mục, `requirements.txt`, `.gitignore`, `.env.example`, và cài đặt git pre-commit hook.
* **Lệnh kiểm tra:**
  ```powershell
  python -c "
  import os, re
  assert os.path.exists('backend/.env.example'), 'Missing .env.example'
  with open('backend/.env.example') as f:
      content = f.read()
  for key in ['LAYA_BASE_URL', 'LLM_PROVIDER', 'LLM_API_KEY', 'LLM_MODEL_NAME']:
      assert key in content, f'Missing {key} in .env.example'
  print('GATE 1: PASS')
  "
  ```

### 📍 GATE 2: Database Migration & Ràng Buộc CHECK
* **Tác vụ:** Viết `backend/database.py` khởi tạo 7 bảng và viết test kiểm tra ràng buộc chống row mồ côi.
* **Lệnh kiểm tra:**
  ```powershell
  pytest backend/tests/test_database.py -v
  ```
  *(File test phải assert `sqlite3.IntegrityError` khi insert vào `llm_syntheses` với `synthesis_type='single_deep_dive'` mà cả `article_id` và `repo_id` đều là NULL).*

### 📍 GATE 3: Laya / Decision 3 Client, Liveness & Benchmark Verification
* **Tác vụ:** Viết `backend/ensure_laya.py` kiểm tra Docker port 8000; hỗ trợ payload chuẩn `state` cho container `d3-serve-1` (`vllm-sr/d3-serve:latest`). Bộ test benchmark tự động tại `backend/tests/test_benchmark_d3.py` và suite đo tải `backend/benchmark_d3.py`.
* **Lệnh kiểm tra:**
  ```powershell
  python backend/ensure_laya.py --check-health && pytest backend/tests/test_benchmark_d3.py -v
  ```
  *(Yêu cầu: Exit code 0, in ra `LAYA SERVICE READY` và 2 tests passed).*
* **Lệnh chạy Benchmark đầy đủ:**
  ```powershell
  python backend/benchmark_d3.py --warm-runs 5 --stress-samples 6 --concurrencies "1,2,4"
  ```
  *(Xuất báo cáo tại `backend/data/d3_benchmark_report.md` và `backend/data/d3_benchmark_report.json`).*

### 📍 GATE 4: Test Khử Trùng Bài Viết (Deduplication Assertion)
* **Tác vụ:** Viết `backend/rss_crawler.py` và test case `backend/tests/test_scraper.py`.
* **Lệnh kiểm tra:**
  ```powershell
  pytest backend/tests/test_scraper.py -v
  ```
  *(Test case phải thực hiện: Cào 1 feed mẫu lần 1 $\rightarrow$ Đếm số row tăng $N$; cào lại feed đó lần 2 $\rightarrow$ Assert số row tăng thêm bằng $0$).*

### 📍 GATE 5: Test Tích Hợp SSE Stream & REST API
* **Tác vụ:** Viết `backend/app.py` chứa endpoint SSE `/api/stream/spider-events` và 2 endpoint tổng hợp tin.
* **Lệnh kiểm tra:**
  ```powershell
  pytest backend/tests/test_api_sse.py -v
  ```
  *(Test case sử dụng `httpx.AsyncClient` kiểm tra stream nhận đúng format `data: {...}\n\n` và header `text/event-stream`).*

### 📍 GATE 6: Typecheck & Build Frontend
* **Tác vụ:** Dựng giao diện React TypeScript với component con nhện SVG + GSAP.
* **Lệnh kiểm tra:**
  ```powershell
  npm --prefix frontend run typecheck && npm --prefix frontend run build
  ```
  *(Yêu cầu: Exit code 0, không có lỗi TypeScript hay bundle failure).*

### 📍 GATE 7: Headless Compile & Configuration Verification Cho Tauri v2
* **Tác vụ:** Cấu hình `frontend/src-tauri` (`Cargo.toml`, `tauri.conf.json`, `src/lib.rs` / `src/main.rs`).
* **Lệnh kiểm tra:**
  ```powershell
  python -c "
  import json, os, subprocess, shutil
  assert os.path.exists('frontend/src-tauri/tauri.conf.json'), 'Missing tauri.conf.json'
  assert os.path.exists('frontend/src-tauri/Cargo.toml'), 'Missing Cargo.toml'
  with open('frontend/src-tauri/tauri.conf.json', encoding='utf-8') as f:
      conf = json.load(f)
  assert 'app' in conf or 'bundle' in conf, 'Invalid tauri.conf.json schema'
  if shutil.which('cargo'):
      res = subprocess.run(['cargo', 'check', '--manifest-path', 'frontend/src-tauri/Cargo.toml'])
      assert res.returncode == 0, 'Cargo check failed'
      print('GATE 7: PASS (Cargo Check Passed)')
  else:
      print('GATE 7: PASS (Tauri Configuration Verified - Install Rust via rustup to build .exe)')
  "
  ```
  *(Yêu cầu: Exit code 0, xác thực file cấu hình Tauri v2 chuẩn xác và Rust compiler nếu có).*

---

## 4. CONTEXT POINTERS
* Khi cần tra cứu đặc tả chi tiết 7 màn hình, nút bấm, ma trận API và component mapping: Tham chiếu [`DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md`](./DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md) và file vẽ gốc [`spider_radar.pen`](./spider_radar.pen).
* Khi cần tra cứu màu sắc, font chữ, layout %: Tham chiếu [`HUONG_DAN_CANVA_AI_VE_MAN_HINH.md`](./HUONG_DAN_CANVA_AI_VE_MAN_HINH.md).
* Khi cần xem toàn văn câu lệnh SQL DDL: Tham chiếu [`KE_HOACH_THIET_KE_DATABASE.md`](./KE_HOACH_THIET_KE_DATABASE.md).
* Khi cần tra cứu bối cảnh kiến trúc tổng thể: Tham chiếu [`HUONG_DAN_KIEN_TRUC_SPIDER_RADAR.md`](./HUONG_DAN_KIEN_TRUC_SPIDER_RADAR.md).

