# 12 — QA CHECKLIST (Kiểm tra toàn deck trước khi xuất)

Chạy checklist này THEO THỨ TỰ trước khi Share → Download (chuẩn kết hợp user precedent + research).

## A. Nội dung & chữ (5 phút)
- [ ] **Dấu tiếng Việt**: soát từng slide "ạ ế ộ ớ ượ ự ỹ đ" render đúng font, không ô vuông/font fallback.
- [ ] Chính tả tiếng Việt (gõ lại các từ khóa tên riêng); số liệu có đơn vị + nguồn.
- [ ] 1 slide = 1 ý; ≤ 4 bullet; 6×6 rule không vượt.
- [ ] Core message của deck phát hiện được ở cover + conclusion (book-end khớp nhau).

## B. Layout & style (5 phút)
- [ ] Margin hai bên ≥ 5% nhất quán mọi slide (bật Rulers & guides kiểm tra).
- [ ] Cùng cấp chữ = cùng cỡ (H1/H2/body đồng nhất vị trí các slide).
- [ ] Không slide nào >3 layout khác hệ; nhưng cũng không trùng archetype >3 slide liên tiếp.
- [ ] Alignment: các khối thẳng trục theo guide dọc/ngang.
- [ ] Palette ≤ 5 màu; cùng màu = cùng ý nghĩa (series chart không đổi màu giữa slides).

## C. Ảnh & icon (5 phút)
- [ ] Ảnh thật (không AI-face) — soi kỹ bất thường: tay, mắt, da, bóng đổ.
- [ ] Không ảnh nào stretch méo; đều ≥1500px.
- [ ] Chữ đè ảnh đều có scrim ≥ 40%.
- [ ] Icon đồng nhất 1 bộ (stroke, radius, màu); icon nhỏ có label.
- [ ] Nguồn ảnh/quote/số liệu đã ghi.

## D. Animation & click (10 phút — QUAN TRỌNG NHẤT)
- [ ] Mọi element animation đều là **On Click** (không auto) — Method A.
- [ ] **Click order** đã kéo-thả đúng trình tự kể chuyện: tiêu đề → chính → chi tiết → nhấn.
- [ ] Đếm tổng click; mỗi slide nội dung ≤ 8-10 click; ~11 giây/click theo kịch bản nói.
- [ ] Group ảnh+caption+icon+label đã group (1 click) — soi lại từng slide.
- [ ] Transition đồng nhất hướng + thời lượng 0.5–0.7s.
- [ ] GIF: ≤ 1/slide và đúng lúc.
- [ ] **Present Full screen → bấm hết từng click từ đầu đến cuối deck** (không skipped slide), vừa bấm vừa đọc notes.
- [ ] Hyperlink (nếu dùng): bấm thử mỗi link ở Present mode; có nút về mục lục.

## E. Contrast & trình chiếu mô phỏng
- [ ] Contrast ≥ 4.5:1 (kiểm WebAIM) cho body; hình thức tắt monitor 1 nửa độ sáng/sang phòng khác xem slide.
- [ ] Slide mở màn (chưa click) đã đủ đẹp: tiêu đề + nền tự đứng được.
- [ ] Test slide PDF version trên nền trắng và nền đen màn hình.

## F. Xuất theo adapter đã chọn (5 phút)
> Bộ 3 MP4/PPTX/PDF chỉ áp dụng khi adapter = **(c) Canva spec**. Với (a) → xuất `deck.html` + assets; với (b) → xuất `deck.pptx`.

- [ ] **(c) Canva**: MP4 (render xem lại 1 lượt) · PPTX (mở PowerPoint thật — click/hyperlink còn sống, font không thay) · PDF (flatten nếu lỗi font). 3 file cùng tên gốc + ngày + version, chung 1 thư mục + USB dự phòng.
- [ ] **(a) HTML**: mở `deck.html` trình duyệt thật, bấm hết click, kiểm font/ảnh/notes.
- [ ] **(b) python-pptx**: mở `deck.pptx` bằng PowerPoint thật, kiểm font/ảnh/notes.
- [ ] Notes đã ghi cho từng slide (hiện ở Presenter View).

## G. Phép "đếm ngược 5 giây"
Mở mỗi slide 5 giây rồi đóng lại — nếu trong 5 giây không hiểu slide nói về điều gì → quay lại sửa (tiêu đề yếu / quá nhiều element / tiêu điểm không rõ).

---
Chốt: pass hết A-F → mới Share/Publish. Checklist này cũng là checklist review deck người khác gửi.
