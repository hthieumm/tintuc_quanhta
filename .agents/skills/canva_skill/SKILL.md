---
name: canva-presentation-skill
description: Thiết kế hoặc sửa deck Canva 16:9 — cho AI. Bắt buộc xuất spec có toạ độ % + hex + contrast (00-output-spec), sau đó adapter theo medium: (a) HTML/reveal.js đẹp nhất, (b) .pptx bằng python-pptx, (c) spec để người dựng tay trong Canva. Tiếng Việt ưu tiên.
---

# Canva Presentation Design Skill (16:9) — Hợp đồng cho AI

Skill này viết **cho AI**, không viết cho người bấm Canva. Mọi spec phải có **toạ độ % + hex 6 ký tự + alt-text + contrast**: không có số thì không có output.

---

## 0. BẮT BUỘC HỎI ĐẦU TIÊN (2 câu, trước khi nạp file design)

```
1) Xuất theo dạng nào?
   a) HTML + reveal.js — mở đẹp nhất, giữ animation on-click (fragments) + transition
   b) file .pptx bằng python-pptx — PowerPoint thật, KHÔNG giữ animation on-click
   c) chỉ viết spec — người dựng tay trong Canva theo spec
   → hỏi xong chỉ nạp đúng 1 mục trong references/16-tool-adapters.md

2) Vẽ deck mới hay sửa deck đang có?
   → new : theo workflow dưới
   → fix-existing : user đưa ảnh chụp slide + mô tả → trả về AUDIT + PATCH (00 §3)
```
Quy tắc: chỉ sinh **1 trong 3** sản phẩm (a/b/c) tương ứng adapter đã chọn. Cấm sinh cả 3 "cho có". QA "xuất 3 định dạng" chỉ đổi khi chọn adapter **(c) Canva spec**.

## 0.1 STYLE DIAGNOSIS (5 câu → chọn pattern, hỏi TRƯỚC khi nạp design file)

> **Nguồn sự thật duy nhất: `00-output-spec.md` §1.1.** Mục này chỉ là tóm tắt để hỏi nhanh — không sao chép bảng ánh xạ. Nếu 2 bản lệch nhau, sửa `00 §1.1` rồi cập nhật bản ở đây.

Sau khi đọc brief / phân tích nội dung slide, hỏi user (hoặc tự suy đoán nếu user không trả lời):

**Q1 — Tông cảm xúc (bắt buộc, chọn 1):** a) Trang nghiêm, uy nghiêm · b) Nhẹ nhàng, mộng mơ · c) Gần gũi, vui tươi · d) Trẻ trung, năng động · e) Trầm tĩnh, học thuật · f) Vui nhộn, hoạt họa (guochao/国潮)

**Q2 — Loại nội dung (bắt buộc, chọn 1):** quy trình có bước · danh sách đặc điểm/nhóm khái niệm · số liệu cụ thể · lịch sử có mốc năm · định nghĩa/khái niệm lý thuyết · trích dẫn/câu quote · mood/mở bài cảm xúc

**Q3 — Loại ảnh (bắt buộc nếu deck có ảnh):** có ảnh thật (ưu tiên, giữ nguồn) · có sẵn stock (04) · không có ảnh nào (vẽ flat/outline cùng palette, cấm AI-face) · có sẵn illustration flat (dùng được nếu giữ palette + stroke width)

**Q4 — Mật độ chữ (tuỳ chọn, chỉ hỏi nếu ≥10 slide):** tối giản (1 ý/slide, ≤3 bullet) · vừa (2-3 ý, 3-4 bullet) · nhiều chữ (tách slide, intro + chi tiết)

**Q5 — Ràng buộc thương hiệu (chỉ hỏi 1 lần, cache luôn):** có màu/font nào bắt buộc không? (VD đang dùng lụa đỏ + gold)

**Ánh xạ Q1+Q2 → pattern:** xem bảng đầy đủ trong `00 §1.1`. 3 dòng hay dùng nhất:
- Trích dẫn / thơ / mở bài cảm xúc → **wavy-asymmetric (18-F)**
- Đề tài cổ phong / di sản / triết học → **ink-pill-seal (18-H)**
- Danh sách phẳng 3-6 mục, nhiều ảnh → **stem-list (18-G biến thể)**

**Quy tắc:** user không trả lời → AI **không dừng**, dùng bảng `00 §1.1` để suy đoán từ đề tài, ghi rõ `Style: <tên pattern> (suy đoán từ đề tài — nói nếu muốn đổi)`. Không hỏi lại lần 2.

**Ghi vào header DECK SPEC (bắt buộc):**
```
Style: <tên pattern> | Q1:<a|b|c|d|e|f> | Q2:<loại nội dung> | Q3:<loại ảnh> | Q4:<mật độ> | Q5:<brand>
```

---

## Workflow

1. **BRIEF** — Số slide, đề tài, thời lượng nói (sec), audience, ngôn ngữ (VN → phải chọn font đủ dấu). Riêng fix-existing: nhận **ảnh chụp slide** + mô tả của user. Xem `09-structure.md`.
2. **STYLE SYSTEM** — Palette hex (≤5, 60-30-10), 2 fonts (1 heading + 1 body, VN). Quyết bằng bảng **IF/THEN trong `00-output-spec.md` §4**, không dựa vào tính từ "modern/clean". Xem `02-typography.md`, `03-color.md`, `05-icons-illustration.md`, `13-anti-ai-style.md`.
3. **STRUCTURE** — Dãy slide type + SCQA + rule of three. Xem `09-structure.md`.
4. **SPEC** — Viết **DECK SPEC** (new) hoặc **AUDIT + PATCH** (fix) theo template cứng trong **`00-output-spec.md` §2/§3** — mỗi slide ghi: archetype, hex, H1/Body, elements `[Ei] x:% y:% w:% h:%` + `alt` + `animation on-click`, `click order`, `transition`, `contrast`. Chưa có DECK SPEC thì cấm sinh file sản phẩm. Xem `01-layout.md`, `04-images.md`, `15-organic-image-blend.md`, `10-data-infographic.md`.
5. **ADAPTER** — Chuyển spec → sản phẩm đã chọn (nạp đúng 1 mục `16-tool-adapters.md`), kèm danh sách tài nguyên cần tải. Xem `16-tool-adapters.md`.
6. **SELF-CHECK** — Chạy checklist pass/fail trong `00-output-spec.md` §5 + `12-qa-checklist.md`. Kết dòng cuối: `Self-check: n/8 PASS`.

