# 16 — TOOL ADAPTERS (Chuyển spec → sản phẩm)

**Nạp file này khi** đã có DECK SPEC (`00-output-spec`) và cần xuất ra medium cụ thể.
AI chỉ nạp **đúng 1 mục** bên dưới — không đọc cả 3.

| Medium | Chọn khi | Sản phẩm | Giữ được gì |
|---|---|---|---|
| **(a) HTML + reveal.js** | Muốn mở đẹp nhất, kiểm soát animation đầy đủ, chạy offline | `deck.html` | Mọi thứ: fragment, transition, auto-animate, background, notes |
| **(b) .pptx bằng python-pptx** | Cần file PowerPoint thật để gửi/nộp bài | `deck.pptx` | Layout + hình + text + chart + transition XML; **không có animation on-click** |
| **(c) Spec Canva** | User giữ nguyên deck Canva, hoặc AI không kiểm soát được browser | Markdown spec (không tạo file) | Người dựng tay theo spec + ảnh tham chiếu |

---

## A. Adapter (a) — HTML + reveal.js

**Nạp khi user chọn "HTML/reveal.js".**

### Cấu trúc 1 file
```
deck.html          ← tự chứa reveal.js từ CDN hoặc local vendor/
assets/            ← ảnh đã tải về (không hotlink — trình chiếu nhiều wifi chậm)
```
Không dùng CDN nếu trình chiếu offline yêu cầu ổn định → tải `reveal.js` + `plugin/notes` về `vendor/`.

### Mapping spec → HTML
| Spec | reveal.js |
|---|---|
| `archetype` | `<section>` + CSS class của archetype trong `<style>` |
| element `role=title` | `<h2 class="t-h1">` |
| `role=body` | `<p class="t-body">` |
| `role=caption` | `<figcaption>` hoặc `<p class="t-cap">` |
| `animation: rise on-click` | `class="fragment fade-up"` |
| `animation: pop` | `class="fragment scale-in"` (có thể tự viết CSS) |
| `click order` | **thứ tự DOM** của các `.fragment` (giống hệt reading order nếu không staging) |
| `transition pan-left 0.6s` | `data-transition="slide"` + config `transitionSpeed: 'fast'` |
| `transition zoom` | `data-transition="zoom"` |
| `transition dissolve` | `data-transition="fade"` |
| `transition match-move` | `data-auto-animate` giữa 2 section + `data-auto-animate-id` |
| `continuity` (14) | dùng `data-auto-animate-id` chung cho element di chuyển giữa 2 slide |
| `bg #XXXXXX` | `data-background-color="#XXXXXX"` |
| ảnh full-bleed nền | `data-background-image="assets/x.jpg"` |
| `scrim` | `<div class="scrim">` phủ trong section |
| `alt` | `alt="..."` bắt buộc với mọi `<img>` |
| `notes` | `<aside class="notes">…</aside>` |

### Config mặc định (khởi tạo deck)
```
width: 1920, height: 1080, margin: 0.04, minScale: 0.2, maxScale: 1.6
transition: 'slide', transitionSpeed: 'fast', backgroundTransition: 'fade'
hash: true, controls: true, progress: true, slideNumber: 'c/t'
plugins: [ Notes, Highlight, Zoom ]   ← Notes = speaker notes
```
`hash: true` để mở lại đúng slide đang trình bày (deep-link).

### Vì sao (a) là mặc định tốt nhất
- Kiểm tra được kết quả bằng cách mở file, không cần PowerPoint.
- Fragment = on-click của Canva, tự nhiên hơn, không giới hạn 50 animation.
- `auto-animate` cho phép element "trôi" giữa 2 slide — hiện thực hoá được Match & Move (14) thật sự.
- Chuyển PDF: trình duyệt → Print → khổ ngang; `pdfSeparateFragments: true` nếu muốn mỗi fragment 1 trang.

### Tránh
- Hotlink ảnh lúc trình chiếu (rủi ro mạng) → tải ảnh về `assets/`.
- Bỏ `alt` (00 §2 bắt buộc).
- Dùng `autoSlide` (tự chạy) — vi phạm Method A, xem 06-animation.

---

## B. Adapter (b) — python-pptx

**Nạp khi user chọn "file .pptx".**

### Script 1 file sinh deck
`build_deck.py`: đọc `deck_spec.json` → `Presentation()` → vòng lặp slide → lưu `.pptx`.

> **Schema của `deck_spec.json`:** xem `19-deck-schema.md` (file 19). Nó là bản JSON hóa DECK SPEC markdown — không thêm trường nào không có trong spec. Adapter (a) và (c) không dùng file này.

### Mapping spec → python-pptx
| Spec | API |
|---|---|
| canvas | `prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)` (16:9) |
| slide trắng | `prs.slides.add_slide(prs.slide_layouts[6])` |
| `role=img` | `slide.shapes.add_picture(path, left, top, width, height)` |
| crop ảnh | `pic.crop_left / crop_top / crop_right / crop_bottom` (0–1) — dùng cho crop chủ đích (04-images) |
| khối màu / rule / scrim | `slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ...)` + `shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor.from_string("A61E22")` |
| `opacity` (scrim) | **không có API trực tiếp** → thêm `<a:alpha>` vào XML `solidFill` (xem snippet dưới) hoặc bake trước vào ảnh PNG |
| `role=title/body/caption` | `add_textbox(...)` → `tf.paragraphs[0]` + `run.font.size/bold/name/color` |
| font | `run.font.name = "Be Vietnam Pro"` — **phải cài font trên máy mở file**, nếu không PowerPoint thay font |
| cỡ chữ | `Pt()` — chuyển từ px: `pt = px * 0.75` (72px → 54pt) |
| toạ độ % | `left = Inches(13.333 * x/100)`, `top = Inches(7.5 * y/100)`; `w`, `h` cùng công thức |
| z-order | theo thứ tự `add_*` (shape sau đè shape trước) → thêm theo z tăng dần |
| hyperlink | `run.hyperlink.address = "..."` — **chỉ text run**; shape không có hyperlink API → dùng text run hoặc bỏ qua |
| chart (10-data) | `slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, ...)` — bỏ gridlines qua `chart.value_axis.has_major_gridlines = False` |
| alt-text | `shape._element._nvXxPr.cNvPr.set("descr", alt)` (bắt buộc cho accessibility) |
| speaker notes | `slide.notes_slide.notes_text_frame.text = "..."` |

