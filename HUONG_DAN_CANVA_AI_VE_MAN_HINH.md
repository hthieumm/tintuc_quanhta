# 🎨 HƯỚNG DẪN CANVA AI THIẾT KẾ MÀN HÌNH (CANVA SCREEN SPEC)
> **Dự án:** Spider News Radar (Tin Tức Quanh Ta)  
> **Chuẩn thiết kế:** Tuân thủ 100% hợp đồng `D:\code\skill_AI\canva_skill` (`00-output-spec.md` & `18-poetic-botanical-ink.md`).  
> **Mục tiêu:** Cung cấp thông số tọa độ `%`, mã màu Hex, Typography và Prompt chính xác để Canva AI (Magic Studio) vẽ bản xem trước (Mockup 16:9).

---

## 0. STYLE DIAGNOSIS (Khởi tạo hệ thống phong cách)

```
Style: Poetic Botanical Ink (Wavy-Pastoral 18-F & Branch-Spine 18-G)
Q1 (Tông cảm xúc): b) Nhẹ nhàng, mộng mơ, trang nhã kiểu tạp chí tri thức
Q2 (Nội dung): Dashboard đọc tin, Radar vĩ mô, Code Reader & Báo cáo
Q3 (Hình ảnh): Illustration vector thảo mộc, hoa văn dây leo, nhện giọt sương trong suốt
Q4 (Mật độ chữ): Vừa phải (Bố cục 3 cột thoáng mắt, safe zone 5%)
Q5 (Thương hiệu): Nền giấy ngà (#FAF8F5), chữ xanh rừng (#2D4A2B), nhấn đào (#F8AFA6) & vàng hổ phách (#E5B869)
Tỷ lệ khung hình: 16:9 (1920 x 1080 px)
```

### 🌿 GỢI Ý 3 BẢNG MÀU CHỦ ĐẠO (SCREEN-FIRST UI COLOR PALETTES)

#### 🎨 Lựa Chọn 1: Poetic Botanical Ink (Mặc định — Tạp Chí Tri Thức Thơ Mộng)
* **Triết lý:** Thanh lịch, dịu mắt, mang hơi thở giấy dó cổ điển và gốm sứ. Rất hợp với phong cách nhện giọt sương và người thích đọc tin thư thái.
* **Bảng màu:**
  * **Nền chính (Background 60%):** `#FAF8F5` (Ivory Paper - Giấy ngà ấm, chống mỏi mắt).
  * **Bề mặt Panels (Surface 30%):** `#FFFFFF` (Trắng sứ tinh khôi) với viền mỏng `1px` màu `#E0EBD6`.
  * **Chữ chính (Text Primary):** `#2D4A2B` (Deep Forest - Xanh rừng già, tương phản cực nét **11.9:1 PASS AAA**).
  * **Chữ phụ (Text Secondary):** `#5F7D58` (Sage Muted - Xanh xô thơm trầm, **4.8:1 PASS AA**).
  * **Điểm nhấn thị trường (Accents):**
    * 🌸 Tăng trưởng / Tin tốt: `#F8AFA6` (Hồng đào san hô).
    * 🍂 Rủi ro / Tiêu cực: `#C86D51` (Cam đất ấm - thay vì đỏ chói gắt).
    * 🌾 Chính sách / Vĩ mô: `#E5B869` (Vàng hổ phách).
    * 🪙 Crypto: `#8E7CC3` (Tím tử đinh hương pastel).

#### 🌌 Lựa Chọn 2: Dark Cyber-Botanical (Dark Mode Sang Trọng — Dành Cho Trader & Dev Cày Đêm)
* **Triết lý:** Phong cách trạm thông tin tình báo ban đêm (Bloomberg Terminal giao thoa Botanical). Nhện thủy tinh phát sáng dạ quang neon trên nền đêm huyền bí.
* **Bảng màu:**
  * **Nền chính (Background 60%):** `#121513` (Obsidian Ink - Đen than chì trầm, không đen tuyệt đối `#000000` để tránh gắt mắt).
  * **Bề mặt Panels (Surface 30%):** `#1B221B` (Moss Slate - Xanh rêu đá đêm) viền hairline `1px` `#2E3A2E`.
  * **Chữ chính (Text Primary):** `#E8EFE8` (Ghost White - Trắng bạc ánh xanh, tương phản **14:1 PASS AAA**).
  * **Chữ phụ (Text Secondary):** `#8A9E8A` (Pale Sage - Xám ngọc bích).
  * **Điểm nhấn dạ quang (Luminescent Accents):**
    * ⚡ Tơ nhện & Tăng trưởng: `#00E676` (Electric Emerald - Lục bảo dạ quang) hoặc `#64FFDA` (Cyan Neon).
    * 🥇 Giá Vàng & Hàng hóa: `#FFD54F` (Digital Gold).
    * 🪙 Crypto & Web3: `#B388FF` (Electric Lavender).
    * 🍂 Cảnh báo / Tiêu cực: `#FF7043` (Coral Flame).

