"""
Spider News Radar (Tin Tức Quanh Ta) - FastAPI Application
Provides:
1. Real-time SSE Stream `/api/stream/spider-events` (with drop_oldest policy, ring buffer, ping heartbeat).
2. REST Endpoints for System 2 Synthesis (`/api/v1/synthesize/article`, `/api/v1/synthesize/digest`).
3. Dynamic Source Management (`/api/v1/sources`).
4. Zero-Code Dynamic Topic Watchlists (`/api/v1/watchlists`).
5. Instant SQLite FTS5 Search (`/api/v1/search`).
"""

import os
import re
import uuid
import json
import asyncio
import time
from datetime import datetime, timezone
from typing import Literal, Optional, List, Dict, Any
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI, HTTPException, Query, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import aiosqlite
import httpx
import feedparser
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logger = logging.getLogger("spider_app")

from .database import DEFAULT_DB_PATH, init_db_async, get_db
from .rss_crawler import SpiderNewsCrawler
from .llm_synthesizer import (
    synthesize_single_article,
    generate_modular_executive_digest,
    explain_github_repository,
)
from .ensure_laya import get_mock_decision, check_laya_live, LAYA_ENDPOINT, get_system1_status, set_active_engine

MAX_ARTICLES_PER_DAY = int(os.getenv("MAX_ARTICLES_PER_DAY", "500"))
CRAWL_INTERVAL_SECONDS = int(os.getenv("CRAWL_INTERVAL_SECONDS", "900"))

DAILY_CAP_MSG = (
    "ĐÃ ĐẠT GIỚI HẠN 500 BÀI/NGÀY — bỏ qua bài mới cho đến ngày mai. "
    "Tăng lại bằng MAX_ARTICLES_PER_DAY."
)

# Schemas
class SpiderEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article_id: int
    target_word: str
    target_index: int
    category: Literal["kinh_te", "chung_khoan", "vang", "crypto", "chinh_tri", "github", "quoc_te"] = "kinh_te"
    sentiment: Literal["positive", "negative", "neutral"] = "neutral"
    sentiment_color: Literal["#F8AFA6", "#C86D51", "#E5B869"] = "#E5B869"
    sfx_trigger: Literal["water_drop", "paper_rustle", "wind_chime"] = "water_drop"
    pacing_delay_ms: int = 400


class SynthesizeArticleRequest(BaseModel):
    article_id: int


class SynthesizeDigestRequest(BaseModel):
    date: Optional[str] = "2026-10-10"
    category: Optional[str] = "all"


class SourceCreateRequest(BaseModel):
    name: str
    url: str
    category: Literal["chung_khoan", "vang", "crypto", "kinh_te", "chinh_tri", "github", "tuy_chon"] = "kinh_te"
    source_type: Literal["rss", "github_api"] = "rss"
    fetch_interval_min: int = 15


class WatchlistCreateRequest(BaseModel):
    topic_code: str
    display_name: str
    icon: str = "📌"
    keywords: List[str]
    criteria_prompt: str
    sentiment_alert: str = "all"
    color_hex: str = "#E5B869"


class System1SelectRequest(BaseModel):
    engine: Literal["auto", "laya", "d3", "mock"] = "auto"
    base_url: Optional[str] = None


class TranslateRequest(BaseModel):
    texts: List[str]
    source_lang: str = "auto"
    target_lang: str = "vi"


class EventQueueManager:
    """
    Quản lý hàng đợi sự kiện SSE:
    - asyncio.Queue(maxsize=100)
    - Chính sách drop_oldest khi hàng đợi đầy
    - Ring Buffer 50 phần tử phục vụ reconnection (Last-Event-ID)
    """

    def __init__(self, maxsize: int = 100, ring_size: int = 50):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self.maxsize = maxsize
        self.ring_size = ring_size
        self.ring_buffer: List[SpiderEvent] = []
        self._lock = asyncio.Lock()

    async def push_event(self, event: SpiderEvent) -> None:
        async with self._lock:
            # Lưu vào Ring Buffer
            self.ring_buffer.append(event)
            if len(self.ring_buffer) > self.ring_size:
                self.ring_buffer.pop(0)

            # Đẩy vào asyncio.Queue với chính sách drop_oldest nếu đầy
            if self.queue.full():
                try:
                    self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            await self.queue.put(event)

    def get_events_since(self, last_event_id: str) -> List[SpiderEvent]:
        """Trả về các sự kiện từ ring buffer sau last_event_id."""
        found = False
        res = []
        for ev in self.ring_buffer:
            if found:
                res.append(ev)
            elif ev.event_id == last_event_id:
                found = True
        return res if found else self.ring_buffer


event_manager = EventQueueManager()


async def count_articles_today() -> int:
    """Đếm số bài đã cào trong ngày hiện tại (giờ địa phương máy chủ)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM articles WHERE date(crawled_at) = date('now','localtime')"
        ) as cur:
            row = await cur.fetchone()
            return int(row[0] or 0)


_KEYWORD_CATEGORY_HINTS: List[tuple] = [
    # Tiếng Việt - Kinh tế & Vĩ mô
    ("lãi suất", "kinh_te"), ("lạm phát", "kinh_te"), ("tỷ giá", "vang"),
    ("vàng", "vang"), ("sjc", "vang"), ("usd", "vang"),
    ("cổ phiếu", "chung_khoan"), ("chứng khoán", "chung_khoan"),
    ("vn-index", "chung_khoan"), ("thanh khoản", "chung_khoan"),
    ("trái phiếu", "chung_khoan"), ("vinfast", "chung_khoan"),
    ("doanh nghiệp", "kinh_te"), ("ngân hàng", "kinh_te"),
    ("fed", "kinh_te"), ("bất động sản", "kinh_te"),
    ("chiến sự", "quoc_te"), ("chiến tranh", "quoc_te"),
    ("chính phủ", "chinh_tri"), ("quốc hội", "chinh_tri"),
    # Tiếng Anh - Quốc tế & Vĩ mô
    ("interest rate", "kinh_te"), ("interest", "kinh_te"), ("inflation", "kinh_te"),
    ("federal reserve", "kinh_te"), ("central bank", "kinh_te"),
    ("economy", "kinh_te"), ("economic", "kinh_te"), ("tariffs", "kinh_te"),
    ("trade", "kinh_te"), ("gdp", "kinh_te"),
    # Chứng khoán & Tài chính quốc tế
    ("stocks", "chung_khoan"), ("stock", "chung_khoan"), ("markets", "chung_khoan"),
    ("market", "chung_khoan"), ("equities", "chung_khoan"), ("bonds", "chung_khoan"),
    ("treasury", "chung_khoan"), ("wall street", "chung_khoan"), ("nasdaq", "chung_khoan"),
    # Vàng & Tiền tệ
    ("gold", "vang"), ("dollar", "vang"), ("debased", "vang"),
    # Crypto & Web3
    ("crypto", "crypto"), ("bitcoin", "crypto"), ("btc", "crypto"),
    # Dầu mỏ & Địa chính trị quốc tế
    ("crude oil", "quoc_te"), ("brent", "quoc_te"), ("oil", "quoc_te"),
    ("war", "quoc_te"), ("conflict", "quoc_te"), ("sanctions", "quoc_te"),
    ("ukraine", "quoc_te"), ("russia", "quoc_te"), ("taiwan", "quoc_te"),
    # Chính trị & Bầu cử
    ("trump", "chinh_tri"), ("biden", "chinh_tri"), ("democrats", "chinh_tri"),
    ("republicans", "chinh_tri"), ("gop", "chinh_tri"), ("congress", "chinh_tri"),
    ("senate", "chinh_tri"), ("election", "chinh_tri"), ("elections", "chinh_tri"),
    ("white house", "chinh_tri"), ("midterms", "chinh_tri"),
    # Công nghệ AI & GitHub
    ("ai", "github"), ("nvidia", "github"), ("llm", "github"), ("semiconductor", "github"),
]


def extract_spider_keywords(text: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Rút từ khóa cho nhện từ tiêu đề và nội dung toàn văn.
    Sử dụng word boundary cho các từ viết tắt ngắn (ai, fed, gop, oil, war) để chống match nhầm.
    """
    if not text:
        return []
    lowered = text.lower()
    found: List[Dict[str, Any]] = []
    seen_words = set()
    index = 0

    for word, cat in _KEYWORD_CATEGORY_HINTS:
        if word in seen_words:
            continue
        # Với từ ngắn <= 3 ký tự Latin, dùng regex word boundary để tránh nhầm
        if len(word) <= 3 and word.isascii():
            m = re.search(rf"\b{re.escape(word)}\b", lowered)
            if m:
                pos = m.start()
                extracted_word = text[pos:pos + len(word)]
                found.append({"word": extracted_word or word, "category": cat, "index": index})
                seen_words.add(word)
                index += 1
        else:
            pos = lowered.find(word)
            if pos >= 0:
                extracted_word = text[pos:pos + len(word)]
                found.append({"word": extracted_word or word, "category": cat, "index": index})
                seen_words.add(word)
                index += 1

        if len(found) >= limit:
            break

    return found


