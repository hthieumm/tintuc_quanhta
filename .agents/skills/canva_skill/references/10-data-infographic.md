# 10 — DATA & INFOGRAPHIC (Slide số liệu trong 16:9)

Nghiên cứu từ nguyên tắc data-ink ratio (Tufte) áp dụng Canva, presentations.ai, precedent big-number slides.

## 1. Chọn đúng chart

| Dữ liệu | Chart | Tránh |
|---|---|---|
| So sánh giữa các mục | Bar (ngang khi nhãn dài) | Pie nhiều miếng |
| Diễn tiến thời gian | Line (≤3-4 đường) | Bar 3D |
| Tỷ lệ ≤5 phần, chênh rõ | Donut + % ở tâm | Pie 7+ miếng |
| Phân bố | Histogram / scatter | |
| Quan hệ 2 biến | Scatter + đường xu hướng | |
| Bước quy trình | Process arrow / numbered circles | |
| Timeline sự kiện | Trục ngang + chấm mốc | Bảng chữ |

## 2. Dọn rác chart (data-ink ratio)

- **Bỏ gridlines** (hoặc để mảnh 5% opacity), bỏ legend khi đã label trực tiếp.
- **Label trực tiếp** trên bar/dòng (không bắt người đọc dòm legend).
- Trục bắt đầu từ 0 với bar (tránh nói quá); line có thể zoom nhưng ghi rõ.
- Tối đa **2 màu**: màu chính = series quan trọng (accent), màu xám = phần còn lại. **Bôi vàng-series-cần-nói** (highlight) là kỹ thuật mạnh nhất.
- Số làm tròn đẹp: "≈ 68%" thay vì "67.83%".

## 3. Big number (slide kết luận số)

Mẫu slide 1 số duy nhất:
```
[ SỐ TO — 160px, accent color ]
[ 1 dòng giải thích — 40px ]
[ nguồn nhỏ 24px, opacity 60% ]
```
- Số chiếm 40-50% diện tích slide, xuất hiện bằng effect Pop/Rise on-click.
- Chỉ dùng khi số ĐÓ là câu chuyện (vd: "19 clicks" precedent).

## 4. Trước/Sau & so sánh

- 2 cột ảnh/2 số đặt cạnh nhau bằng nhau, đường phân cách mảnh, label "Trước → Sau".
- Hoặc 1 ảnh chia đôi bởi diagonal split (mask 2 tam giác).
- On-click: hiện "Trước" trước, click sau hiện "Sau" — kịch tính tự nhiên.

## 5. Timeline (hợp đề tài lịch sử/văn hóa precedent user)

- Trục ngang (đường mảnh 2px), chấm mốc tròn, nhãn trên-dưới so le.
- **On-click từng mốc** theo trình tự thời gian (nói đến đâu hiện đến đó).
- Ảnh nhỏ crop circle đứng cạnh mốc quan trọng.
- ≥5 mốc → gom nhóm theo giai đoạn, divider giữa giai đoạn.

## 6. Infographic trong Canva

- Elements → search "chart" (editable chart: nhập số liệu trực tiếp), "infographic", "timeline", "process".
- Chart Canva chỉnh được màu theo palette — đồng bộ với deck.
- Điền số liệu thật, **ghi nguồn** 24px ở góc (dữ liệu không có nguồn = không đưa lên).

## 7. Tránh
- Chart 3D, shadow, gradient đổ cột.
- 2 chart chung 1 slide khi không so sánh trực tiếp.
- Màu series đổi giữa các slide (cùng 1 loại dữ liệu = cùng 1 màu).
- Số liệu viết tắt không đơn vị ("1,2" — 1,2 gì? triệu? %).
