# 🕷️ SPIDER NEWS RADAR (Tin Tức Quanh Ta)

> Hệ thống radar quét và phân tích tin tức kinh tế - chính trị - tài chính tự động, tích hợp trực quan hóa bằng **Sân Đấu Giăng Tơ "Spider Web Arena" (SVG 2D Layered + GSAP)** lấy cảm hứng từ trend TikTok, điều khiển bởi **System 1 (Laya RL Agent `laya-laya-serve:latest` 30–60ms | Decision 3.0 Lite `vllm-sr/d3-lite` 150–200ms NVIDIA GPU | Mock 0.5ms)** và **System 2 LLM Synthesizer (Gemini Flash)**, đóng gói máy tính native qua **Tauri v2**.

---

## 📚 HỆ THỐNG TÀI LIỆU CHÍNH THỨC (SINGLE SOURCE OF TRUTH)

* 🤖 **[HỢP ĐỒNG THỰC THI CHO AI AGENT (AGENTS.md)](./AGENTS.md)** ⭐ *(Bắt buộc đọc trước khi code — Chứa các CLI Verifiable Gates nhị phân, schemas, DOM binding contracts)*  
* 🏛️ **[Hướng Dẫn Kiến Trúc & Kỹ Thuật Chi Tiết](./HUONG_DAN_KIEN_TRUC_SPIDER_RADAR.md)** *(Kiến trúc Hybrid 2 tầng, Decision 3.0 Lite Multimodal, Waterfall Pipeline 4 tầng, Watchlist động Zero-Code, Cache 3 tầng)*  
* 🎨 **[Hướng Dẫn Canva AI Vẽ Màn Hình Desktop UI (16:9)](./HUONG_DAN_CANVA_AI_VE_MAN_HINH.md)** *(Quy tắc vẽ giao diện phần mềm chống biến thành slide, 3 bảng màu Light/Dark/Swiss, tọa độ % và prompt tiếng Anh)*  
* 🗄️ **[Kế Hoạch Thiết Kế Database SQLite WAL & FTS5](./KE_HOACH_THIET_KE_DATABASE.md)** *(Sơ đồ ERD 9 bảng, ràng buộc CHECK chống row mồ côi, bảng ảo FTS5 tra cứu siêu tốc < 2ms)*  

---

## ⚡ CÁC TÍNH NĂNG ĐỘT PHÁ CỦA DỰ ÁN

### 1. 🕸️ Sân Khấu "SPIDER WEB ARENA" (Bản Đồ Giăng Tơ 63% – 32%)
* **Không gian mênh mông (63% Text/Code Canvas):** Con nhện có toàn bộ trang báo giấy ngà `#FAF8F5` để tự do di chuyển, lướt qua các từ khóa `<mark>` và code blocks mà không bị nhốt trong khung hẹp.
* **Vũ đạo Giăng Tơ Bezier Vút Dài (Web Casting):** Phóng các sợi tơ ánh sáng siêu mảnh (`0.75px`, tự tiêu biến sau 1.2s, tối đa 2 tơ đồng thời) bay vút qua khoảng trống 300px găm thẳng vào các **Node Quyết Định** bên phải.
* **Ngăn Kéo Trượt (Slide-over Feed Drawer):** Dòng tin đa nguồn giấu gọn ở lề trái, trượt ra chọn bài rồi tự động thu lại trả trọn vẹn sân khấu cho nhện diễn.
* **Thanh Chỉ Số Đáy (Bottom Telemetry Bar):** Tái hiện trọn vẹn phong cách công nghệ: `[⚡ Độ trễ Decision 3: 45ms] • [🕸️ Tơ đã giăng: 6/14] • [🧮 Ma trận Token Đã Đọc: ●●●●●●○○○○○○○○] • [⏱️ 60 FPS]`.

