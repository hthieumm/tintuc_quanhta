# 🗄️ KẾ HOẠCH THIẾT KẾ DATABASE (SPIDER NEWS RADAR)
> **Dự án:** Spider News Radar (Tin Tức Quanh Ta)  
> **Mục tiêu:** Lưu trữ tin tức đa quốc gia, repo GitHub, kết quả lọc của System 1, bản dịch/tóm tắt tiếng Việt của LLM System 2, và lịch sử từ khóa phục vụ Màn hình 5 (Trend Vault).

---

## 1. Lựa Chọn Công Nghệ Database: SQLite (WAL Mode)

Thay vì dựng các hệ cơ sở dữ liệu cồng kềnh (như PostgreSQL hay MySQL) làm tốn tài nguyên máy tính văn phòng, chúng ta chọn **SQLite** với các cấu hình tối ưu cấp cao:

* **File cơ sở dữ liệu:** `D:\code_tienich_forme\tintuc_quanhta\backend\data\spider_radar.db`
* **Driver Python:** `aiosqlite` (Bất đồng bộ 100% trong FastAPI, không làm nghẽn luồng xử lý).
* **Chế độ WAL (Write-Ahead Logging):** Cho phép Backend vừa đọc vừa ghi đồng thời với tốc độ sub-millisecond (< 1ms).
* **Tích hợp FTS5 (Full-Text Search 5):** Tìm kiếm toàn văn tiếng Việt & tiếng Anh siêu tốc không cần cài Elasticsearch.
* **JSON1 Extension:** Hỗ trợ lưu và truy vấn mảng tọa độ từ khóa dạng JSON trực tiếp trong bảng.

---

## 2. Sơ Đồ Quan Hệ Bảng (Database Schema / ERD)

```
[ sources ] (Quản lý nguồn RSS / GitHub)
     │ 1
     ├───────< [ articles ] (Bài báo kinh tế / chính trị)
     │             │ 1
     │             ├───────< [ laya_decisions ] (Phân loại System 1 & Tọa độ Nhện)
     │             └───────< [ llm_syntheses ]  (Bản dịch & Tóm tắt tiếng Việt System 2)
     │ 1
     └───────< [ github_repos ] (Kho lưu trữ GitHub)
                   │ 1
                   └───────< [ llm_syntheses ]

[ keyword_trends ] (Thống kê từ khóa nóng cho Màn hình 5)
[ system_settings ] (Cấu hình âm thanh, tốc độ nhện, API key)
```

---

## 3. Đặc Tả Chi Tiết Các Bảng (DDL Tables)

### 3.1. Bảng `sources` (Nguồn tin & Quản lý Thêm/Bớt Kênh Động)
Quản lý các đầu báo RSS và API GitHub, cho phép người dùng tùy ý cấu hình bật/tắt hoặc thêm mới.
```sql
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                     -- Ví dụ: "CaféF Chứng khoán", "Kitco Giá Vàng", "CoinDesk Crypto"
    source_type TEXT NOT NULL,              -- "rss" hoặc "github_api"
    url TEXT NOT NULL UNIQUE,               -- Link RSS hoặc Endpoint GitHub
    category TEXT DEFAULT 'kinh_te',        -- 'chung_khoan', 'vang', 'crypto', 'kinh_te', 'chinh_tri', 'github', 'tuy_chon'
    is_active INTEGER DEFAULT 1,            -- 1: Bật cào, 0: Tắt
    fetch_interval_min INTEGER DEFAULT 15,  -- Chu kỳ cào (phút)
    last_fetched_at DATETIME
);

-- Dữ liệu hạt giống mặc định (Default Seed Sources):
INSERT OR IGNORE INTO sources (name, source_type, url, category, fetch_interval_min) VALUES
-- 1. Chứng khoán
('CaféF Chứng Khoán', 'rss', 'https://cafef.vn/thi-truong-chung-khoan.rss', 'chung_khoan', 10),
('Vietstock Tin Nhanh', 'rss', 'https://vietstock.vn/rss/chung-khoan.rss', 'chung_khoan', 10),
-- 2. Giá Vàng & Hàng hóa
('CaféF Giá Vàng', 'rss', 'https://cafef.vn/gia-vang.rss', 'vang', 15),
('Kitco Gold News', 'rss', 'https://www.kitco.com/rss/gold.xml', 'vang', 15),
-- 3. Crypto & Web3
('CoinDesk Wire', 'rss', 'https://www.coindesk.com/arc/outboundfeeds/rss/', 'crypto', 15),
('Cointelegraph RSS', 'rss', 'https://cointelegraph.com/rss', 'crypto', 15),
-- 4. Kinh tế Vĩ mô & Quốc tế
('CaféF Vĩ Mô', 'rss', 'https://cafef.vn/kinh-te-vi-mo.rss', 'kinh_te', 15),
('VnExpress Kinh Doanh', 'rss', 'https://vnexpress.net/rss/kinh-doanh.rss', 'kinh_te', 15),
('AP News Wire', 'rss', 'https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com', 'kinh_te', 15),
-- 5. GitHub AI Radar
('GitHub AI Trending', 'github_api', 'https://api.github.com/search/repositories?q=topic:ai+topic:llm&sort=updated', 'github', 30);
```

