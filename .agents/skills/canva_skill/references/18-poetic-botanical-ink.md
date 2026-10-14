# 18 — POETIC / BOTANICAL / INK (3 phong cách trình bày đặc biệt)

> **Lớp design, nạp khi Q1 (tông cảm xúc) trong `00 §1.1` trả lời là b) mộng mơ / a) trang nghiêm có thơ**, hoặc khi nội dung có hình vẽ cành – lá – thủy mặc – tranh cổ.
> Bổ sung cho `15-organic-image-blend.md` (giải quyết ảnh); file này giải quyết **cả bố cục + chữ + ornament**.

Nghiên cứu từ bộ ảnh tham chiếu user: cover "Vịt Văn Tích" (pastel wavy + lettering dây leo), poster "Niffler's Fancy" (branch spine infographic), thiệp "Bát Vân Xuyên" (pill + seal + thủy mặc).

---

## 1. Ba pattern, ba nhánh style

| Pattern | Dùng khi | Palette sẵn có | Font | Archetype |
|---|---|---|---|---|
| **F. Wavy-Pastoral** | thơ, trích dẫn, văn hoá dân gian, mở bài | pastel meadow | custom lettering + Be Vietnam Pro | wavy-asymmetric |
| **G. Branch-Spine** | quy trình, giai đoạn, phát triển, lịch sử dài | botanical ink | Fraunces/Merriweather + Be Vietnam Pro | branch-spine |
| **H. Ink-Pill-Seal** | đề tài cổ phong, di sản, triết học, trang nghiêm | ink jade + gold | CJK serif + Be Vietnam Pro | ink-pill-seal |

---

## 2. F. WAVY-PASTORAL (mở bài, trích dẫn, mood)

### Triệu chứng nhận dạng
- Nền trắng / giấy **chiếm 60-70%**, không có khung, không có viền.
- Ảnh ở góc trái hoặc góc phải, cắt viền **sóng lượn** (wave) hoặc blob cỏ hoa.
- Chữ tiêu đề là **lettering vẽ tay dây leo** — không phải font hệ thống.
- Trang trí: mũi tên chấm, đường lượn, tam giác nhỏ, sóng nhỏ ở đáy.
- Palette: **pastel đơn sắc** — 1 họ màu chủ đạo + 1 accent lệch sắc bùng trên.

### Palette F (copy thẳng vào spec)
```
bg        #FFFFFF
surface   #E8F5D8   (xanh non nhạt — ô chữ thứ cấp, sóng đáy)
accent    #F8AFA6   (hồng đào — CHỈ dùng cho từ khóa / dấu nhấn, ~10%)
text      #2D4A2B   (xanh rừng rất đậm — đọc tốt trên nền trắng, 11.9:1)
text-soft #6B8E5A   (xanh trung — caption, ~4.6:1)
```
Biến thể: thay họ xanh → họ hồng/be theo đề tài, giữ nguyên quan hệ sáng/tối.

### Font F
```
Tiêu đề : custom lettering (PNG trong suốt) — 1 từ khóa, KHÔNG cần chữ hệ thống
           → Canva: Elements → search "hand lettering" / "doodle text" / "wreath lettering"
Sub-head : Be Vietnam Pro 600/400, 32-40px, màu text
Body     : Be Vietnam Pro 400, 32px
Caption  : Be Vietnam Pro 400, 24px, màu text-soft
```
Không có lettering → dùng **Playfair Display Italic 800** (serif nghiêng, cảm giác thủ công gần nhất) + thêm ornament bù (mũi tên chấm, squiggle line).

