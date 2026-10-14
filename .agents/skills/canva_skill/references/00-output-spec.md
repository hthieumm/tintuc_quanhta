# 00 — OUTPUT SPEC (Hợp đồng đầu ra cho AI)

File này là **bắt buộc đọc trước khi sinh bất kỳ slide nào**. Nó thay thế kiểu "slide nên có ảnh lớn bên trái" bằng dữ liệu máy đọc được: mã màu hex, toạ độ %, id từng element, thứ tự đọc, thứ tự click, contrast đã tự tính.

## 1. Nguyên tắc: AI không mở Canva, không nhìn thấy slide

Vì vậy **mọi phán đoán phải có số liệu**. Cấm trả lời bằng mô tả định tính.
- ❌ "Dùng tiêu đề lớn, màu nhấn là vàng, ảnh chiếm 60% bên trái."
- ✅ Toạ độ + hex + px + contrast ratio + id + alt-text.

## 1.1 STYLE DIAGNOSIS (5 câu hỏi → chọn pattern, hỏi TRƯỚC khi nạp design file)

Sau khi đọc brief / phân tích nội dung slide, hỏi user (hoặc tự suy đoán nếu user không trả lời):

**Q1 — Tông cảm xúc (bắt buộc, chọn 1):**
> Deck muốn người nghe cảm thấy gì sau 3 giây nhìn slide đầu?
> a) Trang nghiêm, uy nghiêm · b) Nhẹ nhàng, mộng mơ · c) Gần gũi, vui tươi · d) Trẻ trung, năng động · e) Trầm tĩnh, học thuật · f) Vui nhộn, hoạt họa (guochao/国潮)

**Q2 — Loại nội dung (bắt buộc, chọn 1):**
> Nội dung chính thuộc loại nào?
> - Quy trình có bước / giai đoạn → branch spine (18-G)
> - Danh sách đặc điểm / nhóm khái niệm → stem-list (18-G biến thể); chỉ 3-col-grid khi pass guard §4
> - Số liệu cụ thể → big-number / chart (10-data)
> - Lịch sử có mốc năm → timeline (10-data) hoặc branch spine (18-G)
> - Định nghĩa / khái niệm lý thuyết → card + pill nhãn
> - Trích dẫn / câu quote → overlay card / wavy-pastoral (18-F)
> - Mood / mở bài cảm xúc → wavy-pastoral (18-F)

**Q3 — Loại ảnh (bắt buộc nếu deck có ảnh):**
> Bạn có ảnh riêng không?
> - Có ảnh thật (tự chụp / tư liệu) → ưu tiên ảnh thật, giữ nguồn
> - Có sẵn stock → tải Unsplash/Pexels/Pixabay (04)
> - Không có ảnh nào → vẽ/illustrate: flat/outline cùng palette, cấm AI-face
> - Có sẵn illustration flat → dùng được (điều kiện: giữ đúng palette, cùng stroke width)

**Q4 — Mật độ chữ (tuỳ chọn, chỉ hỏi nếu ≥10 slide):**
> Deck nhiều chữ hay ít chữ?
> - Tối giản: 1 ý/slide, ≤3 bullet
> - Vừa: 2-3 ý/slide, 3-4 bullet
> - Nhiều chữ: tài liệu đọc kèm → tách slide, dùng intro slide + chi tiết

**Q5 — Ràng buộc thương hiệu (chỉ hỏi 1 lần, cache luôn):**
> Có màu/font nào bắt buộc không? (VD đang dùng lụa đỏ + gold)

### Bảng ánh xạ Q1 + Q2 → pattern