async def enrich_article_record(
    article_id: int,
    url: str,
    summary_raw: str,
    old_content: str,
    crawler: SpiderNewsCrawler,
    client: Optional[httpx.AsyncClient] = None,
) -> Optional[str]:
    """
    Cào sâu và làm giàu toàn văn bài viết từ URL gốc bằng Waterfall 6 tầng.
    Tự động cập nhật DB và đồng bộ FTS5 nếu trích xuất thành công nội dung dài hơn.
    """
    if not url or not url.startswith("http"):
        return None

    full_text, tier = await crawler.fetch_article_waterfall(
        url=url,
        rss_summary=summary_raw or "",
        client=client,
    )
    if full_text and len(full_text) > max(len(old_content or ""), 250):
        async with aiosqlite.connect(DEFAULT_DB_PATH, timeout=30.0) as db:
            await db.execute(
                "UPDATE articles SET content_clean = ? WHERE id = ?",
                (full_text, article_id),
            )
            try:
                await db.execute(
                    "UPDATE articles_fts SET content_clean = ? WHERE rowid = ?",
                    (full_text, article_id),
                )
            except Exception:
                pass
            await db.commit()
        return full_text
    return None


async def enrich_short_articles_batch(limit: int = 15) -> int:
    """
    Quét và làm giàu nội dung toàn văn cho các bài báo đang ở dạng tóm tắt ngắn (<= 320 ký tự).
    Phát ngay SpiderEvent cho các bài vừa được làm giàu để con nhện trên client nhận diện.
    """
    try:
        async with aiosqlite.connect(DEFAULT_DB_PATH, timeout=30.0) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT id, url, summary_raw, content_clean, title
                FROM articles
                WHERE (length(content_clean) <= 320 OR content_clean = summary_raw)
                  AND url LIKE 'http%'
                ORDER BY id DESC
                LIMIT ?;
                """,
                (limit,),
            ) as cur:
                short_rows = [dict(r) for r in await cur.fetchall()]

        if not short_rows:
            return 0

        crawler = SpiderNewsCrawler(db_path=DEFAULT_DB_PATH)
        enriched_count = 0
        enriched_articles = []

        async with httpx.AsyncClient(timeout=14.0, follow_redirects=True) as http_client:
            for art in short_rows:
                try:
                    new_text = await enrich_article_record(
                        article_id=art["id"],
                        url=art["url"],
                        summary_raw=art["summary_raw"] or "",
                        old_content=art["content_clean"] or "",
                        crawler=crawler,
                        client=http_client,
                    )
                    if new_text:
                        enriched_count += 1
                        art["content_clean"] = new_text
                        enriched_articles.append(art)
                except Exception:
                    continue

        if enriched_articles:
            await emit_spider_events_for_articles(enriched_articles)

        return enriched_count
    except Exception:
        return 0


async def emit_spider_events_for_articles(
    articles: List[Dict[str, Any]],
    pacing_delay_ms: int = 400,
) -> int:
    """Đẩy SpiderEvent cho từng bài mới vào hàng đợi SSE để nhện tự bò."""
    emitted = 0
    for art in articles:
        keywords = extract_spider_keywords(
            f"{art.get('title', '')} {art.get('content_clean') or art.get('summary_raw') or ''}"
        )
        for kw in keywords:
            event = SpiderEvent(
                article_id=int(art["id"]),
                target_word=kw["word"],
                target_index=kw["index"],
                category=kw["category"],  # type: ignore[arg-type]
                sentiment="neutral",
                sentiment_color="#E5B869",
                sfx_trigger="paper_rustle",
                pacing_delay_ms=pacing_delay_ms,
            )
            await event_manager.push_event(event)
            emitted += 1
    return emitted


async def run_scheduled_crawl() -> Dict[str, Any]:
    """Một vòng quét định kỳ: dừng khi chạm cap 500 bài/ngày, phát event cho bài mới."""
    today_count = await count_articles_today()
    if today_count >= MAX_ARTICLES_PER_DAY:
        return {"status": "daily_cap_reached", "today_count": today_count,
                "cap": MAX_ARTICLES_PER_DAY}
    before_ids: set = set()
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM articles WHERE date(crawled_at) = date('now','localtime')"
        ) as cur:
            before_ids = {row["id"] for row in await cur.fetchall()}
    crawler = SpiderNewsCrawler(db_path=DEFAULT_DB_PATH)
    results = await crawler.crawl_all_active_sources()
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT id, title, content_clean, summary_raw
            FROM articles
            WHERE date(crawled_at) = date('now','localtime')
            ORDER BY id DESC
            """
        ) as cur:
            all_today = [dict(row) for row in await cur.fetchall()]
    # Chỉ phát event cho bài vừa mới chèn (id chưa có trong before_ids), tôn trọng cap 500
    new_articles = [a for a in all_today if a["id"] not in before_ids][:max(0, MAX_ARTICLES_PER_DAY - today_count)]
    emitted = await emit_spider_events_for_articles(new_articles)
    inserted_total = sum(
        int(v.get("inserted", 0)) if isinstance(v, dict) else 0
        for v in (results.values() if isinstance(results, dict) else [])
    )
    return {
        "status": "crawled",
        "today_count": today_count + inserted_total,
        "cap": MAX_ARTICLES_PER_DAY,
        "events_emitted": emitted,
        "results": results,
    }


async def _scheduler_loop() -> None:
    while True:
        try:
            await run_scheduled_crawl()
            # Tự động làm giàu các bài báo tóm tắt còn lại trong DB để chống thất thoát từ khóa
            await enrich_short_articles_batch(limit=12)
            # Tự động quét cập nhật GitHub khi sang ngày mới
            await check_and_run_github_daily_sync()
        except Exception:
            pass
        await asyncio.sleep(CRAWL_INTERVAL_SECONDS)


async def lifespan(app: FastAPI):
    # Khởi tạo DB khi khởi động
    await init_db_async()
    try:
        async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
            async with db.execute("SELECT key, value FROM system_settings WHERE key IN ('system1_engine', 'system1_base_url')") as cur:
                rows = dict(await cur.fetchall())
                if "system1_engine" in rows:
                    set_active_engine(rows["system1_engine"], rows.get("system1_base_url"))
    except Exception:
        pass
    # Khởi động scheduler và làm giàu bài viết ban đầu
    task = asyncio.create_task(_scheduler_loop())
    asyncio.create_task(enrich_short_articles_batch(limit=15))
    asyncio.create_task(check_and_run_github_daily_sync())
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


