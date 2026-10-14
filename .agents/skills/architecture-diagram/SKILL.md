---
name: architecture-diagram
description: Hướng dẫn vẽ và biểu diễn sơ đồ kiến trúc hệ thống, sơ đồ tuần tự (Sequence Diagram), luồng dữ liệu (Data-Flow) và ERD bằng Mermaid / HTML.
---

# Architecture & System Diagrams Standards

Sử dụng quy chuẩn này khi được yêu cầu giải thích kiến trúc hoặc mô tả luồng hoạt động của hệ thống.

---

## 1. Cú pháp Mermaid phổ biến

### Sơ đồ kiến trúc / Luồng dữ liệu (Flowchart)
```mermaid
graph TD
    Client["Client (Web / Mobile)"] -->|HTTPS / REST / GraphQL| Gateway["API Gateway / Reverse Proxy"]
    Gateway -->|JWT Verify| AuthService["Auth Service"]
    Gateway -->|Forward Request| CoreService["Core Application Service"]
    CoreService -->|Read / Write| Database[("Main Database (PostgreSQL)")]
    CoreService -->|Cache| RedisCache[("Redis Cache")]
    CoreService -->|Publish Events| MessageQueue["Message Broker (Kafka / RabbitMQ)"]
    MessageQueue -->|Async Job| Worker["Background Worker"]
```

### Sơ đồ tuần tự (Sequence Diagram)
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as Web Client
    participant API as Backend API
    participant DB as Database

    User->>Frontend: Điền thông tin đăng nhập
    Frontend->>API: POST /api/v1/auth/login
    API->>DB: Tìm người dùng theo Email
    DB-->>API: Trả về User Record & Hashed Password
    API->>API: So khớp bcrypt hash
    alt Mật khẩu đúng
        API-->>Frontend: 200 OK + JWT Token
        Frontend-->>User: Chuyển hướng vào Dashboard
    else Mật khẩu sai
        API-->>Frontend: 401 Unauthorized
        Frontend-->>User: Hiển thị thông báo lỗi
    end
```

---

## 2. Nguyên tắc vẽ sơ đồ
1. **Rõ ràng, không quá tải:** Một sơ đồ chỉ nên tập trung vào 1 phạm vi logic (không nhồi nhét toàn bộ hệ thống vào 1 hình duy nhất).
2. **Quy ước hình khối:**
   - Hình chữ nhật: Service / Component.
   - Hình trụ (`[(...)]`): Database / Storage.
   - Hình bình hành / Icon: External Third-party Service.
3. **Mô tả hành động trên mũi tên:** Luôn ghi rõ phương thức (HTTP method, message event) và dữ liệu truyền tải trên từng đường kết nối.
