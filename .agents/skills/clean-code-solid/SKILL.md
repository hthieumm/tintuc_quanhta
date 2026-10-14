---
name: clean-code-solid
description: Hướng dẫn viết mã nguồn sạch (Clean Code), áp dụng chuẩn SOLID, DRY, KISS và tối ưu hóa khả năng bảo trì cho mọi ngôn ngữ lập trình.
---

# Clean Code & SOLID Engineering Standards

Áp dụng bộ quy chuẩn này khi viết mã mới hoặc tái cấu trúc (refactor) mã nguồn trong dự án.

---

## 1. Các nguyên tắc thiết kế cốt lõi

### SOLID Principles
- **S - Single Responsibility Principle (SRP):** Mỗi hàm, class hoặc module chỉ đảm nhận một trách nhiệm duy nhất và chỉ có một lý do để thay đổi.
- **O - Open/Closed Principle (OCP):** Mở rộng tính năng bằng cách thêm mới code (interface/kế thừa/composition), không sửa đổi code cũ đã hoạt động ổn định.
- **L - Liskov Substitution Principle (LSP):** Lớp con phải có thể thay thế lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
- **I - Interface Segregation Principle (ISP):** Chia nhỏ interface, không bắt client phải phụ thuộc vào các method mà họ không dùng.
- **D - Dependency Inversion Principle (DIP):** Module cấp cao không phụ thuộc module cấp thấp; cả hai phụ thuộc vào abstraction (interface/abstract class).

### Quy tắc bổ trợ
- **DRY (Don't Repeat Yourself):** Tránh trùng lặp logic, gom code chung thành helper/service khi logic lặp lại từ 3 lần trở lên.
- **KISS (Keep It Simple, Stupid):** Ưu tiên giải pháp đơn giản, dễ hiểu, tránh over-engineering.
- **YAGNI (You Aren't Gonna Need It):** Chỉ viết code phục vụ yêu cầu hiện tại, không cài đặt trước các tính năng giả định trong tương lai.

---

## 2. Quy chuẩn viết code & hàm

1. **Độ dài hàm:** Mỗi hàm lý tưởng dưới 20-30 dòng, thực hiện đúng một việc và thực hiện nó thật tốt.
2. **Đặt tên (Naming):**
   - Tên biến/hàm phải tự giải thích ý nghĩa (self-documenting), không viết tắt khó hiểu.
   - Hàm xử lý logic đặt theo động từ (`calculateTotalPrice`, `validateUserToken`).
   - Biến boolean bắt đầu bằng tiền tố (`isValid`, `hasPermission`, `canAccess`).
3. **Guard Clauses (Return sớm):**
   - Xử lý các điều kiện lỗi/ngoại lệ ngay đầu hàm và `return` sớm.
   - Tránh lồng `if/else` quá 2-3 tầng (chống hiệu ứng mũi tên Pyramid of Doom).
4. **Xử lý lỗi (Error Handling):**
   - Luôn bắt lỗi cụ thể, không nuốt lỗi (empty catch block).
   - Log lỗi kèm context rõ ràng để dễ debug.