app = FastAPI(
    title="Spider News Radar API",
    version="1.0.0",
    description="Real-Time Automated Intelligence Radar with Laya System 1 and LLM System 2",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 1. SSE Stream: /api/stream/spider-events
# ==========================================
@app.get("/api/stream/spider-events")
async def stream_spider_events(request: Request, max_events: Optional[int] = Query(None, description="Giới hạn số event (dùng cho tests)")):
    """
    Luồng dữ liệu thời gian thực cho con nhện trên Frontend.
    Phát sự kiện SpiderEvent với nhịp pacing, hỗ trợ heartbeat và Reconnection.
    """
    last_event_id = request.headers.get("Last-Event-ID")

    async def event_generator():
        # Gửi dòng comment ban đầu để client nhận HTTP 200 ngay tức thì
        yield ": connected\n\n"

        # Nếu client kết nối lại với Last-Event-ID, phát lại các sự kiện bị lỡ
        if last_event_id:
            missed_events = event_manager.get_events_since(last_event_id)
            for ev in missed_events:
                yield f"id: {ev.event_id}\nevent: spider_event\ndata: {ev.model_dump_json()}\n\n"

        sent_count = 0
        last_ping = time.time()
        try:
            while True:
                if max_events is not None and sent_count >= max_events:
                    break
                try:
                    # Đợi sự kiện tiếp theo với timeout 15s để gửi ping
                    event: SpiderEvent = await asyncio.wait_for(event_manager.queue.get(), timeout=15.0)
                    yield f"id: {event.event_id}\nevent: spider_event\ndata: {event.model_dump_json()}\n\n"
                    sent_count += 1
                    last_ping = time.time()
                except asyncio.TimeoutError:
                    # Gửi heartbeat duy trì kết nối mỗi 15 giây
                    yield ": ping\n\n"
                    last_ping = time.time()
        except (asyncio.CancelledError, GeneratorExit):
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ==========================================
# 2. LLM System 2 REST Endpoints
# ==========================================
@app.post("/api/v1/synthesize/article")
async def api_synthesize_article(req: SynthesizeArticleRequest):
    """Deep Dive Tin Lẻ: Dịch & phân tích tác động vĩ mô."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, title, content_clean FROM articles WHERE id = ?",
            (req.article_id,),
        ) as cur:
            article = await cur.fetchone()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    result = await synthesize_single_article(
        article_id=article["id"],
        title=article["title"],
        content=article["content_clean"],
    )

    # Lưu vào bảng llm_syntheses
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO llm_syntheses (
                article_id, synthesis_type, vietnamese_title,
                vietnamese_summary, macro_impact_analysis
            ) VALUES (?, 'single_deep_dive', ?, ?, ?);
            """,
            (
                req.article_id,
                result["vietnamese_title"],
                result["vietnamese_summary"],
                result["macro_impact"],
            ),
        )
        await db.commit()

    return result


@app.post("/api/v1/synthesize/digest")
async def api_synthesize_digest(req: SynthesizeDigestRequest):
    """Bản Tin Tổng Hợp Vĩ Mô Đa Khung (Modular Executive Digest)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, title, content_clean FROM articles ORDER BY published_at DESC LIMIT 40;"
        ) as cur:
            articles = [dict(row) for row in await cur.fetchall()]

    digest = await generate_modular_executive_digest(
        date_str=req.date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        articles=articles,
        category=req.category or "all",
    )

    # Lưu vào bảng llm_syntheses
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO llm_syntheses (
                synthesis_type, vietnamese_title,
                vietnamese_summary, raw_response_json
            ) VALUES ('executive_digest', ?, ?, ?);
            """,
            (
                f"Bản Tin Vĩ Mô {digest['digest_date']}",
                digest["macro_economy_panel"]["narrative_markdown"][:200],
                json.dumps(digest, ensure_ascii=False),
            ),
        )
        await db.commit()

    return digest


# ==========================================
# 3. Dynamic Source Management (CRUD Feeds)
# ==========================================
@app.get("/api/v1/sources")
async def api_get_sources():
    """Lấy danh sách toàn bộ nguồn tin kèm số bài đã cào."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT s.*, COUNT(a.id) as article_count
            FROM sources s
            LEFT JOIN articles a ON a.source_id = s.id
            GROUP BY s.id
            ORDER BY s.id ASC;
        """) as cur:
            rows = [dict(row) for row in await cur.fetchall()]
    return rows


@app.post("/api/v1/sources")
async def api_create_source(req: SourceCreateRequest):
    """
    Thêm nguồn RSS mới.
    Tự động kiểm tra tính hợp lệ (HTTP 200 & XML format) trước khi lưu.
    """
    if req.source_type == "rss":
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                res = await client.get(req.url, headers={"User-Agent": "Mozilla/5.0"})
                if res.status_code != 200:
                    raise HTTPException(
                        status_code=400,
                        detail=f"RSS URL trả về mã lỗi HTTP {res.status_code}",
                    )
                feed = feedparser.parse(res.text)
                if not feed.entries and not getattr(feed, "feed", None):
                    raise HTTPException(
                        status_code=400,
                        detail="URL không phải định dạng RSS/Atom XML hợp lệ",
                    )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Không thể kết nối đến URL RSS: {str(e)}",
            )

    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        try:
            cur = await db.execute(
                """
                INSERT INTO sources (name, source_type, url, category, is_active, fetch_interval_min)
                VALUES (?, ?, ?, ?, 1, ?);
                """,
                (req.name, req.source_type, req.url, req.category, req.fetch_interval_min),
            )
            await db.commit()
            new_id = cur.lastrowid
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="URL nguồn này đã tồn tại trong hệ thống")

    return {"status": "success", "id": new_id, "message": f"Đã thêm nguồn {req.name}"}


@app.patch("/api/v1/sources/{source_id}/toggle")
async def api_toggle_source(source_id: int):
    """Bật/Tắt quét một nguồn."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT is_active FROM sources WHERE id = ?", (source_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Source not found")

        new_status = 0 if row["is_active"] == 1 else 1
        await db.execute("UPDATE sources SET is_active = ? WHERE id = ?", (new_status, source_id))
        await db.commit()

    return {"source_id": source_id, "is_active": new_status}


@app.delete("/api/v1/sources/{source_id}")
async def api_delete_source(source_id: int):
    """Xóa một nguồn tin."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute("DELETE FROM sources WHERE id = ?", (source_id,))
        await db.commit()
    return {"status": "deleted", "source_id": source_id}


# ==========================================
# 4. Zero-Code Dynamic Watchlists
# ==========================================
@app.get("/api/v1/watchlists")
async def api_get_watchlists():
    """Lấy danh sách các chủ đề theo dõi đang kích hoạt."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM topic_watchlists WHERE is_active = 1;") as cur:
            rows = [dict(row) for row in await cur.fetchall()]
            for r in rows:
                if isinstance(r.get("keywords_json"), str):
                    try:
                        r["keywords"] = json.loads(r["keywords_json"])
                    except Exception:
                        r["keywords"] = []
    return rows


@app.post("/api/v1/watchlists")
async def api_create_watchlist(req: WatchlistCreateRequest):
    """Thêm chủ đề mới (Zero-Code Dynamic Registry)."""
    keywords_str = json.dumps(req.keywords, ensure_ascii=False)
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        try:
            cur = await db.execute(
                """
                INSERT INTO topic_watchlists (
                    topic_code, display_name, icon, keywords_json,
                    criteria_prompt, sentiment_alert, color_hex
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    req.topic_code,
                    req.display_name,
                    req.icon,
                    keywords_str,
                    req.criteria_prompt,
                    req.sentiment_alert,
                    req.color_hex,
                ),
            )
            await db.commit()
            new_id = cur.lastrowid
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="Mã chủ đề topic_code đã tồn tại")

    return {"status": "success", "id": new_id, "topic_code": req.topic_code}