---

## Index — Chỉ nạp khi gặp điều kiện

| File | Điều kiện nạp | Chủ đề |
|---|---|---|
| `00-output-spec.md` | **LUÔN NẠP ĐẦU TIÊN** trước mọi slide | Hợp đồng đầu ra + bảng IF/THEN + self-check |
| `01-layout.md` | Nạp khi cần chọn archetype, khoảng trống, alignment | Grid (12 col, pitch 7.60%), ≥13 archetype (7 gốc + 4 từ 18 + 2 từ 20), F/Z, whitespace, safe zone |
| `02-typography.md` | Nạp khi brief nêu ngôn ngữ/tone | Font VP đủ dấu, type scale, 6×6 |
| `03-color.md` | Nạp khi cần chọn palette/contrast | 60-30-10, WCAG, dark/light, tâm lý màu |
| `04-images.md` | Nạp khi slide có ảnh | Crop chủ đích, frames/masks, overlay scrim |
| `05-icons-illustration.md` | Nạp khi slide gắn icon | Đồng nhất stroke, icon grid |
| `06-animation.md` | Nạp khi cần pacing/click | Method A (on-click), click order, choreography |
| `07-gif-video.md` | Nạp khi brief yêu cầu video/GIF | Background video, sticker trong suốt |
| `08-navigation.md` | Nạp khi cần hyperlink/QR giữa slide | Go-to-page, QR |
| `09-structure.md` | Nạp khi cần dàn ý/SCQA | Slide types, SCQA, rule of three, pacing |
| `10-data-infographic.md` | Nạp khi slide có số liệu/chart | Chọn chart, big number, timeline |
| `11-export-present.md` | Nạp khi thống nhất dạng xuất — chỉ bộ 3 khi adapter **(c) Canva** | MP4/PPTX/PDF (c) hoặc HTML/pptx (a/b) |
| `12-qa-checklist.md` | Nạp khi chạy self-check §6 | Checklist toàn deck |
| `13-anti-ai-style.md` | Nạp khi QA trước khi trả — nhóm humanize | AI tells, slightly-less-perfect |
| `14-cinematic-flow.md` | Nạp khi cần slide sau nối slide trước | Match & Move, element chain, edge-bleed |
| `15-organic-image-blend.md` | Nạp khi ảnh không khung | Cutout organic, blend mode, panorama |
| `16-tool-adapters.md` | **Nạp đúng 1 mục sau khi có spec** | 3 adapter: HTML / python-pptx / Canva-spec |
| `17-example.md` | Nạp khi cần học pattern | Brief → spec 3 slide + 2 medium + ca sửa deck |
| `18-poetic-botanical-ink.md` | Nạp khi Q1 = b/c hoặc brief có thơ/cổ phong/cây lá/serif | 3 pattern: Wavy-Pastoral, Branch-Spine, Ink-Pill-Seal |
| `19-deck-schema.md` | Nạp khi adapter = **(b) python-pptx** | Schema `deck_spec.json`, quy tắc Markdown → JSON |
| `20-guochao-toon.md` | Nạp khi Q1 = f hoặc brief có guochao/国潮/hoạt hình viền mực | 2 pattern: Guochao-Stage, Guochao-Center; nét vẽ mực 2 chế độ, palette mẫu kế thừa Q2/Q5 |

Chưa đọc `00` → cấm trả lời bằng lời văn định tính.  
Token giảm: nạp tối đa **5 file/lần** — `00` + adapter + topped 3 file design liên quan.

---

## Quy tắc vàng

- Mọi element có `id` + toạ độ % + hex + `alt` (img/icon); mọi cặp chữ/nền contrast ≥ 4.5:1.
- Tối đa **2 font + 5 màu + 1 ý/slide**; slide tiếng Việt → kiểm dấu trước khi xuất.
- Ảnh thật Unsplash/Pexels/Pixabay — cấm ảnh AI-face; ảnh hòa vào nền phải kiểm contrast lại.
- Tiêu đề là **quan điểm có số/tên riêng**, cấm nhãn chung (Overview/Key takeaways).
- 1 hướng transition chủ đạo toàn deck; deck có quan điểm, layout đổi nhịp, hơi lệch có chủ đích (13).
- Slide sau nối slide trước (14); ảnh cutout chỉ ở cover/mood, slide nhiều chữ giữ ảnh chuẩn (15).
- Chỉ có DECK SPEC (00 §2) mới làm đầu ra — bản văn mô tả "slide nên có…" vô dụng.

---

## Kích hoạt OpenCode (chế độ TUI/agents)

- Lệnh: `opencode mcp call` hoặc hỏi thường: *“Dùng skill canva_presentation — brief: … | medium: a/b/c | mode: new/fix | kèm ảnh chụp nếu fix”*
- Trước khi trả lời trong TUI, phải chạy self-check `00 §5` và kết dòng `Self-check: n/8 PASS`.
