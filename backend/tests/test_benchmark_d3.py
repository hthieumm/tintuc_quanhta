"""
Automated Pytest Suite for System 1 (Decision 3 / Laya RL Agent / Mock) Response Speed and Accuracy.
Tests live Docker container or mock fallback.
"""

import pytest
import httpx
from backend.ensure_laya import check_laya_live, LAYA_ENDPOINT, get_system1_status


@pytest.mark.asyncio
async def test_system1_health_and_models():
    """Kiểm tra healthcheck và trạng thái của System 1 (Laya hoặc D3)."""
    status = await get_system1_status()
    assert status is not None
    assert "effective_engine" in status
    assert status["status"] in ("online", "mock_active", "fallback_mock")
    assert status["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_system1_inference_latency_and_accuracy():
    """Kiểm tra phản hồi, độ trễ và định dạng phân loại của System 1."""
    is_live = await check_laya_live(timeout=3.0)
    if not is_live:
        pytest.skip("System 1 container port 8000 is offline; skipping live inference test.")

    async with httpx.AsyncClient(timeout=5.0) as client:
        payload = {
            "state": "Ngân hàng Nhà nước Việt Nam tuyên bố giảm mạnh lãi suất điều hành để thúc đẩy kinh tế vĩ mô.",
            "questions": {
                "category": {
                    "type": "choice",
                    "instructions": "Chủ đề chính là gì?",
                    "criteria": {
                        "kinh_te": "lãi suất, ngân hàng, tài chính, GDP",
                        "chinh_tri": "ngoại giao, bầu cử, luật"
                    }
                },
                "sentiment": {
                    "type": "choice",
                    "instructions": "Tâm lý thị trường?",
                    "criteria": {
                        "positive": "hạ lãi suất, thúc đẩy, tích cực",
                        "negative": "suy thoái, khủng hoảng, rủi ro"
                    }
                }
            }
        }
        resp = await client.post(LAYA_ENDPOINT, json=payload)
        assert resp.status_code == 200
        data = resp.json()

        # Kiểm tra cấu trúc trả về
        assert "answers" in data
        assert "category" in data["answers"]
        assert "sentiment" in data["answers"]

        # Kiểm tra kết quả phân loại
        cat_ans = data["answers"]["category"]
        cat_val = cat_ans if isinstance(cat_ans, str) else cat_ans.get("choice")
        assert cat_val == "kinh_te"

        sent_ans = data["answers"]["sentiment"]
        sent_val = sent_ans if isinstance(sent_ans, str) else sent_ans.get("choice")
        assert sent_val == "positive"