### Transition (giới hạn)
python-pptx **không có API transition/animation**. Chọn 1:
1. Bỏ transition, thay bằng "slide mới hiện thẳng" — chấp nhận được, đơn giản nhất.
2. Chèn XML transition thủ công vào `<p:transition>` (fade/push) — khả năng mở lỗi trên phiên bản PowerPoint khác, chỉ làm khi user đòi.

### Giới hạn phải nói rõ với user
- **Không có on-click animation** → toàn bộ `click order` trong spec **biến mất**. Thay bằng: nhiều slide cùng nội dung (progressive build) hoặc export PowerPoint dùng Slide Show → Animation → Add Animation → With Previous/On Click thủ công.
- Font phải cài máy; ảnh phải nhúng (dung lượng tăng).
- python-pptx không xuất được GIF động hay blend mode → chỉ dùng ảnh tĩnh (đã flatten sẵn).

### Skeleton tối thiểu
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(5), Inches(7.5))
bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor.from_string("3A0A0A")
tb = s.shapes.add_textbox(Inches(1.06), Inches(1.08), Inches(7.9), Inches(1.3))
r = tb.text_frame.paragraphs[0].add_run(); r.text = "Tiêu đề"
r.font.size = Pt(54); r.font.bold = True; r.font.name = "Playfair Display"
prs.save("deck.pptx")
```

---

## C. Adapter (c) — Spec Canva (người dựng tay)

**Nạp khi user chọn "chỉ viết spec"** hoặc mode = `fix-existing` (user đưa ảnh chụp slide + mô tả).

### Trả về 2 phần
1. **DECK SPEC / PATCH SPEC** theo `00-output-spec` §2/§3 — đủ để người dựng lại từ đầu.
2. **Bảng thao tác Canva** — cột trái: element cần tạo; cột phải: đường dẫn trong Canva (mỗi dòng ≤ 1 số):

| Element cần tạo | Đường dẫn Canva |
|---|---|
| Đặt ảnh vào khung bo tròn | Elements → frames → chọn frame → kéo ảnh vào → double-click để chỉnh crop trong frame |
| Lề + thước | File → Settings → bật Rulers & guides |
| Chuyển cảnh giữa 2 trang | Hover giữa 2 thumbnail → Add transition → chọn style → kéo Duration |
| Element xuất hiện từng click | Chọn element → Animate → effect → bật Appear on click |
| Sắp thứ tự click | Presentation settings → Click order → kéo-thả |
| Xóa phông | Ảnh → Effects → Background Remover → Save as PNG |
| Hòa ảnh vào nền | Chọn ảnh → Blend → Multiply |
| Nhóm ảnh + caption | Chọn cả hai → Ctrl/Cmd+G, **đặt tên group** theo id trong spec |
| Xuất | Share → Download |

### Bắt buộc kèm theo
- **Danh sách tài nguyên**: ảnh nào cần tải (URL nguồn + nơi dùng), icon family, font cài trước.
- **Đo lại trước khi bắt đầu**: Canva snap position có thể lệch 1-2px so với toạ độ % → nói rõ dùng guide làm chuẩn, không copy số px tuyệt đối.
- **Xác nhận cuối**: sau khi người dựng xong, chạy lại `00` §5 self-check trên deck thật (dùng `12-qa-checklist.md` cho bước click thủ công).

### Giới hạn
- AI không xác minh được kết quả → nói rõ đâu là chỗ dễ sai (contrast sau Multiply, crop trong frame, thứ tự click).
- Không tạo file. Không hứa "đã xong" — chỉ "spec đã sẵn sàng để dựng".

---

## Chọn medium — câu hỏi mở đầu (luôn hỏi trước)

Hỏi **1 lần, 2 câu, dạng lựa chọn** (dùng tool question nếu có):

1. "Xuất deck theo dạng nào?" → `a) HTML/reveal.js — mở đẹp nhất, kiểm soát animation đầy đủ` / `b) file .pptx bằng python-pptx — PowerPoint thật, không giữ on-click animation` / `c) spec Canva — người dựng tay theo spec`
2. "Viết deck mới hay sửa deck Canva đang có?" → `new` / `fix (kèm ảnh chụp slide + mô tả)`

Sau đó chỉ nạp 1 adapter tương ứng + các file design cần thiết theo bảng điều kiện nạp ở `SKILL.md`.

## Tránh (chung)
- Sinh cả 3 sản phẩm cùng lúc để "cho có" → 1 medium, đúng yêu cầu.
- Adapter (b) mà hứa "giữ animation" → nói rõ giới hạn trước khi code.
- Dùng px trong khi spec quy định % (lệch khi đổi canvas).
- Bỏ alt-text khi chuyển từ spec sang HTML/pptx.