#### 🏛️ Lựa Chọn 3: Swiss Financial Monochrome (Tối Giản Tạp Chí Tài Chính Quốc Tế)
* **Triết lý:** Chuẩn thiết kế quốc tế Bauhaus / Swiss Style của báo *Financial Times* và *Wall Street Journal*. Tối giản tối đa, tập trung vào typographic grid và số liệu chính xác.
* **Bảng màu:**
  * **Nền chính:** `#F4F3EF` (Warm Newsprint).
  * **Bề mặt Panels:** `#FFFFFF` viền xám kỹ thuật `1px solid #E2E1DC`.
  * **Chữ chính:** `#1A1A1A` (Carbon Black).
  * **Chữ phụ:** `#666666` (Steel Gray).
  * **Accent màu duy nhất:** `#0F2C59` (Deep Financial Navy) hoặc `#F2A987` (FT Salmon Peach).

---

### 🖋️ Typography System (Chuẩn Phần Mềm Desktop)
* **Tiêu đề tin / Repo (Heading):** `Playfair Display` (hoặc `Fraunces`) — 22px – 28px (vừa vặn khung chữ, không phóng to 72px như slide).
* **Nội dung đọc (Body text):** `Be Vietnam Pro` (Regular 400, SemiBold 600) — 14px – 16px, line-height 1.7.
* **Số liệu / Độ trễ / Telemetry (Monospace):** `JetBrains Mono` hoặc `Fira Code` — 11px – 13px (chuẩn số liệu kỹ thuật).

---

## 🛑 BỘ QUY TẮC VÀNG VẼ GIAO DIỆN (UI/UX SCREEN RULES CHO CANVA AI)
> ⚠️ **LƯU Ý CỐT LÕI:** Đây là bản thiết kế **MÀN HÌNH PHẦN MỀM DESKTOP NATIVE (DESKTOP APPLICATION UI)**, **TUYỆT ĐỐI KHÔNG PHẢI SLIDE THUYẾT TRÌNH HAY POSTER QUẢNG CÁO!**  
> Canva AI rất hay sinh ra slide PowerPoint (chữ to tướng ở giữa, gạch đầu dòng bullet point, hình 3D lềnh bềnh, khoảng trống vô nghĩa). Phải áp dụng nghiêm ngặt 4 quy tắc sau:

### 📐 Quy tắc 1: Bắt Buộc Có Khung Cửa Sổ Ứng Dụng (Window App Chrome)
* Mọi ảnh dựng màn hình phải có **Thanh Tiêu Đề Cửa Sổ (Top Window Bar)**:
  * Góc trái: 3 nút điều khiển cửa sổ kiểu macOS (nút tròn đỏ/vàng/xanh nhạt) hoặc Windows titlebar.
  * Giữa: Thanh Breadcrumbs hoặc Bộ chuyển đổi chế độ xem (`[🕸️ SPIDER ARENA] | [📰 EDITORIAL DIGEST]`).
   * Góc phải: Trạng thái kết nối động cơ (`SYSTEM 1: Laya 30-60ms / D3 150-200ms NVIDIA GPU — hiển thị latency trung bình`), nút Mute SFX `[🔊]`, nút Cài đặt `[⚙️]`.

### 📊 Quy tắc 2: Mật Độ Thông Tin Chuẩn Phần Mềm (High Information Density)
* **Không dùng chữ to khổng lồ kiểu tiêu đề slide trình chiếu.**
* Bắt buộc có các thành phần giao diện thực tế (Functional UI Elements):
  * **Thẻ tin (Cards) có cấu trúc:** Badge chuyên mục nhỏ (`#chung_khoan`, `#vang`), tiêu đề 2 dòng, ngày giờ metadata 12px, nguồn báo.
  * **Nút bấm (Buttons):** Có padding rõ ràng (`8px 16px`), bo góc chuẩn phần mềm (`rounded: 8px-12px`), viền mỏng `1px`.
  * **Thước đo & Bảng trạng thái (Telemetry & Gauges):** Đồng hồ đo sentiment, ma trận chấm tròn Token Grid (`●●●●○○○○`), biểu đồ thanh phân bổ dòng tin.

