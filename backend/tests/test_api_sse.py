"""
Test Suite for Gate 5: SSE Stream & REST API Integration
Verifies:
1. SSE Stream `/api/stream/spider-events` returns `text/event-stream` and proper `data: {...}` format.
2. REST Deep Dive `/api/v1/synthesize/article` returns Vietnamese analysis.
3. REST Executive Digest `/api/v1/synthesize/digest` returns modular intelligence panels.
4. Dynamic Watchlists & Sources endpoints function properly.
"""

import os
import json
import pytest
import asyncio
import httpx
import aiosqlite

from backend.app import app, event_manager, SpiderEvent
from backend.database import init_db_sync, DEFAULT_DB_PATH


@pytest.fixture(autouse=True)
def setup_test_database(tmp_path, monkeypatch):
    """Thiết lập DB tạm và mock LLM để test chạy siêu tốc < 1s."""
    db_file = os.path.join(tmp_path, "test_api.db")
    init_db_sync(db_file)
    monkeypatch.setattr("backend.app.DEFAULT_DB_PATH", db_file)
    monkeypatch.setattr("backend.llm_synthesizer.LLM_API_KEY", "")
    monkeypatch.setattr("backend.llm_synthesizer.LLM_PROVIDER", "mock")
    return db_file


@pytest.mark.asyncio
async def test_sse_stream_spider_events_gate_5():
    """
    Gate 5 Primary Assertion:
    Kiểm tra SSE stream nhận đúng format `data: {...}\n\n` và header `text/event-stream`.
    """
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Chuẩn bị 1 sự kiện mẫu để đẩy vào hàng đợi
        test_event = SpiderEvent(
            article_id=1,
            target_word="Lãi suất",
            target_index=0,
            category="kinh_te",
            sentiment="positive",
            sentiment_color="#F8AFA6",
            sfx_trigger="water_drop",
            pacing_delay_ms=400,
        )

        # Đẩy sự kiện vào event_manager
        await event_manager.push_event(test_event)

        # Kết nối tới endpoint SSE với max_events=1 để test nhận diện stream và ngắt an toàn
        async with client.stream("GET", "/api/stream/spider-events?max_events=1") as response:
            assert response.status_code == 200
            content_type = response.headers.get("content-type", "")
            assert "text/event-stream" in content_type, f"Content-Type phải là text/event-stream, nhận được: {content_type}"

            # Đọc dòng đầu tiên từ stream với timeout an toàn
            received_lines = []
            try:
                async with asyncio.timeout(3.0):
                    async for line in response.aiter_lines():
                        if line:
                            received_lines.append(line)
                            if line.startswith("data:"):
                                break
            except TimeoutError:
                pass
            finally:
                await response.aclose()

            # Kiểm tra định dạng SSE
            has_id = any(l.startswith("id:") for l in received_lines)
            has_event = any(l.startswith("event: spider_event") for l in received_lines)
            data_line = next((l for l in received_lines if l.startswith("data:")), None)

            assert has_id, "SSE stream phải có trường 'id:'"
            assert has_event, "SSE stream phải có trường 'event: spider_event'"
            assert data_line is not None, "SSE stream phải có trường 'data:'"

            # Parse dữ liệu payload
            payload_str = data_line[len("data:"):].strip()
            payload = json.loads(payload_str)
            assert payload["target_word"] == "Lãi suất"
            assert payload["category"] == "kinh_te"
            assert payload["sentiment_color"] == "#F8AFA6"


@pytest.mark.asyncio
async def test_synthesize_single_article(setup_test_database):
    """Kiểm tra POST /api/v1/synthesize/article."""
    # Thêm 1 bài viết mẫu vào database
    async with aiosqlite.connect(setup_test_database) as db:
        cur = await db.execute("""
            INSERT INTO articles (url, url_hash, title, content_clean, language)
            VALUES ('https://news.com/fed', 'hash_fed_12', 'FED giữ nguyên lãi suất', 'Cục Dự trữ Liên bang Mỹ quyết định giữ nguyên lãi suất cơ bản.', 'vi');
        """)
        await db.commit()
        article_id = cur.lastrowid

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/synthesize/article", json={"article_id": article_id})
        assert resp.status_code == 200
        data = resp.json()
        assert data["article_id"] == article_id
        assert "vietnamese_title" in data
        assert "vietnamese_summary" in data
        assert "macro_impact" in data
        assert data["confidence_score"] > 0


@pytest.mark.asyncio
async def test_synthesize_executive_digest():
    """Kiểm tra POST /api/v1/synthesize/digest."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/synthesize/digest", json={"date": "2026-10-10", "category": "all"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["digest_date"] == "2026-10-10"
        assert "macro_economy_panel" in data
        assert "geopolitics_panel" in data
        assert "github_tech_panel" in data
        assert "chart_metrics" in data


@pytest.mark.asyncio
async def test_sources_and_watchlists_endpoints():
    """Kiểm tra API quản lý nguồn tin và watchlists động."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Lấy danh sách nguồn tin
        sources_resp = await client.get("/api/v1/sources")
        assert sources_resp.status_code == 200
        sources = sources_resp.json()
        assert len(sources) >= 5

        # Lấy danh sách watchlists
        watchlists_resp = await client.get("/api/v1/watchlists")
        assert watchlists_resp.status_code == 200
        watchlists = watchlists_resp.json()
        assert len(watchlists) >= 5
        assert any(w["topic_code"] == "gia_dau" for w in watchlists)

        # Tìm kiếm FTS
        search_resp = await client.get("/api/v1/search?q=dau")
        assert search_resp.status_code == 200
        search_data = search_resp.json()
        assert "results" in search_data
