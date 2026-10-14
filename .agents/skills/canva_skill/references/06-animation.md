# 06 — MOTION & ANIMATION (Method A: On Click)

> **Lớp design (bất biến, áp dụng cả 3 medium).** Phần thao tác chuột trong Canva ("bật Appear on click", "kéo-thả Click order") đã chuyển sang `16-tool-adapters.md` §C — AI không cần đọc phần đó trừ khi medium = (c) hoặc mode = fix-existing.

Nghiên cứu từ Canva Help (Apply animations), Canva Learn, NN/g (animation duration), UX in Motion Manifesto, Material Design (choreography), precedent user (19 clicks/3 slides).

## 1. Hai cấp animation trong Canva

| Cấp | Vị trí | Phạm vi |
|---|---|---|
| **Page animation** (transition) | Chọn page nền → Animate | Cả slide chuyển (dissolve, pan, slide...) |
| **Element animation** | Chọn element/group → Animate | Từng element: Basic (fade, rise, pan, pop, tumble...), Exaggerate, Photo Movement (ken burns), Motion paths |

Free vs Pro: nhiều effect hay (tumble, typewriter...) gắn nhãn Try Canva Pro — kiểm tra trước khi chọn.

## 2. METHOD A — On Click thủ công (chuẩn user, BẮT BUỘC)

Nguyên tắc: **mọi element animation đều "Appear on click"**, KHÔNG auto-play. Người trình bày kiểm soát nhịp.

### Thiết lập trong Canva
> Chi tiết thao tác chuột (chọn element → Animate, bật Appear on click, kéo-thả Click order) nằm ở `16-tool-adapters.md` §C. Đoạn dưới đây chỉ để đọc hiểu; khi xuất chọn thao tác từ 16 §C.

1. Chọn element/group → **Animate** → chọn effect.
2. Bật **Presentation settings → Appear on click**.
3. **Click order**: Presentation settings → Click order → **kéo-thả** element để sắp thứ tự xuất hiện (first → last). Đây chính là "checklist click" của user.
4. Preview: Present → bấm từng click để test.

### Pacing (tiêu chuẩn từ precedent user)
- Kinh nghiệm chuẩn: 19 clicks / 3 slides ≈ 3.5 phút → **~6 clicks/slide nội dung**, ~11 giây/click.
- Mỗi click = 1 ý nhỏ được nói tới (UCSD: "make objects appear only when mentioned").
- Không quá 8-10 clicks/slide → người xem mỏi tay thay vì mỏi mắt; nếu nhiều hơn, tách slide.

### Nhóm để giảm click
- **Group ảnh + caption + số thứ tự** → 1 click.
- Group icon + label → 1 click.
- Tiêu đề slide: cho xuất hiện cùng page transition (không cần click riêng).

## 3. Choreography (dàn chuyển động)

Từ Material Design choreography + UX in Motion:

- **Staging — 1 tiêu điểm/lúc**: không cho mọi element bay vào cùng lúc. Người xem phải biết nhìn đâu (graduateschool.edu: "when every element animates simultaneously, the viewer cannot focus on any of them").
- **Thứ tự chuẩn**: tiêu đề/câu chủ đề → khối chính → chi tiết → số liệu nhấn.
- **Offset & delay**: các element anh em vào lệch nhau ~100-200ms thay vì đồng loạt — Canva: group riêng + click liền nhau, hoặc dùng transition page cho cả nhóm.
- **Follow-through**: element pop nhẹ rồi mới xuống vị trí — chọn effect "Pop"/"Rise" thay vì "Instant".

## 4. Easing & timing

- **Ease-out cho element VÀO** (vào nhanh, hạ cánh chậm — mắt đoán được điểm dừng); ease-in cho element RỜI đi. (NN/g)
- Linear motion = cảm giác robot — tránh.
- Tham chiếu thời lượng UI: ~300ms cảm giác responsive; Canva effect mặc định đã ease — giữ mặc định, không phóng đại.
- Slide transition: **0.5–0.7s**, hướng nhất quán (precedent user: chuyển sang trái 0.7s — tức nội dung "tiến về trước").

## 5. Chọn effect theo nội dung

| Nội dung | Effect gợi ý |
|---|---|
| Tiêu đề câu chủ đề | Rise / Pan |
| Ảnh minh họa | Photo Movement (ken burns chậm) / Rise |
| Số liệu to | Pop / Scale |
| Danh sách bullet | Rise lần lượt (mỗi click 1 dòng) |
| Quote | Dissolve / Typewriter |
| Nút CTA cuối | Pop + nhấn màu accent |

- Tối đa **2-3 loại effect/deck**; hiệu ứng lặp lại tạo nhịp, đổi tùy slide gây rối.
- Motion path (Canva Pro): chỉ dùng khi có lý do kể chuyện (vd chấm trượt theo bản đồ).

## 6. Tránh
- Spin/Bounce/Zoom ầm ầm toàn bộ element.
- Animation tự chạy (auto) — mất quyền kiểm soát khi nói.
- Page transition != hướng nhất quán (slide trước trái, sau phải).
- Animation che nội dung: effect bay ngang qua vùng chữ đang hiển thị.
- Quên test click order trong Present mode thật.

## 7. Magic Shortcuts (khi đang Present)
- Nhấn **C** = confetti, **D** = drumroll, **M** = mic drop — dùng đúng 1 lần ở thời điểm đắt (kết bài, công bố số liệu bất ngờ).