### 🔲 Quy tắc 3: Bố Cục Phân Khu Vực Rõ Ràng (Strict Container & Viewport Grid)
* Không dùng các hình khối đồ họa trừu tượng trôi lơ lửng giữa màn hình (No floating abstract blobs).
* Mọi thành phần đều nằm trong **Panels / Containers cố định**:
  * Panel bên trái: Không gian đọc bài có lề padding 24px và thanh cuộn mảnh.
  * Panel bên phải: Cụm hộp quyết định (Decision Nodes) xếp theo cung tròn.
  * Panel đáy: Status Bar chạy dài sát mép dưới màn hình.
* **Góc nhìn bắt buộc:** Trực diện phẳng 90 độ (`Flat 2D front-facing direct screen UI`), tuyệt đối không vẽ nghiêng góc, không vẽ chiếc iPad/Laptop đặt trên bàn làm việc có bóng đổ xiên xẹo.

### 🚫 Quy tắc 4: Công Thức Prompting & Bộ Lọc Chặn Slide (Negative Prompting)
* **Từ khóa BẮT BUỘC có trong Prompt:**
  `Desktop software application UI screenshot, Figma UI design system, native desktop window interface, modern financial intelligence software, 63-32-5 split panel layout (63% reader, 32% decision arc, 5% telemetry bar), elegant typography hierarchy, realistic software components, 8k resolution`.
* **Bộ lọc TIÊU CỰC bắt buộc chặn (Negative Prompts):**
  `--no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle, isometric table shot, photorealistic computer screen bezel`.

---

## 🕷️ TẠO ASSET CON NHỆN CỐ ĐỊNH TRÊN CANVA AI
> **Nơi thực hiện:** Mở Canva $\rightarrow$ Chọn **Ứng dụng (Apps)** $\rightarrow$ **Magic Media** (Text to Image) hoặc thanh tìm kiếm Elements.

### Prompt tạo nhân vật Nhện Thảo Mộc (Botanical Crystal Spider):
```text
Top-down view of a delicate minimalist mechanical spider made of translucent sea-glass and polished bronze wire, floral botanical joints, tiny dewdrop abdomen, watercolor ink wash aesthetic, clean white background, isometric product shot, pastel sage green and peach accents, studio lighting, vector style, 8k resolution, no shadows, character sheet --no realistic hairy spider, no dark gothic
```
* **Cách xử lý trong Canva:**
  1. Sau khi Canva AI sinh ảnh, bấm **Edit Image** $\rightarrow$ **Background Remover** (Xóa nền).
  2. Lưu thành sticker PNG trong suốt để đưa vào các màn hình ứng dụng dưới đây.

---

## 🖥️ CHI TIẾT SPEC 5 MÀN HÌNH ĐỂ VẼ TRÊN CANVA
> **Mapping sang chuẩn 7 màn hình** ([`DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md`](./DOCS_THIET_KE_GIAO_DIEN_7_MAN_HINH.md)): Màn hình 1–4 bên dưới giữ nguyên số thứ tự; **MÀN HÌNH 5** bên dưới tương ứng **Màn hình 6 (Settings & Data Retention)**; còn **Màn hình 2 (Curated Feeds)** và **Màn hình 7 (Macro Analytics)** chỉ tồn tại trong chuẩn 7 màn. Layout mọi màn hình tuân thủ **63% / 32% + Bottom Telemetry Bar 5%**.

---

### MÀN HÌNH 1: SPIDER WEB ARENA (Bản Đồ Giăng Tơ Decision 3.0 & Sân Khấu Nhện Độc Lập)
* **Archetype:** `spider-web-arena` (Sân khấu trực quan 2 cột lớn: 63% Không gian bài báo/Code + 32% Vòng cung quyết định + Bottom Telemetry Bar 5%).
* **Cảm hứng trực tiếp:** Trend *"Anh IT họ Lào - Prompt Spider // Mỗi hàm, một ngã rẽ"* trên TikTok.
* **Mục tiêu:** Cho con nhện không gian rộng thênh thang để bò tự do, phô diễn trọn vẹn vũ đạo giăng tơ Bezier vút dài sang các Node quyết định mà không bị bó hẹp trong khung nhỏ. Cột danh sách tin được giấu vào **Ngăn kéo trượt (Slide-over Feed Drawer)** ở cạnh trái.

