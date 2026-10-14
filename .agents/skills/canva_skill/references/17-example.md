# 17 — EXAMPLE (Ví dụ đầu-cuối: brief → spec → adapter)

**Nạp file này khi** đã đọc `00-output-spec` nhưng chưa rõ format output, hoặc user yêu cầu ví dụ. Đây là file học pattern — mọi lần sinh deck, đối chiếu với ví dụ này.

---

## Ví dụ 1 — Mode NEW, Medium (a) HTML/reveal.js

### Input (brief từ user)
> "Deck 8 slide, đề tài 'Đặc điểm dân tộc Việt Nam', ~4 phút nói, tiếng Việt, lụa đỏ + chữ vàng như lần trước. Xuất HTML/reveal.js."

### Xác nhận trước khi làm (16 § câu hỏi mở đầu)
`medium: a-html | mode: new | duration: 4 phút = 240s → pacing 240/11 ≈ 22 clicks → 22/8 ≈ 3 clicks/slide → đặt total_clicks 21 (trong 22±2)`

> Check #4 của 00 §5: với 8 slide/4 phút thì **3 clicks/slide** là đúng (7 clicks/slide là số cho deck dài ~10 phút). Đừng ghi 7.

### Output trả về (trích 3 slide đầu — toàn bộ deck chạy đúng format này)