### 2. 🛢️ Hệ Thống Linh Động 100% Zero-Code (Dynamic Sources & Topic Watchlists)
* **Không cần sửa một dòng code nào:**
  * **Thêm/Bớt nguồn tin RSS tùy ý:** Nhập link báo bất kỳ (OilPrice, Al Jazeera, Vietstock...), backend tự kiểm tra (Health check) và cào tự động.
  * **Thêm chủ đề theo dõi mới (Chiến tranh, Giá dầu, Bán dẫn, Vàng nhẫn...):** Người dùng chỉ cần tạo trên UI hoặc DB $\rightarrow$ Vòng cung bên phải tự mọc thêm Node mới $\rightarrow$ Decision 3 System 1 tự nhận criteria $\rightarrow$ Nhện tự phóng tơ vào Node đó!
  * **Tra cứu tức thời qua SQLite FTS5:** Tìm kiếm toàn văn hàng chục nghìn bài báo đã lưu trong **dưới 2 mili-giây**.

### 3. 🧠 Kiến Trúc Hybrid Hai Tầng AI Tối Ưu Chi Phí & Tài Nguyên
* **Tầng 1 (System 1 - Decision 3.0 Lite):** 
  * Chạy Docker GPU local port 8000 (`vllm-sr/d3-serve:latest`, RTX 3050 CUDA 12.4).
  * **Qwen 3.5 0.85B Multimodal:** Đọc trọn vẹn bài báo dài (Context native 32K+ tokens, không bao giờ bị cắt cụt hay tràn context).
  * **Hải quan diệt giật tít (Anti-Clickbait Gatekeeper):** Đọc đối chiếu Tiêu đề vs Nội dung, loại bỏ 80% tin giật gân/PR vô thưởng vô phạt ngay trên máy, giúp **tiết kiệm 80% chi phí API LLM**.
  * **Đa phương thức (Multimodal):** Đọc được cả hình ảnh bìa báo, biểu đồ nến chứng khoán, infographic giá vàng, video tin tức.
   * **Cực nhẹ:** Chỉ ăn ~1.8GB VRAM (nằm trọn trong 4GB VRAM RTX 3050), **Laya 30–60ms / Decision 3.0 150–200ms (NVIDIA GPU)**, cấu hình `restart: "no"` để người dùng tự do bật/tắt thủ công khi cần. Backend hiển thị **latency trung bình** trên Bottom Telemetry Bar và `GET /api/v1/system1/status`.
* **Tầng 2 (System 2 - LLM Synthesizer):** Gemini Flash / DeepSeek dịch chuẩn tiếng Việt văn phong tài chính, giải thích tác động vĩ mô theo từng tin lẻ hoặc tạo **Bản Tin Tạp Chí Vĩ Mô Toàn Cảnh** 3 khung chuyên biệt.

### 4. 🛡️ Cơ Chế Cache 3 Tầng Giảm Tải Tuyệt Đối Cho Phần Cứng
* **Tầng 1 (Input Deduplication Hash):** Băm SHA-256 URL bài báo, loại bỏ tin trùng lặp trong 0.1ms, GPU không phải chạy lại bài cũ.
* **Tầng 2 (Result Persistence):** Lưu vĩnh viễn phân loại và bản dịch vào SQLite `spider_radar.db`. Đọc lại bài cũ trong < 1ms, 0% CPU/GPU.
* **Tầng 3 (GPU Hardware Cache):** Triton CUDA Autotune (`TRITON_CACHE_AUTOTUNING=1`) và SafeTensors Zero-Copy mmap trực tiếp từ ổ `D:\docker_data\d3-serve\model`.

### 5. 🎨 3 Bộ Màu Chủ Đạo Đẳng Cấp Phần Mềm (Screen-First Palettes)
* 🌿 **Poetic Botanical Ink (Mặc định):** Nền giấy ngà `#FAF8F5`, chữ xanh rừng sâu `#2D4A2B`, nhấn đào `#F8AFA6`, vàng `#E5B869`.
* 🌌 **Dark Cyber-Botanical (Dark Mode):** Đen than chì `#121513`, chữ bạc ánh xanh `#E8EFE8`, tơ nhện lục bảo dạ quang `#00E676`.
* 🏛️ **Swiss Financial Monochrome:** Chuẩn báo *Financial Times* / *Wall Street Journal*, tối giản typography grid.

### 6. 💻 Nền Tảng Desktop Native (Tauri v2)
* Đóng gói bằng Rust + WebView2 (`.exe` ~15MB, RAM < 30MB).
* Cửa sổ không viền (Frameless floating window), chạy ngầm góc khay hệ thống (System Tray), bật thông báo Windows khi có Breaking News.