```yaml
Elements Layout (Tỷ lệ % trên khung 16:9):
[E1] Background: x:0% y:0% w:100% h:100% | fill: #FAF8F5 (Trắng ngà giấy dó cổ điển)

[E2] Top Header Bar: x:2% y:2% w:96% h:6% | fill: #F0F5EA, rounded: 14px, border: 1px #E0EBD6
  - Trái: Nút mở ngăn kéo tin [📂 DÒNG TIN] + Logo "SPIDER RADAR // WEB ARENA" (Playfair Display 20px #2D4A2B)
  - Giữa: Nút chuyển đổi chế độ xem: [● 🕸️ SPIDER ARENA] [○ 📰 EDITORIAL DIGEST] (Pill Switcher)
   - Phải: Engine Status: "SYSTEM 1 TB: Laya 30-60ms / D3 150-200ms NVIDIA GPU" + Nút Âm thanh [🔊 SFX: 70%] + Pacing [⚡ SYNC | ☕ CHILL]

[E3] Khung Chính Trái - Text & Code Canvas (63% chiều rộng): x:2% y:9% w:63% h:81% | fill: #FFFFFF, rounded: 22px, border: 1px #E8F0E2, shadow: soft
  - Họa tiết nền: Hoa văn cành lá chìm mờ ở góc (Watermark Botanical Ink #F5FAF0)
  - Tiêu đề tin/Repo: "Ngân Hàng Nhà Nước Họp Khẩn: Duy Trì Trần Lãi Suất & Ổn Định Tỷ Giá" (Playfair Display 26px #2D4A2B)
  - Thanh Thông Tin & Chuyển Đổi Song Ngữ (Meta Header Bar):
    * Góc trái: Nguồn tin & Thời gian: "Bloomberg / CaféF Vĩ Mô • 10/10/2026 • 2 phút trước" (Be Vietnam Pro 13px #5F7D58)
    * Góc phải: Công tắc song ngữ: [● 🇻🇳 Tiếng Việt (Tóm tắt AI)] [○ 🌐 Bản Gốc (Original Text)] (Pill bo tròn 12px, fill #F0F5EA, border 1px #E0EBD6, font 12px)
  - Toàn văn bài báo / Code blocks (Body): Trải dài thoáng đãng, font Be Vietnam Pro 15px, line-height 1.8.
  - Vị trí từ khóa gắn thẻ:
    * `<mark data-spider-index="0">LÃI SUẤT ĐIỀU HÀNH</mark>` (Highlight pastel hồng đào #F8AFA6)
    * `<mark data-spider-index="1">THANH KHOẢN HỆ THỐNG</mark>` (Highlight vàng hổ phách #E5B869)
    * `<mark data-spider-index="2">VN-INDEX 1.300 ĐIỂM</mark>` (Highlight xanh non #C8DEC0)
  - Asset Con Nhện [SPIDER]: Đang đứng ngay trên từ khóa "LÃI SUẤT ĐIỀU HÀNH", chân phát xung sóng nước (Ripple ring #A8D5BA).
  - HIỆU ỨNG GIĂNG TƠ (Spider Web Casting): Một sợi tơ ánh sáng siêu mảnh (stroke 0.75px, cong mềm mại SVG Bezier màu xanh ngọc #A8D5BA bán trong suốt) đang PHÓNG VÚT TỪ CHÂN NHỆN vượt qua khoảng trống 300px để cắm thẳng vào [NODE KINH TẾ] bên phải!

[E4] Khung Phải - Vòng Cung Quyết Định Decision 3 (32% chiều rộng): x:66% y:9% w:32% h:81% | fill: #FBFDF9, rounded: 22px, border: 1px #E0EBD6
  - Tiêu đề khung: "DECISION 3 NEURAL ROUTING ARC" (15px Bold #2D4A2B) + Phụ đề "Mỗi thực thể, một nhánh rẽ • Anti-Clickbait: PASS"
  - Cụm các Node Quyết Định (Decision Nodes) xếp theo vòng cung:
    * Node 1 (Đang nhận tơ - Chớp sáng): [🏛️ NODE KINH TẾ & DÒNG TIỀN]
      - Trạng thái: Viền phát sáng hồng đào #F8AFA6, số đếm: "4 sợi tơ đã kết nối"
      - Chi tiết: Lãi suất trần 4.5% • Tín dụng tăng trưởng 12%
    * Node 2: [📈 NODE CHỨNG KHOÁN (VN-INDEX)]
      - Viền xanh non #C8DEC0, số đếm: "2 sợi tơ"
    * Node 3: [🥇 NODE GIÁ VÀNG & TỶ GIÁ USD/VND]
      - Viền vàng hổ phách #E5B869, số đếm: "1 sợi tơ"
    * Node 4: [🌐 NODE CHÍNH SÁCH VĨ MÔ]
      - Viền be nhạt #E8EFE3, số đếm: "3 sợi tơ"
    * Node 5 (Dưới cùng): [⚡ BREAKING NEWS & RỦI RO]
      - Mức độ ưu tiên: Cao • Tâm lý thị trường: TÍCH CỰC (+0.78)
  - Action Box: Nút bấm nổi bật "⚡ TỔNG HỢP TOÀN VĂN TIẾNG VIỆT (SYSTEM 2)" (Fill: #2D4A2B, chữ trắng)

[E5] Bottom Telemetry Bar (Bảng Chỉ Số Đáy): x:2% y:91% w:96% h:7% | fill: #F0F5EA, rounded: 14px, border: 1px #E0EBD6
   - Metric 1: "⚡ Độ trễ System 1 TB: Laya 30-60ms / D3 150-200ms (NVIDIA GPU)" (Green dot #00BA88)
  - Metric 2: "🕸️ Tơ đã giăng: 6 / 14 thực thể" (Bold #2D4A2B)
  - Metric 3: "🧮 Ma trận Token Đã Đọc: [●●●●●●○○○○○○○○]" (Dot matrix grid 14 chấm đổi màu theo nhịp nhện)
  - Metric 4: "⏱️ FPS: 60.0 • VRAM: 1.8GB / RTX 3050 • Tauri Native"
```

