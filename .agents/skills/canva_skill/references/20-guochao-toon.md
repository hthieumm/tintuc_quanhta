# 20 — GUOCHAO TOON (国潮) — vui nhộn, hoạt họa viền mực

> **Nạp khi Q1 (tông cảm xúc, `00 §1.1`) = f) Vui nhộn, hoạt họa**, hoặc brief nhắc guochao / 国潮 / cartoon Á Đông / hoạt hình viền mực.
> 2 pattern: **I-1. Guochao-Stage** (slide nội dung) + **I-2. Guochao-Center** (cover / divider / quote).
> Font + palette trong file này là **quy tắc chọn và mẫu mặc định** — bản cuối kế thừa Q2/Q5 theo nội dung (xem §3, §4).

Nghiên cứu: 8 nhánh guochao (zhihu/数艺设 — flat, 潮酷, 卡通, 描边, 噪点, 版画…), kỹ thuật cổ họa (勾线 / cao cổ du ti miêu 十八描), bố cục poster đối xứng trục giữa + khung tròn + mây/sóng.

---

## 1. Nhận dạng + ranh giới

| Triệu chứng nhận dạng | Ranh giới với 18-H Ink-Pill-Seal |
|---|---|
| Nền **sáng** (ivory/giấy), flat màu + **viền mực nét đều hoặc ngoại dày-nội mảnh** | H: nền **tối**, tĩnh, trang nghiêm (di sản/triết lý) |
| Nhân vật hoạt hình hình học tròn, biểu cảm phóng đại — 1 tiêu điểm/slide | I: sáng, pop, có nhân vật hoạt hình (lễ hội/sản phẩm/giáo dục trẻ) |
| Mây cuộn, sóng đế, đèn lồng, con seal, grain 5-8% (噪点风 — làm thoáng) | Cả 2 đều dùng seal/mây — phân biệt bằng tông sáng + độ hoạt hình |
| Màu tương phản mạnh: đỏ chu sa + gold + xanh thạch trên ivory | Chọn H khi Q1 = a) trang nghiêm; chọn I khi Q1 = f) vui nhộn |

---

## 2. Nét vẽ (decide 1 lần cho cả deck)

**Chỉ chọn 1 trong 2 chế độ — không trộn trong cùng deck** (đúng tinh thần `05 §1`):

| Chế độ | Nguồn | Thông số | Hợp khi |
|---|---|---|---|
| **A. Nét đều mảnh** (du ti miêu 游丝描) | Cổ họa | stroke 2-3px đều như tơ, liên tục, không đổi độ đậm | Nhân vật/chi tiết thanh mảnh, deck nhiều chữ |
| **B. Ngoại dày — nội mảnh** (勾线 chuẩn) | Cổ họa | viền ngoài nhân vật 4-6px, chi tiết bên trong 2px | Nhân vật to, pop, trẻ em |

Quy tắc bắt buộc:
- **Màu nét = tông đậm nhất của palette** (mẫu: `#2E2A26` mực nâu), **cấm `#000000`** — đen cứng mất cảm giác mực.
- **Thưa dày có nhịp** (疏密有致): nét tập trung ở tiêu điểm (nhân vật), nền/mây/sóng đơn giản hoá, ít nét hơn poster gốc — slide phải thở.
- Mọi illustration/ornament trong deck **cùng 1 chế độ nét + cùng màu viền** — không trộn PNG nhiều nguồn nét khác nhau.

---

## 3. Palette — MẪU mặc định, kế thừa Q2/Q5

```
bg        #FFFBF0   (ivory giấy — 60%)
surface   #FFFFFF / #FFF3DC   (card, mây — 30%)
accent    #FF4612   (chu sa 朱砂 — tiêu đề lớn, rule, seal viền — 10%)
accent-2  #177CB0   (azurite 石青 — khối phụ, mây xanh)
gold      #F2BE45   (gold foil — viền khung, seal, ornament)
ink       #2E2A26   (mực — nét vẽ + toàn bộ chữ — 13.8:1 trên ivory)
```

Contrast đã tính (theo `00 §6`):

