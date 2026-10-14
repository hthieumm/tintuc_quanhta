# ĐẶC TẢ CHI TIẾT THIẾT KẾ 7 MÀN HÌNH & GIAO DIỆN NGƯỜI DÙNG (FRONTEND DESIGN SPECIFICATION)
> **Dự án:** Spider News Radar (Tin Tức Quanh Ta)  
> **Phiên bản:** v2.5.0 (Native Desktop App — Tauri v2 + React TypeScript + GSAP)  
> **Mục tiêu:** Bản đặc tả kỹ thuật chi tiết nhất về giao diện, cấu trúc DOM/Component, hệ thống Design Tokens, sự kiện tương tác của từng nút bấm và phụ lục kỹ thuật để các AI Coding Agents (Claude Code, Cursor, Antigravity, Roo-Code) lập trình Frontend chính xác 100% mà không bị ảo giác.  
> **Single Source of Truth:** Tương thích hoàn toàn với file thiết kế Canvas [`spider_radar.pen`](file:///d:/code_tienich_forme/tintuc_quanhta/spider_radar.pen) và hợp đồng kỹ thuật [`AGENTS.md`](file:///d:/code_tienich_forme/tintuc_quanhta/AGENTS.md).

---

## 1. HỆ THỐNG DESIGN TOKENS & NGUYÊN TẮC THẨM MỸ (POETIC BOTANICAL INK)

Hệ thống giao diện tuân thủ phong cách **Poetic Botanical Ink (18-F & 18-G)**: Kết hợp giữa nét đẹp trang nhã của giấy dó truyền thống, gốm sứ và trạm thông tin tình báo tri thức hiện đại.

### 1.1. Bảng Màu Chuẩn (Color Palette Tokens)
| Tên Token | Mã Hex | Tỷ lệ sử dụng | Mục đích sử dụng | Tiêu chuẩn tương phản |
|---|---|---|---|---|
| `bg-primary` | `#F4F1EA` / `#FAF8F5` | 60% | Nền canvas ứng dụng, giấy ngà ấm dịu mắt | Nền tảng chống mỏi mắt |
| `surface-white` | `#FFFFFF` | 30% | Nền các thẻ bài báo, bảng điều khiển, tấm ArXiv, thẻ đồ thị | Trắng sứ tinh khiết |
| `surface-panel` | `#EBE6DC` | — | Nền TopBar, Sidebar, BottomBar | Phân tách khu vực điều hướng |
| `surface-highlight` | `#FBF9F5` | — | Nền các khối callout, trích dẫn, code background phụ | Giấy cói cao cấp |
| `border-subtle` | `#DCD5C5` | — | Đường viền panels, divider hairline 1px | Tách khối mềm mại |
| `border-card` | `#EBE6DC` | — | Viền trong của các thành phần con | Tách viền nhẹ |
| `text-primary` | `#2D4A2B` | 10% | Tiêu đề chính, nhãn quan trọng, điểm nhấn rêu rừng | **11.9:1 (PASS AAA)** |
| `text-secondary` | `#4A6647` / `#5A6B5C` | — | Chữ mô tả, thông số phụ, breadcrumbs | **4.8:1 (PASS AA)** |
| `text-muted` | `#8A9A86` | — | Placeholder, dấu phân cách, text mờ | Chữ bổ trợ |
| `accent-good` | `#1B5E20` / `#E8F0E8` | — | Tích cực, thị trường xanh, Decision 3 Lite Online, node ổn định | Tông thảo mộc xanh lá |
| `accent-risk` | `#C86D51` / `#FDF2EE` | — | Rủi ro, biến động, cảnh báo địa chính trị, xóa tin RSS | Tông đất nung Terracotta |
| `accent-amber` | `#E5B869` / `#FFF8E1` | — | Vàng SJC, token nhện bắn tơ, Tech Vault bookmark | Tông hổ phách hoàng kim |
| `accent-tech` | `#4A6B82` / `#EAF1F7` | — | Công nghệ AI, GitHub, WebAssembly | Tông xanh đá bảng Slate |
| `code-bg` | `#1E2621` | — | Nền khối code snippet trong README | Đen rêu kỹ thuật cổ điển |
| `code-text` | `#E2F0D9` | — | Chữ mã nguồn Python / Rust | Trắng ánh lục bảo |

### 1.2. Hệ Thống Font Chữ (Typography Tokens)
* **Font Tiêu Đề Lớn (Serif Headings):** `Playfair Display` (hoặc `Fraunces`), `font-weight: 700`.  
  * Kích thước: `18px – 24px` (Headings chính 20px, sub-headings 15px - 18px; giữ chuẩn tỷ lệ desktop app).
* **Font Nội Dung & Nhãn Giao Diện (Body & UI):** `Be Vietnam Pro`, `font-weight: 400, 500, 600`.  
  * Kích thước: Body đạt chuẩn đọc `13px – 14px`, Line-height `1.6 – 1.7` (Đảm bảo độ tương phản AA rõ nét, không bị mờ).
* **Font Kỹ Thuật, Code & Dữ Liệu (Telemetry & Code):** `JetBrains Mono` (hoặc `Fira Code`), `font-weight: 400, 700`.  
  * Kích thước: `10px – 11.5px`, dùng cho độ trễ (latency), số lượng token, SHA-256 hash, mã lệnh code, trục biểu đồ.

### 1.3. Khung Kích Thước & Bo Góc Chuẩn (Geometry & Spatial Tokens)
* **Độ phân giải chuẩn:** `1920px x 1080px` (Không cuộn toàn trang, nội dung cuộn nội bộ bên trong các container con).
* **Padding viền ngoài:** `12px`, khoảng cách khối `gap: 10px – 12px`.
* **Cấu trúc 3 dải ngang cố định:**
  1. `Top Window Header Bar`: Cao `48px`.
  2. `Main Viewport Container`: Cao `940px`, layout `horizontal`, khoảng cách `gap: 12px`.
  3. `Bottom Telemetry Bar`: Cao `44px`, nền `#F0F5EA`, viền `#DCD5C5`, chữ `#2D4A2B` đậm (AAA).
* **Quy chuẩn Bo Góc Bất Biến (Locked Radii Standards):**
  * Thẻ nội dung / Khung Dashboard (Cards / Containers): Cố định `cornerRadius: 12px`.
  * Nút bấm dạng viên con nhộng / Badges (Pill Buttons / Status Badges): Cố định `cornerRadius: 999px`.

---

## 2. APP CHROME TOÀN CỤC (GLOBAL SHELL & NAVIGATION)

Cả 7 màn hình đều dùng chung App Chrome cố định bao gồm **Top Window Header Bar**, **Left Navigation** và **Bottom Telemetry Bar**.

### 2.1. Top Window Header Bar (Thanh Điều Hướng Đỉnh — Cao 48px)
* **Bố cục Flexbox:** `layout: horizontal`, `justify-content: space-between`, `align-items: center`, `padding: 8px 16px`, `background: #EBE6DC`, `border: 1px solid #DCD5C5`, `border-radius: 12px`.
* **Phần bên trái (Top Left):**
  * 3 nút tròn macOS Window Controls: Đỏ `#E06C75` (Close), Vàng `#E5C07B` (Minimize), Xanh `#98C379` (Maximize) — đường kính `11px`, `gap: 6px`.
  * Tiêu đề ứng dụng: `SPIDER RADAR` (`Playfair Display`, 13px, bold, `#2D4A2B`).
  * Dấu chấm phân cách: `•` (`#8A9A86`).
  * Phụ đề chế độ: Tên màn hình hiện tại (`JetBrains Mono`, 11px, `#5A6B5C`).
* **Phần trung tâm (Center Navigation Tabs — 7 Tabs Toàn Cục):**
  * 7 nút Tab chuyển trang toàn cục (Pill buttons, `cornerRadius: 999px`):
    1. `○ 🕸️ SPIDER ARENA` $\rightarrow$ Chuyển sang Screen 1
    2. `○ 📑 DÒNG TIN ĐÃ LỌC` $\rightarrow$ Chuyển sang Screen 2
    3. `○ 📰 EXECUTIVE DIGEST` $\rightarrow$ Chuyển sang Screen 3
    4. `○ 📊 BIỂU ĐỒ & CHỈ SỐ` $\rightarrow$ Chuyển sang Screen 7
    5. `○ 🐙 GITHUB TECH` $\rightarrow$ Chuyển sang Screen 4
    6. `○ 🌳 TREND VAULT` $\rightarrow$ Chuyển sang Screen 5
    7. `○ ⚙️ CÀI ĐẶT` $\rightarrow$ Chuyển sang Screen 6
  * **Trạng thái Tab:**
    * *Tab Active:* `background: #2D4A2B`, `color: #F4F1EA`, `font-weight: bold`, tiền tố `●`.
    * *Tab Inactive:* `background: transparent`, `color: #5A6B5C`, `hover: background: #E2DCD0`, tiền tố `○`.
* **Phần bên phải (Top Right Telemetry):**
  * Badge Chế độ hoạt động (Badge xám ngà `#E2DCD0`).
  * Badge Trực tiếp Decision 3 Lite: `⚡ Decision 3: 5.4ms - 14ms` / `DECISION 3 LITE: 8.5ms ONLINE` (`#E8F0E8`, viền `#2D4A2B`, chữ `#1B5E20`).
  * Badge Trạng thái mạng: `🟢 HOÀN TẤT` / `🟢 THEO DÕI ACTIVE`.

### 2.2. Phân Bổ Điều Hướng Trái (Spatial Logic & Action Hierarchy)
* **Thiết Kế Icon-Rail Tối Ưu Dominant Region (Màn hình 1, 5, 6 — Rộng 64px):**
  * Thu nhỏ thành thanh icon-rail dọc `64px` gồm các icon điều hướng nhanh, chừa trọn không gian cho Vùng Trọng Tâm (Dominant Center `1450px`).
  * Khi người dùng nhấp vào biểu tượng danh sách, ngăn kéo trượt **Slide-over Feeds Drawer** sẽ mở ra mượt mà mà không làm xô lệch bố cục chính.
* **Cột Sidebar Chi Tiết (Màn hình 2, 3, 4, 7 — Rộng 240px):**
  * Rộng `240px`, Cao `fill_container` (940px), `background: #EBE6DC`, `border: 1px solid #DCD5C5`, `border-radius: 12px`, `padding: 14px`, `gap: 12px`.
  * Đảm nhiệm các bộ lọc sâu (FTS5 search, chuyên mục vĩ mô, ngày phát hành bản tin, chỉ số repo...).

### 2.3. Bottom Telemetry Bar (Thanh Giám Sát Đáy — Cao 44px)
* **Bố cục Flexbox:** `layout: horizontal`, `justify-content: space-between`, `align-items: center`, `padding: 10px 16px`, `background: #F0F5EA`, `border: 1px solid #DCD5C5`, `border-radius: 12px`.
* Chứa 3 khối thông tin telemetry giám sát hệ thống thời gian thực theo chuẩn `JetBrains Mono` 11px chữ đậm màu rêu `#2D4A2B` (Đạt chuẩn tương phản AAA):
  * **Trái:** `ĐỘNG CƠ: DECISION 3 LITE (SYSTEM 1) • ĐỘ TRỄ: 5.4ms • DUAL-SYSTEM GEMINI 2.5 ACTIVE`.
  * **Giữa:** `TRẠNG THÁI: THEO DÕI ACTIVE • CÀO TIN: 15 PHÚT/LẦN • ĐÃ QUÉT: 342/500 BÀI`.
  * **Phải:** `SQLITE WAL: 14.2 MB • FTS5: 4.8 MB • TECH VAULT: 48 BÀI BẢO VỆ`.

---

## 3. ĐẶC TẢ CHI TIẾT TỪNG MÀN HÌNH (SCREEN-BY-SCREEN SPECIFICATIONS)

---

### 📍 MÀN HÌNH 1: SPIDER WEB ARENA (ĐẤU TRƯỜNG NHỆN QUÉT BÁO CÁO GỐC)
* **Node ID trong Pencil:** `R7QDP`  
* **File ảnh xuất:** [`pencil_exports/01_spider_web_arena.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/01_spider_web_arena.png)  
* **Mục tiêu:** Màn hình chính tái hiện trải nghiệm độc nhất: Hiển thị bài báo nghiên cứu chi tiết bằng ngôn ngữ gốc (ArXiv / Financial Paper Sheet Style). Con nhện 2D SVG bò trực tiếp trên các từ khóa (tokens), phóng sợi tơ tự tiêu biến sang Vòng cung quyết định Decision 3 Lite để phân loại nhị phân trong thời gian thực (< 10ms).

#### Bố cục 3 Phân Vùng (Screen 1):
1. **Left Icon-Rail & Feed Drawer Trigger (64px):**
   * Chiều rộng: `64px`, `layout: vertical`, `alignItems: center`, `gap: 16px`.
   * Gồm các nút icon hành động: Icon Feeds Drawer `📑` (mở slide-over 4 bài đang chờ quét), Icon Search `🔍`, Icon Lọc `⚡`.
   * Nút gạt nhịp độ (Pacing Control Pill): `[● Decision 3 Sync (400ms)]` `[○ Chill Mode (1200ms)]`.
2. **Center Arena — Tờ Báo Cáo Gốc Tinh Khiết (Dominant Region — 1450px):**
   * Kích thước: Rộng `1450px`, cao `940px`, nền trắng sứ `#FFFFFF`, viền `#DCD5C5`, bo góc `12px`, đổ bóng dịu `0 4px 16px rgba(45, 74, 43, 0.05)`, cuộn nội bộ mượt mà.
   * Header bài báo:
     * Badge & Metadata: `DECISION 3 LITE NEURAL RESEARCH LAB` • `NGUỒN: CAFEF VĨ MÔ • 10:42 AM • BẢN GỐC TIẾNG VIỆT/ANH`.
     * Tiêu đề lớn (`Playfair Display`, 20px, bold, `#2D4A2B`): *Ngân hàng Nhà nước bơm ròng 42,000 tỷ đồng qua kênh OMO nhằm ổn định thanh khoản tiền tệ.*
   * Nội dung bài báo định dạng 2 cột báo cáo chuẩn học thuật:
     * Typography thân bài: `Be Vietnam Pro`, cỡ `14px`, line-height `1.6` (độ rõ ràng tuyệt đối).
     * Từng từ khóa nhạy cảm được bọc trong thẻ: `<mark data-spider-index="0" data-word="lãi suất">lãi suất liên ngân hàng</mark>`.
     * Màu nền mark: Vàng ngọc bích `#FFF8E1` hoặc Xanh ngọc bích `#E8F0E8`.
   * **Lớp Nhện SVG 2D (`SpiderCanvas.tsx`):**
     * Nằm đè lên văn bản (`pointer-events: none`). Mai nhện ngọc bích `#2D4A2B`, 8 khớp chân linh hoạt.
     * Khi nhận `SpiderEvent`: Nhện bò tới tọa độ từ khóa bằng `gsap.to()`.
     * Bắn sợi tơ Bezier mảnh `0.75px – 1.0px` (`#E5B869`, `opacity: 0.6`) nối từ chân nhện sang Vòng cung Decision 3 Lite, tự mờ dần và biến mất sau 1.2s (tối đa 2 sợi tơ đồng thời).
3. **Right Decision 3 Lite Neural Routing Arc Column (350px cố định):**
   * Kích thước: Rộng `350px`, `background: #EBE6DC`, `border-radius: 12px`, `padding: 16px`.
   * Header: `DECISION 3 LITE NEURAL ROUTING ARC` • Badge: `⚡ 8.5ms`.
   * Hộp phán quyết lớn: `QUYẾT ĐỊNH: VĨ MÔ TRỌNG ĐIỂM (PASS THRESHOLD)`.
   * Thước đo độ tin cậy Tensor: `Confidence Score: 0.942 / 1.000`.
   * Bảng token đã bắt: `Decision 3 Lite Tensor` (+0.88), `Thanh khoản OMO` (+0.92), `Tỷ giá USD/VND` (+0.79).
   * Nút giải trình: `🧠 XEM GIẢI TRÌNH QUYẾT ĐỊNH DECISION 3 (EXPLAIN) →` (mở slide drawer giải trình riêng biệt).
   * Nút hành động chính: `⚡ ĐẨY SANG LLM SYSTEM 2 TỔNG HỢP TIẾNG VIỆT` (Dẫn sang Screen 2).
4. **Lớp Phủ Overlays Độc Lập (Modal Backdrop 40% Scrim):**
   * Hộp thoại tìm kiếm toàn văn `Cmd+K` FTS5: Nằm chính giữa màn hình với nền mờ bán trong suốt 40% (`Modal Backdrop 40% Scrim`), độc lập hoàn toàn với ngăn kéo giải trình, đóng bằng phím Esc hoặc click bên ngoài.

---

### 📍 MÀN HÌNH 2: CURATED FEEDS & BILINGUAL READER (DÒNG TIN ĐÃ LỌC & TRÌNH ĐỌC SONG NGỮ)
* **Node ID trong Pencil:** `BBamp`  
* **File ảnh xuất:** [`pencil_exports/02_curated_feeds_bilingual_reader.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/02_curated_feeds_bilingual_reader.png)  
* **Mục tiêu:** Màn hình đọc tin chiến lược Master-Detail. Cột trái là danh sách các bài báo đã được Decision 3 Lite (System 1) sàng lọc sạch rác. Cột phải là Trình đọc Song Ngữ tức thì, có công tắc chuyển đổi giữa Bản dịch vĩ mô tiếng Việt và Bản gốc quốc tế mà không cần gọi lại mạng.

#### Bố cục 3 Phân Vùng (Screen 2):
1. **Left Filter Sidebar (240px):**
   * Ô tìm kiếm tức thì SQLite FTS5: `[ 🔍 Tra cứu toàn văn... ]` (< 2ms).
   * Bộ lọc chủ đề: `● Tất cả đã lọc (18)`, `○ Vĩ mô & Tiền tệ (8)`, `○ Chứng khoán (5)`, `○ Vàng & Ngoại tệ (3)`, `○ Địa chính trị (2)`.
   * Bộ lọc điểm Decision 3 Lite: `Ngưỡng lọc: Score >= 0.75`.
2. **Center Master Feed List Column (560px):**
   * Danh sách bài viết đã lọc, sắp xếp theo thời gian mới nhất.
   * Thẻ bài báo (Card bo góc 12px, nền `#FFFFFF`, viền `#DCD5C5`):
     * Badge thể loại: `#E8F0E8` (`KINH TẾ VĨ MÔ`).
     * Tiêu đề: *FED giữ nguyên lãi suất điều hành, phát tín hiệu nới lỏng quý 4/2026.*
     * Nguồn & thời gian: *Reuters / AP News • 15 phút trước*.
     * Badge định tuyến: `⚡ SYSTEM 1 ROUTED: Laya 30-60ms / D3 150-200ms (NVIDIA GPU) • ON-DEMAND TRANSLATE (0đ)`.
     * Nút Bookmark: Biểu tượng sao `★` ghim vào Tech Vault.
3. **Right Bilingual Article Reader (1060px):**
   * Thanh điều khiển đỉnh đọc tin:
     * **Công Tắc Song Ngữ Độc Nhất:** Nút chuyển đổi tức thì `[● 🇻🇳 Tiếng Việt] [○ 🌐 Bản Gốc]`.
     * Nút thao tác nhanh: `★ Ghim Tech Vault`, `📋 Sao chép Markdown`, `🔗 Mở bài gốc`.
   * **Nội dung đọc bài báo:**
     * **Chế độ Bản Gốc:** Giữ nguyên văn tiếng Anh/quốc tế từ nguồn RSS sạch với đầy đủ đoạn văn và dẫn chứng. (Con Nhện bò trên màn hình 1 luôn diễn trên 100% bản gốc này để bắt từ khóa chuẩn xác).
     * **Chế độ Tiếng Việt:** Khi người dùng click chọn bài và gạt sang Tiếng Việt, hệ thống kích hoạt dịch On-Demand từng đoạn văn (`<p> by <p>`) bằng `deep-translator` (0đ API, 0% VRAM, không làm vỡ cấu trúc DOM). Bản dịch được giữ trên In-Memory RAM (React State) để hoán đổi tức thì trong 0ms, không lưu vào đĩa SQLite nhằm chống phình to database (chỉ lưu vĩnh viễn vào SQLite nếu người dùng nhấn `★ Ghim Tech Vault`). Hộp Tóm tắt Điều hành (Executive Summary Box - Nền `#FBF9F5`, viền `#2D4A2B`): 3 điểm cốt lõi và Phân tích Tác động Vĩ mô từ LLM System 2.

---

### 📍 MÀN HÌNH 3: EXECUTIVE INTELLIGENCE DIGEST (BẢN TIN TỔNG HỢP VĨ MÔ ĐIỀU HÀNH)
* **Node ID trong Pencil:** `Vem3L`  
* **File ảnh xuất:** [`pencil_exports/03_executive_digest.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/03_executive_digest.png)  
* **Mục tiêu:** Màn hình báo cáo tình báo vĩ mô điều hành tổng hợp toàn bộ các tin tức trong ngày, được biên soạn bởi LLM System 2 (Gemini 2.5 Flash) sau khi Decision 3 Lite sàng lọc. Áp dụng chuẩn bố cục **Hero + 2** tạo nhịp điệu thị giác rõ nét.

#### Bố cục Phân Vùng (Screen 3):
1. **Left Date & Digest Picker (240px):**
   * Tiêu đề: `LỊCH SỬ BẢN TIN VĨ MÔ`
   * Danh sách bản tin theo ngày: `● Bản Tin Hôm Nay (11/10/2026 - 42 bài phân tích)`, `○ Bản Tin 10/10/2026 (38 bài)`.
   * Bộ đo tâm lý thị trường tổng hợp: Đồng hồ đo tâm lý `Chỉ số Tâm Lý: 0.65 (Lạc Quan Thận Trọng)`.
2. **Right Digest Container (1640px — Cấu Trúc Hero + 2):**
   * **Khối Hero Macro Panel (Toàn Cảnh Kinh Tế & Dòng Tiền Vĩ Mô — Full Width 1640px):**
     * Nền kem giấy ngà sang trọng `#FBF9F5`, viền rêu `#2D4A2B`, padding rộng 1.4x (24px).
     * Tiêu đề lớn (`Playfair Display`, 20px, bold, `#2D4A2B`): *BÁO CÁO TỔNG HỢP TÌNH BÁO VĨ MÔ & CHIẾN LƯỢC TOÀN CẢNH*.
     * Metadata: *Ngày 11/10/2026 • 42 bài báo đã phân tích • Lọc phản xạ Decision 3 Lite (System 1) + Gemini 2.5 Flash*.
     * Nội dung vĩ mô: Tóm tắt chính sách tiền tệ, thanh khoản OMO, tỷ giá USD/VND, lãi suất liên ngân hàng kèm 3 sự kiện tâm điểm có trích dẫn nguồn.
     * Nút thao tác: `📥 Xuất Báo Cáo PDF`, `📋 Sao Chép Bản Tin`.
   * **Hai Cột Phân Tích Chuyên Sâu Bên Dưới (Bottom Two Columns — Đường Phân Tách Hairline):**
     * **Cột Trái — Toàn Cảnh Địa Chính Trị & Chuỗi Cung Ứng (808px):** Biến động ngoại giao, xung đột khu vực, chính sách thuế quan thương mại EU/Mỹ, tác động tới xuất nhập khẩu Việt Nam.
     * **Cột Phải — Đột Phá Công Nghệ AI & GitHub Open Source (808px):**
       * Điểm tin: Phát hành mô hình `decision-ai/decision-3-lite` System 1 suy luận nhị phân 5.4ms, kiến trúc Sparse Attention giảm 40% VRAM khi chạy cục bộ trong Docker.
       * Spider Radar hoàn tất tích hợp Dual-System: Decision 3 Lite + Gemini 2.5 Flash, giảm 84.6% chi phí token.

---

### 📍 MÀN HÌNH 4: GITHUB TECH RADAR (TRẠM THEO DÕI CÔNG NGHỆ & MÃ NGUỒN MỞ)
* **Node ID trong Pencil:** `G3FlA`  
* **File ảnh xuất:** [`pencil_exports/04_github_tech_radar.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/04_github_tech_radar.png)  
* **Mục tiêu:** Màn hình trinh sát công nghệ, quét các GitHub Repositories thịnh hành trong ngày. Trọng tâm phân tích mô hình `decision-ai/decision-3-lite` với trình đọc mã nguồn / README chuyên sâu và Đánh giá kỹ thuật System 1.

#### Bố cục 3 Phân Vùng (Screen 4):
1. **Left Tech Trends Sidebar (240px):**
   * Bộ lọc ngôn ngữ: `● Python`, `○ Rust`, `○ TypeScript`, `○ C++`.
   * Bộ lọc chủ đề: `● Edge Inference & Docker Serving`, `○ Autonomous Agents`.
   * Danh sách Repo Trending:
     * `● decision-ai/decision-3-lite (⭐ 3,842 • +421 today)` *(Active)*
     * `○ vllm-project/vllm (⭐ 28,100 • +180 today)`
     * `○ huggingface/candle (⭐ 15,200 • +95 today)`
2. **Middle Code & README Inspector (1040px):**
   * Thanh điều hướng Repo: Tên `decision-ai / decision-3-lite`, License Apache 2.0, Star count, Fork count.
   * Tab xem: `[● README.md] [○ Kiến Trúc Mã Nguồn] [○ Cài Đặt Docker]`.
   * Khối nội dung README & Code Snippet cao cấp:
     * Nền khối code màu đen rêu `#1E2621`, chữ `#E2F0D9`, font `JetBrains Mono`:
       ```python
       from decision_engine import SystemOneEngine, TensorClassifier

       # 1. Tải checkpoint siêu nhẹ (180MB RAM footprint trong Docker)
       engine = SystemOneEngine.load('checkpoints/decision3_core.safetensors')

       # 2. Suy luận nhị phân siêu tốc độ (Single-pass tensor)
       result = engine.predict_binary(text='Lãi suất điều hành tăng nhẹ')

       # 3. Trả về kết quả cho Spider Canvas trong 5.4ms
       print(f'Decision: {result.decision}, Latency: {result.latency_ms}ms')
       ```
     * Hướng dẫn chạy Docker System 1 Decision 3 Lite Serve port 8000:
       `docker run -d -p 8000:8000 decision-3-lite-serve:latest`
3. **Right Decision 3 Lite Tech Arc Column (580px):**
   * Header: `ĐÁNH GIÁ KỸ THUẬT DECISION 3 LITE` • Badge: `ĐIỂM: 9.6 / 10`.
   * Phân tích tương thích:
     * `Tương thích CPU x86/ARM: 100% (Không cần GPU VRAM, VRAM = 0)`.
     * `Độ trễ phản hồi: < 10ms (P50: 8.5ms)`.
     * `Độ trễ HTTP roundtrip: < 50ms`.
   * Nút hành động: `★ Ghim Vào Tech Vault`, `🌐 Mở GitHub Repo Trên Trình Duyệt`.

---

### 📍 MÀN HÌNH 5: TREND VAULT & KNOWLEDGE GRAPH (KHO LƯU TRỮ XU HƯỚNG & CÂY TRI THỨC)
* **Node ID trong Pencil:** `AiK8m`  
* **File ảnh xuất:** [`pencil_exports/05_trend_vault_graph.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/05_trend_vault_graph.png)  
* **Mục tiêu:** Màn hình quản lý các bài báo và công nghệ đã được ghim (Tech Vault). Hiển thị dưới dạng Cây tri thức thảo mộc hữu cơ (Organic Branch-Spine Knowledge Graph) bằng SVG 2D. Toàn bộ nội dung trong Vault được miễn trừ chính sách TTL 30 ngày và lưu trữ vĩnh viễn.

#### Bố cục 3 Phân Vùng (Screen 5):
1. **Left Icon-Rail & Vault Drawer Trigger (64px):**
   * Thu gọn thành thanh icon-rail 64px; nút mở Slide-over Drawer quản lý `48 BÀI BÁO VĨNH VIỄN`.
   * Danh sách mục đã ghim: `★ Mô hình Decision 3 Lite Serving (GitHub)`, `★ Báo cáo OMO Ngân hàng Nhà nước (Vĩ mô)`, `★ Quyết định nới lỏng lãi suất FED (Kinh tế)`.
2. **Middle Organic Botanical Knowledge Graph Canvas (1450px — Dominant Region):**
   * Nền giấy ngà sáng dịu `#F4F1EA`, diện tích áp đảo 1450px.
   * **Cây Tri Thức Thảo Mộc (SVG 2D Canvas - `BotanicalTree.tsx`):**
     * Thân cây chính (Main Trunk) đại diện dòng thời gian hệ thống.
     * Các cành nhánh Bezier mềm mại tỏa ra 3 cụm chủ đề lớn: Kinh Tế Vĩ Mô (`#2D4A2B`), Địa Chính Trị (`#C86D51`), Công Nghệ AI (`#4A6B82`).
     * Các node lá dạng pill tương tác nhẹ nhàng bằng GSAP, hover phóng to hiển thị trích dẫn nhanh.
3. **Right Entity Inspector Card (350px cố định):**
   * Hiển thị thông tin node tri thức đang chọn: Nguồn gốc, quan hệ cha con trong đồ thị.
   * Nút thao tác: `Mở Bài Báo`, `Bỏ Ghim (Unbookmark)`, `Xuất Trích Dẫn BibTeX`.

---

### 📍 MÀN HÌNH 6: SETTINGS & DATA RETENTION MANAGEMENT (CÀI ĐẶT & QUẢN TRỊ DỮ LIỆU)
* **Node ID trong Pencil:** `QKmAR`  
* **File ảnh xuất:** [`pencil_exports/06_settings_data_retention.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/06_settings_data_retention.png)  
* **Mục tiêu:** Màn hình trung tâm thiết lập hệ thống với nguyên tắc **Progressive Disclosure (Mở có chọn lọc)**: Chỉ mở phần Quản lý nguồn tin RSS thường xuyên sử dụng; thu gọn phần cấu hình nâng cao Động cơ AI và Vòng đời dữ liệu để giao diện thoáng đãng, chuyên nghiệp.

#### Bố cục Phân Vùng (Screen 6):
1. **Left Icon-Rail & System Status (64px):**
   * Thanh 64px gọn gàng, hiển thị icon trạng thái hệ thống: SQLite WAL `14.2 MB`, RAM `142 MB`, VRAM `0 MB (CPU Ready)`.
2. **Right Settings Dashboard (fill_container — Áp dụng Progressive Disclosure):**

   * **Section 1 (COLLAPSED Mặc định): Cấu Hình Động Cơ Kép (Decision 3 Lite + Gemini 2.5 Flash)**
     * Header: `3. ĐỘNG CƠ SUY LUẬN DECISION 3 LITE & LLM DUAL-SYSTEM` • Badge: `5.4ms SINGLE-PASS • ONLINE`.
     * Nút bấm: `Mở Rộng Cấu Hình ▼`
     * Chi tiết khi mở:
       * Decision 3 Lite (System 1): `http://127.0.0.1:8000/v1/systemone` (🟢 Latency: 14ms).
       * Docker Container: `decision-3-lite-serve:latest` (Đang chạy ổn định).
       * LLM System 2: `Google Gemini 2.5 Flash` (API Key mã hóa AES-GCM an toàn).
       * Tần suất kiểm tra RSS: `15 phút / lần` (Tối ưu phản xạ Decision 3 Lite System 1).
       * Nhịp di chuyển của nhện: `[● Decision 3 Sync (400ms)]` `[○ Chill Mode (1200ms)]`.

   * **Section 2 (OPEN Mặc định): Quản Lý Nguồn RSS Động (Dynamic Feeds Manager)**
     * Header: `2. QUẢN LÝ NGUỒN RSS ĐỘNG (FEEDS MANAGER)` • Badge: `5 NGUỒN HOẠT ĐỘNG`.
     * Bảng danh sách nguồn tin trực quan:
       1. `CaféF Vĩ Mô (cafef.vn/kinh-te-vi-mo.rss)` • 142 bài • Active
       2. `VnExpress Kinh Doanh (vnexpress.net/rss/kinh-doanh.rss)` • 118 bài • Active
       3. `Tuổi Trẻ Thế Giới (tuoitre.vn/rss/the-gioi.rss)` • 82 bài • Active
       4. `AP News Top Stories (apnews.com RSS)` • 34 bài • Active
       5. `GitHub Trending AI (GraphQL Scraper)` • 26 repos • Active
     * Nút thao tác xóa: Nút xóa màu cam đất Terracotta `#C86D51` nổi bật.
     * Nút thêm mới: `+ Thêm Nguồn RSS Mới` (Backend tự động validate HTTP 200 & XML trước khi ghi DB).

   * **Section 3 (COLLAPSED Mặc định): Quản Lý Watchlists & Vòng Đời Lưu Trữ (TTL 30 Ngày)**
     * Quản lý chủ đề động (Zero-Code Dynamic Watchlists).
     * Quản lý Quota quét tin hàng ngày (500 bài/ngày, thanh tiến độ 68.4%).
     * Chính sách TTL 30 ngày (Bảo vệ tuyệt đối các bài viết trong Tech Vault).
     * Cặp nút thao tác trực tiếp:
       * `🧹 Dọn Dẹp Tin Quá Hạn Ngay`: Xóa bài > 30 ngày (trừ Tech Vault).
       * `💾 Thu Hồi Đĩa VACUUM (FTS5)`: Kích hoạt `PRAGMA incremental_vacuum;` và re-index.

---

### 📍 MÀN HÌNH 7: MACRO ANALYTICS & QUANTITATIVE CHART METRICS (THỐNG KÊ BIỂU ĐỒ ĐỊNH LƯỢNG VĨ MÔ)
* **Node ID trong Pencil:** `R8OCUi`  
* **File ảnh xuất:** [`pencil_exports/07_macro_analytics_charts.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/07_macro_analytics_charts.png)  
* **Mục tiêu:** Màn hình phân tích định lượng vĩ mô (Quantitative Analytics Dashboard) theo chuẩn bố cục **Bento Grid 4-Card (2x2 Layout, gap 16)**. Biến toàn bộ dữ liệu cào tin và suy luận thành các trực quan hóa sắc nét, thể hiện rõ hiệu quả lọc sạch tin rác của Decision 3 Lite, độ trễ sub-10ms và tiết kiệm 84.6% chi phí token.

#### Bố cục Phân Vùng (Screen 7):
1. **Left Analytics Sidebar (240px):**
   * Tiêu đề: `BỘ LỌC CHỈ SỐ (METRICS)`
   * Khung Thời Gian (Time Horizon Pills): `○ 24 Giờ Qua`, `○ 7 Ngày Qua`, `● 30 Ngày Gần Nhất (1,842 bài)` *(Active)*, `○ Toàn Quý`.
   * Bộ Lọc Phân Khúc: `● Toàn Bộ Thị Trường`, `○ Vĩ Mô & Tiền Tệ`, `○ Địa Chính Trị`, `○ Công Nghệ AI`.
   * Thẻ Tóm Tắt Tình Báo (Quick KPI Summary Card — Bo góc 12px):
     * Tổng tin quét: `1,842 bài`
     * Tỷ lệ nén lọc sạch: `76.4% sạch`
     * Token tiết kiệm: `-84.6%`
     * Độ trễ trung bình: `8.5ms`
2. **Right Quantitative Charts Matrix (1640px — 4-Card Bento Grid 2x2, gap 16):**

   * **Card 1 (Hàng 1, Cột 1 — Cao 450px): Chỉ Số Tâm Lý Thị Trường 30 Ngày (Sentiment Step-Curve)**
     * Header: `1. CHỈ SỐ TÂM LÝ THỊ TRƯỜNG & BIẾN ĐỘNG (SENTIMENT STEP-CURVE)` • Badge: `TÍCH CỰC (+0.68 RISK-ON)`.
     * Trục Y: `-1.0` (Bi quan cực độ) $\rightarrow$ `0.0` (Trung hòa) $\rightarrow$ `+1.0` (Lạc quan).
     * Đường vẽ: Step-curve mượt mà màu xanh rêu `#2D4A2B`, diện tích fill mờ nhạt bên dưới `#E8F0E8` (opacity 0.25).
     * Chú thích các mốc biến động vĩ mô (Event Callout Pins):
       * `Pin 1 (Ngày 8): FED giữ lãi suất (Bước nhảy +0.32)`.
       * `Pin 2 (Ngày 18): OMO bơm ròng 42k tỷ (Bước nhảy +0.55)`.
       * `Pin 3 (Ngày 28): VN-Index bứt phá & Dòng tiền ngoại (Chạm đỉnh +0.68)`.

   * **Card 2 (Hàng 2, Cột 1 — Cao 456px): Phân Phối Độ Trễ Suy Luận Decision 3 Lite (Latency Histogram)**
     * Header: `PHÂN PHỐI ĐỘ TRỄ SUY LUẬN Decision 3 Lite (System 1)` • Badge: `P50: 8.5ms • P95: 14.2ms`.
     * Biểu đồ cột phân phối tần suất dạng Histogram (10 bins từ 2ms đến 25ms).
     * Đỉnh phân phối Gaussian tập trung dày đặc nhất ở dải `7ms – 10ms` (chiếm 64% tổng số lượt gọi).
     * 100% tất cả inference hoàn tất dưới 25ms (Đáp ứng chuẩn Hard Invariant của Hợp đồng `AGENTS.md`).

   * **Card 3 (Hàng 1, Cột 2 — Cao 450px): Cơ Cấu Chủ Đề Vĩ Mô Trọng Điểm & Xung Lực (Topic Allocation & Ratio Bar)**
     * Header: `CƠ CẤU CHỦ ĐỀ VĨ MÔ TRỌNG ĐIỂM` • Badge: `KINH TẾ 45%`.
     * Thanh tỷ trọng phân bổ chủ đề xếp chồng (Stacked Horizontal Ratio Bar):
       * `Kinh Tế Vĩ Mô & Tiền Tệ`: `45%` (Xanh rừng `#2D4A2B`).
       * `Địa Chính Trị & Thương Mại`: `30%` (Đất nung `#C86D51`).
       * `Công Nghệ AI & GitHub`: `25%` (Xanh đá Slate `#4A6B82`).
     * Chỉ số xung lực gia tốc (Momentum Indicators): Kinh tế `▲ +14%`, Công nghệ AI `▲ +28%`.

   * **Card 4 (Hàng 2, Cột 2 — Cao 456px): Ma Trận Nhiệt Từ Khóa Trọng Điểm 4x3 (Keyword Co-occurrence Heatmap)**
     * Header: `MA TRẬN NHIỆT TỪ KHÓA TRỌNG ĐIỂM (KEYWORD HEATMAP 4x3)` • Badge: `TOP: LÃI SUẤT & TỶ GIÁ`.
     * Ma trận 12 ô màu nhiệt độ:
       * Ô `Lãi Suất` (342 lần): Đỏ đất nung đậm `#C86D51` (Cực nóng).
       * Ô `Tỷ Giá USD` (288 lần): Đất nung vừa `#D98A72` (Nóng).
       * Ô `Vàng SJC` (195 lần): Vàng hổ phách `#E5B869` (Ấm).
       * Ô `Bán Dẫn AI` (241 lần): Xanh đá Slate đậm `#4A6B82` (Rất nóng).
       * Ô `Thanh Khoản OMO` (178 lần): Vàng cam `#EEBC6D`.
       * Các ô còn lại (`Bất Động Sản`, `Nợ Xấu`, `Lạm Phát EU`, `Trái Phiếu`...): Tông ngà xám `#EBE6DC` đến lục nhạt `#C8D6C6` (Bình ổn).

   * **Chỉ Số Định Lượng Tiết Kiệm Chi Phí (Cost & Resource Efficiency):**
     * **Mô hình thuần Cloud (100% tin vào LLM):** Tiêu thụ ~2.8M tokens/tháng $\rightarrow$ `$48.60 / tháng`.
     * **Mô hình Hybrid Dual-System (Decision 3 Lite sàng lọc trước):** Tiêu thụ ~430K tokens/tháng $\rightarrow$ `$7.50 / tháng`.
     * **Mức tiết kiệm ròng:** `$41.10 / tháng (-84.6% chi phí API)`.
     * **Tài nguyên phần cứng:** RAM 142 MB, VRAM 0 MB (chạy hoàn toàn trên CPU container Docker).

---

## 4. MA TRẬN SỰ KIỆN TƯƠNG TÁC & API ENDPOINTS (INTERACTION & API MATRIX)

Bảng tra cứu để AI ánh xạ trực tiếp từng nút bấm giao diện tới State và API Backend:

| Tên Nút / Thành Phần Giao Diện | Màn Hình | Hành Động Phía Client (React State / GSAP) | API Endpoint Backend Tương Ứng |
|---|---|---|---|
| **Tabs Chuyển Màn Hình** (`1..7`) | Toàn cục | Cập nhật `activeTab: 1..7` trong App State | Không cần gọi mạng (Client-side routing) |
| **Nút Pacing** (`Sync / Chill`) | Screen 1, 6 | Đổi `pacing_delay_ms: 400` hoặc `1200` | `PATCH /api/v1/settings/pacing` |
| **Thẻ Từ Khóa `<mark>`** | Screen 1 | Kích hoạt `SpiderEvent`, nhện bò tới từ khóa | Nhận qua SSE stream: `/api/stream/spider-events` |
| **Nút Giải Trình Decision 3** | Screen 1 | Mở Slide Drawer giải trình quyết định nhị phân | Đọc từ SSE event data / Decision cache |
| **Nút Tìm Kiếm Nhanh** (`Cmd+K`) | Screen 1 | Mở centered dialog trên nền `Backdrop 40% Scrim` | `GET /api/v1/search?q={query}` (< 2ms) |
| **Nút Tổng Hợp Tiếng Việt** | Screen 1 | Chuyển sang Screen 2, hiển thị bài dịch | `POST /api/v1/synthesize/article` |
| **Ô Tìm Kiếm FTS5** | Screen 2, 5 | Debounce 150ms, lọc danh sách bài viết tức thì | `GET /api/v1/search?q={query}` (< 2ms) |
| **Công Tắc Song Ngữ** (`🇻🇳 / 🌐`) | Screen 2 | Hoán đổi `isVietnameseView = !isVietnameseView` | Đọc từ React In-Memory RAM Cache (0ms), kích hoạt dịch On-Demand qua `deep-translator` khi mở lần đầu |
| **Nút Ghim Tech Vault** (`★`) | Screen 2, 4, 5 | Cập nhật `is_bookmarked = 1`, icon sao phát sáng | `POST /api/v1/articles/{id}/bookmark` |
| **Nút Sao Chép Markdown** | Screen 2, 3 | Copy nội dung bài báo vào `navigator.clipboard` | Không cần gọi mạng (Client Web API) |
| **Nút Xuất Báo Cáo PDF** | Screen 3 | Mở dialog lưu file PDF của Tauri v2 | `POST /api/v1/export/pdf` |
| **Lọc Khung Thời Gian Charts** | Screen 7 | Đổi time range (`24h`, `7d`, `30d`, `90d`) | `GET /api/v1/analytics/metrics?range={range}` |
| **Nút Xem Biểu Đồ Từ Decision 3 Arc** | Screen 1 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Link Nhịp Đập Vĩ Mô Từ Sidebar** | Screen 2 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Link 4 Biểu Đồ Từ Hero Banner** | Screen 3 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Nút Chỉ Số Tăng Trưởng Repo** | Screen 4 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Nút Xem Ma Trận Nhiệt Từ Khóa** | Screen 5 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Link Hiệu Năng Token Từ Cài Đặt** | Screen 6 | Chuyển `activeTab = 4` (Screen 7 Biểu đồ) | Không cần gọi mạng (Client-side routing) |
| **Nút Chạy Dọn Dẹp Ngay** (`🧹`) | Screen 6 | Hiển thị loader, xóa bài > 30 ngày trừ Tech Vault | `POST /api/v1/retention/purge-now` |
| **Nút Thu Hồi Đĩa VACUUM** (`💾`) | Screen 6 | Chạy `PRAGMA incremental_vacuum;` | `POST /api/v1/database/vacuum` |
| **Nút Thêm Nguồn RSS Mới** | Screen 6 | Mở Modal Form nhập URL và thể loại | `POST /api/v1/sources` |
| **Bộ Chọn Động Cơ System 1** | Screen 6 | Đổi động cơ: `Auto-Detect`, `Laya GPU CUDA (30-60ms)`, `Decision 3.0 (150-200ms NVIDIA GPU)`, `Mock Engine`; hiển thị latency trung bình đo được | `GET /api/v1/system1/status` & `POST /api/v1/system1/select` |
| **Kích Hoạt Cào Tin Ngay** (`🔄`) | Screen 1, 6 | Kích hoạt quét ngầm toàn bộ các nguồn tin active | `POST /api/v1/crawl` |
| **Công Tắc Bật/Tắt RSS** | Screen 6 | Toggle `is_active = 0/1` cho feed | `PATCH /api/v1/sources/{id}/toggle` |
| **Nút Xóa Nguồn RSS** | Screen 6 | Xóa nguồn tin RSS (Nút màu cam đất `#C86D51`) | `DELETE /api/v1/sources/{source_id}` |

---

## 5. CẤU TRÚC THƯ MỤC & COMPONENT MAPPING (FRONTEND FILE TREE)

Khi AI sinh code Frontend React TypeScript (`frontend/src/`), cấu trúc file phải tuân thủ nghiêm ngặt mô hình sau:

```
frontend/src/
├── assets/
│   └── sfx/                         # File âm thanh Web Audio
│       ├── water_drop.mp3           # Giọt nước khi nhện nhảy
│       └── paper_rustle.mp3         # Sột soạt giấy cói
├── components/
│   ├── chrome/                      # App Chrome toàn cục
│   │   ├── TopHeaderBar.tsx         # Thanh tiêu đề 48px, 7 tabs, macOS dots
│   │   ├── LeftSidebar.tsx          # Cột điều hướng 64px (icon-rail) hoặc 240px
│   │   └── BottomTelemetryBar.tsx   # Thanh giám sát đáy 44px (#F0F5EA, 11px bold)
│   ├── screens/                     # 7 Màn hình chính
│   │   ├── Screen1SpiderArena.tsx   # Screen 1: Dominant 1450px ArXiv & Decision 3 Routing Arc
│   │   ├── Screen2BilingualReader.tsx # Screen 2: Master List (560px) & Bilingual Reader (1060px)
│   │   ├── Screen3ExecutiveDigest.tsx # Screen 3: Hero + 2 Structure (Hero 1640px + 2 Cols)
│   │   ├── Screen4GitHubRadar.tsx   # Screen 4: README Code Inspector & Decision 3 Scorecard
│   │   ├── Screen5TrendVault.tsx    # Screen 5: 1450px Organic Botanical Knowledge Graph
│   │   ├── Screen6Settings.tsx      # Screen 6: Progressive Disclosure (Feeds OPEN, Engines COLLAPSED)
│   │   └── Screen7Analytics.tsx     # Screen 7: 4-Card Bento Grid Macro & Decision 3 Charts
│   ├── charts/                      # Các thành phần biểu đồ Recharts / SVG Canvas
│   │   ├── SentimentStepCurve.tsx   # Step-curve 30 ngày tâm lý thị trường
│   │   ├── FilteringRatioBar.tsx    # Biểu đồ cột nén tin rác Decision 3 Lite
│   │   ├── LatencyHistogram.tsx     # Phân phối độ trễ suy luận Decision 3 Lite (ms)
│   │   ├── CategoryRatioDonut.tsx   # Tỷ trọng vĩ mô & momentum gia tốc
│   │   ├── KeywordHeatmap.tsx       # Ma trận nhiệt 4x3 từ khóa nhạy cảm
│   │   └── CostEfficiencyCard.tsx   # So sánh chi phí token Dual-System (-84.6%)
│   ├── overlays/                    # Các lớp phủ modal & drawer độc lập
│   │   ├── SearchModalFTS5.tsx      # Centered Cmd+K dialog với 40% backdrop scrim
│   │   ├── FeedsSlideDrawer.tsx     # Slide-over feeds queue drawer
│   │   └── DecisionExplainDrawer.tsx # Slide drawer giải trình quyết định Decision 3
│   └── visual/                      # Thành phần đồ họa độc nhất
│       ├── SpiderCanvas.tsx         # SVG Nhện 2D + GSAP animation + Tơ Bezier
│       ├── BotanicalTree.tsx        # Cây tri thức thảo mộc hữu cơ
│       └── LossSurfaceProjection.tsx # Biểu đồ 3D Loss surface 2D
├── styles/
│   ├── tokens.css                   # Biến màu Hex, Font, Spacing, Locked Radii (12px / 999px)
│   └── global.css                   # Reset CSS, Typography (14px body) & Scrollbar
├── store/
│   └── useAppStore.ts               # Zustand State: ActiveTab, Pacing, Article Cache
└── App.tsx                          # Root component điều phối 7 màn hình
```

---

## 6. DANH MỤC THAM CHIẾU HÌNH ẢNH & NODE ID TRONG FILE PENCIL

Toàn bộ 7 màn hình đã được hoàn thiện trong Canvas [`spider_radar.pen`](file:///d:/code_tienich_forme/tintuc_quanhta/spider_radar.pen) và xuất thành 7 tệp hình ảnh độ phân giải cao tại [`pencil_exports/`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/):

| Số hiệu | Tên màn hình | Node ID trong `spider_radar.pen` | Tọa độ Canvas (X, Y) | Tập tin ảnh xuất PNG tương ứng |
|---|---|---|---|---|
| **Screen 1** | Spider Web Arena (Paper Sheet Style) | `R7QDP` | `(0, 0)` | [`pencil_exports/01_spider_web_arena.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/01_spider_web_arena.png) |
| **Screen 2** | Curated Feeds & Bilingual Reader | `BBamp` | `(2020, 0)` | [`pencil_exports/02_curated_feeds_bilingual_reader.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/02_curated_feeds_bilingual_reader.png) |
| **Screen 3** | Executive Intelligence Digest | `Vem3L` | `(4040, 0)` | [`pencil_exports/03_executive_digest.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/03_executive_digest.png) |
| **Screen 4** | GitHub Tech Radar | `G3FlA` | `(0, 1180)` | [`pencil_exports/04_github_tech_radar.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/04_github_tech_radar.png) |
| **Screen 5** | Trend Vault & Knowledge Graph | `AiK8m` | `(2020, 1180)` | [`pencil_exports/05_trend_vault_graph.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/05_trend_vault_graph.png) |
| **Screen 6** | Settings & Data Retention Management | `QKmAR` | `(4040, 1180)` | [`pencil_exports/06_settings_data_retention.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/06_settings_data_retention.png) |
| **Screen 7** | Macro Analytics & Quantitative Metrics | `R8OCUi` | `(0, 2360)` | [`pencil_exports/07_macro_analytics_charts.png`](file:///d:/code_tienich_forme/tintuc_quanhta/pencil_exports/07_macro_analytics_charts.png) |

---
*Tài liệu này là bản đặc tả kỹ thuật giao diện bất biến, phục vụ trực tiếp cho việc sinh mã nguồn tự động ở Gate 6 và Gate 7 theo hợp đồng `AGENTS.md`.*
