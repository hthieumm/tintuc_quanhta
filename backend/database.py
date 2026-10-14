"""
Database module for Spider News Radar (Tin Tức Quanh Ta).
Uses SQLite in WAL mode with aiosqlite for async non-blocking operations.
"""

import os
import hashlib
import sqlite3
from typing import Optional, List, Dict, Any
import aiosqlite

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "spider_radar.db")

DDL_STATEMENTS = [
    # 1. Bảng sources (Nguồn tin & Cấu hình cào)
    """
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        source_type TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        category TEXT DEFAULT 'kinh_te',
        is_active INTEGER DEFAULT 1,
        fetch_interval_min INTEGER DEFAULT 15,
        last_fetched_at DATETIME
    );
    """,

    # 2. Bảng articles (Bài báo tin tức)
    """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER REFERENCES sources(id),
        url TEXT NOT NULL,
        url_hash TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        summary_raw TEXT,
        content_clean TEXT NOT NULL,
        language TEXT DEFAULT 'en',
        title_vi TEXT,
        summary_vi TEXT,
        author TEXT,
        published_at DATETIME,
        crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending',
        is_bookmarked INTEGER DEFAULT 0
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_articles_url_hash ON articles(url_hash);",
    "CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);",

    # 3. Bảng github_repos (Kho lưu trữ GitHub Radar)
    """
    CREATE TABLE IF NOT EXISTS github_repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_full_name TEXT NOT NULL UNIQUE,
        repo_url TEXT NOT NULL,
        stars INTEGER DEFAULT 0,
        forks INTEGER DEFAULT 0,
        primary_language TEXT,
        topics_json TEXT,
        readme_content TEXT,
        ai_explanation_json TEXT,
        crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 4. Bảng laya_decisions (Kết quả phân loại System 1 & Dữ liệu cho Nhện)
    """
    CREATE TABLE IF NOT EXISTS laya_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER REFERENCES articles(id),
        repo_id INTEGER REFERENCES github_repos(id),
        category TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        sentiment_score REAL DEFAULT 0.0,
        is_breaking_news INTEGER DEFAULT 0,
        keywords_json TEXT NOT NULL,
        latency_ms REAL,
        evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        CHECK (article_id IS NOT NULL OR repo_id IS NOT NULL)
    );
    """,

    # 5. Bảng llm_syntheses (Bản dịch & Tóm tắt tiếng Việt của LLM System 2)
    """
    CREATE TABLE IF NOT EXISTS llm_syntheses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER REFERENCES articles(id),
        repo_id INTEGER REFERENCES github_repos(id),
        synthesis_type TEXT NOT NULL,
        vietnamese_title TEXT NOT NULL,
        vietnamese_summary TEXT NOT NULL,
        macro_impact_analysis TEXT,
        raw_response_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        CHECK (
            (synthesis_type = 'single_deep_dive' AND (article_id IS NOT NULL OR repo_id IS NOT NULL))
            OR (synthesis_type = 'executive_digest')
        )
    );
    """,

    # 6. Bảng keyword_trends (Kho xu hướng cho Màn hình 4 - Trend Vault)
    """
    CREATE TABLE IF NOT EXISTS keyword_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        keyword_type TEXT NOT NULL,
        article_date DATE NOT NULL,
        frequency INTEGER DEFAULT 1,
        sentiment_avg REAL DEFAULT 0.0,
        UNIQUE(keyword, article_date)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_keyword_date ON keyword_trends(article_date);",

    # 7. Bảng system_settings (Cấu hình người dùng)
    """
    CREATE TABLE IF NOT EXISTS system_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 8. Bảng topic_watchlists (Chủ đề theo dõi & Từ khóa tra cứu động)
    """
    CREATE TABLE IF NOT EXISTS topic_watchlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_code TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL,
        icon TEXT DEFAULT '📌',
        keywords_json TEXT NOT NULL,
        criteria_prompt TEXT NOT NULL,
        sentiment_alert TEXT DEFAULT 'all',
        color_hex TEXT DEFAULT '#E5B869',
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 9. Bảng ảo FTS5 articles_fts (Tìm kiếm toàn văn siêu tốc không dấu & có dấu)
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
        title,
        content_clean,
        content='articles',
        content_rowid='id',
        tokenize='unicode61 remove_diacritics 2'
    );
    """
]