### Layout F — `wavy-asymmetric`
```
[E1] img      x:0%   y:0%   w:46%  h:88%   frame: wave-bottom-right  | organic cut
[E2] wave-fill x:0%   y:76%  w:46%  h:24%   fill:#E8F5D8              | sóng đáy, đè dưới E1
[E3] title    x:52%  y:22%  w:42%  h:16%   lettering PNG / Playfair Italic 800, 96px, #2D4A2B
[E4] accent   x:52%  y:40%  w:16%  h:1.5%  rule #F8AFA6               | gạch dưới 1 từ khóa
[E5] body     x:52%  y:48%  w:40%  h:22%   32px, #2D4A2B
[E6] caption  x:52%  y:74%  w:30%  h:6%    24px, #6B8E5A
[E7] ornament x:56%  y:14%  w:6%   h:8%    dotted arrow #6B8E5A      | dẫn mắt từ E3
```
- Ảnh **không box-shadow**, không viền — mép sóng màu `surface` là ranh giới duy nhất.
- **Cấm dùng `#F8AFA6` làm màu chữ.** Trên `#FFFFFF` chỉ đạt ≈1.9:1 → FAIL WCAG. Chỉ dùng cho rule/ornament/surface mảnh (10% diện tích). Mọi chữ trên nền sáng dùng `text #2D4A2B` hoặc `text-soft #6B8E5A` (≈5.2:1 trên trắng).
- E6 caption 24px dùng `#6B8E5A` — kiểm lại nếu nền thực tế là `#E8F5D8` thay vì trắng.
- Không đối xứng: để **12-16% lệch** giữa trục ảnh và trục chữ → có chủ đích, không phải lỗi (13 §3).
- Ornament chỉ 2-3 element/slide, đặt ở góc trống, mỗi deck tối đa 2 slide dùng.

### Cách làm trong Canva
| Việc | Cách |
|---|---|
| Ảnh viền sóng | Elements → search "wave frame" / "scribble frame" → kéo ảnh vào frame |
| Không có frame sóng | Ảnh chữ nhật → **Background Remover** → đắp 1 shape bo tròn cùng tông → thêm shape sóng `#E8F5D8` đè mép dưới |
| Lettering | Elements → search "hand lettering"/"doodle" → chọn màu text, đặt x:52% y:22% |
| Sóng trang trí | Elements → "squiggle" / "wavy line" → xoay nhẹ, đặt 2-3 bản nhỏ |
| Mũi tên chấm | Elements → "doodle arrow" → stroke mảnh, màu `text-soft` |

Với medium (a) HTML: dùng `clip-path: path()` cho mép sóng hoặc `mask-image` với SVG path — ghi shape path vào spec thay cho tên frame.
Với medium (b) pptx: dùng `add_picture` + `crop` vuông, bù lại bằng shape sóng PNG overlay; ghi chú giới hạn "không giữ được mép sóng vector".

---

## 3. G. BRANCH-SPINE (quy trình, giai đoạn, phát triển)

### Triệu chứng nhận dạng
- **Không dùng grid cột** — 1 cành/thân cây làm **trục đi dọc slide**.
- 4-6 mốc (Seedling → Sprout → Flowering → Fruiting) bám vào cành bằng đường nối.
- Mỗi mốc: icon/nhân vật nhỏ + thẻ chữ (card hoặc "mây xé").
- Nền: landscape/cây mờ (very low contrast, blur) — trục nổi lên trên nền.

### Palette G
```
bg        #F4F1E8   (giấy cũ)
ink       #2E4A3D   (xanh mực đậm — chữ + cành)
accent    #B8894A   (gold foil — tiêu đề, mốc nhấn)
accent-2  #6E8B5A   (xanh lá — lá cây)
surface   #FFFFFF   (thẻ chữ)
text-soft #5E6B5E   (caption, ~5.2:1)
```

### Font G
```
Tiêu đề : Fraunces 600 (organic serif) hoặc Merriweather 700 + gradient gold (#B8894A→#E8C87A)
Body     : Be Vietnam Pro 400/600, 32px
Số mốc   : Fraunces 700, 48px, màu accent
Caption  : Be Vietnam Pro 400, 24px
```

### Layout G — `branch-spine`
```
[E1] bg-scene  x:0% y:0% w:100% h:100%  img, blur 4-6px, opacity 35-45%, duotone #2E4A3D
[E2] stem      x:46% y:8% w:8%  h:84%  branch illustration (PNG trong suốt hoặc SVG), màu #6E8B5A
[E3] node-1    x:8%  y:12% w:32% h:18%  card #FFFFFF, radius 16px + shadow 15% | icon 24px + text
[E4] node-2    x:56% y:32% w:36% h:18%  card #FFFFFF (lệch phía đối diện cành)
[E5] node-3    x:8%  y:52% w:32% h:18%  card #FFFFFF
[E6] node-4    x:56% y:72% w:36% h:18%  card #FFFFFF
[E7] title     x:6%  y:4%  w:50% h:10%  72px gradient gold + leaf icon 32px lặp mỗi nhánh
```
Quy tắc bắt buộc:
- **Zig-zag**: node 1 trái → 2 phải → 3 trái → 4 phải (hoặc ngược lại nhưng **giữ nguyên cả slide**). Không xếp cả 4 cùng một phía — sẽ thành cột chữ, mất hết ý nghĩa cành.
- Card **phải đụng cành** (không rời hẳn) — 1 đường connector mảnh 1px `#B8894A` nối card vào cành.
- Nếu node có icon → **cùng 1 bộ icon, cùng stroke width** (05). Không trộn outline + filled.
- Số nhấn: **mỗi mốc chỉ 1 số liệu**, font gấp 1.5× body, không nhét 3 con số.
- Click order: title → (node-1) → (node-2) → ... 1 click/mốc (06 §2).