````markdown
## DECK SPEC — Đặc điểm dân tộc Việt Nam
Mode: new
Medium: a-html
Grid: 12 col | canvas 1920×1080 | margin 5% (96px) | gutter 24px
Palette: bg #A61E22 | surface #FEF9E3 | accent #FACC15 | text #1A1A1A (chỉ dùng trên surface) | text-inverse #FEF9E3 (chỉ dùng trên bg)
Type: H1 72px/800 Playfair Display | Body 32px/400 Be Vietnam Pro | Caption 24px/400 Be Vietnam Pro
Fonts loaded: Playfair Display (VN subset ✓), Be Vietnam Pro (VN subset ✓)
Motion: total_clicks 21 | pacing 7/8 clicks per slide | transition pan-left 0.7s (nhất quán toàn deck)
Continuity: nền đỏ đậm (#A61E22) chạy xuyên suốt; số chương ghost "01" ở x:92% y:92% mọi slide

### SLIDE 1 — cover
Title: "Đặc điểm dân tộc Việt Nam — 54 dân tộc, 1 văn hoá giao thoa"
Archetype: full-bleed-hero
Intent: mở ra ấn tượng bằng ảnh chợ phiên, ấn định tông đỏ-gold
Contrast: text #FEF9E3 on #A61E22 = 6.8:1 PASS
Notes: "4 phút — đây là trang mở. Không nói gì hết, chờ 2s rồi bấm."

Elements (reading order = click order):
  [E1] img    x:0% y:0% w:100% h:100% | z:1 | font:n/a
       alt: "Chợ phiên vùng cao, dân phục nhiều màu sắc, nắng sớm"
       animation: none (hiện sẵn)
  [E2] scrim  x:0% y:0% w:100% h:100% | z:2 | fill:#3A0A0A opacity:55%
       alt: n/a | animation: none
  [E3] title  x:8% y:62% w:70% h:16% | z:3 | align:left
       font:H1 72px/800 Playfair Display | color:#FEF9E3 | line-height:1.1
       alt: n/a | animation: rise on-click
  [E4] rule   x:8% y:80% w:24% h:4px | z:3 | fill:#FACC15
       alt: n/a | animation: pan-left on-click
Click order: E3 → E4
Transition: pan-left 0.7s (section đầu — không có prior)
Notes → aside: "Slogan 1 câu: 54 dân tộc, 1 bức tranh văn hoá."

### SLIDE 2 — agenda
Title: "5 nét đặc trưng sẽ thấy ngay"   ← có con số, KHÔNG phải "Agenda"
Archetype: 3-col-grid
Intent: người xem biết 5 mục và bao lâu
Contrast:
  - Title #FEF9E3 on bg #A61E22 (vùng 0..22%) = 6.8:1 PASS (≥4.5:1)
  - Body #1A1A1A on card #FEF9E3 (vùng y:34..84%) = 15.9:1 PASS
  Card: fill #FEF9E3, radius 16px, chiếm x:8..38% / 38..70% / 70..95% trong vùng thân

Elements:
  [E0] card   x:6% y:30% w:88% h:62% | z:1 | fill:#FEF9E3 | frame:rounded 16px
        alt: n/a (role=container)
  [E1] title   x:8% y:10% w:70% h:10% | z:2 | font:H1 72px/800 Playfair Display | color:#FEF9E3
        animation: rise on-click
  [E2] number  x:8% y:34% w:26% h:34% | z:2 | font:96px/800 Be Vietnam Pro | color:#A61E22 | text:"01"
        animation: scale-in on-click
  [E3] body    x:8% y:68% w:26% h:16% | z:2 | font:Body 32px/400 | color:#1A1A1A
        text:"Quần áo, trang phục vùng cao"
        alt: n/a | animation: fade on-click
  [E4] icon    x:38% y:34% w:26% h:34% | z:2 | style:outline 24px #A61E22
        alt: "Biểu tượng nhà sàn vùng cao"
        animation: scale-in on-click
  [E5] body    x:38% y:68% w:26% h:16% | z:2 | text:"Kiến trúc nhà sàn"
        animation: fade on-click
  [E6] img     x:70% y:34% w:24% h:34% | z:2 | frame:rounded 24px
        alt: "Tín ngưỡng thờ cúng, trang thờ dân tộc Mường"
        animation: scale-in on-click
  [E7] body    x:70% y:68% w:24% h:16% | z:2 | text:"Thờ cúng tổ tiên"
        animation: fade on-click
Click order: E1 → (E2→E3) → (E4→E5) → (E6→E7)   ← pair = cùng 1 click khi group
Transition: pan-left 0.7s
Continuity: nền #A61E22 giữ nguyên, ghost "01" x:92% y:92%

### SLIDE 3 — divider chương 1
Title: "Quần áo — nói hộ cả dân tộc"
Archetype: overlay-card
...
````

### Output cuối (adapter a) — phần code sinh ra
Đoạn trích `deck.html` cho Slide 1–2 (đủ xem pattern; toàn deck lặp theo):

```html
<section data-background-color="#A61E22" data-transition="slide">
  <img src="assets/cho-phien.jpg" alt="Chợ phiên vùng cao, dân phục nhiều màu sắc"
       class="bg-cover">
  <div class="scrim" style="opacity:.55"></div>
  <h2 class="fragment fade-up t-h1">Đặc điểm dân tộc Việt Nam — 54 dân tộc, 1 văn hoá giao thoa</h2>
  <div class="fragment pan-left accent-rule"></div>
  <aside class="notes">4 phút — mở. Không nói, chờ 2s rồi bấm.</aside>
</section>

<section class="arch-3col" data-background-color="#A61E22" data-transition="slide">
  <h2 class="fragment fade-up t-h1">5 nét đặc trưng sẽ thấy ngay</h2>
  <div class="col"><span class="fragment scale-in num">01</span>
       <p class="fragment fade-up">Quần áo, trang phục vùng cao</p></div>
  <div class="col"><span class="fragment scale-in num">02</span>
       <p class="fragment fade-up">Kiến trúc nhà sàn</p></div>
  <div class="col"><img class="fragment scale-in frame" src="assets/tho-cung.jpg"
       alt="Tín ngưỡng thờ cúng, trang thờ dân tộc Mường">
       <p class="fragment fade-up">Thờ cúng tổ tiên</p></div>
  <aside class="notes">3 mục này nói nhanh, mỗi mục 1 câu.</aside>
</section>
```
Config: `Reveal.initialize({ width:1920, height:1080, hash:true, transition:'slide', transitionSpeed:'fast', plugins:[RevealNotes] })`.

**Self-check ghi cuối output:** `Self-check: 8/8 PASS — total_clicks 21 (kỳ vọng 22±2 ✓), archetype sequence cover→3col→overlay không trùng 3 liên tiếp ✓`

---

## Ví dụ 2 — Mode FIX-EXISTING, Medium (c) Canva spec

### Input từ user
> "Fix deck này, 3 ảnh chụp slide + ghi chú: 'Nền trắng buồn, ảnh nhỏ nhạt, slide 3 quá nhiều chữ'"

### Output trả về (trích phần audit + 1 patch)

````markdown
## EXISTING DECK AUDIT
Slide count: 3 (từ ảnh) | Canvas: 16:9 (khớp) | Theme fonts: Helvetica-like → thay Be Vietnam Pro (VN dấu)
Detected palette: #FFFFFF, #2E4A9E, #000000 (suy đoán từ ảnh — xác nhận với user trước khi đổi)
Issues found:
  - S01 · contrast body #2E4A9E trên #FFFFFF = 6.2:1 → pass, giữ
  - S01 · ảnh chiếm w:34% có phần trắng chết ở y:40..55% → đẩy ảnh lên y:10%, tăng h thành 70%
  - S02 · sắc trắng chiếm 78% diện tích (giá trị ước tính từ ảnh) → đổi nền #FEF9E3, thêm rule #A61E22
  - S03 · 7 bullet × 2 dòng = text block h:64% → tách thành 2 slide (3+4 bullet), mỗi bullet ≤6 từ
  - S03 · không có alt-text cho 2 ảnh → thêm
  - Cả 3 slide cùng archetype split-50-50 (nhất quán quá mức) → S03 đổi sang asymmetric

## PATCH SPEC
S01: [CHANGE] img x:8% y:10% w:34% h:70% (trước: x:8% y:22% w:34% h:46%)
S01: [KEEP] title, body, palette blue (user chưa yêu cầu đổi)
S02: [CHANGE] bg #FFFFFF → #FEF9E3
S02: [ADD] [E5] rule x:8% y:28% w:84% h:3px fill:#A61E22 z:1 | animation: pan-left on-click
S03: [CHANGE] split-50-50 → asymmetric: text block x:8% y:10% w:54%, ảnh x:66% y:18% w:34%
S03 → (tách thành S03a + S03b, nội dung chia đôi)
S03a: [ADD] alt: "..."
S03b: [ADD] alt: "..."
````

Kèm theo (adapter c) **bảng thao tác Canva** cho từng `[CHANGE]`/`[ADD]`:
| Cần làm | Canva |
|---|---|
| Đổi bg | Bấm tràn nền → Color → dán hex #FEF9E3 |
| Đổi bg sang ảnh | Elements → Images → chọn ảnh (có nguồn trong danh sách tài nguyên) |
| Xóa bớt bullet | Chọn text box → Delete line |
| Tách slide | Duplicate page → xóa nửa bullet không cần ở mỗi page |
| Căn lại ảnh | Nhấn ảnh → đặt x/y % qua Position panel (nhập % theo guide) |

Cuối output: **danh sách tài nguyên** (URL ảnh Unsplash theo keyword, family font) + ghi chú "chạy `12-qa-checklist` mục D sau khi dựng".

---

## Pattern rút ra (dùng cho mọi deck)
1. **1 brief → 1 spec đầy đủ trước**, adapter sinh sau — không code trực tiếp.
2. **Tiêu đề = quan điểm**, có con số/tên riêng; không dùng nhãn chung.
3. **Pair click** = group element cùng 1 cặp (number+body) → click count giảm, pacing giữ.
4. **Continuity** ghi ở header deck (nền + ghost object) — không lặp trong từng slide.
5. **Fix-existing**: audit → patch → bảng thao tác → tài nguyên. Tối thiểu can thiệp, `[KEEP]` mặc định.
6. Luôn kết bằng `Self-check: n/8 PASS`.