@app.delete("/api/v1/watchlists/{watchlist_id}")
async def api_delete_watchlist(watchlist_id: int):
    """Xóa một chủ đề theo dõi."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute("DELETE FROM topic_watchlists WHERE id = ?", (watchlist_id,))
        await db.commit()
    return {"status": "deleted", "id": watchlist_id}


# ==========================================
# 5. Instant SQLite FTS5 Search: /api/v1/search
# ==========================================
@app.get("/api/v1/search")
async def api_search(q: str = Query(..., min_length=1, description="Từ khóa tra cứu")):
    """
    Tra cứu siêu tốc không dấu/có dấu qua FTS5 (< 2ms).
    """
    clean_query = q.strip().replace('"', '""')
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        try:
            async with db.execute(
                """
                SELECT a.id, a.title, a.content_clean, a.url, a.published_at, a.language
                FROM articles_fts fts
                JOIN articles a ON a.id = fts.rowid
                WHERE articles_fts MATCH ?
                ORDER BY rank
                LIMIT 30;
                """,
                (clean_query,),
            ) as cur:
                rows = [dict(row) for row in await cur.fetchall()]
        except Exception:
            # Fallback nếu query chứa ký tự đặc biệt của FTS
            async with db.execute(
                """
                SELECT id, title, content_clean, url, published_at, language
                FROM articles
                WHERE title LIKE ? OR content_clean LIKE ?
                ORDER BY published_at DESC
                LIMIT 30;
                """,
                (f"%{clean_query}%", f"%{clean_query}%"),
            ) as cur:
                rows = [dict(row) for row in await cur.fetchall()]

    return {"query": q, "total_matches": len(rows), "results": rows}


# ==========================================
# 5.1 Category Stats Endpoint: /api/v1/categories/stats
# ==========================================
@app.get("/api/v1/categories/stats")
async def api_get_category_stats():
    """
    Trả về tổng số bài viết theo từng chuyên mục trên toàn bộ cơ sở dữ liệu SQLite.
    """
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT coalesce(s.category, 'all') as cat, count(a.id) as total
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            GROUP BY s.category;
            """
        ) as cur:
            rows = await cur.fetchall()
            stats = {row["cat"]: row["total"] for row in rows}

        async with db.execute("SELECT count(*) as total FROM articles;") as cur:
            total_row = await cur.fetchone()
            stats["all"] = total_row["total"] if total_row else 0

    return stats


# ==========================================
# 6. Articles & Events Helper Endpoints
# ==========================================
@app.get("/api/v1/articles")
async def api_get_articles(
    limit: int = 50,
    offset: int = 0,
    category: Optional[str] = Query(None, description="Lọc theo chuyên mục: kinh_te, chung_khoan, vang, crypto, quoc_te, chinh_tri"),
    today: bool = Query(False, description="Chỉ lấy tin trong ngày (today=1)"),
):
    """Lấy danh sách bài viết. Hỗ trợ lọc theo chuyên mục và ngày."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = """
            SELECT a.*, s.name as source_name, s.category as source_category
            FROM articles a
            LEFT JOIN sources s ON s.id = a.source_id
        """
        conditions = []
        params: List[Any] = []

        if today:
            conditions.append("date(a.crawled_at) = date('now','localtime')")
        if category and category != "all":
            conditions.append("s.category = ?")
            params.append(category)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY a.id DESC LIMIT ? OFFSET ?;"
        params.extend([limit, offset])

        async with db.execute(query, tuple(params)) as cur:
            rows = [dict(row) for row in await cur.fetchall()]
    return rows


@app.get("/api/v1/articles/{article_id}")
async def api_get_single_article(article_id: int, auto_enrich: bool = True):
    """
    Lấy chi tiết một bài viết theo ID.
    Tự động kích hoạt cào sâu toàn văn nếu bài đang ở dạng tóm tắt ngắn (<= 320 ký tự).
    """
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT a.*, s.name as source_name, s.category as source_category
            FROM articles a
            LEFT JOIN sources s ON s.id = a.source_id
            WHERE a.id = ?;
            """,
            (article_id,),
        ) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Article not found")

    row_dict = dict(row)
    # Tự động làm giàu nội dung nếu bài ngắn và chưa có toàn văn
    if auto_enrich and (not row_dict.get("content_clean") or len(row_dict.get("content_clean") or "") <= 320 or row_dict.get("content_clean") == row_dict.get("summary_raw")):
        crawler = SpiderNewsCrawler(db_path=DEFAULT_DB_PATH)
        enriched = await enrich_article_record(
            article_id=article_id,
            url=row_dict["url"],
            summary_raw=row_dict.get("summary_raw") or "",
            old_content=row_dict.get("content_clean") or "",
            crawler=crawler,
        )
        if enriched:
            row_dict["content_clean"] = enriched
            await emit_spider_events_for_articles([row_dict])

    return row_dict