DEFAULT_SEED_STATEMENTS = [
    # Nguồn tin hạt giống mặc định
    """
    INSERT OR IGNORE INTO sources (name, source_type, url, category, fetch_interval_min) VALUES
    -- 1. Nguồn Quốc Tế Hàng Đầu (Top International Newspapers & Wires)
    ('The Guardian International', 'rss', 'https://www.theguardian.com/international/rss', 'quoc_te', 15),
    ('Reuters Wire', 'rss', 'https://news.google.com/rss/search?q=when:24h+site:reuters.com&hl=en-US&gl=US&ceid=US:en', 'quoc_te', 15),
    ('BBC News World', 'rss', 'https://feeds.bbci.co.uk/news/world/rss.xml', 'quoc_te', 15),
    ('AP News Wire', 'rss', 'https://news.google.com/rss/search?q=when:24h+site:apnews.com&hl=en-US&gl=US&ceid=US:en', 'quoc_te', 15),
    ('Financial Times World', 'rss', 'https://www.ft.com/world?format=rss', 'kinh_te', 20),
    ('The Wall Street Journal', 'rss', 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml', 'chung_khoan', 15),
    ('Bloomberg Markets Wire', 'rss', 'https://news.google.com/rss/search?q=when:24h+site:bloomberg.com&hl=en-US&gl=US&ceid=US:en', 'kinh_te', 15),
    ('The Economist', 'rss', 'https://www.economist.com/finance-and-economics/rss.xml', 'kinh_te', 30),
    ('The New York Times World', 'rss', 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'quoc_te', 20),
    ('The Washington Post World', 'rss', 'https://feeds.washingtonpost.com/rss/world', 'quoc_te', 20),
    ('Politico Politics', 'rss', 'https://rss.politico.com/politics-news.xml', 'chinh_tri', 15),
    -- 2. Nguồn Trong Nước & Chuyên Biệt
    ('CaféF Chứng Khoán', 'rss', 'https://cafef.vn/thi-truong-chung-khoan.rss', 'chung_khoan', 10),
    ('CaféF Tài Chính Quốc Tế', 'rss', 'https://cafef.vn/tai-chinh-quoc-te.rss', 'kinh_te', 10),
    ('Tuổi Trẻ Kinh Doanh', 'rss', 'https://tuoitre.vn/rss/kinh-doanh.rss', 'kinh_te', 10),
    ('Tuổi Trẻ Thế Giới', 'rss', 'https://tuoitre.vn/rss/the-gioi.rss', 'quoc_te', 10),
    ('VnExpress Kinh Doanh', 'rss', 'https://vnexpress.net/rss/kinh-doanh.rss', 'kinh_te', 15),
    ('Vietstock Tin Nhanh', 'rss', 'https://vietstock.vn/rss/chung-khoan.rss', 'chung_khoan', 10),
    ('Kitco Gold News', 'rss', 'https://www.kitco.com/rss/gold.xml', 'vang', 15),
    ('CoinDesk Wire', 'rss', 'https://www.coindesk.com/arc/outboundfeeds/rss/', 'crypto', 15),
    ('Cointelegraph RSS', 'rss', 'https://cointelegraph.com/rss', 'crypto', 15),
    ('GitHub AI Trending', 'github_api', 'https://api.github.com/search/repositories?q=topic:ai+topic:llm&sort=updated', 'github', 30);
    """,

    # Chủ đề theo dõi động mặc định (Watchlists)
    """
    INSERT OR IGNORE INTO topic_watchlists (topic_code, display_name, icon, keywords_json, criteria_prompt, color_hex) VALUES
    ('chien_tranh', 'Chiến Sự & Địa Chính Trị', '⚔️', '["chiến tranh", "tên lửa", "quân sự", "xung đột", "không kích", "nato", "ukraine", "trung đông"]', 'xung đột vũ trang, chiến sự, tên lửa, căng thẳng ngoại giao, hiệp ước phòng thủ', '#C86D51'),
    ('gia_dau', 'Giá Dầu & Năng Lượng', '🛢️', '["giá dầu", "dầu brent", "wti", "opec", "khí đốt", "xăng dầu", "năng lượng", "hormuz"]', 'biến động giá dầu mỏ thế giới, sản lượng cắt giảm OPEC+, khủng hoảng năng lượng, khí đốt', '#D97706'),
    ('vang_hanghoa', 'Giá Vàng & Kim Loại Quý', '🥇', '["giá vàng", "sjc", "doji", "vàng nhẫn", "xau/usd", "bạc"]', 'biến động giá vàng miếng SJC, vàng nhẫn 9999 trong nước và kim loại quý thế giới', '#E5B869'),
    ('chung_khoan', 'Thị Trường Chứng Khoán', '📈', '["vn-index", "hnx", "cổ phiếu", "khối ngoại", "tự doanh", "thanh khoản", "s&p 500", "nasdaq"]', 'diễn biến chỉ số chứng khoán, thanh khoản thị trường, giao dịch khối ngoại, cổ phiếu', '#2E7D32'),
    ('crypto_web3', 'Tiền Mã Hóa & Crypto', '🪙', '["bitcoin", "btc", "ethereum", "eth", "crypto", "blockchain", "sec", "etf"]', 'thị trường tiền mã hóa, bitcoin etf, chính sách quản lý tài sản kỹ thuật số', '#8E7CC3'),
    ('kinh_te_vi_mo', 'Kinh Tế Vĩ Mô & Dòng Tiền', '🏛️', '["lãi suất", "lạm phát", "fed", "nhnn", "tỷ giá", "gdp", "cpi", "tín dụng"]', 'chính sách tiền tệ, lãi suất điều hành, lạm phát, tỷ giá USD/VND, thanh khoản ngân hàng', '#2D4A2B'),
    ('cong_nghe_ai', 'Đột Phá AI & GitHub', '🐙', '["ai", "llm", "mô hình", "github", "bán dẫn", "nvidia", "deepseek", "chip"]', 'tiến bộ trí tuệ nhân tạo, mã nguồn mở, chip bán dẫn, thuật toán mới', '#0284C7');
    """
]