| Q1 (cảm xúc) | Q2 (nội dung) | → Pattern / archetype | File |
|---|---|---|---|
| a) Trang nghiêm | Di sản, lịch sử, cổ phong, triết học | **H. Ink-Pill-Seal** | 18 |
| a) Trang nghiêm | Ảnh tranh/tượng/artifact | Museum dark | 15-E |
| a) Trang nghiêm | Luật pháp / dữ liệu pháp lý | Flat corporate, nền sáng | 01 |
| b) Mộng mơ | Trích dẫn, thơ, mood, mở bài | **F. Wavy-Pastoral** | 18 |
| b) Mộng mơ | Quy trình, hành trình, phát triển | **G. Branch-Spine** | 18 |
| b) Mộng mơ | Danh sách phẳng 3-6 mục | **G biến thể stem-list** | 18-G |
| c) Gần gũi, vui | Đặc điểm văn hoá dân gian | Organic cut + cutout nhân vật | 15-A/B |
| c) Gần gũi, vui | Sản phẩm / dịch vụ | 3-col-grid sản phẩm | 01 |
| d) Trẻ trung | Công nghệ, startup, số liệu | Asymmetric bold 2 màu | 01 |
| e) Học thuật | Nghiên cứu, phân tích | Paper texture + serif editorial | 15-C |
| e) Học thuật | Báo cáo kinh doanh | 3-col-grid + data | 10-data |
| f) Vui nhộn, hoạt họa | Lễ hội, văn hoá Á Đông, ẩm thực, sản phẩm trẻ | **I-1. Guochao-Stage** | 20 |
| f) Vui nhộn, hoạt họa | Cover / divider / quote / mood | **I-2. Guochao-Center** | 20 |
| f) Vui nhộn, hoạt họa | Danh sách đặc điểm 3-6 mục | **I-1 + stem-list dọc trong card** | 20 + 18-G |

**Quy tắc:** user không trả lời → AI **không dừng**, dùng bảng trên để suy đoán từ đề tài, ghi rõ:
`Style: <tên pattern> (suy đoán từ đề tài — nói nếu muốn đổi)`.
Không hỏi lại lần 2.

**Ghi vào header DECK SPEC (bắt buộc):**
```
Style: <tên pattern> | Q1:<a|b|c|d|e|f> | Q2:<loại nội dung> | Q3:<loại ảnh> | Q4:<mật độ> | Q5:<brand>
```

## 2. Hợp đồng đầu ra (template bắt buộc)

````markdown
## DECK SPEC — <tên deck>
Mode: <new | fix-existing>
Medium: <a-html | b-pptx | c-canva-spec>
JSON: <deck_spec.json theo 19-deck-schema.md — chỉ khi Medium = b-pptx; bỏ dòng này với (a) và (c)>
Style: <tên pattern> | Q1:<a|b|c|d|e|f> | Q2:<loại nội dung> | Q3:<loại ảnh> | Q4:<mật độ> | Q5:<brand>
Grid: 12 col | canvas 1920×1080 | margin 5% (96px) | gutter 24px | pitch 7.60%
Palette: bg #XXXXXX | surface #XXXXXX | accent #XXXXXX | text #XXXXXX | text-inverse #XXXXXX
Type: H1 72px/800 <Family> | H2 48px/600 <Family> | Body 32px/400 <Family> | Caption 24px/400 <Family>
Fonts loaded: <2 family names, tiếng Việt đủ dấu — xác nhận>
Motion: total_clicks <n> | duration_sec <n> | pacing <total_clicks ÷ slide_count> clicks/slide | transition <type> <dir> <0.7s>
         (b-pptx: ghi `total_clicks N/A — không on-click` và bỏ transition)

### SLIDE <n> — <type: cover|agenda|divider|content|data|quote|cta|closing>
Title (quantified claim, không phải nhãn chung): "<tiêu đề có quan điểm>"
Archetype: <full-bleed-hero | split-50-50 | hero-caption | 3-col-grid | magazine | overlay-card | asymmetric | wavy-asymmetric (18-F) | branch-spine (18-G) | stem-list (18-G) | ink-pill-seal (18-H) | guochao-stage (20-I1) | guochao-center (20-I2)>
Intent: <1 câu: slide này làm người xem hiểu/nhớ điều gì>
Contrast: text #XXXXXX on #XXXXXX = <ratio>:1 PASS
Notes: <1-2 câu để nói, ≤25 từ>

Elements (reading order = thứ tự đọc; click order = thứ tự hiện):
  [E1] <role: title|subhead|body|caption|img|icon|rule|chip|number>
       x:8% y:10% w:60% h:12% | z:2 | align:left | font:H1 72px/800 <Family>
       color:#XXXXXX | tracking:0 | line-height:1.1
       alt: "<mô tả ảnh cho screen reader>"   ← bắt buộc với role=img/icon
       animation: <fade|rise|pan-left|pop|scale> on-click
  [E2] ...
Click order: E1 → E2 → E3 → E4
Transition: <match-move | pan-left | zoom | dissolve> <dir> 0.6s
Continuity: <nếu có — element nào kế thừa từ slide trước, match-move gì>
````

