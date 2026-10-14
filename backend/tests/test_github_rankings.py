import pytest
import httpx
from backend.app import app

@pytest.mark.asyncio
async def test_github_top_starred_25():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/github/top-starred?limit=25")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 25
        # Verify descending order of stars
        for i in range(len(data) - 1):
            assert data[i]["stars"] >= data[i + 1]["stars"]

@pytest.mark.asyncio
async def test_github_top_trending_10():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/github/top-trending?limit=10")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 10
        # Verify descending order of today_stars
        for i in range(len(data) - 1):
            assert data[i]["today_stars"] >= data[i + 1]["today_stars"]

@pytest.mark.asyncio
async def test_github_sync_status_and_daily_sync():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Check status
        status_res = await client.get("/api/v1/github/sync-status")
        assert status_res.status_code == 200
        status_data = status_res.json()
        assert "last_sync_date" in status_data
        assert "total_repos" in status_data
        assert status_data["total_repos"] >= 25

        # Trigger sync
        sync_res = await client.post("/api/v1/github/daily-sync?force=true")
        assert sync_res.status_code == 200
        sync_data = sync_res.json()
        assert sync_data["status"] == "success"
        assert sync_data["updated_count"] >= 25


@pytest.mark.asyncio
async def test_github_repo_explain_endpoint():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Lấy 1 repo bất kỳ
        res = await client.get("/api/v1/github/top-starred?limit=1")
        assert res.status_code == 200
        first_repo = res.json()[0]
        repo_id = first_repo["id"]

        # Gọi explain
        exp_res = await client.post(f"/api/v1/github/repos/{repo_id}/explain")
        assert exp_res.status_code == 200
        exp_data = exp_res.json()
        assert "what_it_does" in exp_data
        assert "problem_solved" in exp_data
        assert "quickstart" in exp_data