### Biến thể — danh sách phẳng (KHÔNG phải quy trình)
Nếu nội dung là **4 đặc điểm / 4 nhóm khái niệm** (không có thứ tự thời gian), KHÔNG dùng branch spine — dùng **`stem-list`**: 1 đường thẳng dọc + 4 card xếp cùng phía, số 01-04. Giữ "có nhịp" nhưng không gợi nhầm quy trình.

### Cách làm trong Canva
| Việc | Cách |
|---|---|
| Cành | Elements → search "botanical branch" / "floral line art" → PNG tối ưu cắt trước; xoay nhẹ để tự nhiên |
| Nền mờ | Ảnh → Effects → **Blur** ~30% + **Adjust → Brightness** +15% |
| Card | Elements → search "torn paper" / "cloud" (nếu muốn thẻ hình mây xé như ảnh tham chiếu) → fill `#FFFFFF` |
| Gradient gold chữ | Text → Effects → **Gradient** (2 chặng `#B8894A` → `#E8C87A`) → đặt góc chữ 45° |
| Connector | Elements → Line, stroke 1px `#B8894A`, đầu dạng tròn |

---

## 4. H. INK-PILL-SEAL (đề tài cổ phong, di sản, trang nghiêm)

### Triệu chứng nhận dạng
- **2 lớp**: khối ngoài hình pill/bo tròn dày (pill xanh đậm hoặc son) → bên trong **card chữ nhật bo góc** chứa tranh/ảnh.
- Chữ Hán-Việt + Hán Hỗn, hướng trộn (ngang + dọc) — cổ phong.
- Ornament: **ink-trail / rồng khói mực** nối chữ với cảnh; **seal tròn** chồng mép; mắt + sao lấp lánh rải rác theo quỹ đạo.
- Tổng thể **đối xứng, tĩnh, sang trọng** — khác hẳn F (vui, méo) và G (sinh trưởng).

### Palette H
```
bg        #0E1F1A   (ink jade rất đậm — nền)
pill      #1A5C42   (xanh đậm — khối ngoài)
surface   #F5F0E1   (giấy dó — card trong, chữ đậm trên nền này)
accent    #C9A227   (gold — tiêu đề, seal, đường viền)
text-inv  #F5F0E1   (chữ sáng trên pill)
ink-trail #1A5C42   (khói mực, rồng)
```
Quy tắc: chữ sáng **chỉ** trên `bg`/`pill`; chữ đậm `#0E1F1A` **chỉ** trên `surface`. Trộn hai chiều = mất WCAG.

### Font H
```
Tiêu đề : CJK serif — Noto Serif SC / Source Han Serif (chọn 1) 700, 72-88px, màu #C9A227
          → Canva: search "Noto Serif SC" hoặc dùng chữ Hán + font VN cho chú thích
Body     : Be Vietnam Pro 400, 32px, #F5F0E1
Nhãn dọc : Be Vietnam Pro 600, 28px, viết dọc (vertical text) — 1 nhãn, không lạm dụng
Seal     : image PNG seal tròn, hoặc chữ trong shape tròn fill #C9A227, text #0E1F1A
```