**Bắt buộc:**
- Mọi `role=img|icon` có `alt`.
- Mọi màu dạng hex 6 ký tự, không dùng tên màu ("đỏ", "vàng").
- Mọi element có `x/y/w/h` **theo %** (không px — để adapter đổi theo canvas).
- `click order` khớp `reading order` nếu không có lý do staging.
- Medium (b) → kèm `deck_spec.json` theo `19-deck-schema.md`; (a)/(c) không cần.

## 3. Chế độ `fix-existing` (sửa deck Canva đang có)

Input từ user: **ảnh chụp slide** + mô tả. Output thêm 2 phần:

````markdown
## EXISTING DECK AUDIT
Slide count: <n> | Canvas: <size> | Theme fonts: <nhận diện từ ảnh>
Detected palette: #.. #.. #.. (ghi rõ suy đoán từ ảnh)
Issues found (mỗi dòng = 1 lỗi + vị trí + cách sửa):
  - S07 · title lệch 4% khỏi lề trái → chỉnh x:8%
  - S12 · contrast #FFF trên ảnh chụp = 2.1:1 → thêm scrim 50%
  - S03 · 2 archetype liên tiếp giống nhau → đổi sang asymmetric

## PATCH SPEC
Slide <n>: [CHANGE] <element role/id> <before> → <after>
Slide <n>: [ADD] <new element with full spec>
Slide <n>: [REMOVE] <element> — lý do
Slide <n>: [KEEP] <element> — đã đúng, không đụng
````

Quy tắc sửa deck: **tối thiểu can thiệp** — `[KEEP]` mặc định cho mọi element không nêu lỗi; không đổi palette/font toàn deck trừ khi user yêu cầu; sửa 1 slide/lần để user duyệt.

## 4. Bảng quyết định IF/THEN (thay tính từ mơ hồ)

**Guard chọn layout cho nội dung liệt kê — kiểm TRƯỚC mọi dòng bảng dưới, không pass thì bảng dưới không áp dụng:**
1. Đếm số nhóm ý: đúng 2 nhóm → `split-50-50`, **cấm** 3-col-grid (cột thừa).
2. Mỗi mục >2 dòng body HOẶC ≥3 bullet → `stem-list` / card dọc 1 cột, **cấm** chia cột.
3. Chỉ dùng `3-col-grid` khi đủ cả 3 điều kiện: ≥3 mục · mỗi mục ≤2 dòng · các mục song song (không quan hệ trước/sau, tổng/quan, nhân/quả).
4. Không đếm được số mục → mặc định `stem-list`, **không** mặc định 3-col-grid.

| Nếu deck có… | Archetype | Type | Palette nghiêng |
|---|---|---|---|
| ≤8 slide, nội dung lý thuyết | split-50-50 | Be Vietnam Pro 700/400 | neutral + 1 accent |
| Bài lịch sử, có mốc năm | timeline (10-data) hoặc **branch-spine (18-G)** | Playfair Display + Be Vietnam Pro | nền tối + gold |
| Văn hóa dân tộc / bảo tàng | full-bleed-hero + organic cut (15) | display serif + sans | nền ảnh tối + gold |
| ≥3 nhóm số liệu | 3-col-grid hoặc big-number | Montserrat 800/400 | neutral + accent 1 màu |
| Có so sánh trước/sau | split-50-50 (2 số đối xứng) | tabular numerals | accent cho số "sau" |
| Nhiều ảnh lịch sử | frameless collage (15-B) | caption 24px | paper texture + 1 màu |
| Có quy trình (3-5 bước) | **branch-spine (18-G)** hoặc 3-col-grid số lớn | Fraunces/Be Vietnam Pro 800 | accent cho số bước |
| Câu chuyện từ tổng quan → chi tiết | zoom storytelling (14-B) | display + caption | 1 tông ảnh xuyên slide |
| Tiếng Việt, giáo dục/giảng dạy | split-50-50 / hero-caption | Be Vietnam Pro | sáng, accent ấm |
| Báo cáo kinh doanh | 3-col-grid + data | Inter/Montserrat | corporate 1 accent |
| **Trích dẫn / thơ / mở bài cảm xúc** | **wavy-asymmetric (18-F)** | lettering + Be Vietnam Pro | pastel meadow |
| **Đề tài cổ phong / di sản / triết học** | **ink-pill-seal (18-H)** | Noto Serif SC + Be Vietnam Pro | ink jade + gold |
| **Danh sách phẳng 3-6 mục, nhiều ảnh** | **stem-list (18-G biến thể)** | Be Vietnam Pro 700/400 | botanical ink |
| **Lễ hội / văn hoá Á Đông, vui nhộn hoạt hoạ** | **guochao-stage (20-I1)** | theo đề tài: Noto Serif SC hoặc BeVN Pro 800 + BeVN Pro | chu sa + gold + azurite trên ivory (mẫu, kế thừa Q2/Q5) |
| **Cover / divider guochao đối xứng** | **guochao-center (20-I2)** | như trên | như trên |

