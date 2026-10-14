# 14 — CINEMATIC FLOW (Slide liên tục — deck chảy như video)

> **Lớp design.** Match & Move / thao tác chuột trong Canva → `16-tool-adapters.md` §C. Với medium (a) HTML, Match & Move được hiện thực hoá bằng `data-auto-animate-id`; với medium (b) pptx không có transition → nói rõ giới hạn cho user trước khi code.

Nghiên cứu từ Canva Help (page transitions), Canva Design School + Reddit r/canva (Match & Move), nguyên tắc motion continuity (UX in Motion, Material Design).

Mục tiêu: số slide bất kỳ, nhưng slide sau **nối tiếp** slide trước — ảnh nối ảnh, nội dung nối nội dung — transitions mượt như scroll/quay video.

## 1. Cài transition giữa các trang (page transition)

- Editor: **hover giữa 2 thumbnail page** (panel trái) → nút **Add transition** → chọn style.
- **Duration slider 0.1–2.5s** — chuẩn: 0.5–0.7s; zoom/pancinematic có thể 0.8–1.2s.
- Một số style có **hướng** (trái/phải/lên/xuống) — chọn theo hướng "cuộn" của deck.
- Transition áp **cặp trang**, không áp cả deck một phát — phối theo cảm giác từng cặp (bảng mục 4).

## 2. Match & Move — kỹ thuật cốt lõi (Canva Pro)

Element **giống hệt nhau** trên 2 trang liên tiếp sẽ tự động được Canva animate: vị trí, kích thước, màu, độ trong suốt **biến đổi mượt** từ trang N sang N+1. Đây chính là "ảnh trước → ảnh sau" liền mạch như video.

### Setup chuẩn (tránh fallback về fade)
1. Hoàn thiện slide N, chọn trang → **Duplicate page** (bản sao giữ element identical).
2. Trên bản sao: **kéo element** sang vị trí mới, đổi cỡ/màu/opacity nếu muốn.
3. Resize **chỉ dùng corner handle** (kéo chéo) — dùng side/top handle làm Match & Move mất hiệu lực, rơi về fade (gotcha Reddit).
4. Hover giữa 2 trang → chọn transition **Match & Move**.
5. Preview Present — element phải trôi mượt từ vị trí cũ sang mới.

### Ứng dụng
- Ảnh hero trang cover → thu nhỏ thành ảnh nhỏ góc trang content.
- Số chương to → thu nhỏ thành badge nhỏ trên divider kế tiếp.
- Khối màu nền → đổi màu dần (đỏ → đỏ đậm → tím đêm) tạo color flow toàn deck.

## 3. Hệ thống continuity (liên kết nội dung xuyên deck)

| Kỹ thuật | Cách làm | Hiệu ứng |
|---|---|---|
| **Element chain** | 1 ảnh/shape "nhân vật" đi xuyên deck: mỗi slide đổi vị trí/cỡ (Match & Move chuỗi) | Mắt người xem bám theo — như nhân vật trong phim |
| **Edge-bleed** | Khối (ảnh/màu/shape) tràn **sang phải slide N** → xuất hiện ở **l mép trái slide N+1**, transition Pan ngang | Cảm giác "cuộn ngang" 1 bức tranh dài cắt qua nhiều slide |
| **Color flow** | Palette trôi dần theo mạch truyện: ấm → đậm → tối theo chương (đổi nền bằng Match & Move hoặc transition Dissolve) | Tension tự nhiên như grading phim |
| **Persistent object** | Số chương/chấm tiến trình/mini-map cố định cùng vị trí mọi slide, chỉ đổi trạng thái | Người xem luôn biết mình ở đâu trong "cuộn phim" |

## 4. Bảng transition theo cảm giác

| Cảm giác muốn tạo | Transition | Duration |
|---|---|---|
| Cuộn ngang (timeline, truyện dài) | **Pan/Slide** hướng nhất quán + edge-bleed | 0.7–1.0s |
| Zoom vào chi tiết (từ tổng quan → cụ thể) | **Uncover/Orbit** hoặc Match & Move phóng to element | 0.8–1.2s |
| Đổi cảnh/chương | **Dissolve** | 0.5–0.7s |
| Ảnh trước → ảnh sau cùng nội dung | **Match & Move** | 0.5–0.8s |
| Nhanh, năng lượng | **Slide/Instant** ngắn | 0.3–0.5s |

Quy tắc: **1 hướng chủ đạo toàn deck** (vd luôn sang trái = tiến về trước); chỉ Dissolve khi đổi chương. Trộn hướng tùy hứng = say máy.

## 5. 4 pattern dựng sẵn (áp vào đề tài bất kỳ)

### A. Horizontal timeline scroll
Đề tài lịch sử/diễn tiến (hợp precedent dân tộc VN): dải ảnh+chấm mốc trải ngang qua 4-6 slide bằng edge-bleed; mỗi slide Pan trái 0.7s; element chain = con trỏ/vệt sáng đánh dấu mốc hiện tại.

### B. Zoom-in storytelling
Cover full-bleed → Match & Move crop dần vào chi tiết ảnh (mỗi slide zoom sâu 1 tầng): slide 1 toàn cảnh chợ → slide 2 cận gánh hàng → slide 3 cận đôi bàn tay. Mỗi tầng = 1 câu chuyện.

### C. Ken-burns xuyên slide
1 ảnh lớn cắt làm nhiều "khung nhìn": slide N hiện phần trên (Photo Movement pan chậm), slide N+1 Match & Move trôi xuống phần giữa → phần dưới. Người xem như đang camera movement trên 1 bức tranh.

### D. Chapter flow
Divider chương = khối màu + số chương to → Match & Move: khối màu co lại thành thanh mảnh + số nhỏ góc mọi slide còn lại của chương (persistent object). Sang chương: Dissolve, lặp pattern.

## 6. Playback & export (quyết định user)

- **Present trực tiếp**: Method A — click tay từng element (giữ 19 clicks/3 slides precedent), page transition chạy tự động khi sang trang.
- **MP4 export**: mọi click + transition render thành **video tuyến tính** — đây chính là "presentation như video" khi chia sẻ. Render lại MP4 sau mỗi lần sửa.
- PPTX: Match & Move/transition Canva KHÔNG mang sang PowerPoint hoàn chỉnh → PPTX chỉ là bản click dự phòng (11-export).
- PDF: chỉ còn frame đầu mỗi slide → đảm bảo mỗi slide tĩnh vẫn tự đứng được.

## 7. Giới hạn kỹ thuật Canva (nhớ khi làm deck dài)
- **350 pages/design** tối đa.
- **50 animations/design** — deck dài: gom element thành group (1 animation/group), ưu tiên Match & Move + page transition (transition không ăn ngân hàng animation).
- **10 giây** tối đa mỗi animation đơn.
- Element timing (More → Show element timing) chỉnh tốc độ từng element: Slow/Medium/Fast.

## 8. Tránh
- Match & Move với element đã chỉnh side-handle → âm thầm rơi về fade, luôn test Present.
- Transition khác hướng mỗi cặp trang.
- Edge-bleed mà khối không khớp vị trí mép (đo bằng guide) → giật khúc.
- Lạm dụng Match & Move cho MỌI element — chỉ 1-2 "nhân vật" chính xuyên slide, phần còn lại rise/fade như bình thường (06-animation).
- Quên check "Reduce motion" của người xem chỉ ảnh hưởng playback, không phá design gốc.
