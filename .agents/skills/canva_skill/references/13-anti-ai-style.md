# 13 — ANTI-AI STYLE (Khử dấu vết AI trong thiết kế)

Nghiên cứu từ Perceptis (2026), 2slides, llemental, winningpresentations về "AI tells" — dấu hiệu nhận biết slide do AI tạo.

## 1. Vì sao cần file này

Slide AI có 2 lớp lỗi: **tư duy mỏng** (nội dung chung chung) và **dấu vết thị giác máy móc** (layout giống hệt nhau, nhịp typography đều tăm tắp). Người xem ngầm cảm nhận cả hai trong ~5 giây. File này xử lý cả 2 lớp.

## 2. Bảng AI tells → cách sửa

| Dấu hiệu AI | Cách khử |
|---|---|
| Tiêu đề chung chung: "Overview", "Key Takeaways", "Introduction" | Tiêu đề = **luận điểm có quan điểm**: "Gia đình là nơi giữ tiếng Việt lâu nhất", thay vì "Về gia đình" |
| Layout giống hệt nhau mọi slide (một khung chết) | Đổi archetype có chủ đích mỗi 2-3 slide (xem 01-layout), trộn split + full-bleed + asymmetric |
| 1 font duy nhất toàn deck, nhất là Inter/Roboto mặc định | 2 font có contrast rõ (display + body, xem 02-typography); tránh Inter làm font chính |
| Nền kem + thanh màu trên đầu + bullet chấm tròn (dấu vết ChatGPT) | Bỏ pattern này hoàn toàn; dùng nền từ ảnh chủ đề (precedent: lụa đỏ + gold) |
| Nhịp chữ đều đều — mọi slide "nặng" như nhau | Tạo **tương phản scale mạnh**: 1 slide chỉ có số to 160px, slide kế dày đặc caption 28px |
| Illustration isometric tím bão hòa | Ảnh thật Unsplash/Pexels (04-images) + grain 5-10%; **Ngoại lệ hợp lệ**: nếu Q3 trả lời "có sẵn illustration flat" hoặc "không có ảnh nào" → vẽ flat/outline CÙNG palette, cùng stroke width (05). Vẫn cấm AI-face, vẫn cấm isometric tím gradient |
| Ảnh stock placeholder (handshake, office cười giả) | Ảnh thật có nguồn, ưu tiên ảnh tư liệu/đề tài cụ thể; caption ghi nguồn |
| Quá sạch, quá đối xứng, zero lỗi hierarchy | Cố ý **lệch một chút**: offset khối ảnh 8-16px khỏi lưới, accent đặt lệch góc, để hơi "bừa" có chủ đích |
| Số liệu/khẳng định không nguồn | Mọi số + quote ghi nguồn 24px góc slide (xem 10-data) |
| Màu palette "AI default" (tím-xanh gradient) | Palette rút từ ảnh chủ đề (03-color), giữ hệ lụa đỏ + gold của user |

## 3. Nguyên tắc "slightly less perfect"

Chuẩn của slide tự thiết kế: **hơi lộn xộn hơn, hơi lệch đối xứng hơn, hơi có quan điểm hơn**. Cụ thể:

- 1 khối ảnh/shape **deliberately offset** khỏi grid mỗi vài slide (8-16px, không quá — vẫn phải alignment chủ đạo).
- Chữ viết tay / marker underline (Canva Elements: "brush stroke", "marker") gạch dưới 1-2 từ khóa mỗi deck — đúng 1-2 lần, không lạm dụng.
- Ảnh để nguyên khung gốc/bo góc không đều (blob) xen giữa các ảnh chữ nhật đều — tạo nhịp thủ công.
- Caption kiểu ghi chú: "Ảnh: chợ phiên Điện Biên, 2019" thay vì auto-caption vô cảm.

## 4. Nội dung "human" (lớp tư duy)

- Mỗi chương mở bằng **câu hỏi/tranh luận**, không phải định nghĩa.
- Tiêu đề slide viết như **câu người thật nói**, có số, có tên riêng: "3 lễ hội kéo dài quá Tết" > "Lễ hội truyền thống".
- Có tối thiểu 1 slide "lời người thật" (quote tư liệu, phỏng vấn) — AI hiếm khi tạo được.
- Cắt nội dung dư: AI filler ("Trong thời đại hiện nay...") → xóa hết.

## 5. Checklist humanize (chạy TRƯỚC QA 12-qa-checklist)

- [ ] Không tiêu đề nào là "Overview/Introduction/Key Takeaways/Thank you" trơn tru — đều có quan điểm?
- [ ] Có tối thiểu 2-3 archetype layout khác nhau trong deck?
- [ ] Font chính không phải Inter/Roboto mặc định?
- [ ] Không có pattern "nền kem + thanh màu đầu trang + bullet chấm"?
- [ ] Có ít nhất 1 slide tương phản scale mạnh (số to/chữ to vs dày)?
- [ ] Mọi ảnh là ảnh thật có nguồn — zero ảnh AI-face, zero illustration tím isometric?
- [ ] Có 1-2 điểm "lệch có chủ đích" (offset, brush stroke, blob frame)?
- [ ] Mọi số liệu + quote có nguồn?
- [ ] Đọc lại 5 tiêu đề liên tiếp — nghe như 1 người kể chuyện hay như machine?

Nếu ≥3 ô chưa đạt → deck vẫn "hơi AI", sửa trước khi xuất.