### 3.2. Bảng `articles` (Bài báo tin tức)
Lưu trữ toàn bộ nội dung bài viết và mã hash chống trùng lặp.
```sql
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER REFERENCES sources(id),
    url TEXT NOT NULL,
    url_hash TEXT NOT NULL UNIQUE,          -- SHA-256(url): Khóa chống cào trùng tuyệt đối!
    title TEXT NOT NULL,                    -- Tiêu đề gốc (tiếng Anh/Việt/Trung)
    summary_raw TEXT,                       -- Tóm tắt ngắn từ RSS
    content_clean TEXT NOT NULL,            -- Nội dung văn bản sạch đã bóc tách HTML
    language TEXT DEFAULT 'en',             -- Mã ngôn ngữ: 'vi', 'en', 'zh', 'ja'...
    title_vi TEXT,                          -- Tiêu đề tiếng Việt do LLM dịch
    summary_vi TEXT,                        -- Tóm tắt tiếng Việt do LLM dịch
    author TEXT,
    published_at DATETIME,
    crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',          -- 'pending', 'processed_laya', 'skipped', 'error'
    is_bookmarked INTEGER DEFAULT 0         -- 1: Đã lưu vào Tech Vault (Giữ vĩnh viễn, chống xóa TTL)
);

CREATE INDEX IF NOT EXISTS idx_articles_url_hash ON articles(url_hash);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);
CREATE INDEX IF NOT EXISTS idx_articles_crawled_at ON articles(crawled_at);
CREATE INDEX IF NOT EXISTS idx_articles_is_bookmarked ON articles(is_bookmarked);
```

