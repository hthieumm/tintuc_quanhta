"""
Tests for Database Schema, WAL mode, and CHECK Constraints.
Ensures zero orphan rows and strict validation in SQLite.
"""

import os
import sqlite3
import tempfile
import pytest
from backend.database import init_db_sync, generate_url_hash, DDL_STATEMENTS

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db_sync(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_tables_created(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    expected_tables = {
        "sources", "articles", "github_repos",
        "laya_decisions", "llm_syntheses", "keyword_trends", "system_settings",
        "topic_watchlists", "articles_fts"
    }
    assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"


def test_orphan_check_llm_syntheses_single_deep_dive(temp_db):
    """
    Ràng buộc: single_deep_dive bắt buộc phải có article_id hoặc repo_id.
    Nếu cả hai đều là NULL, SQLite phải raise IntegrityError.
    """
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO llm_syntheses (
                article_id, repo_id, synthesis_type, vietnamese_title, vietnamese_summary
            ) VALUES (
                NULL, NULL, 'single_deep_dive', 'Tiêu đề thử nghiệm', 'Tóm tắt thử nghiệm'
            );
        """)
        conn.commit()
    conn.close()


def test_llm_syntheses_executive_digest_allows_null_ids(temp_db):
    """
    Ràng buộc: executive_digest tổng hợp toàn bộ bài trong ngày,
    nên cho phép article_id và repo_id là NULL.
    """
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO llm_syntheses (
            article_id, repo_id, synthesis_type, vietnamese_title, vietnamese_summary
        ) VALUES (
            NULL, NULL, 'executive_digest', 'Toàn cảnh vĩ mô', 'Bản tin ngày hôm nay'
        );
    """)
    conn.commit()
    cursor.execute("SELECT id, synthesis_type FROM llm_syntheses WHERE synthesis_type = 'executive_digest';")
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == 'executive_digest'
    conn.close()


def test_orphan_check_laya_decisions(temp_db):
    """
    Ràng buộc: laya_decisions bắt buộc phải gắn với article_id hoặc repo_id.
    """
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO laya_decisions (
                article_id, repo_id, category, sentiment, keywords_json
            ) VALUES (
                NULL, NULL, 'kinh_te', 'positive', '[]'
            );
        """)
        conn.commit()
    conn.close()


def test_article_url_hash_uniqueness(temp_db):
    """
    Khử trùng lặp: url_hash bắt buộc UNIQUE.
    """
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    
    url = "https://cafef.vn/tin-tuc-vi-mo-hom-nay.chn?utm_source=facebook"
    url_hash = generate_url_hash(url)
    
    cursor.execute("""
        INSERT INTO articles (url, url_hash, title, content_clean)
        VALUES (?, ?, 'Bài viết 1', 'Nội dung bài viết 1');
    """, (url, url_hash))
    conn.commit()

    # Thử insert lại cùng url_hash
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO articles (url, url_hash, title, content_clean)
            VALUES (?, ?, 'Bài viết trùng lặp', 'Nội dung bài viết trùng');
        """, (url, url_hash))
        conn.commit()
    conn.close()


def test_dynamic_topic_watchlist_and_fts(temp_db):
    """
    Kiểm tra tính linh động: Người dùng có thể tự thêm chủ đề (vd: Chiến tranh, Giá dầu)
    và tìm kiếm toàn văn FTS5 mà KHÔNG CẦN sửa một dòng code nào.
    """
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # 1. Kiểm tra các seed chủ đề mặc định đã được nạp sẵn (vd: gia_dau, chien_tranh)
    cursor.execute("SELECT topic_code FROM topic_watchlists WHERE topic_code='gia_dau';")
    assert cursor.fetchone() is not None

    # 2. Thêm một chủ đề hoàn toàn mới do người dùng tự định nghĩa (vd: Năng Lượng Hạt Nhân)
    cursor.execute("""
        INSERT INTO topic_watchlists (topic_code, display_name, icon, keywords_json, criteria_prompt, color_hex)
        VALUES ('nang_luong_hat_nhan', 'Năng Lượng Hạt Nhân & Uranium', '☢️', '["uranium", "hạt nhân", "sMR"]', 'công nghệ lò phản ứng hạt nhân', '#A855F7');
    """)
    conn.commit()

    cursor.execute("SELECT topic_code, display_name FROM topic_watchlists WHERE topic_code='nang_luong_hat_nhan';")
    topic = cursor.fetchone()
    assert topic is not None
    assert topic[0] == 'nang_luong_hat_nhan'

    # 3. Thêm bài viết về giá dầu
    cursor.execute("""
        INSERT INTO articles (url, url_hash, title, content_clean)
        VALUES ('https://news.com/oil', 'hash_oil_1', 'Căng thẳng eo biển Hormuz đẩy giá dầu Brent vượt mốc 90 USD', 'OPEC cân nhắc cắt giảm sản lượng khi căng thẳng địa chính trị leo thang.');
    """)
    conn.commit()

    # Đồng bộ FTS5
    cursor.execute("""
        INSERT INTO articles_fts(rowid, title, content_clean)
        SELECT id, title, content_clean FROM articles WHERE url_hash='hash_oil_1';
    """)
    conn.commit()

    # 4. Tra cứu nhanh bằng FTS5 (hỗ trợ cả gõ KHÔNG DẤU nhờ remove_diacritics 2)
    cursor.execute("SELECT rowid, title FROM articles_fts WHERE articles_fts MATCH 'dau brent';")
    search_res = cursor.fetchall()
    assert len(search_res) == 1
    assert "Hormuz" in search_res[0][1]

    conn.close()