def generate_url_hash(url: str) -> str:
    """Chuẩn hóa URL và tạo mã băm SHA-256 chống trùng lặp tuyệt đối."""
    clean_url = url.split("?")[0].strip().lower()
    return hashlib.sha256(clean_url.encode("utf-8")).hexdigest()


def init_db_sync(db_path: str = DEFAULT_DB_PATH) -> None:
    """Khởi tạo cơ sở dữ liệu đồng bộ (dùng cho migration, tests, startup script)."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30.0)
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=30000;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        for statement in DDL_STATEMENTS:
            cursor.execute(statement)
        for seed in DEFAULT_SEED_STATEMENTS:
            cursor.execute(seed)
        
        # Safe column migrations
        cursor.execute("PRAGMA table_info(articles)")
        art_cols = [r[1] for r in cursor.fetchall()]
        if "is_bookmarked" not in art_cols:
            cursor.execute("ALTER TABLE articles ADD COLUMN is_bookmarked INTEGER DEFAULT 0")

        cursor.execute("PRAGMA table_info(github_repos)")
        repo_cols = [r[1] for r in cursor.fetchall()]
        if "is_bookmarked" not in repo_cols:
            cursor.execute("ALTER TABLE github_repos ADD COLUMN is_bookmarked INTEGER DEFAULT 0")
        if "ai_explanation_json" not in repo_cols:
            cursor.execute("ALTER TABLE github_repos ADD COLUMN ai_explanation_json TEXT")

        conn.commit()
    finally:
        conn.close()


async def init_db_async(db_path: str = DEFAULT_DB_PATH) -> None:
    """Khởi tạo cơ sở dữ liệu bất đồng bộ với aiosqlite."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    async with aiosqlite.connect(db_path, timeout=30.0) as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA busy_timeout=30000;")
        await db.execute("PRAGMA foreign_keys=ON;")
        for statement in DDL_STATEMENTS:
            await db.execute(statement)
        for seed in DEFAULT_SEED_STATEMENTS:
            await db.execute(seed)

        # Safe column migrations
        async with db.execute("PRAGMA table_info(articles)") as cur:
            art_cols = [r[1] for r in await cur.fetchall()]
        if "is_bookmarked" not in art_cols:
            await db.execute("ALTER TABLE articles ADD COLUMN is_bookmarked INTEGER DEFAULT 0")

        async with db.execute("PRAGMA table_info(github_repos)") as cur:
            repo_cols = [r[1] for r in await cur.fetchall()]
        if "is_bookmarked" not in repo_cols:
            await db.execute("ALTER TABLE github_repos ADD COLUMN is_bookmarked INTEGER DEFAULT 0")
        if "ai_explanation_json" not in repo_cols:
            await db.execute("ALTER TABLE github_repos ADD COLUMN ai_explanation_json TEXT")

        await db.commit()



async def get_db(db_path: str = DEFAULT_DB_PATH) -> aiosqlite.Connection:
    """Lấy connection bất đồng bộ với cấu hình WAL & Foreign Keys."""
    db = await aiosqlite.connect(db_path, timeout=30.0)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys=ON;")
    await db.execute("PRAGMA busy_timeout=30000;")
    return db