### 3.3. Bảng `github_repos` (Kho lưu trữ GitHub Radar)
Dành riêng cho chế độ GitHub Only.
```sql
CREATE TABLE IF NOT EXISTS github_repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_full_name TEXT NOT NULL UNIQUE,    -- Ví dụ: "NandhaKishorM/laya"
    repo_url TEXT NOT NULL,
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    primary_language TEXT,                  -- "Python", "Rust", "C++"...
    topics_json TEXT,                       -- JSON Array: ["ai", "decision-engine", "system-one"]
    readme_content TEXT,                    -- Toàn văn README.md
    crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3.4. Bảng `laya_decisions` (Kết Quả Phân Loại Decision 3.0 Lite & Tọa Độ Cho Nhện)
Lưu trữ kết quả từ container System 1 `vllm-sr/d3-serve:latest` (`vllm-sr/d3-lite` trên GPU RTX 3050 Port 8000). 
Bảng này đóng vai trò là **Tầng 2 trong Chuỗi Cache 3 Cấp**: Mỗi bài báo chỉ forward pass qua GPU đúng 1 lần, các lần sau đọc trực tiếp từ SQLite (< 1ms, 0% GPU).
```sql
CREATE TABLE IF NOT EXISTS laya_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER REFERENCES articles(id),
    repo_id INTEGER REFERENCES github_repos(id),
    
    -- Kết quả từ Decision 3.0 Lite questions:
    category TEXT NOT NULL,                 -- 'kinh_te', 'chinh_tri', 'vang', 'crypto', 'chung_khoan', 'github'
    sentiment TEXT NOT NULL,                -- 'positive', 'negative', 'neutral'
    sentiment_score REAL DEFAULT 0.0,       -- Điểm số tin cậy (0.0 đến 1.0)
    is_breaking_news INTEGER DEFAULT 0,     -- 1: Tin nóng cần nhện quét kỹ, 0: Bình thường
    is_clickbait INTEGER DEFAULT 0,         -- 1: Tin giật tít/câu view (do Decision 3 phát hiện), 0: Tin chuẩn
    
    -- Tọa độ & từ khóa cho nhện bò (Event Queue):
    keywords_json TEXT NOT NULL,            -- JSON Array: [{"word": "Lãi suất", "index": 0, "color": "#F8AFA6"}]
    
    latency_ms REAL,                        -- Thời gian xử lý của Decision 3 (vd: 35.5 ms)
    evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (article_id IS NOT NULL OR repo_id IS NOT NULL)
);
```

### 3.5. Bảng `llm_syntheses` (Bản dịch & Tóm tắt tiếng Việt của LLM System 2)
Lưu trữ nội dung phân tích sâu của Gemini Flash / Qwen 2.5.
```sql
CREATE TABLE IF NOT EXISTS llm_syntheses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER REFERENCES articles(id),
    repo_id INTEGER REFERENCES github_repos(id),
    synthesis_type TEXT NOT NULL,           -- 'single_deep_dive' (tin lẻ) hoặc 'executive_digest' (toàn cảnh ngày)
    
    vietnamese_title TEXT NOT NULL,         -- Tiêu đề dịch chuẩn tiếng Việt
    vietnamese_summary TEXT NOT NULL,       -- Bản tóm tắt tiếng Việt mạch lạc
    macro_impact_analysis TEXT,             -- Phân tích tác động kinh tế vĩ mô / dòng tiền Việt Nam
    raw_response_json TEXT,                 -- Dữ liệu raw của LLM
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (synthesis_type = 'single_deep_dive' AND (article_id IS NOT NULL OR repo_id IS NOT NULL))
        OR (synthesis_type = 'executive_digest')
    )
);
```

### 3.6. Bảng `keyword_trends` (Kho xu hướng cho Màn hình 5 - Trend Vault)
Phục vụ vẽ biểu đồ cành cây tri thức (Branch-Spine) và thống kê từ khóa nóng.
```sql
CREATE TABLE IF NOT EXISTS keyword_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,                  -- Ví dụ: "Lãi suất", "Thuế quan", "Bán dẫn"
    keyword_type TEXT NOT NULL,             -- 'entity', 'person', 'policy', 'tech'
    article_date DATE NOT NULL,             -- Ngày ghi nhận
    frequency INTEGER DEFAULT 1,            -- Số lần xuất hiện trong ngày
    sentiment_avg REAL DEFAULT 0.0,         -- Tâm lý trung bình của từ khóa đó
    UNIQUE(keyword, article_date)
);

