import pytest
import aiosqlite
import httpx
from backend.app import app
from backend.database import DEFAULT_DB_PATH

@pytest.mark.asyncio
async def test_get_db_stats():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/system/db-stats")
        assert res.status_code == 200
        data = res.json()
        assert "total_articles" in data
        assert "bookmarked_articles" in data
        assert "unbookmarked_articles" in data
        assert "db_size_mb" in data
        assert data["total_articles"] == data["bookmarked_articles"] + data["unbookmarked_articles"]

@pytest.mark.asyncio
async def test_toggle_article_bookmark():
    # Pick first article ID
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id, is_bookmarked FROM articles LIMIT 1") as cur:
            row = await cur.fetchone()
    
    if not row:
        pytest.skip("No articles in database to test bookmark toggle")

    art_id = row["id"]
    old_status = row["is_bookmarked"] or 0

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        res = await client.patch(f"/api/v1/articles/{art_id}/bookmark")
        assert res.status_code == 200
        data = res.json()
        assert data["article_id"] == art_id
        assert data["is_bookmarked"] != old_status

        # Revert back to original status
        res2 = await client.patch(f"/api/v1/articles/{art_id}/bookmark")
        assert res2.status_code == 200
        assert res2.json()["is_bookmarked"] == old_status

@pytest.mark.asyncio
async def test_vacuum_database():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/v1/system/vacuum")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "success"
        assert "db_size_mb" in data