### Layout H — `ink-pill-seal`
```
[E1] pill       x:8% y:6% w:84% h:88%  fill:#1A5C42 radius: 999px (bo tròn toàn bộ)
[E2] card       x:16% y:14% w:68% h:72% fill:#F5F0E1 radius: 24px | ảnh tranh/artifact
[E3] title      x:22% y:20% w:40% h:14%  80px #C9A227 (trên nền ink, ngoài card) — nếu title nằm trong card dùng #0E1F1A
[E4] ink-trail  x:56% y:26% w:26% h:20%  PNG rồng khói mực #1A5C42, opacity 80% — nối chữ với cảnh
[E5] seal       x:74% y:76% w:10% h:10%  tròn #C9A227, chữ 24px #0E1F1A — chồng mép card
[E6] sparkle    x:30% y:64% w:4%  h:5%   ornament mắt/sao lấp lánh #C9A227
[E7] vlabel    x:88% y:20% w:4%  h:40%  text dọc 28px #F5F0E1
```
Quy tắc bắt buộc:
- **Seal chồng mép** (không đặt giữa card) — điểm nhấn cổ phong, đặt ở 1 góc dưới.
- Sparkle **tối đa 3**, rải theo đường cong nối title → card, không rải đều như texture.
- Ink-trail **1 con/slide**, opacity 70-85%, đuôi tan (PNG trong suốt) — không đặt nó đè lên chữ.
- Nếu ảnh trong card là tranh/thủy mặc → thêm grain 5% (04 §5) để không bị "sạch máy".

### Cách làm trong Canva
| Việc | Cách |
|---|---|
| Pill bo tròn | Elements → search "pill shape"/"rounded rectangle" → kéo cạnh bo về max (999px) |
| Card trong pill | Thêm rect thứ 2 radius 24px, đặt lên trên, lệch 6-8% mỗi phía |
| Rồng khói mực | Elements → search "ink splash"/"smoke brush" → Multiply lên nền tối → tông #1A5C42 |
| Seal | Elements → "seal"/"stamp" hoặc shape tròn + chữ, chồng mép, xoay 6-10° (có chủ đích) |
| Grain | Elements → "grain"/"noise" → phủ full-slide, opacity 5-8%, trên cùng |

---

## 5. Bảng chọn nhanh (dùng trong `00 §4`)

| Nếu Q1 cảm xúc = … | Và nội dung là … | → Pattern | Archetype |
|---|---|---|---|
| b) nhẹ nhàng, mộng mơ | trích dẫn, thơ, mood, mở bài | **F. Wavy-Pastoral** | wavy-asymmetric |
| b) mộng mơ | quy trình, hành trình, phát triển | **G. Branch-Spine** | branch-spine |
| c) gần gũi, vui | danh sách phẳng 3-6 mục | G biến thể **stem-list** | stem-list |
| a) trang nghiêm, uy nghiêm | di sản, lịch sử, cổ phong, triết học | **H. Ink-Pill-Seal** | ink-pill-seal |
| a) trang nghiêm | ảnh tranh/tượng/artifact | **15-E Museum dark** (đã có) | full-bleed-hero |

---

## 6. Checklist chung cho cả 3 pattern (chạy trước QA 12)

- [ ] **Nền không bao giờ trắng tinh 100%** với F/G — dùng `#FFFFFF` thì phải có wave/sóng/grain phá vỡ (tránh slide trông như template chưa chỉnh).
- [ ] Ảnh/ornament **không bao giờ** stretch méo; mép organic phải cùng tông palette.
- [ ] Mọi element mới có `alt` (00 §2) — kể cả lettering PNG, seal, ink-trail.
- [ ] Lettering/seal/sparkle **không lạm dụng**: F tối đa 2 slide có lettering, H tối đa 3 sparkle/slide, G 1 ink-trail/slide.
- [ ] Contrast kiểm **2 chiều** (H đặc biệt): sáng-trên-tối VÀ tối-trên-sáng — tính cả 2.
- [ ] Không archetype nào của 18 lặp 3 slide liên tiếp (01 §4).
- [ ] Pattern 18 **không** dùng cho slide data/chart nhiều số — quay về 10-data-infographic.

---

## 7. Tránh

- Trộn 2 pattern trong 1 slide (ví dụ pill + wavy + branch cùng lúc) → rối. **1 slide = 1 pattern.**
- Dùng F (mộng mơ) cho deck báo cáo tài chính → sai tông, người xem không tin.
- H nhưng nền sáng — mất hết yêu thuỳ cổ phong.
- G với 6+ node → thành slide liệt kê, nên tách thành 2 slide hoặc chuyển 3-col-grid.
- Cho AI tự vẽ lettering/rồng khói mực → luôn ưu tiên PNG trong suốt có sẵn, hoặc để chữ hệ thống + ornament thay thế.