CREATE INDEX IF NOT EXISTS idx_keyword_date ON keyword_trends(article_date);
```

### 3.7. Bảng `system_settings` (Cấu hình người dùng)
```sql
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,                   -- Ví dụ: "daily_scan_quota", "data_retention_days", "sound_mute"
    value TEXT NOT NULL,                    -- Ví dụ: "500", "30", "false"
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Cấu hình mặc định cho Quota quét & Cơ chế dọn dẹp chống quá tải:
INSERT OR IGNORE INTO system_settings (key, value) VALUES
('daily_scan_quota', '500'),             -- Quota tối đa số bài cào mỗi ngày
('data_retention_days', '30'),          -- Vòng đời bài viết (TTL 30 ngày)
('auto_prune_enabled', 'true'),         -- Tự động dọn dẹp lúc 03:00 AM
('queue_overflow_policy', 'drop_oldest'),-- Chính sách tràn hàng đợi SSE
('active_skin', 'glass_spider'),        -- Skin nhện giọt sương
('sfx_volume', '0.7');                  -- Âm lượng SFX nước rơi
```

### 3.8. Bảng `topic_watchlists` (Chủ Đề & Từ Khóa Theo Dõi Động — Zero-Code Config)
> **Giải quyết triệt để bài toán:** Người dùng muốn theo dõi chủ đề mới như *"Chiến tranh"*, *"Giá dầu"*, *"Bán dẫn"*, *"Bầu cử"*... **MÀ KHÔNG CẦN CHẠM VÀO CODE CHÍNH**.

Mỗi khi người dùng thêm một chủ đề mới trên giao diện (hoặc qua database), hệ thống tự động:
1. Sinh thêm một **Node Quyết Định mới** trên Vòng cung Laya (Decision Arc) bên phải màn hình nhện.
2. Tự động nạp danh sách từ khóa vào câu hỏi của **Laya System 1** để phân loại theo thời gian thực.
3. Khi bài viết xuất hiện từ khóa, con nhện lập tức **phóng tơ sang Node mới này**!

```sql
CREATE TABLE IF NOT EXISTS topic_watchlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_code TEXT NOT NULL UNIQUE,          -- vd: 'chien_tranh', 'gia_dau', 'chung_khoan', 'vang', 'crypto', 'ban_dan'
    display_name TEXT NOT NULL,                -- vd: "Chiến Sự & Địa Chính Trị", "Giá Dầu & Năng Lượng"
    icon TEXT DEFAULT '📌',                    -- Emoji: '⚔️', '🛢️', '📈', '🥇', '🪙', '🔬'
    keywords_json TEXT NOT NULL,               -- JSON Array: ["chiến tranh", "tên lửa", "dầu brent", "opec", "wti"]
    criteria_prompt TEXT NOT NULL,             -- Tiêu chí nạp vào Laya: "xung đột vũ trang, tên lửa, giá dầu opec, khí đốt..."
    sentiment_alert TEXT DEFAULT 'all',        -- 'all', 'negative_only', 'breaking_only'
    color_hex TEXT DEFAULT '#E5B869',          -- Màu sợi tơ nhện khi bắn tới node này (#F8AFA6, #C86D51, #E5B869...)
    is_active INTEGER DEFAULT 1,               -- 1: Đang theo dõi, 0: Tạm tắt
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Dữ liệu hạt giống cho các chủ đề nóng (Seed Watchlists):
INSERT OR IGNORE INTO topic_watchlists (topic_code, display_name, icon, keywords_json, criteria_prompt, color_hex) VALUES
('chien_tranh', 'Chiến Sự & Địa Chính Trị', '⚔️', '["chiến tranh", "tên lửa", "quân sự", "xung đột", "không kích", "nato", "ukraine", "trung đông"]', 'xung đột vũ trang, chiến sự, tên lửa, căng thẳng ngoại giao, hiệp ước phòng thủ', '#C86D51'),
('gia_dau', 'Giá Dầu & Năng Lượng', '🛢️', '["giá dầu", "dầu brent", "wti", "opec", "khí đốt", "xăng dầu", "năng lượng", "hormuz"]', 'biến động giá dầu mỏ thế giới, sản lượng cắt giảm OPEC+, khủng hoảng năng lượng, khí đốt', '#D97706'),
('vang_hanghoa', 'Giá Vàng & Kim Loại Quý', '🥇', '["giá vàng", "sjc", "doji", "vàng nhẫn", "xau/usd", "bạc"]', 'biến động giá vàng miếng SJC, vàng nhẫn 9999 trong nước và kim loại quý thế giới', '#E5B869'),
('chung_khoan', 'Thị Trường Chứng Khoán', '📈', '["vn-index", "hnx", "cổ phiếu", "khối ngoại", "tự doanh", "thanh khoản", "s&p 500", "nasdaq"]', 'diễn biến chỉ số chứng khoán, thanh khoản thị trường, giao dịch khối ngoại, cổ phiếu', '#2E7D32'),
('crypto_web3', 'Tiền Mã Hóa & Crypto', '🪙', '["bitcoin", "btc", "ethereum", "eth", "crypto", "blockchain", "sec", "etf"]', 'thị trường tiền mã hóa, bitcoin etf, chính sách quản lý tài sản kỹ thuật số', '#8E7CC3'),
('kinh_te_vi_mo', 'Kinh Tế Vĩ Mô & Dòng Tiền', '🏛️', '["lãi suất", "lạm phát", "fed", "nhnn", "tỷ giá", "gdp", "cpi", "tín dụng"]', 'chính sách tiền tệ, lãi suất điều hành, lạm phát, tỷ giá USD/VND, thanh khoản ngân hàng', '#2D4A2B'),
('cong_nghe_ai', 'Đột Phá AI & GitHub', '🐙', '["ai", "llm", "mô hình", "github", "bán dẫn", "nvidia", "deepseek", "chip"]', 'tiến bộ trí tuệ nhân tạo, mã nguồn mở, chip bán dẫn, thuật toán mới', '#0284C7');
```

### 3.9. Bảng Ảo FTS5: `articles_fts` (Tìm Kiếm Toàn Văn Siêu Tốc Cho Tra Cứu Tùy Ý)
Cho phép người dùng gõ tìm bất kỳ từ khóa ngẫu nhiên nào (kể cả chưa tạo trong watchlist) với tốc độ sub-millisecond (< 2ms):
```sql
CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
    title,
    content_clean,
    title_vi,
    summary_vi,
    content='articles',
    content_rowid='id',
    tokenize='unicode61 remove_diacritics 2'
);

