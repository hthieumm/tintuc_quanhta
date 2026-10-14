# 04 — IMAGES: Crop, Frames/Masks, Overlays

> **Lớp design.** Thao tác chuộng ("kéo vào frame, double-click chỉnh") → `16-tool-adapters.md` §C. Với medium (a)/(b), alignment/crop hiện thực bằng CSS absolute `x/y/w/h%` hoặc `add_picture` crop.

Nghiên cứu từ BrightCarbon (Google Slides image hacks — nguyên lý dùng chung), Noun Project guide, presentations.ai, SlidesCarnival, precedent user.

Nghiên cứu từ BrightCarbon (Google Slides image hacks — nguyên lý dùng chung), Noun Project guide, presentations.ai, SlidesCarnival, precedent user.

## 1. Nguồn ảnh (precedent user — BẮT BUỘC)

- **Ảnh thật, royalty-free**: Unsplash, Pexels, Pixabay (tìm tiếng Việt/Anh theo keyword).
- **KHÔNG dùng ảnh AI-generated** (đặc biệt AI-face: da quá mịn, tay/mắt lỗi, ánh sáng giả) — user ghét.
- Đề tài Việt Nam culture → ưu tiên ảnh stock thật, ảnh tư liệu có nguồn, ảnh do người dùng tự chụp.
- Ảnh upload phải **≥ 1500px cạnh lớn** với 1920×1080 slide; không phóng ảnh vượt 100% kích thước gốc (UCSD evidence-based) → vỡ/nhòe khi chiếu.
- Ghi nguồn ảnh ở caption 24px, opacity 60-70%.

## 2. Crop chủ đích (intentional crop)

- **Mắt người nhìn theo hướng mắt nhân vật**: đặt mặt/people ở nửa KHÔNG chữ, hướng nhìn **về phía nội dung chữ** (leading). Nguồn: nguyên lý eye-direction trong composition.
- Crop để **tập trung chủ thể**: cắt bỏ nền rối, đưa subject theo rule of thirds.
- Crop cũng là ngôn ngữ thiết kế: crop toàn bộ ảnh về cùng 1 shape/kích thước tạo identity đồng nhất (BrightCarbon).
- **Tuyệt đối không stretch méo** ảnh để lấp chỗ trống — chỉ crop (che) hoặc resize giữ ratio.

## 3. Frames & Masks (Canva)

Canva dùng khái niệm **Frames** (Elements → search "frames"): kéo ảnh vào frame, ảnh tự bị mask theo hình khung, double-click để reposition ảnh bên trong.

| Frame | Dùng cho |
|---|---|
| Vuông/Chữ nhật bo góc (radius 16-24px) | Ảnh nội dung, grid ảnh |
| **Circle** | Avatar, chân dung, icon-ảnh, magnifier |
| Hexagon | Ảnh kỹ thuật, tổ ong, tech |
| Blob / organic shape | Deck trẻ, editorial, đỡ cứng nhắc |
| Chữ (text mask) | Cover một từ khóa |
| Full-bleed | Hero/cover |

Kỹ thuật nâng cao (BrightCarbon, làm được trong Canva bằng frames + layer):
- **Collage**: nhiều ảnh crop cùng shape ghép grid có khe (gutter 16px) đều nhau.
- **Before/After**: 2 ảnh cùng kích thước đặt cạnh nhau, phân cách đường mảnh.
- **Timeline strip**: dãy ảnh chữ nhật nhỏ bằng nhau theo trục ngang — diễn tiến thời gian.
- **Magnify**: ảnh nhỏ đặt trên ảnh toàn cảnh cùng nội dung, tạo vòng tròn phóng to.
- **Image-through-frame**: đặt ảnh làm fill của chữ/shape to (Canva: text → chọn ảnh làm texture).

## 4. Overlay / Scrim (chữ đè ảnh)

- Chữ nằm trên ảnh → **luôn luôn** có lớp chặn:
  - Rectangle đen transparency **40–60%** phủ vùng chữ (BrightCarbon: "dark enough to read, clear enough to see the picture").
  - Gradient đen từ mép (dưới/1 bên) → chữ đặt phía đậm.
  - Hoặc scrim màu đề tài (vd xanh đêm cho deck biển) giữ brand.
- Full-bleed hero: chữ tối thiểu, 1 câu ngắn, đặt trong vùng ảnh đơn giản nhất (bầu trời, mặt phẳng).

## 5. Vị trí & kích thước

- Full-bleed khi ảnh **chính là thông điệp**; ảnh nhỏ lơ lửng giữa slide đông chữ = tội lỗi thiết kế (presentations.ai: "if you have to explain why an image is on the slide, leave it off").
- Ảnh-grid: mọi ô cùng ratio, cùng gutter; binding element = đường kẻ mảnh hoặc nền card.
- Group **ảnh + caption + số thứ tự** thành 1 group (để animate 1 click — xem 06-animation).
- Ảnh nền editorial: thêm **grain/noise texture** 5-10% (Canva Elements: "noise", "grain") cho cảm giác tạp chí in.

## 6. Checklist ảnh cho 1 slide
- [ ] Ảnh thật, ≥1500px, có nguồn?
- [ ] Crop chủ đích — subject theo thirds, mắt hướng về chữ?
- [ ] Cùng shape/ratio với ảnh khác trên deck (hoặc chủ đích khác)?
- [ ] Chữ đè ảnh có scrim ≥40%?
- [ ] Đã group ảnh+caption?
- [ ] Không ảnh nào bị stretch méo?