| Cặp | Ratio | Quy tắc dùng |
|---|---|---|
| `ink` trên `bg` ivory | 13.8:1 PASS | toàn bộ chữ |
| `#FFFFFF` trên `azurite` | 4.6:1 PASS | chữ trên khối xanh |
| `ink` trên `gold` | 8.3:1 PASS | chữ trong seal |
| `#FFFFFF` trên `chu sa` | 3.4:1 | **chỉ chữ ≥48px/800** (tiêu đề trên khối đỏ) |
| `chu sa` trên `bg` | 3.3:1 | **chỉ tiêu đề ≥48px + rule/ornament**, cấm body |
| `gold` trên `bg` | 1.7:1 FAIL | **cấm làm chữ trên nền sáng** — chỉ surface/viền |

**Kế thừa theo nội dung (bắt buộc):** palette trên là mẫu khi user không nói gì (Q5 trống). Nếu đề tài gợi màu khác — công nghệ → azurite chủ; ẩm thực → đỏ/vàng ấm; môi trường → xanh lục — **giữ nguyên quan hệ**: nền sáng neutral + 1 accent đậm + 1 gold/surface phụ + ink làm nét/chữ, tuân 60-30-10 và ≤5 màu (`03`). Q5 (brand) luôn thắng.

---

## 4. Font — QUY TẮC chọn theo nội dung, không fix cứng

| Đề tài | Heading | Body |
|---|---|---|
| Truyền thống, văn hoá, lễ hội, di sản vui | Noto Serif SC 700 (CJK serif) | Be Vietnam Pro |
| Hiện đại, sản phẩm, startup, giáo dục trẻ | Be Vietnam Pro 800 | Be Vietnam Pro 400 |

- Luôn **≤2 family**; body tiếng Việt **luôn Be Vietnam Pro** (đủ dấu).
- Q5 (brand font) > quy tắc đề tài. Không có Noto Serif SC trong môi trường → thay serif display bất kỳ + ornament bù (mây, seal).
- Caption 24px Be Vietnam Pro 400, màu ink/70%.

---

## 5. I-1. GUOCHAO-STAGE — slide nội dung (lệch trục)

```
[E1] bg        x:0%   y:0%   w:100%  h:100%  fill:#FFFBF0 | grain 5-8% phủ trên cùng
[E2] character x:4%   y:14%  w:36%   h:76%   PNG trong suốt, 1 nhân vật hoạt hình, viền mực
[E3] cloud-band x:0%  y:84%  w:100%  h:16%   mây cuộn/sóng đế fill #FFF3DC — đè chân E2
[E4] title     x:45%  y:10%  w:50%   h:13%   64px/800, ink, trái
[E5] rule      x:45%  y:25%  w:10%   h:1.5%  fill chu sa #FF4612
[E6] card      x:45%  y:31%  w:50%   h:50%   #FFFFFF radius 16px, shadow 10% | 3-4 mục
[E7] caption   x:45%  y:84%  w:44%   h:6%    24px, ink 70%
[E8] ornament  x:90%  y:6%   w:8%    h:12%   đèn lồng/mây nhỏ, opacity 80%
```

Quy tắc:
- **1 nhân vật/slide** — nhân vật là tiêu điểm duy nhất, nét dày nhất slide (§2).
- Mây/sóng **tối đa 2 dải**; ornament (kể seal) **≤3 element**.
- Danh sách >4 mục hoặc mục >2 dòng → đổi card ngang thành **stem-list dọc** (18-G biến thể) giữ nguyên nền/mây.
- Click order: E4 → E6 (các mục) → E2; nhân vật hiện sẵn hoặc rise cuối để "chào".

---

## 6. I-2. GUOCHAO-CENTER — cover / divider / quote (trục giữa đối xứng)