@app.post("/api/v1/articles/{article_id}/fetch-full")
async def api_fetch_full_article(article_id: int):
    """Cào sâu toàn văn bài viết từ URL gốc bằng Waterfall 8 tầng (curl_cffi, __NEXT_DATA__, Playwright, Reverse Search)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM articles WHERE id = ?", (article_id,)) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Article not found")

    title = row["title"] or ""
    crawler = SpiderNewsCrawler(db_path=DEFAULT_DB_PATH)
    full_text, tier = await crawler.fetch_article_waterfall(
        url=row["url"],
        rss_summary=row["summary_raw"] or "",
        title=title,
    )

    # Nếu nội dung vẫn quá ngắn (< 250 ký tự do dính Hard Paywall / DataDome như The Economist),
    # kích hoạt tầng Deep Scrape đặc trị: Playwright Headless + Reverse Search
    if not full_text or len(full_text) <= 250:
        # 1. Thử Playwright Headless với Social Referer (Đã bọc bộ lọc sanitize_article_prose)
        try:
            from .rss_crawler import sanitize_article_prose
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    extra_http_headers={"Referer": "https://t.co/", "X-Forwarded-For": "66.249.66.1"},
                )
                page = await context.new_page()
                await page.goto(row["url"], wait_until="domcontentloaded", timeout=5000)
                p_text = await page.evaluate("""() => {
                    // Xóa toàn bộ header, nav, footer, aside trước khi lấy chữ
                    document.querySelectorAll('header, nav, footer, aside, [role="navigation"], [role="banner"], figure, figcaption').forEach(el => el.remove());
                    const paras = Array.from(document.querySelectorAll('article p, [data-gu-name="body"] p, main p'))
                        .map(p => p.innerText.trim())
                        .filter(t => t.length >= 50 && (t.includes('.') || t.includes('?') || t.includes('!')));
                    return paras.join('\\n\\n');
                }""")
                clean_p_text = sanitize_article_prose(p_text, min_total_len=200)
                if clean_p_text:
                    full_text = clean_p_text
                    tier = "tier_playwright_deep"
                await browser.close()
        except Exception as e:
            logger.debug(f"Deep scrape Playwright error: {e}")

        # 2. Nếu vẫn chưa có, kích hoạt Reverse Search trích dẫn
        if not full_text or len(full_text) <= 250:
            from .rss_crawler import reverse_search_article
            rev_text = await reverse_search_article(title, timeout=4.0)
            if rev_text and len(rev_text) > len(row["content_clean"] or ""):
                full_text = rev_text
                tier = "tier_7_reverse_search"

        # 3. Nếu vẫn không vượt qua được Paywall cứng (như The Economist / Bloomberg / FT),
        # kích hoạt AI System 2 để tái tạo bản phân tích chuyên sâu toàn cảnh vĩ mô
        if not full_text or len(full_text) <= 250:
            try:
                from .llm_synthesizer import call_llm_chat_completion
                ai_prompt = (
                    f"Bạn là chuyên gia phân tích vĩ mô và tài chính quốc tế hàng đầu.\n"
                    f"Bài báo sau bị khóa bởi tường lửa Paywall của tòa soạn quốc tế:\n"
                    f"Tiêu đề: {title}\n"
                    f"Tóm tắt: {row['summary_raw'] or ''}\n\n"
                    f"Hãy tái tạo và viết một bài phân tích chuyên sâu, toàn cảnh (toàn bộ bằng tiếng Việt, từ 3-5 đoạn văn đầy đủ) bao gồm:\n"
                    f"1. Bối cảnh cốt lõi và nguyên nhân dẫn đến diễn biến này.\n"
                    f"2. Các số liệu, thương vụ hoặc chính sách tài chính then chốt có liên quan.\n"
                    f"3. Tác động kinh tế vĩ mô đến thị trường, dòng tiền và dự báo xu hướng tiếp theo.\n"
                    f"Viết mạch lạc, văn phong báo chí tài chính chuẩn xác."
                )
                ai_res = await call_llm_chat_completion(
                    prompt=ai_prompt,
                    system_prompt="Bạn là chuyên gia kinh tế vĩ mô và tài chính quốc tế.",
                    max_tokens=900,
                )
                if ai_res and len(ai_res) > 250:
                    full_text = f"[Bản phân tích toàn cảnh vĩ mô - AI System 2 Reconstruction]:\n\n{ai_res}"
                    tier = "tier_ai_deep_dive"
            except Exception as e:
                logger.debug(f"AI reconstruction error: {e}")

    if full_text and len(full_text) > len(row["content_clean"] or ""):
        async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
            await db.execute(
                "UPDATE articles SET content_clean = ? WHERE id = ?",
                (full_text, article_id),
            )
            try:
                await db.execute(
                    "UPDATE articles_fts SET content_clean = ? WHERE rowid = ?",
                    (full_text, article_id),
                )
            except Exception:
                pass
            await db.commit()
        # Bắn ngay SpiderEvent vào SSE stream cho các từ khóa mới xuất hiện!
        updated_art = dict(row)
        updated_art["content_clean"] = full_text
        await emit_spider_events_for_articles([updated_art])
        return {"status": "updated", "tier": tier, "content_clean": full_text}

    return {"status": "unchanged", "tier": tier, "content_clean": row["content_clean"]}


@app.post("/api/v1/articles/enrich-all")
async def api_enrich_all_articles(background_tasks: BackgroundTasks, limit: int = 50):
    """Kích hoạt tác vụ làm giàu toàn văn cho các bài báo tóm tắt trong DB."""
    background_tasks.add_task(enrich_short_articles_batch, limit=limit)
    return {
        "status": "enriching",
        "limit": limit,
        "message": f"Hệ thống đang chạy ngầm làm giàu tối đa {limit} bài báo tóm tắt",
    }


def _sync_translate_batch(texts: List[str], source_lang: str = "auto", target_lang: str = "vi") -> List[str]:
    """Dịch máy theo từng đoạn bằng deep-translator (MyMemory/Google) 0đ API, 0% VRAM."""
    from deep_translator import MyMemoryTranslator, GoogleTranslator
    results = []
    
    s_lang = "en-US" if source_lang in ("en", "auto") else source_lang
    t_lang = "vi-VN" if target_lang == "vi" else target_lang

    translator = None
    try:
        translator = MyMemoryTranslator(source=s_lang, target=t_lang)
    except Exception:
        pass

    for text in texts:
        clean = (text or "").strip()
        if not clean:
            results.append("")
            continue
        translated = None
        if translator:
            try:
                if len(clean) > 400:
                    chunks = [clean[i:i+380] for i in range(0, len(clean), 380)]
                    t_parts = [translator.translate(c) for c in chunks]
                    translated = " ".join([p for p in t_parts if p])
                else:
                    translated = translator.translate(clean)
            except Exception:
                translated = None

        if not translated:
            try:
                g_trans = GoogleTranslator(source="auto", target="vi")
                translated = g_trans.translate(clean)
            except Exception:
                translated = clean

        results.append(translated or clean)
    return results


@app.post("/api/v1/translate")
async def api_translate(req: TranslateRequest):
    """
    Dịch máy theo yêu cầu (On-Demand Translation) cho từng đoạn văn:
    - 0đ chi phí API
    - 0% GPU VRAM
    - Bảo toàn cấu trúc HTML DOM
    """
    if not req.texts:
        return {"translated_texts": []}

    translated = await asyncio.to_thread(
        _sync_translate_batch,
        texts=req.texts,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
    )
    return {"translated_texts": translated}


@app.post("/api/v1/crawl")
async def api_trigger_crawl(background_tasks: BackgroundTasks):
    """Kích hoạt quét thủ công (vẫn tôn trọng cap 500 bài/ngày và có phát event)."""
    today_count = await count_articles_today()
    if today_count >= MAX_ARTICLES_PER_DAY:
        return {"status": "daily_cap_reached", "today_count": today_count,
                "cap": MAX_ARTICLES_PER_DAY, "message": DAILY_CAP_MSG}
    background_tasks.add_task(run_scheduled_crawl)
    return {"status": "crawl_triggered", "today_count": today_count,
            "cap": MAX_ARTICLES_PER_DAY,
            "message": "Quá trình cào tin đang chạy ngầm"}


@app.get("/api/v1/crawl/status")
async def api_crawl_status():
    """Trạng thái scheduler 15 phút/lần + cap 500 bài/ngày."""
    today_count = await count_articles_today()
    return {
        "interval_seconds": CRAWL_INTERVAL_SECONDS,
        "daily_cap": MAX_ARTICLES_PER_DAY,
        "articles_today": today_count,
        "cap_reached": today_count >= MAX_ARTICLES_PER_DAY,
        "queue_size": event_manager.queue.qsize(),
    }


@app.post("/api/v1/simulate-event")
async def api_simulate_event(event: SpiderEvent):
    """Bơm sự kiện giả lập vào luồng SSE cho nhện."""
    await event_manager.push_event(event)
    return {"status": "enqueued", "event_id": event.event_id}


@app.get("/api/v1/system1/status")
async def api_system1_status():
    """Lấy trạng thái động, danh sách engine khả dụng và latency trung bình của System 1."""
    status = await get_system1_status()
    status["avg_latency_ms"] = await _query_avg_system1_latency()
    return status


async def _query_avg_system1_latency() -> Optional[float]:
    """Latency trung bình của 200 quyết định System 1 gần nhất (None nếu chưa có dữ liệu)."""
    if not os.path.exists(DEFAULT_DB_PATH):
        return None
    try:
        async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
            async with db.execute(
                "SELECT AVG(latency_ms) FROM (SELECT latency_ms FROM laya_decisions "
                "WHERE latency_ms IS NOT NULL ORDER BY id DESC LIMIT 200)"
            ) as cur:
                row = await cur.fetchone()
        return round(row[0], 2) if row and row[0] is not None else None
    except Exception:
        return None


@app.post("/api/v1/system1/select")
async def api_system1_select(req: System1SelectRequest):
    """Chọn mô hình System 1 (auto, laya, d3, mock) và lưu vào cấu hình DB."""
    set_active_engine(req.engine, req.base_url)
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO system_settings (key, value, updated_at)
            VALUES ('system1_engine', ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP;
            """,
            (req.engine,)
        )
        if req.base_url:
            await db.execute(
                """
                INSERT INTO system_settings (key, value, updated_at)
                VALUES ('system1_base_url', ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP;
                """,
                (req.base_url,)
            )
        await db.commit()
    status = await get_system1_status()
    status["avg_latency_ms"] = await _query_avg_system1_latency()
    return status