Từ "chuyên nghiệp / modern / clean / tối giản / editorial" **không được dùng** làm tiêu chí quyết định. Nếu brief chỉ có mấy từ này → hỏi Q1-Q5 ở §1.1, suy đoán từ đề tài nếu user không trả lời.

## 5. Self-check trước khi trả lời (pass/fail, tự tính)

Chạy từng dòng, không pass thì sửa spec rồi mới trả. Ghi kết quả 1 dòng cuối output: `Self-check: 8/8 PASS`.

| # | Điều kiện | Cách kiểm |
|---|---|---|
| 1 | Mọi element có `id` + toạ độ % đủ 4 số | đếm element không có x/y/w/h |
| 2 | Mọi `img|icon` có `alt` | đếm |
| 3 | Contrast mọi cặp chữ/nền ≥ 4.5:1 (chữ ≥48px: ≥3:1) | tự tính theo công thức 00 §6 |
| 4 | `total_clicks ≈ duration_sec / 11 ± 2` — chỉ medium (a)/(c); medium (b) ghi `N/A — python-pptx mất on-click, kiểm bằng số slide: 1 slide/30s nói` | chia và soá (pacing 06-animation) |
| 5 | Không archetype nào trùng 3 slide liên tiếp; nội dung liệt kê pass guard cột §4 | soá dãy archetype + đếm nhóm/mục |
| 6 | Tiêu đề slide nào cũng **không phải** nhãn chung (Overview/Introduction/Key takeaways) | đọc 5 tiêu đề |
| 7 | Palette ≤5 màu, fonts ≤2 family | đếm |
| 8 | Header DECK SPEC có dòng `Style:` + lý do (Q1-Q5 / suy đoán), và style khớp nội dung | kiểm header |

Nếu không pass được ≥6/8 → hỏi user 1 câu thay vì đoán.

## 6. Công thức contrast (tự tính, không gọi tool ngoài)

```
L = 0.2126·R + 0.7152·G + 0.0722·B     (R,G,B ∈ [0,1], sRGB tuyến tính hoá:
   c ≤ 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4)
ratio = (Lmax + 0.05) / (Lmin + 0.05)
```
Ví dụ: `#1A1A1A` trên `#FEF9E3` → ≈ 15.9:1 PASS.

## 7. Toạ độ % — quy ước

- Canvas 1920×1080, origin top-left.
- Margin an toàn 5% → nội dung nằm trong `x:5..95%`, `y:5..95%`.
- Vùng nội dung 90% / 12 cột = **cột 6.35%**; gutter 1.25% (24px); **pitch (cột+gutter) = 7.60%**.
  Cột `k` (0-indexed): `x = 5 + k × 7.60%`. Cột 0 → x:5%, cột 6 → x:50.6%, cột 11 → x:88.6% (cùng w:6.35%).
- Chia đôi: nửa trái `x:5..48.75%`, nửa phải `x:51.25..95%` (gutter 2.5% ở giữa).
- Mọi giá trị phải là số nguyên hoặc 1 chữ số thập phân.

## 8. Token dự kiến

Ví dụ đầy đủ 1 slide (mẫu chuẩn — lấy làm mốc format):

```
[E1] title  x:8% y:10% w:60% h:12% | z:2 | align:left | font:H1 72px/800 Playfair Display
     color:#FEF9E3 | line-height:1.1
     alt: n/a (role=title)
     animation: rise on-click
[E2] img    x:60% y:0% w:40% h:100% | z:1 | font:n/a
     alt: "Người phụ nữ đang thêu hoa văn lên lụa đỏ, chụp gần"
     animation: none (nền, hiện sẵn)
[E3] scrim  x:0% y:0% w:60% h:100% | z:1.5 | fill:#3A0A0A opacity:55%
     alt: n/a (role=rule) | animation: none
```