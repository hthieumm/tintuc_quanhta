---
name: ui-ux-design-system
description: Hướng dẫn xây dựng giao diện người dùng (UI/UX) chuẩn chỉ, hiện đại, responsive, tuân thủ Accessibility (a11y) và Design Tokens.
---

# UI/UX & Design System Guidelines

Áp dụng quy chuẩn này khi thiết kế hoặc phát triển các thành phần giao diện Frontend (Web/Mobile).

---

## 1. Thiết kế & Bố cục (Layout & Responsiveness)

1. **Mobile-First Approach:** Thiết kế trải nghiệm tốt trên thiết bị di động trước, sau đó mở rộng cho Tablet và Desktop.
2. **Hệ thống lưới (Spacing Grid):** Sử dụng hệ số 4px hoặc 8px (4, 8, 12, 16, 24, 32, 48, 64px) cho margin, padding và khoảng cách các thành phần để tạo sự đồng nhất.
3. **Phân cấp thị giác (Visual Hierarchy):**
   - Tiêu đề (H1, H2, H3), nội dung chính và phụ phải có sự tương phản rõ ràng về font size, font weight và màu sắc.
   - Nhấn mạnh các Action quan trọng (Primary CTA) bằng màu sắc nổi bật.

---

## 2. Khả năng tiếp cận (Accessibility - a11y)

- **Độ tương phản màu (Color Contrast):** Đảm bảo tỷ lệ tương phản giữa chữ và nền đạt tối thiểu **WCAG AA (4.5:1)**.
- **Thẻ ngữ nghĩa (Semantic HTML):** Sử dụng đúng thẻ `<button>`, `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>` thay vì lạm dụng toàn bộ thẻ `<div>`.
- **Keyboard Navigation:** Mọi tương tác (click, mở modal, submit form) đều phải hoạt động được bằng bàn phím (`Tab`, `Enter`, `Escape`).
- **Hình ảnh & Icon:** Luôn cung cấp thuộc tính `alt` cho hình ảnh và `aria-label` cho các nút chỉ có icon.

---

## 3. Trạng thái giao diện (Component States)

Mỗi component/form tương tác phải hỗ trợ đầy đủ các trạng thái:
1. **Default:** Trạng thái bình thường.
2. **Hover / Focus:** Phản hồi trực quan khi người dùng rê chuột hoặc focus bằng bàn phím.
3. **Active / Pressed:** Khi người dùng bấm xuống.
4. **Loading / Skeleton:** Hiển thị spinner hoặc skeleton loader khi dữ liệu đang tải, tránh giao diện bị giật.
5. **Disabled:** Khi action tạm thời không khả dụng.
6. **Error / Empty State:** Thông báo lỗi thân thiện hoặc màn hình hướng dẫn khi không có dữ liệu.