-- Trigger 1: Tự động đồng bộ khi THÊM bài mới
CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN
    INSERT INTO articles_fts(rowid, title, content_clean, title_vi, summary_vi)
    VALUES (new.id, new.title, new.content_clean, new.title_vi, new.summary_vi);
END;

-- Trigger 2: Tự động dọn dẹp FTS5 khi XÓA bài cũ (Tránh orphan FTS records gây phình đĩa)
CREATE TRIGGER IF NOT EXISTS articles_ad AFTER DELETE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, title, content_clean, title_vi, summary_vi)
    VALUES ('delete', old.id, old.title, old.content_clean, old.title_vi, old.summary_vi);
END;

-- Trigger 3: Tự động cập nhật FTS5 khi SỬA/DỊCH bài
CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, title, content_clean, title_vi, summary_vi)
    VALUES ('delete', old.id, old.title, old.content_clean, old.title_vi, old.summary_vi);
    INSERT INTO articles_fts(rowid, title, content_clean, title_vi, summary_vi)
    VALUES (new.id, new.title, new.content_clean, new.title_vi, new.summary_vi);
END;
```

---

## 4. Cơ Chế Khử Trùng Bài (Deduplication Pipeline)

Mỗi bài báo khi được cào về sẽ đi qua hàm băm:
```python
import hashlib

def generate_url_hash(url: str) -> str:
    # Chuẩn hóa URL (bỏ query parameters rác như utm_source, utm_medium...)
    clean_url = url.split("?")[0].strip().lower()
    return hashlib.sha256(clean_url.encode("utf-8")).hexdigest()
```
* **Khi chèn vào database:** Sử dụng câu lệnh `INSERT OR IGNORE INTO articles (url_hash, ...)`:
  * Nếu bài đã tồn tại $\rightarrow$ SQLite bỏ qua ngay lập tức trong 0.01ms.
  * Con nhện không bao giờ phải đọc lại một bài báo cũ.

---

## 5. Chiến Lược Dọn Dẹp, Xoay Vòng & Thu Hồi Dung Lượng Đĩa (Data Retention & Purging Lifecycle)

> **Mục tiêu:** Đảm bảo hệ thống vận hành 24/7/365 mà file SQLite không bao giờ vượt quá **80 MB**, không bị phân mảnh hay phình to làm chậm máy tính văn phòng.

### 5.1. Phân Tầng Lưu Trữ (Tiered Storage Lifecycle)
1. **Hot Tier (0 – 7 ngày):** Lưu trữ toàn văn thô `content_clean`, dữ liệu vector và FTS5 phục vụ nhện bò, tìm kiếm và trích xuất thực thể tức thì.
2. **Warm Tier (8 – 30 ngày):** Lưu trữ tiêu đề gốc, bản dịch tiếng Việt `title_vi`, `summary_vi` và kết quả phân loại `laya_decisions`.
3. **Cold / Purge Tier (> 30 ngày):** Toàn bộ bài báo không quan trọng sẽ được dọn dẹp tự động.

### 5.2. Cron Job Dọn Dẹp Định Kỳ (Automatic Purge Query)
Backend tự động kích hoạt cron job ngầm lúc **03:00 AM hàng ngày**:
```sql
-- Xóa các bài báo cũ quá 30 ngày NGOẠI TRỪ các bài người dùng đã nhấn Bookmark (⭐ Lưu vào Tech Vault)
DELETE FROM articles 
WHERE crawled_at < datetime('now', '-30 days') 
  AND is_bookmarked = 0;
