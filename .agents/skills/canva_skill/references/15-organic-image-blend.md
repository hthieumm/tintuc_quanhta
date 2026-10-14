# 15 — ORGANIC IMAGE BLEND (Ảnh không khung, hoà vào bố cục)

Nghiên cứu từ bộ ảnh tham chiếu user (PPT cover cắt organic, collage History, danh thiếp thủy mặc TQ, banner anh đào panoramic, template bảo tàng tối) + Canva Help (Background Remover, Blend modes, image as fill).

Khác `04-images.md` (crop trong frame chuẩn): file này biến ảnh thành **phần của bố cục** — không viền, cắt hình tự do, hòa nền, tràn mép.

## 1. Kỹ thuật Canva cốt lõi

| Kỹ thuật | Cách làm (Canva) | Cho ra |
|---|---|---|
| **Xóa phông** | Chọn ảnh → Effects → **Background Remover** (Pro); tay refine vùng tóc/bờ | Ảnh subject rời nền → tự do đặt |
| **Đổ vào shape** | Upload ảnh PNG đã xóa phông → đặt trong **Frame** có hình blob/organic (Elements → frames); hoặc Set image as background của shape | Viền organic tự nhiên |
| **Blend modes** | Chọn ảnh → toolbar **Blend** → **Multiply** (hòa vào giấy/giấy có texture, tối); **Screen/Overlay** (ánh sáng lên nền tối); **Darken** (giữ bóng tối) | Ảnh "thấm" vào nền thay vì dán đè |
| **Ảnh làm texture chữ** | Text → Effects/texture fill bằng ảnh (tham khảo `04-images` text-mask) | Chữ giấy, chữ hoa văn |
| **Gradient xóa mờ cạnh** | Canva không có feather native → đè **gradient rectangle** cùng màu nền (opacity chuyển từ 0 → 70%) ra 4 mép ảnh | Viền mờ, ảnh tan vào nền |
| **Glow / soft edge** | Effects → Shadow/Glow cùng màu nền, blur lớn | Softening mép ảnh |
| **Edge-bleed tĩnh** | Đặt ảnh vượt mép slide (giữ guide margin cho phần chữ) | Tràn viền không khung |

## 2. 5 pattern từ ảnh tham chiếu (áp dụng 1-1)

### A. Organic cut (ảnh 1–2: cover PPT + collage History)
Ảnh cắt viền hình tự do đè lên khối màu cùng hệ:
1. Background Remover → đưa vào Frame blob (hoặc đắp 2-3 shape màu lệch nhau dưới ảnh).
2. Ảnh tràn **qua mép slide** (edge-bleed), chữ đặt vùng nền trống.
3. Tối đa 1 ảnh chính/slide; ở cover: ảnh organic lấy 60-65% diện tích, chữ trong khoảng trống còn lại.

### B. Frameless collage (ảnh 2)
3–5 ảnh đã xóa phông, kích thước KHÁC nhau, chồng lệch (không viền, không border):
- Thay border bằng **drop shadow cùng tông deck** (opacity 15-25%, blur 24) → cảm giác giấy dán, không phải thẻ.
- Một ảnh làm anchor (lớn ~50% cluster), các ảnh nhỏ 20-30% quanh nó, overlap 15-30%.
- Không group: để từng ảnh animate lần lượt (Method A — mỗi click 1 lớp chồng lên).

### C. Ink-wash / hài hòa texture (ảnh 3: danh thiếp thủy mặc)
Nền giấy/texture trước (Elements: "paper texture", "rice paper", "mottled paper") → ảnh chồng lên → **Blend = Multiply** → ảnh thấm vào texture như mực ngấm giấy:
- Chữ đặt trên vùng giấy "sạch" nhất (khu texture nhẹ), không đè lên chi tiết ảnh sau Multiply.
- Kèm 1-2 element "ink splash"/"brush stroke" cùng tone để nối ảnh – giấy.
- Tông deck nhất quán 1-2 màu (đen-mực, hoặc xanh mực nhạt).

