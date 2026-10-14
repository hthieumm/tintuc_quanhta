---
name: tdd-testing-expert
description: Hướng dẫn quy trình phát triển hướng kiểm thử (TDD), viết Unit Test, Integration Test chất lượng cao, bao phủ các trường hợp biên (Edge Cases) và Mocking an toàn.
---

# Test-Driven Development (TDD) & Testing Standards

Áp dụng quy chuẩn này khi viết mã nguồn và xây dựng test suite cho dự án.

---

## 1. Chu trình TDD (Red - Green - Refactor)

1. **Red (Viết test trước):** Viết unit test mô tả hành vi mong muốn trước khi viết code logic. Chạy test và xác nhận test thất bại (Red).
2. **Green (Viết code tối thiểu):** Viết lượng code tối thiểu để làm bài test vượt qua (Green). Không viết thừa logic.
3. **Refactor (Tối ưu mã nguồn):** Tái cấu trúc code cho sạch đẹp, dễ bảo trì mà vẫn đảm bảo toàn bộ bài test tiếp tục vượt qua.

---

## 2. Quy tắc cấu trúc bài Test (AAA Pattern)

Mỗi test case phải tuân theo cấu trúc 3 giai đoạn rõ ràng:
- **Arrange (Chuẩn bị):** Khởi tạo dữ liệu đầu vào, thiết lập mock, khởi tạo service.
- **Act (Thực thi):** Gọi hàm hoặc endpoint cần kiểm thử.
- **Assert (Kiểm tra):** Xác minh kết quả trả về, trạng thái thay đổi hoặc các hàm mock đã được gọi đúng tham số.

---

## 3. Các trường hợp bắt buộc phải test (Test Coverage)

1. **Happy Path:** Dữ liệu đầu vào hoàn toàn hợp lệ, luồng thực thi diễn ra suôn sẻ.
2. **Edge Cases (Trường hợp biên):**
   - Giá trị rỗng: `null`, `undefined`, chuỗi rỗng `""`, mảng rỗng `[]`.
   - Giá trị cực hạn: Số âm, số 0, số cực lớn (Number.MAX_SAFE_INTEGER).
3. **Error Cases:**
   - Dữ liệu không hợp lệ (sai định dạng email, mật khẩu quá ngắn).
   - Ngoại lệ mạng (Network Timeout, Database Connection Failure).
   - Kiểm tra mã lỗi trả về (ví dụ: 400 Bad Request, 404 Not Found, 403 Forbidden).