* **Prompt Canva AI vẽ UI Screen SPIDER WEB ARENA (Chuẩn Phần Mềm Desktop):**
```text
Desktop software application UI screenshot of Spider News Radar, flat 2D direct front-facing viewport, 63-32-5 split panel layout (63% reader, 32% decision arc, 5% telemetry bar), elegant ivory paper #FAF8F5 background, native window title bar with macOS window buttons and System 1 latency online badge showing average latency, left 63% panel displaying financial news text with subtle bilingual language toggle pill [Vietnamese | Original] and glowing translucent teal spider silk bezier thread shooting across the screen, right 32% panel containing glowing circular decision nodes, bottom telemetry status bar with dot matrix token grid, Figma UI design system, high information density, crisp typography, 8k resolution --no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle, isometric table shot
```

---

### MÀN HÌNH 2: EXECUTIVE INTELLIGENCE DIGEST (Bản tin Vĩ mô Tổng hợp)
* **Archetype:** `editorial-magazine` (Tạp chí tri thức 2 cột có trích dẫn lớn).
* **Mục tiêu:** Bản tổng hợp cô đọng của LLM System 2 xâu chuỗi 30 tin thành 1 báo cáo duy nhất.

```yaml
Elements Layout:
[E2] Top Banner & Biểu Đồ Cơ Cấu Dòng Tin: x:6% y:3% w:88% h:14%
  - Tag nhỏ: "BẢN TIN CHIẾN LƯỢC VĨ MÔ HÔM NAY • HỆ THỐNG SPIDER RADAR" (Be Vietnam Pro 12px #5F7D58)
  - Tiêu đề chính: "Bức Tranh Kinh Tế & Công Nghệ Toàn Cầu" (Playfair Display 36px #2D4A2B)
  - Biểu đồ Phân bổ Dòng tin (Category Distribution Bar): Thanh chia đoạn ngang:
    `[ 45% Kinh tế vĩ mô #C8DEC0 ] [ 30% Chính trị quốc tế #F6E6C2 ] [ 25% GitHub AI #F8AFA6 ]`

[E3] Ba Khung Độc Lập Chuyên Biệt Của LLM System 2 (Modular Holistic Panels): x:6% y:19% w:88% h:70%
  - Khung 1: 🏛️ TOÀN CẢNH KINH TẾ & DÒNG TIỀN (Macro & Markets): Fill #F2F7ED, rounded 16px, border: 1px #D5E2CB
    * Heading: "1. Lãi Suất, Tỷ Giá & Thị Trường Chứng Khoán" (18px SemiBold #2D4A2B)
    * Tóm tắt xâu chuỗi: Báo cáo do LLM tổng hợp các động thái của FED, NHNN, tỷ giá USD/VND.
    * Chỉ số mini: [Tâm lý vĩ mô: +0.65 Tích cực] [Dòng tiền: Ổn định]
  - Khung 2: 🌐 TOÀN CẢNH CHÍNH TRỊ & ĐỊA CHÍNH TRỊ (Geopolitics & Policy): Fill #FBF3E8, rounded 16px, border: 1px #EDDEC8
    * Heading: "2. Ngoại Giao, Bầu Cử & Rủi Ro Thuế Quan" (18px SemiBold #2D4A2B)
    * Tóm tắt xâu chuỗi: Tác động của các nghị quyết thương mại và địa chính trị tới chuỗi cung ứng.
    * Thước đo rủi ro: [Mức độ rủi ro: Trung bình - Vàng hổ phách #E5B869]
  - Khung 3: 🐙 TOÀN CẢNH GITHUB & ĐỘT PHÁ AI (Open-Source Tech Radar): Fill #F7EFF0, rounded 16px, border: 1px #ECCFD2
    * Heading: "3. Làn Sóng Mô Hình Nhỏ (SLM) & Công Nghệ Mới" (18px SemiBold #2D4A2B)
    * Tóm tắt xâu chuỗi: Các phát hiện công nghệ nổi bật trong ngày (Laya System 1, Qwen 2.5, Rust tools).
    * Tag: [Top Repo: NandhaKishorM/laya ⭐ 4.2k]

[E4] Bottom Actions: x:6% y:91% w:88% h:6%
  - Nút: [📋 Sao chép tóm tắt] [📤 Xuất file Markdown / PDF] [⬅ Quay lại Màn hình Radar]
```

* **Prompt Canva AI vẽ UI Screen EXECUTIVE DIGEST (Chuẩn Phần Mềm Desktop):**
```text
Desktop software application UI dashboard of an executive financial news report, flat 2D direct front-facing viewport, native desktop window frame, 3 modular card panels with thin borders and soft drop shadows, category distribution bar chart, Fraunces serif headlines, sage green and ivory aesthetics, export button bar, realistic modern SaaS interface, Figma UI design system, high information density, 8k resolution --no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle
```

---

### MÀN HÌNH 3: GITHUB TECH RADAR (Chế độ chuyên sâu cho Developer)
* **Archetype:** `code-editorial` (Sự kết hợp giữa Code Terminal hiện đại và Tạp chí Thơ mộng).
* **Mục tiêu:** Nhện bò trên trang `README.md` của GitHub, bóc tách công nghệ lõi.

```yaml
Elements Layout:
[E1] Background: x:0% y:0% w:100% h:100% | fill: #F7F5F0 (Màu giấy tái chế ấm)
[E2] Top Bar GitHub Header: x:3% y:2% w:94% h:8%
  - Breadcrumb: "github.com / NandhaKishorM / laya" (JetBrains Mono 18px #2D4A2B)
  - Stats Badges: [⭐ 4.2k Stars] [🍴 312 Forks] [Apache-2.0] (Pill tags viền mảnh)

[E3] Cột Trái - Code & README Viewer (60%): x:3% y:12% w:60% h:84% | fill: #FFFFFF, rounded: 18px
  - Header giả lập macOS: 3 nút tròn pastel (hồng nhạt, vàng nhạt, xanh nhạt)
  - Nội dung README: Trình bày Markdown có syntax highlighting màu pastel nhã nhặn.
  - Vị trí Nhện [SPIDER]: Đang đứng trên code block:
    `POST /v1/systemone`
  - Vết chân nhện: Để lại các giọt sương phát sáng nhẹ nối từ chữ này sang chữ khác.

[E4] Cột Phải - LLM Tech Breakdown (32%): x:65% y:12% w:32% h:84% | fill: #F3F7EF, rounded: 18px
  - Tiêu đề: "ĐÁNH GIÁ CÔNG NGHỆ BỞI AI" (18px #2D4A2B)
  - Mục 1: "🎯 Bài toán giải quyết:" (Phân loại single-pass thay thế LLM cồng kềnh)
  - Mục 2: "⚡ Độ đột phá kỹ thuật:" (Non-autoregressive, độ trễ < 10ms)
  - Mục 3: "🛠️ Độ sẵn sàng thực tế:" (Điểm 9/10 - Đã có docker image chạy ổn định)
  - Nút bấm: [📥 Clone Repo] [⭐ Lưu vào Bộ sưu tập Tech Vault]
```

* **Prompt Canva AI vẽ UI Screen GITHUB RADAR (Chuẩn Phần Mềm Desktop):**
```text
Desktop software application UI interface of a modern GitHub markdown code reader and AI telemetry panel, flat 2D direct front-facing viewport, split 60-34 code viewer and AI evaluation panel, pastel syntax highlighted code block, breadcrumb header with star badges, subtle botanical accents, Figma UI component design, JetBrains Mono font details, 8k resolution --no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle
```

---

### MÀN HÌNH 4: TREND VAULT & KNOWLEDGE GRAPH (Kho Lưu Trữ Xu Hướng)
* **Archetype:** `branch-spine` (Cành cây tri thức phân nhánh theo thời gian - 18-G).
* **Mục tiêu:** Thống kê lịch sử tin tức 7 ngày/30 ngày dưới dạng nhánh cây thảo mộc.

```yaml
Elements Layout:
[E1] Background: x:0% y:0% w:100% h:100% | fill: #FAF8F5
[E2] Header: x:5% y:4% w:90% h:10%
  - Title: "Cành Cây Tri Thức & Xu Hướng Tuần Qua" (Playfair Display 32px #2D4A2B)
  - Subtitle: "Thống kê 248 bài báo & 42 repo do Nhện Spider thu thập" (Be Vietnam Pro 14px #5F7D58)

[E3] Trục Chính Cành Cây (Branch Spine Graphic): x:10% y:20% w:80% h:72%
  - Trục dọc giữa: Thân cây nét mực uốn lượn mềm mại (#2D4A2B, stroke 2px).
  - Nhánh 1 (Thứ Hai): Rẽ trái $\rightarrow$ Cụm lá "Thuế Quan Mỹ - Trung" (45 bài)
  - Nhánh 2 (Thứ Tư): Rẽ phải $\rightarrow$ Cụm lá "Lãi Suất & Tín Dụng NHNN" (80 bài)
  - Nhánh 3 (Thứ Sáu): Rẽ trái $\rightarrow$ Cụm hoa đào "Sốt Chip Bán Dẫn & AI Local" (120 bài)
  - Mỗi cụm lá là một chiếc thẻ hình oval/lá cây (Pill surface #F0F5EA) có thể bấm vào xem lại danh sách bài gốc.
```

* **Prompt Canva AI vẽ UI Screen TREND VAULT GRAPH (Chuẩn Phần Mềm Desktop):**
```text
Desktop software application dashboard interface showing an interactive timeline knowledge graph shaped like delicate botanical tree branches, flat 2D direct front-facing viewport, clean software UI window, date nodes and topic leaf tags, ivory and sage green palette, elegant data visualization software, Figma UI design system, 8k resolution --no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle
```

---

### MÀN HÌNH 5: SYSTEM SETTINGS & TELEMETRY (Bảng Điều Khiển Kỹ Thuật)
* **Archetype:** `ink-pill-modal` (Hộp thoại thẻ ngọc phong cách cổ điển thanh lịch - 18-H).
* **Mục tiêu:** Giám sát Docker Decision 3.0 Lite (`d3-serve-1`), tình trạng GPU RTX 3050, cache 3 tầng và cài đặt hệ thống.

```yaml
Elements Layout:
[E1] Background Scrim: x:0% y:0% w:100% h:100% | fill: rgba(45, 74, 43, 0.25) (Lớp màng mờ)
[E2] Modal Box (Hộp thoại trung tâm): x:25% y:12% w:50% h:76% | fill: #FAF8F5, rounded: 24px, border: 2px #E0EBD6
  - Header: "THIẾT LẬP HỆ THỐNG & ĐỘNG CƠ AI" (Playfair Display 24px #2D4A2B)

  - Section 1: "Trạng thái Docker Decision 3.0 Lite (GPU)"
    * Box xanh non: `http://127.0.0.1:8000/health` • Model: d3-lite (0.85B Qwen 3.5) • PING: 4ms • VRAM: 1.8 GB / RTX 3050 • Restart: Manual
    * Nút điều khiển: [▶️ Bật Container] [⏹️ Dừng Container (Giải phóng VRAM)] [🔄 Kiểm tra kết nối]

  - Section 2: "Cấu hình LLM System 2"
    * Dropdown: [Gemini 2.5 Flash (Cloud API) | Qwen 2.5 7B (Ollama Local)]
    * Input box: Nhập API Key (Màu viền #D5E2CB)

  - Section 3: "Quản lý Nguồn tin Động (Feed Manager)"
    * Danh sách nguồn kèm Toggle Switch & Tag chuyên mục:
      - [ON] CaféF Chứng Khoán (Pill xanh lá: #chung_khoan)
      - [ON] Kitco Gold News (Pill vàng: #vang)
      - [ON] CoinDesk Wire (Pill tím pastel: #crypto)
      - [ON] CaféF Vĩ Mô (Pill nâu đất: #kinh_te)
      - [ON] GitHub AI Trending (Pill xanh ngọc: #github)
    * Khung thêm nguồn mới: [Input Tên Nguồn] [Input Link RSS] [Dropdown: Chọn Chủ Đề] [+ Thêm & Kiểm Tra]

  - Section 4: "Giao diện & Âm thanh"
    * Skin Nhện: [○ Nhện Thảo Mộc] [● Nhện Thủy Tinh Giọt Sương] [○ Nhện Gốm Sứ]
    * Âm lượng SFX Giọt Nước: Slider 70%

  - Footer: Nút [LƯU THIẾT LẬP] (#2D4A2B, chữ trắng)
```

* **Prompt Canva AI vẽ UI Screen SETTINGS & FEED MANAGER (Chuẩn Phần Mềm Desktop):**
```text
Desktop software application modal window for system settings and RSS feed manager, flat 2D direct front-facing viewport, translucent scrim background, centered ivory dialog box with soft borders, list of news sources with toggle switches and category pills, API key inputs, spider skin selector, realistic SaaS software preferences UI, Figma UI design system, 8k resolution --no presentation slide, keynote, powerpoint, pitch deck, bullet points, marketing poster, brochure, 3d floating clay characters, abstract floating blobs, empty slide margins, giant headline text, stock photo background, laptop mockup on desk, tilted angle
```

---

## 🛠️ HƯỚNG DẪN THAO TÁC TRÊN CANVA CHO BẠN (CHUẨN DESKTOP APP):

1. **Bước 1: Khởi tạo Canvas chuẩn Màn hình Máy tính:**
   * Vào [Canva.com](https://www.canva.com) $\rightarrow$ Bấm nút **"Cỡ tùy chỉnh" (Custom Size)** $\rightarrow$ Nhập chính xác: **1920 x 1080 px** (Tỷ lệ Desktop App 16:9).
   * *Lưu ý:* Tuyệt đối không chọn mẫu "Bản thuyết trình" (Presentation) hay "Poster" để tránh bị Canva tự động gợi ý layout slide.
2. **Bước 2: Thiết lập Màu nền chính:**
   * Bấm vào nền canvas $\rightarrow$ Đặt mã màu chính: `#FAF8F5` (cho Light Mode Giấy Ngà) hoặc `#121513` (nếu chọn Dark Mode Dạ Quang).
3. **Bước 3: Dùng Canva Magic Media (Text-to-Image):**
   * Vào mục **Ứng dụng (Apps)** $\rightarrow$ Mở **Magic Media**.
   * Dán nguyên văn đoạn **Prompt chuẩn UI Application** ở từng màn hình tương ứng ở trên.
   * Chọn phong cách: **Concept Art / Digital Art / Photo** $\rightarrow$ Bấm Tạo.
4. **Bước 4: Căn chỉnh Layout bằng Thước kẻ (Rulers & Guides):**
   * Bật **File $\rightarrow$ Cài đặt chế độ xem $\rightarrow$ Hiển thị thước & đường gióng**.
   * Kéo các đường gióng theo đúng tỷ lệ phần trăm đã đặc tả (Ví dụ: vạch chia 63% cho Arena, 32% cho Decision Arc và 5% cho Bottom Telemetry Bar).
5. **Bước 5: Typography & Elements:**
   * Sử dụng đúng font chữ: `Playfair Display` (tiêu đề bài viết), `Be Vietnam Pro` (thân bài tin tức), và `JetBrains Mono` / `Courier` (cho các chỉ số đo đạc, độ trễ ms).

Bản spec chuẩn này đảm bảo AI Canva sẽ render ra **giao diện một ứng dụng máy tính chuyên nghiệp, sắc nét, mật độ thông tin cao**, hoàn toàn thoát khỏi cái bóng của một bản slide thuyết trình!