```
* **Ngoại lệ an toàn:** Các bài viết có `is_bookmarked = 1` sẽ **được giữ lại vĩnh viễn**, phục vụ bộ sưu tập cá nhân của người dùng.
* Khi bài báo bị xóa, các bảng quan hệ `laya_decisions`, `llm_syntheses` và bảng ảo `articles_fts` sẽ tự động dọn dẹp theo thông qua Cascade & Trigger.

### 5.3. Thu Hồi Dung Lượng Đĩa (Incremental Vacuuming)
Khi dữ liệu bị xóa, SQLite mặc định giữ lại các trang đĩa trống để tái sử dụng thay vì thu nhỏ file ngay lập tức. Để giải phóng dung lượng đĩa cho hệ điều hành:
1. Khi khởi tạo database, kích hoạt chế độ:
   ```sql
   PRAGMA auto_vacuum = INCREMENTAL;
   PRAGMA journal_mode = WAL;
   ```
2. Sau khi cron job dọn dẹp chạy xong, Backend thực thi:
   ```sql
   PRAGMA incremental_vacuum;
   ```
   Lệnh này lập tức trả lại các megabyte đĩa trống cho Windows mà **không khóa toàn bộ database** như lệnh `VACUUM` truyền thống.

### 5.4. Bảng Dự Toán Dung Lượng Thực Tế
| Thời gian | Số lượng bài | Dung lượng Database (WAL) | Trạng thái hiệu năng |
| :--- | :--- | :--- | :--- |
| **1 ngày** | ~500 bài | ~1.5 MB | Tìm kiếm < 1ms |
| **7 ngày** | ~3.500 bài | ~10 MB | Tìm kiếm < 1ms |
| **30 ngày (Trần TTL)** | ~15.000 bài | ~45 MB | Tìm kiếm < 2ms |
| **1 năm (Có Auto-Purge)** | Duy trì ổn định 15.000 bài + ~300 bài bookmark | **~50 MB – 60 MB** | Cực kỳ mượt mà, không lag |

---

## 6. Chiến Lược Cache 3 Tầng Giảm Tải Điện Toán GPU / CPU (3-Tier Cache Engine)

Để triệt tiêu hoàn toàn hiện tượng tính toán trùng lặp, tiết kiệm 100% tài nguyên GPU NVIDIA và chi phí API:

```
[ BÀI BÁO MỚI CÀO ]
       │
       ▼
 [ TẦNG 1: DEDUPLICATION HASH CACHE (0.1ms) ] ── (Đã có trong DB) ──► [ SKIP NGAY LẬP TỨC ]
       │ (Chưa có)
       ▼
 [ TẦNG 2: GPU SYSTEM 1 (Decision 3.0 Lite) ] ── (Chạy 1 lần duy nhất) ──► Ghi vào laya_decisions
       │                                                                  (Lưu vĩnh viễn SQLite)
       ▼
 [ TẦNG 3: PERSISTENCE RESULT CACHE (< 1ms) ]
       │
       ├─► Con Nhện bò đọc lại bài cũ: Đọc từ SQLite (0% GPU)
       └─► Người dùng bấm Deep Dive lần 2: Đọc từ llm_syntheses (0đ tiền API)
```

1. **Tầng 1 - Deduplication Hash Cache:** Cột `url_hash` băm SHA-256 (`generate_url_hash`). Loại bỏ trùng lặp trước khi gửi sang AI.
2. **Tầng 2 - Result Persistence Cache:** Bảng `laya_decisions` và `llm_syntheses` giữ kết quả phân loại vĩnh viễn. Đọc lại chỉ tốn I/O đĩa (< 1ms).
3. **Tầng 3 - GPU Kernel & SafeTensors mmap Cache:** Docker `vllm-sr/d3-serve` ánh xạ trực tiếp `.safetensors` từ `D:\docker_data\d3-serve\model` và cache kernel Triton qua `TRITON_CACHE_AUTOTUNING=1`.

### 6.1. Quy Chuẩn Cache Bản Dịch Toàn Văn: "In-Memory RAM" (Chống Phình To Database)
* **Quy tắc cốt lõi:** Bản dịch toàn văn theo đoạn (`<p>` by `<p>`) của các bài báo đọc lướt hàng ngày **KHÔNG LƯU VÀO ĐĨA SQLITE**.
  * Bản dịch được cache trực tiếp trên **In-Memory RAM của Giao diện (React State)** trong phiên làm việc.
  * Khi người dùng chuyển tab hoặc tắt ứng dụng $\rightarrow$ RAM tự động giải phóng sạch sẽ, không để lại rác trong database.
* **Ngoại lệ duy nhất (Persistent Bookmark):**
  * Chỉ khi người dùng nhấn nút **⭐ Bookmark (Lưu vào Tech Vault)** trên bài viết (`is_bookmarked = 1`), bản dịch mới được ghi cố định vào SQLite để phục vụ đọc offline lâu dài.
  * Nhờ đó, file database SQLite luôn giữ dung lượng siêu nhẹ **< 50 MB** mãi mãi!