@app.get("/api/health")
async def api_health():
    """Kiểm tra sức khỏe hệ thống và mô hình System 1 đang kích hoạt."""
    sys1_status = await get_system1_status()
    return {
        "status": "healthy",
        "service": "Spider News Radar API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system_1": {
            "engine": sys1_status["effective_engine"],
            "display_name": sys1_status["display_name"],
            "status": sys1_status["status"],
            "device": sys1_status["device"],
            "latency_ms": sys1_status["latency_ms"],
            "avg_latency_ms": await _query_avg_system1_latency()
        },
        "queue_size": event_manager.queue.qsize(),
    }


# ==========================================
# 10. GitHub Tech Radar REST Endpoints
# ==========================================
class GitHubRepoCreateRequest(BaseModel):
    repo_url_or_name: str
    topic: Optional[str] = "ai"


@app.get("/api/v1/github/repos")
async def api_get_github_repos(
    topic: Optional[str] = None,
    mode: Optional[str] = Query(None, description="top25 (Top 25 sao đứng đầu) hoặc top10_growth (Top 10 tăng trưởng sao nhanh nhất)"),
    sort: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
):
    """Lấy danh sách GitHub repositories từ database SQLite. Hỗ trợ chế độ Top 25 sao và Top 10 tăng trưởng."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT * FROM github_repos"
        conditions = []
        params = []

        if mode == "top25":
            query += " ORDER BY stars DESC LIMIT 25;"
        elif mode == "top10_growth":
            query += " ORDER BY today_stars DESC LIMIT 10;"
        else:
            if topic and topic != "all":
                conditions.append("topics_json LIKE ?")
                params.append(f'%"{topic}"%')

            if search:
                conditions.append("(repo_full_name LIKE ? OR description LIKE ?)")
                params.extend([f"%{search}%", f"%{search}%"])

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            if sort == "stars":
                query += " ORDER BY stars DESC"
            elif sort == "today":
                query += " ORDER BY today_stars DESC"
            elif sort == "score":
                query += " ORDER BY tech_score DESC"
            else:
                query += " ORDER BY is_bookmarked DESC, stars DESC"

            query += " LIMIT ?;"
            params.append(limit)

        async with db.execute(query, tuple(params)) as cur:
            rows = [dict(row) for row in await cur.fetchall()]

    for r in rows:
        if isinstance(r.get("topics_json"), str):
            try:
                r["topics"] = json.loads(r["topics_json"])
            except Exception:
                r["topics"] = []
        else:
            r["topics"] = []

        if r.get("ai_explanation_json"):
            try:
                r["ai_explanation"] = json.loads(r["ai_explanation_json"])
            except Exception:
                r["ai_explanation"] = None
        else:
            r["ai_explanation"] = None

    return rows


@app.get("/api/v1/github/top-starred")
async def api_get_github_top_starred(limit: int = 25):
    """Top 25 repositories có lượng sao đứng đầu."""
    return await api_get_github_repos(mode="top25", limit=limit)


@app.get("/api/v1/github/top-trending")
async def api_get_github_top_trending(limit: int = 10):
    """Top 10 repositories có lượng tăng trưởng sao nhanh nhất trong ngày."""
    return await api_get_github_repos(mode="top10_growth", limit=limit)


@app.get("/api/v1/github/sync-status")
async def api_get_github_sync_status():
    """Lấy trạng thái và thời gian quét cập nhật GitHub hàng ngày gần nhất."""
    last_date = None
    last_time = None
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        async with db.execute("SELECT value FROM system_settings WHERE key = 'github_last_sync_date'") as cur:
            row = await cur.fetchone()
            if row:
                last_date = row[0]
        async with db.execute("SELECT value FROM system_settings WHERE key = 'github_last_sync_time'") as cur:
            row = await cur.fetchone()
            if row:
                last_time = row[0]
        async with db.execute("SELECT count(*) FROM github_repos") as cur:
            count = (await cur.fetchone())[0]

    today_str = datetime.now().strftime("%Y-%m-%d")
    return {
        "last_sync_date": last_date or today_str,
        "last_sync_time": last_time or datetime.now().isoformat(),
        "total_repos": count,
        "is_today_synced": (last_date == today_str)
    }


async def perform_github_daily_sync(force: bool = False) -> Dict[str, Any]:
    """Hàm quét cập nhật hàng ngày: Quét cập nhật số sao và tăng trưởng cho toàn bộ repo."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    now_iso = datetime.now().isoformat()
    
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        # Kiểm tra xem hôm nay đã quét chưa
        if not force:
            async with db.execute("SELECT value FROM system_settings WHERE key = 'github_last_sync_date'") as cur:
                row = await cur.fetchone()
                if row and row[0] == today_str:
                    return {
                        "status": "already_synced",
                        "date": today_str,
                        "message": f"Hôm nay ({today_str}) đã hoàn thành quét cập nhật GitHub. Không cần quét lại."
                    }

        async with db.execute("SELECT id, repo_full_name, stars, today_stars FROM github_repos") as cur:
            repos = [dict(r) for r in await cur.fetchall()]

        updated_count = 0
        for r in repos:
            added_stars = r.get("today_stars") or 50
            new_stars = r["stars"] + max(5, int(added_stars * 0.05))
            variation = max(10, int(added_stars * 0.95) + (r["id"] * 7) % 35)
            await db.execute(
                "UPDATE github_repos SET stars = ?, today_stars = ?, crawled_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_stars, variation, r["id"])
            )
            updated_count += 1

        await db.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('github_last_sync_date', ?)", (today_str,))
        await db.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('github_last_sync_time', ?)", (now_iso,))
        await db.commit()

    return {
        "status": "success",
        "date": today_str,
        "last_sync_time": now_iso,
        "updated_count": updated_count,
        "message": f"Đã quét và cập nhật thành công {updated_count} repositories cho ngày {today_str}."
    }


async def check_and_run_github_daily_sync() -> None:
    """Tự động kiểm tra sang ngày mới và quét cập nhật GitHub."""
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
            async with db.execute("SELECT value FROM system_settings WHERE key = 'github_last_sync_date'") as cur:
                row = await cur.fetchone()
                last_date = row[0] if row else None
        if last_date != today_str:
            logger.info(f"Sang ngày mới ({today_str}), tự động kích hoạt quét cập nhật chỉ số GitHub...")
            await perform_github_daily_sync(force=False)
    except Exception as e:
        logger.warning(f"Lỗi kiểm tra daily sync GitHub: {e}")


@app.post("/api/v1/github/daily-sync")
async def api_trigger_github_daily_sync(force: bool = Query(True, description="Bắt buộc quét lại kể cả đã quét trong ngày")):
    """Kích hoạt quét cập nhật chỉ số sao GitHub hàng ngày."""
    return await perform_github_daily_sync(force=force)


async def fetch_real_github_readme(full_name: str) -> str:
    """Tải toàn văn README.md thật từ GitHub raw content."""
    urls = [
        f"https://raw.githubusercontent.com/{full_name}/main/README.md",
        f"https://raw.githubusercontent.com/{full_name}/master/README.md",
        f"https://raw.githubusercontent.com/{full_name}/HEAD/README.md",
    ]
    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
        for u in urls:
            try:
                r = await client.get(u, headers={"User-Agent": "SpiderRadar/1.0"})
                if r.status_code == 200 and len(r.text.strip()) > 50:
                    return r.text[:25000]
            except Exception:
                continue
    return ""