### D. Panoramic strip (ảnh 4: banner anh đào)
Ảnh panorama (ratio ~4:1–6:1) làm **environment full-bleed**:
- Cách nhanh: ảnh bình thường → Set as background → crop panel kéo ngang; hoặc dùng ảnh panorama thật (Pexels "panorama", ratio 16:6+).
- Chữ overlay trên vùng ảnh có contrast thấp nhất + scrim gradient nhẹ 30-40%.
- Dùng cho: **chapter divider**, slide trích dẫn, slide mở đầu — bức "phông" bao trùm deck.

### E. Museum dark full-bleed (ảnh 5: template lịch sử / bảo tàng)
Toàn ảnh (tranh/phong cảnh) phủ hết slide, tông tối trầm + scrim 45-60%:
- Toàn bộ chữ sáng (gold/trắng — hợp precedent lụa đỏ + gold của user).
- Ảnh trung tâm: tác phẩm/artifact cần tôn (đặt rule-of-thirds), chữ ở vùng tối.
- Đề tài văn hóa/lịch sử/dân tộc → pattern mặc định cho cover + divider.

## 3. Chọn pattern cho loại slide

| Loại slide | Pattern dùng |
|---|---|
| Cover / divider | A, D, E |
| Content nhiều chữ | Ảnh chữ nhật chuẩn (`04-images`) + scrim — KHÔNG organic |
| Slide số liệu/chart | Ảnh đơn giản hoặc bỏ ảnh hẳn |
| Moodboard / lịch sử hình ảnh | B (collage) |
| Quote, trang giấy, danh thiếp | C (ink-wash) |
| Gallery tranh/artifact | E (museum) |

## 4. "Khi Canva không đủ" — tool ngoài cho cutout chất lượng cao

Background Remover của Canva yếu với tóc, lông, viền mảnh, ảnh nhiều chi tiết. Lựa chọn:
- **remove.bg** (web, free): xóa phông nhanh, download PNG → upload Canva.
- **Adobe Express Free / Photoroom**: xóa phông + feather nhẹ.
- **Photoshop** (Select and Mask → Refine Hair): chất lượng cao nhất cho tóc/lông.
- **Figma** (vector clip / blur mask): khi cần shape cắt vector mượt + soft edge.
Quy trình: cắt ngoài → PNG trong suốt → Canva chỉ việc blend/đặt. **Không** cố cứu ảnh vỡ bằng Canva Remover rồi thấy jagged.

## 5. Checklist blend (chạy trước QA)

- [ ] Mép cutout sạch — không viền trắng, không răng cưa (zoom 200%)?
- [ ] Sau Multiply: ảnh **vẫn nhìn thấy** (không biến mất vào nền tối) và chữ **vẫn đọc được** (dùng WebAIM)?
- [ ] Organic cut chỉ ở cover/divider/mood — slide chữ/số liệu vẫn dùng ảnh chuẩn?
- [ ] Không quá 2-3 slide organic liên tiếp (giữ nhịp deck — xem 01-layout)?
- [ ] Collage: shadow cùng tông deck, không border trắng?
- [ ] Panel panorama: chữ đặt trên vùng ít chi tiết nhất?
- [ ] Nếu chữ nằm trên ảnh đã blend → check contrast lại LẦN NỮA (Multiply làm nền tối hơn dự kiến)?

## 6. Tránh
- Xóa phông rồi để viền halo trắng sáng quanh chủ thể.
- Multiply cho ảnh nền đã tối → ảnh thành cái bóng đen mất chi tiết (dùng Screen/Overlay thay).
- Frame blob rainbow nhiều màu — organic cut phải tông với palette (03-color).
- Ảnh cutout lơ lửng giữa slide text-heavy (xem "nếu phải giải thích ảnh vì sao ở đây → bỏ", 01-layout / presentations.ai).