```
[E1] bg        x:0%   y:0%   w:100%  h:100%  fill:#FFFBF0 (divider: fill chu sa) + grain
[E2] ring      x:31%  y:16%  w:38%   h:60%   khung tròn viền kép 6px ink + 3px gold, trong #FFFFFF
[E3] title     x:34%  y:34%  w:32%   h:18%   56-72px/800, giữa, ink trên trắng (trên đỏ: #FFFFFF ≥48px)
[E4] cloud-top x:18%  y:3%   w:64%   h:10%   mây cuộn đối xứng 2 bên trục giữa, fill #FFF3DC
[E5] cloud-bot x:18%  y:87%  w:64%   h:10%   mây/sóng đế
[E6] seal      x:59%  y:64%  w:9%    h:13%   vuông bo 8px, fill gold, chữ ink 20-24px, xoay 4-6°, chồng mép E2
[E7] vlabel-L  x:9%   y:22%  w:4%    h:40%   chữ dọc 28px/600 ink (tùy chọn — câu đối)
[E8] vlabel-R  x:87%  y:22%  w:4%    h:40%   chữ dọc 28px/600 ink (tùy chọn — câu đối)
```

Quy tắc:
- **Đối xứng tuyệt đối qua trục x:50%** — chỉ cover/divider/quote được căn giữa (`01 §6`).
- Seal mang thông tin → fill gold + chữ ink (8.3:1); seal đỏ chỉ để trang trí không chữ.
- Vlabel phải có cặp (trái + phải) hoặc bỏ cả hai — không đứng 1 bên.
- **I-2 ≤30% tổng số slide**; xen kẽ với I-1 để đổi nhịp (`01 §4`).

---

## 7. Cách làm trong Canva

| Việc | Cách |
|---|---|
| Nhân vật | Elements → search "guochao" / "chinese cartoon" / "chinoiserie illustration" → PNG trong suốt, lọc cùng palette |
| Mây cuộn | Elements → "chinese cloud" / "祥云" / "asian cloud" |
| Sóng đế | Elements → "chinese wave" / "海浪纹" / "wave pattern" |
| Khung tròn | Shape circle viền 6px ink + circle thứ 2 viền 3px gold, lệch 1-2% |
| Con dấu | Elements → "chinese seal" / "red stamp" (trang trí) hoặc shape vuông bo + chữ (thông tin) |
| Grain | Elements → "grain" / "noise" → phủ full-slide, opacity 5-8%, trên cùng |
| Chữ dọc | Text → xoay 90°, hoặc dùng vertical text box |

Medium (a) HTML: mây/sóng dùng SVG inline hoặc PNG; grain bằng CSS noise overlay.
Medium (b) pptx: khung tròn = shape oval 2 lớp; grain chèn PNG noise full-slide; ghi giới hạn "đèn lồng PNG không bo theo mép".

---

## 8. Checklist riêng pattern I (chạy trước QA 12)

- [ ] Deck dùng đúng **1 chế độ nét** (A hoặc B) — kiểm mọi PNG viền cùng độ đậm.
- [ ] Màu viền = tông đậm nhất palette, **không có `#000000`**.
- [ ] `chu sa`/accent đỏ **không xuất hiện** làm body text; gold không làm chữ trên nền sáng.
- [ ] Mây/sóng ≤2 dải/slide; ornament ≤3; **1 tiêu điểm** nhân vật.
- [ ] I-2 ≤30% slide; không pattern I nào lặp 3 slide liên tiếp.
- [ ] Grain 5-8% tồn tại trên mọi slide nền phẳng.
- [ ] Mọi PNG có `alt` (00 §2); nhân vật hoạt hình cũng phải có alt.
- [ ] Nếu Q5 có brand palette → ghi rõ palette thực dùng trong DECK SPEC, không dùng mẫu §3.

---

## 9. Tránh

- Dùng I cho deck data nhiều số (→ `10-data-infographic`), pháp lý, trang nghiêm (→ 18-H hoặc corporate nền sáng `01`).
- Làm "đậm đặc như poster 潮酷 gốc" — nhiều nhân vật, nhiều mây chèn kín slide: slide thua poster ở whitespace, phải cắt bớt.
- Trộn PNG nhiều nguồn: nét to + nét nhỏ + ảnh chụp nhân vật cùng slide.
- Seal đỏ + chữ trắng nhỏ dưới 48px (3.4:1 FAIL).
- Viền nhân vật bằng màu khác ink (đen cứng hoặc màuaccent loạn).