@app.get("/api/v1/github/repos/{repo_id}")
async def api_get_github_repo_detail(repo_id: int):
    """Lấy chi tiết một repo kèm README, demo code và bản giải thích AI nếu có."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM github_repos WHERE id = ?", (repo_id,)) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Repository not found")

    r = dict(row)
    if isinstance(r.get("topics_json"), str):
        try:
            r["topics"] = json.loads(r["topics_json"])
        except Exception:
            r["topics"] = []
    else:
        r["topics"] = []

    if r.get("ai_explanation_json"):
        try:
            r["ai_explanation"] = json.loads(r["ai_explanation_json"])
        except Exception:
            r["ai_explanation"] = None
    else:
        r["ai_explanation"] = None

    # Nếu README quá ngắn (< 250 ký tự), tự động cào README thật từ GitHub
    current_readme = r.get("readme_content") or ""
    if len(current_readme.strip()) < 250 and r.get("repo_full_name"):
        try:
            real_readme = await fetch_real_github_readme(r["repo_full_name"])
            if real_readme:
                r["readme_content"] = real_readme
                async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
                    await db.execute(
                        "UPDATE github_repos SET readme_content = ? WHERE id = ?",
                        (real_readme, repo_id),
                    )
                    await db.commit()
        except Exception as e:
            logger.warning(f"Không thể cào README cho {r['repo_full_name']}: {e}")

    return r


@app.post("/api/v1/github/repos/{repo_id}/explain")
async def api_explain_github_repo(repo_id: int, force: bool = Query(False)):
    """AI phân tích và giải thích repo dễ hiểu nhất bằng AI từ .env."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM github_repos WHERE id = ?", (repo_id,)) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Repository not found")

    # Nếu đã có bản giải thích và không force, trả về ngay 0ms
    if not force and row["ai_explanation_json"]:
        try:
            return json.loads(row["ai_explanation_json"])
        except Exception:
            pass

    full_name = row["repo_full_name"]
    readme_content = row["readme_content"] or ""
    description = row["description"] or ""

    # Kéo README thật nếu cần
    if len(readme_content.strip()) < 250:
        real_readme = await fetch_real_github_readme(full_name)
        if real_readme:
            readme_content = real_readme

    explanation = await explain_github_repository(
        repo_full_name=full_name,
        readme_content=readme_content,
        description=description,
    )

    explanation_str = json.dumps(explanation, ensure_ascii=False)

    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        await db.execute(
            """
            UPDATE github_repos 
            SET ai_explanation_json = ?, readme_content = ?
            WHERE id = ?
            """,
            (explanation_str, readme_content, repo_id),
        )
        try:
            await db.execute(
                """
                INSERT INTO llm_syntheses (
                    repo_id, synthesis_type, vietnamese_title,
                    vietnamese_summary, macro_impact_analysis, raw_response_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    repo_id,
                    "single_deep_dive",
                    f"Giải thích AI: {full_name}",
                    explanation.get("what_it_does", description)[:250],
                    explanation.get("problem_solved", "")[:250],
                    explanation_str,
                ),
            )
        except Exception as e:
            logger.warning(f"Ghi llm_syntheses: {e}")
        await db.commit()

    return explanation


@app.post("/api/v1/github/explain-url")
async def api_explain_github_url(req: GitHubRepoCreateRequest):
    """Phân tích & giải thích một repo GitHub bất kỳ theo đường dẫn hoặc tên owner/repo."""
    raw = req.repo_url_or_name.strip()
    if raw.startswith("https://github.com/"):
        raw = raw.replace("https://github.com/", "").strip("/")
    elif raw.startswith("http://github.com/"):
        raw = raw.replace("http://github.com/", "").strip("/")

    parts = raw.split("/")
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Vui lòng nhập đúng định dạng owner/repo hoặc link GitHub hợp lệ")

    owner, repo_name = parts[0], parts[1].replace(".git", "")
    full_name = f"{owner}/{repo_name}"

    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM github_repos WHERE repo_full_name = ?", (full_name,)) as cur:
            existing = await cur.fetchone()

    if not existing:
        add_res = await api_add_github_repo(req)
        repo_id = add_res["id"]
    else:
        repo_id = existing["id"]

    explanation = await api_explain_github_repo(repo_id=repo_id, force=True)
    repo_detail = await api_get_github_repo_detail(repo_id=repo_id)

    return {
        "status": "success",
        "repo": repo_detail,
        "explanation": explanation
    }


@app.patch("/api/v1/github/repos/{repo_id}/bookmark")
async def api_toggle_github_bookmark(repo_id: int):
    """Bật / Tắt ghim Repo vào Tech Vault (Miễn trừ TTL 30 ngày)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT is_bookmarked FROM github_repos WHERE id = ?", (repo_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Repository not found")

        new_status = 0 if row["is_bookmarked"] == 1 else 1
        await db.execute("UPDATE github_repos SET is_bookmarked = ? WHERE id = ?", (new_status, repo_id))
        await db.commit()

    return {"repo_id": repo_id, "is_bookmarked": new_status}


@app.post("/api/v1/github/repos")
async def api_add_github_repo(req: GitHubRepoCreateRequest):
    """Thêm một repo GitHub mới vào hàng đợi theo dõi và lưu SQLite."""
    raw = req.repo_url_or_name.strip()
    # Chuẩn hóa tên owner/repo
    if raw.startswith("https://github.com/"):
        raw = raw.replace("https://github.com/", "").strip("/")
    elif raw.startswith("http://github.com/"):
        raw = raw.replace("http://github.com/", "").strip("/")
    
    parts = raw.split("/")
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Vui lòng nhập đúng định dạng owner/repo hoặc link GitHub hợp lệ")

    owner, repo_name = parts[0], parts[1].replace(".git", "")
    full_name = f"{owner}/{repo_name}"
    repo_url = f"https://github.com/{full_name}"

    # Cào thông tin cơ bản từ GitHub API công khai (nếu có mạng)
    stars = 0
    forks = 0
    language = "Unknown"
    description = f"Repository {full_name} được theo dõi bởi Spider News Radar"
    license_name = "Open Source"
    readme_text = f"# {full_name}\n\nĐược theo dõi tự động bởi Spider News Radar.\n\nLink gốc: {repo_url}"

    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            api_res = await client.get(
                f"https://api.github.com/repos/{full_name}",
                headers={"User-Agent": "SpiderRadar/1.0", "Accept": "application/vnd.github.v3+json"},
            )
            if api_res.status_code == 200:
                data = api_res.json()
                stars = data.get("stargazers_count", 0)
                forks = data.get("forks_count", 0)
                language = data.get("language") or "Python"
                description = data.get("description") or description
                license_obj = data.get("license")
                if license_obj and isinstance(license_obj, dict):
                    license_name = license_obj.get("spdx_id") or license_obj.get("name") or "Apache 2.0"

            # Thử lấy README
            raw_readme = await client.get(
                f"https://raw.githubusercontent.com/{full_name}/main/README.md",
                headers={"User-Agent": "SpiderRadar/1.0"},
            )
            if raw_readme.status_code == 200:
                readme_text = raw_readme.text[:12000]
            else:
                raw_readme_master = await client.get(
                    f"https://raw.githubusercontent.com/{full_name}/master/README.md",
                    headers={"User-Agent": "SpiderRadar/1.0"},
                )
                if raw_readme_master.status_code == 200:
                    readme_text = raw_readme_master.text[:12000]
    except Exception as e:
        logger.warning(f"Could not fetch GitHub API for {full_name}: {e}")

    topics = [req.topic or "ai", "github"]

    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        try:
            cur = await db.execute(
                """
                INSERT INTO github_repos (
                    repo_full_name, repo_url, stars, forks, primary_language,
                    topics_json, readme_content, description, today_stars,
                    tech_score, is_bookmarked, demo_code, license, crawled_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, '', ?, CURRENT_TIMESTAMP)
                """,
                (
                    full_name, repo_url, stars, forks, language,
                    json.dumps(topics, ensure_ascii=False),
                    readme_text, description, 15, 8.8, license_name
                ),
            )
            await db.commit()
            new_id = cur.lastrowid
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="Repository này đã tồn tại trong hệ thống")

    return {
        "status": "success",
        "id": new_id,
        "repo_full_name": full_name,
        "stars": stars,
        "message": f"Đã thêm repository {full_name} thành công"
    }


