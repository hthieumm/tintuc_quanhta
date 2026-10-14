"""
Test Suite for Spider News Radar Scraper & Deduplication (Gate 4)
Verifies:
1. First crawl of a sample feed inserts N articles.
2. Second crawl of the same feed inserts 0 articles (Deduplication assertion).
3. Language tagging works for Vietnamese, English, and other languages.
4. FTS5 index is synchronized and queryable.
"""

import os
import pytest
import aiosqlite

from backend.database import init_db_sync, generate_url_hash
from backend.rss_crawler import SpiderNewsCrawler, detect_language, clean_html_tags

SAMPLE_RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Sample Global Financial Radar Feed</title>
    <link>https://example.com/finance</link>
    <description>Test feed for Gate 4 deduplication verification</description>
    <item>
      <title>Giá dầu Brent leo dốc mốc 88 USD khi căng thẳng Trung Đông gia tăng</title>
      <link>https://example.com/news/oil-brent-surge?utm_source=feed</link>
      <description>Thị trường năng lượng toàn cầu biến động mạnh sau động thái mới từ OPEC+ và căng thẳng địa chính trị.</description>
      <pubDate>Fri, 10 Oct 2026 01:00:00 +0000</pubDate>
      <author>Vĩ Mô Ban</author>
    </item>
    <item>
      <title>Federal Reserve Signals Possible Rate Pause Amid Stable Inflation</title>
      <link>https://example.com/news/fed-rate-pause-signals?ref=rss</link>
      <description>The Federal Open Market Committee noted that monetary policy remains sufficiently restrictive to curb inflation.</description>
      <pubDate>Fri, 10 Oct 2026 01:05:00 +0000</pubDate>
      <author>Sarah Jenkins</author>
    </item>
    <item>
      <title>Giá vàng miếng SJC và vàng nhẫn 9999 duy trì vùng đỉnh lịch sử</title>
      <link>https://example.com/news/sjc-gold-historic-high</link>
      <description>Nhu cầu tích trữ kim loại quý phòng ngừa rủi ro tỷ giá tiếp tục hỗ trợ thị trường vàng trong nước.</description>
      <pubDate>Fri, 10 Oct 2026 01:10:00 +0000</pubDate>
      <author>Thị Trường Vàng</author>
    </item>
  </channel>
</rss>
"""


@pytest.fixture
def temp_db_path(tmp_path):
    """Tạo database SQLite tạm cho test."""
    db_file = os.path.join(tmp_path, "test_scraper.db")
    init_db_sync(db_file)
    return db_file


@pytest.mark.asyncio
async def test_crawler_deduplication_gate_4(temp_db_path):
    """
    Gate 4 Primary Assertion:
    - Lần 1: Cào feed mẫu -> Đếm số row tăng N (3 rows).
    - Lần 2: Cào lại chính feed đó -> Assert số row tăng thêm bằng 0.
    """
    crawler = SpiderNewsCrawler(db_path=temp_db_path)

    # Đếm số row articles ban đầu
    async with aiosqlite.connect(temp_db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM articles;") as cur:
            initial_count = (await cur.fetchone())[0]
    assert initial_count == 0

    # LẦN 1: Cào feed mẫu
    res_round_1 = await crawler.crawl_feed_string(SAMPLE_RSS_XML)
    assert res_round_1["total_entries"] == 3
    assert res_round_1["inserted"] == 3
    assert res_round_1["duplicates"] == 0

    # Kiểm tra database sau lần 1
    async with aiosqlite.connect(temp_db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM articles;") as cur:
            count_after_round_1 = (await cur.fetchone())[0]
    assert count_after_round_1 == 3, "Lần 1 phải insert đúng 3 bài viết"

    # LẦN 2: Cào lại feed mẫu (DEDUPLICATION ASSERTION)
    res_round_2 = await crawler.crawl_feed_string(SAMPLE_RSS_XML)
    assert res_round_2["total_entries"] == 3
    assert res_round_2["inserted"] == 0, "Lần 2 phải có số row tăng thêm BẰNG 0"
    assert res_round_2["duplicates"] == 3, "Tất cả 3 bài đều phải nhận diện là trùng lặp"

    # Kiểm tra database sau lần 2: Tổng số row vẫn giữ nguyên là 3
    async with aiosqlite.connect(temp_db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM articles;") as cur:
            count_after_round_2 = (await cur.fetchone())[0]
    assert count_after_round_2 == 3, "Tổng số row sau lần 2 không được tăng thêm"


@pytest.mark.asyncio
async def test_crawler_language_detection(temp_db_path):
    """Kiểm tra tagger ngôn ngữ tự động (Tiếng Việt vs Tiếng Anh)."""
    crawler = SpiderNewsCrawler(db_path=temp_db_path)
    await crawler.crawl_feed_string(SAMPLE_RSS_XML)

    async with aiosqlite.connect(temp_db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT title, language FROM articles;") as cur:
            rows = await cur.fetchall()

    for row in rows:
        if "Giá dầu" in row["title"] or "Giá vàng" in row["title"]:
            assert row["language"] == "vi", f"Bài tiếng Việt phải có tag 'vi', nhận được: {row['language']}"
        elif "Federal Reserve" in row["title"]:
            assert row["language"] == "en", f"Bài tiếng Anh phải có tag 'en', nhận được: {row['language']}"


@pytest.mark.asyncio
async def test_crawler_fts5_synchronization(temp_db_path):
    """Kiểm tra bài viết sau khi cào được tự động đưa vào bảng ảo FTS5."""
    crawler = SpiderNewsCrawler(db_path=temp_db_path)
    await crawler.crawl_feed_string(SAMPLE_RSS_XML)

    async with aiosqlite.connect(temp_db_path) as db:
        # Tìm kiếm không dấu FTS5: "gia dau brent" phải khớp bài có dấu
        async with db.execute(
            "SELECT rowid, title FROM articles_fts WHERE articles_fts MATCH 'gia dau brent';"
        ) as cur:
            rows = await cur.fetchall()
            assert len(rows) == 1
            assert "Brent" in rows[0][1]

        # Tìm kiếm tiếng Anh: "federal reserve"
        async with db.execute(
            "SELECT rowid, title FROM articles_fts WHERE articles_fts MATCH 'federal reserve';"
        ) as cur:
            rows = await cur.fetchall()
            assert len(rows) == 1
            assert "Signals" in rows[0][1]


def test_url_hash_clean_parameters():
    """Kiểm tra chuẩn hóa URL loại bỏ query parameter chống trùng lặp tracking (utm, ref)."""
    url1 = "https://cafef.vn/bai-viet-hay.chn?utm_source=fb&utm_medium=cpc"
    url2 = "https://cafef.vn/bai-viet-hay.chn?ref=share"
    url3 = "https://cafef.vn/bai-viet-hay.chn"

    hash1 = generate_url_hash(url1)
    hash2 = generate_url_hash(url2)
    hash3 = generate_url_hash(url3)

    assert hash1 == hash2 == hash3, "Các URL cùng gốc dù khác query params phải có cùng SHA-256 hash"
