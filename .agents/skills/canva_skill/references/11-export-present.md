# 11 — EXPORT & PRESENT (Xuất file & trình chiếu)

> **Lớp design.** Mapping sang từng medium ở `16-tool-adapters.md` — (a) HTML/reveal.js, (b) python-pptx, (c) Canva spec. Đây là bản gốc cho chế độ Canva thủ công; 2 medium kia tham chiếu nhưng tự giữ chuẩn animation/transition của mình.

Nghiên cứu từ Canva Help (presenting, animate help), precedent user (workflow 3 định dạng).

## 1. Bộ 3 định dạng xuất — chỉ khi adapter = (c) Canva spec

> Với (a) HTML/reveal.js → xuất `deck.html` + assets; với (b) python-pptx → xuất `deck.pptx`. Bảng dưới là chuẩn cho (c) Canva thủ công.

| Định dạng | Vai trò | Giữ được gì |
|---|---|---|
| **MP4** | Video dự phòng, chia sẻ nhanh, đăng mạng | Page animation + transition (render linear, KHÔNG giữ on-click) |
| **PPTX** | Trình chiếu trên PowerPoint máy khác | Hyperlink; on-click TƯƠNG ĐỐI (Canva convert một phần effect; kiểm tra lại) |
| **PDF** | Fallback máy chiếu yếu, in tài liệu | Tĩnh tuyệt đối — mọi click chết; dùng khi không chắc thiết bị |

Quy trình xuất: **Share → Download** → chọn type; PDF chọn "Flatten PDF" nếu font lỗi; MP4 chọn chất lượng cao.

Tại sao đủ 3: không biết trước máy chiếu ra sao — MP4 chết thì PDF luôn mở được. Đặt tên file: `[đề-tài]_[ngày]_[v1].pdf` (nhất quán 3 file cùng tên gốc).

## 2. Present mode trong Canva

- **Present → Full screen** (hoặc Present & Record nếu muốn quay kèm khuôn mặt nói).
- BấmSpace/mũi tên/phải: click từng element on-click theo Click order đã sắp (06).
- **Presenter View** (nút Present → Presenter view): 2 màn — khán giả thấy slide, mình thấy: slide kế, **notes**, click queue, đồng hồ.
- **Notes**: gõ ở editor (dưới trái "Notes") — speaker notes chỉ hiện ở Presenter View; ghi ý nói từng click vào đây.
- Remote bằng điện thoại: Canva app / trình duyệt đăng nhập → điều khiển present từ xa (khi không có clicker vật lý).

## 3. Kiểm tra trước khi trình chiếu (hiện trường)
- [ ] Mở PDF trên máy chiếu thật — font có vỡ? màu có rửa?
- [ ] Thử PPTX trên PowerPoint bản máy đó — on-click còn hoạt động đúng không?
- [ ] Có MP4 dự phòng trong USB (mở được không cần mạng).
- [ ] Định dạng 16:9 vs màn chiếu 4:3 cũ → nếu 4:3, dùng PDF zoom-to-fit, chấp nhận letterbox.

## 4. Chia sẻ
- **Publish to web**: Share → Publish → link xem trực tiếp (giữ hyperlink + animation trình duyệt; không cần đăng nhập).
- Viewers không cần tài khoản Canva.
- Hạn chế: người xem tự kéo tiến trình — không hợp khi muốn kiểm soát nhịp nói.

## 5. Magic Resize (tái sử dụng)
- Resize (Canva Pro) chỉ nên dùng SAU khi deck 16:9 hoàn thiện.
- 16:9 → 9:16 story: layout phải vẽ lại (full-bleed + chữ ít), không tin auto-convert 100%.
- Trong scope skill này: PRIORITIZE 16:9; resize là bước phụ tùy chọn.

## 6. Tránh
- Chỉ xuất 1 định dạng duyệt rồi ra hiện trường.
- Tin preview trong editor — luôn Present Full screen test thật ít nhất 1 vòng.
- Quên mp4 render lại sau khi sửa lần cuối (3 file phải cùng 1 version).
- Export PDF khi còn text box chồng nhau → lỗi chồng chữ khó thấy trên preview nhỏ.