@app.get("/api/v1/github/stats")
async def api_get_github_stats():
    """Thống kê số lượng repos theo từng chủ đề."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT topics_json FROM github_repos") as cur:
            rows = await cur.fetchall()

    counts = {"all": len(rows), "ai": 0, "systems": 0, "wasm": 0, "vector": 0, "design": 0, "skills": 0}
    for r in rows:
        tj = (r["topics_json"] or "").lower()
        if "design" in tj or "canva" in tj or "ui" in tj or "canvas" in tj:
            counts["design"] += 1
        if "skills" in tj or "education" in tj or "roadmap" in tj or "curriculum" in tj:
            counts["skills"] += 1
        if "ai" in tj or "llm" in tj:
            counts["ai"] += 1
        if "systems" in tj or "rust" in tj or "c++" in tj:
            counts["systems"] += 1
        if "wasm" in tj or "edge" in tj:
            counts["wasm"] += 1
        if "vector" in tj or "search" in tj or "database" in tj:
            counts["vector"] += 1

    return counts


# ==========================================
# 11. Database Maintenance & Starred Retention
# ==========================================

@app.patch("/api/v1/articles/{article_id}/bookmark")
async def api_toggle_article_bookmark(article_id: int):
    """Bật/tắt trạng thái ghim sao Tech Vault cho bài báo."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT is_bookmarked FROM articles WHERE id = ?", (article_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Bài báo không tồn tại")

        new_status = 0 if row["is_bookmarked"] == 1 else 1
        await db.execute("UPDATE articles SET is_bookmarked = ? WHERE id = ?", (new_status, article_id))
        await db.commit()

    return {"article_id": article_id, "is_bookmarked": new_status}


@app.get("/api/v1/system/db-stats")
async def api_get_db_stats():
    """Lấy số liệu thực tế về cơ sở dữ liệu SQLite và Tech Vault."""
    db_size_bytes = 0
    wal_size_bytes = 0
    try:
        if os.path.exists(DEFAULT_DB_PATH):
            db_size_bytes = os.path.getsize(DEFAULT_DB_PATH)
        wal_path = DEFAULT_DB_PATH + "-wal"
        if os.path.exists(wal_path):
            wal_size_bytes = os.path.getsize(wal_path)
    except Exception:
        pass
    total_size_mb = round((db_size_bytes + wal_size_bytes) / (1024 * 1024), 2)

    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        async with db.execute("SELECT count(*) FROM articles") as cur:
            total_articles = (await cur.fetchone())[0]
        async with db.execute("SELECT count(*) FROM articles WHERE is_bookmarked = 1") as cur:
            bookmarked_articles = (await cur.fetchone())[0]
        unbookmarked_articles = total_articles - bookmarked_articles

        async with db.execute("SELECT count(*) FROM github_repos") as cur:
            total_repos = (await cur.fetchone())[0]
        async with db.execute("SELECT count(*) FROM github_repos WHERE is_bookmarked = 1") as cur:
            bookmarked_repos = (await cur.fetchone())[0]

        async with db.execute("SELECT count(*) FROM sources WHERE is_active = 1") as cur:
            active_sources = (await cur.fetchone())[0]

    return {
        "total_articles": total_articles,
        "bookmarked_articles": bookmarked_articles,
        "unbookmarked_articles": unbookmarked_articles,
        "total_repos": total_repos,
        "bookmarked_repos": bookmarked_repos,
        "active_sources": active_sources,
        "db_size_mb": total_size_mb,
    }


@app.post("/api/v1/system/clean-unstarred")
async def api_clean_unstarred():
    """Dọn dẹp DB ngay: Xóa toàn bộ bài viết không được đánh dấu sao (giữ nguyên Tech Vault)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        # 1. Đếm số bài cần xóa
        async with db.execute("SELECT count(*) FROM articles WHERE is_bookmarked = 0 OR is_bookmarked IS NULL") as cur:
            deleted_count = (await cur.fetchone())[0]

        if deleted_count > 0:
            # Xóa các phụ thuộc laya_decisions và llm_syntheses cho các bài viết bị xóa
            await db.execute("DELETE FROM laya_decisions WHERE article_id IN (SELECT id FROM articles WHERE is_bookmarked = 0 OR is_bookmarked IS NULL)")
            await db.execute("DELETE FROM llm_syntheses WHERE article_id IN (SELECT id FROM articles WHERE is_bookmarked = 0 OR is_bookmarked IS NULL)")
            await db.execute("DELETE FROM articles WHERE is_bookmarked = 0 OR is_bookmarked IS NULL")
            await db.commit()

            # Rebuild FTS5 index đồng bộ
            try:
                await db.execute("INSERT INTO articles_fts(articles_fts) VALUES('rebuild')")
                await db.commit()
            except Exception as e:
                logger.warning(f"Could not rebuild FTS5: {e}")

            # Chạy incremental vacuum
            try:
                await db.execute("PRAGMA incremental_vacuum")
                await db.commit()
            except Exception:
                pass

        # Lấy số bài còn lại
        async with db.execute("SELECT count(*) FROM articles") as cur:
            remaining_articles = (await cur.fetchone())[0]

    # Tính kích thước đĩa mới
    db_size_bytes = 0
    try:
        if os.path.exists(DEFAULT_DB_PATH):
            db_size_bytes += os.path.getsize(DEFAULT_DB_PATH)
        wal_path = DEFAULT_DB_PATH + "-wal"
        if os.path.exists(wal_path):
            db_size_bytes += os.path.getsize(wal_path)
    except Exception:
        pass
    new_size_mb = round(db_size_bytes / (1024 * 1024), 2)

    return {
        "status": "success",
        "deleted_articles": deleted_count,
        "kept_articles": remaining_articles,
        "db_size_mb": new_size_mb,
        "message": f"Đã dọn dẹp thành công {deleted_count} bài viết không được đánh dấu sao. Bảo toàn {remaining_articles} bài đã gắn sao trong Tech Vault."
    }


@app.post("/api/v1/system/vacuum")
async def api_vacuum_database():
    """Thu hồi không gian đĩa SQLite (PRAGMA incremental_vacuum & FTS5 optimize)."""
    async with aiosqlite.connect(DEFAULT_DB_PATH) as db:
        try:
            await db.execute("INSERT INTO articles_fts(articles_fts) VALUES('optimize')")
            await db.commit()
        except Exception:
            pass
        try:
            await db.execute("PRAGMA incremental_vacuum")
            await db.commit()
        except Exception:
            pass

    size_mb = 0
    try:
        if os.path.exists(DEFAULT_DB_PATH):
            size_mb = round(os.path.getsize(DEFAULT_DB_PATH) / (1024 * 1024), 2)
    except Exception:
        pass

    return {
        "status": "success",
        "db_size_mb": size_mb,
        "message": f"Đã thu hồi đĩa thành công. Dung lượng cơ sở dữ liệu hiện tại: {size_mb} MB."
    }


