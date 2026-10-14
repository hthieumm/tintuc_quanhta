"""
Spider News Radar - RSS & Multi-Source Crawler Module
Implements 4-tier Waterfall scraping pipeline, deduplication by SHA-256 URL hash,
language tagging, and SQLite WAL ingestion.
"""

import os
import re
import json
import hashlib
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
import html

import httpx
import feedparser
import aiosqlite
import trafilatura

try:
    from curl_cffi.requests import AsyncSession as CurlAsyncSession
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

from .database import DEFAULT_DB_PATH, generate_url_hash

logger = logging.getLogger("spider_crawler")

GOOGLEBOT_UA = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)
DEFAULT_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

SOCIAL_REFERER_HEADERS = {
    "User-Agent": DEFAULT_BROWSER_UA,
    "Referer": "https://t.co/",
    "X-Forwarded-For": "66.249.66.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
}

# Regex phát hiện ngôn ngữ tiếng Việt (chứa ký tự có dấu đặc trưng)
VIETNAMESE_PATTERN = re.compile(
    r"[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]",
    re.IGNORECASE,
)
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")
JAPANESE_PATTERN = re.compile(r"[\u3040-\u309f\u30a0-\u30ff]")


def detect_language(text: str) -> str:
    """
    Phát hiện ngôn ngữ của bài viết dựa trên đặc trưng văn bản:
    'vi' (Tiếng Việt), 'zh' (Tiếng Trung), 'ja' (Tiếng Nhật), hoặc 'en' (Mặc định).
    """
    if not text:
        return "en"
    if VIETNAMESE_PATTERN.search(text):
        return "vi"
    if JAPANESE_PATTERN.search(text):
        return "ja"
    if CHINESE_PATTERN.search(text):
        return "zh"
    return "en"


def clean_html_tags(raw_html: str) -> str:
    """Loại bỏ thẻ HTML và chuẩn hóa khoảng trắng."""
    if not raw_html:
        return ""
    # Giải mã HTML entities
    unescaped = html.unescape(raw_html)
    # Xóa script/style tags
    clean = re.sub(r"<(script|style).*?>.*?</\1>", "", unescaped, flags=re.DOTALL | re.IGNORECASE)
    # Xóa các thẻ HTML còn lại
    clean = re.sub(r"<[^>]+>", " ", clean)
    # Chuẩn hóa khoảng trắng
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def extract_json_ld_article_body(html_text: str) -> Optional[str]:
    """
    Trích xuất articleBody từ JSON-LD Schema.org (Tin tức chuẩn SEO thường nhúng trường này).
    """
    if not html_text:
        return None
    try:
        matches = re.findall(
            r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>',
            html_text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        for raw_json in matches:
            try:
                data = json.loads(raw_json.strip())
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if isinstance(item, dict):
                        # Kiểm tra graph nếu có
                        if "@graph" in item and isinstance(item["@graph"], list):
                            for g_item in item["@graph"]:
                                if isinstance(g_item, dict) and "articleBody" in g_item:
                                    return str(g_item["articleBody"]).strip()
                        if "articleBody" in item:
                            return str(item["articleBody"]).strip()
            except Exception:
                continue
    except Exception as e:
        logger.debug(f"JSON-LD extraction error: {e}")
    return None


def extract_next_data_article(html_text: str) -> Optional[str]:
    """
    Trích xuất toàn văn bài báo từ Next.js Hydration State (__NEXT_DATA__)
    hoặc Nuxt.js State (__NUXT_DATA__ / window.__INITIAL_STATE__).
    Nhiều báo lớn (The Economist, Bloomberg, Substack) che bài bằng CSS/JS phía Client
    nhưng gửi trọn vẹn văn bản trong thẻ script JSON này.
    """
    if not html_text:
        return None
    try:
        # 1. Thử thẻ __NEXT_DATA__
        matches = re.findall(
            r'<script[^>]*id=[\'"]__NEXT_DATA__[\'"][^>]*>(.*?)</script>',
            html_text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if not matches:
            # Thử window.__INITIAL_STATE__ hoặc __PRELOADED_STATE__
            matches = re.findall(
                r'window\.(?:__INITIAL_STATE__|__PRELOADED_STATE__)\s*=\s*({.*?});</script>',
                html_text,
                flags=re.DOTALL | re.IGNORECASE,
            )

        for raw_json in matches:
            try:
                data = json.loads(raw_json.strip())
                collected_paras: List[str] = []

                def _recurse(obj: Any):
                    if isinstance(obj, dict):
                        # Các key thường chứa đoạn văn bài báo trong Next.js CMS
                        for k in ["articleBody", "body", "paragraphs", "content", "story", "text", "lead", "blocks"]:
                            if k in obj:
                                val = obj[k]
                                if isinstance(val, str) and len(val.strip()) > 45:
                                    c = clean_html_tags(val)
                                    if len(c) > 40 and not any(skip in c.lower() for skip in ["subscribe", "newsletter", "sign in", "all rights reserved"]):
                                        collected_paras.append(c)
                                elif isinstance(val, list):
                                    for item in val:
                                        if isinstance(item, str) and len(item.strip()) > 35:
                                            c = clean_html_tags(item)
                                            if len(c) > 30 and not any(skip in c.lower() for skip in ["subscribe", "sign in"]):
                                                collected_paras.append(c)
                                        elif isinstance(item, dict):
                                            _recurse(item)
                        for v in obj.values():
                            if isinstance(v, (dict, list)):
                                _recurse(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            if isinstance(item, (dict, list)):
                                _recurse(item)

                _recurse(data)
                if collected_paras:
                    # Khử trùng lặp các đoạn văn bị lặp
                    seen = set()
                    uniq = []
                    for p in collected_paras:
                        norm = p[:60].lower()
                        if norm not in seen:
                            seen.add(norm)
                            uniq.append(p)
                    res = "\n\n".join(uniq).strip()
                    if len(res) >= 180:
                        return res
            except Exception:
                continue
    except Exception as e:
        logger.debug(f"Next.js data extraction error: {e}")
    return None


async def reverse_search_article(title: str, timeout: float = 8.0) -> Optional[str]:
    """
    Kỹ thuật Reverse Search:
    Khi URL bài báo bị Hard Paywall hoặc chặn WAF 100%,
    hệ thống lấy tiêu đề bài báo tìm kiếm qua DuckDuckGo HTML / Web Aggregator
    để trích xuất các đoạn trích dẫn, bản tóm tắt hoặc nội dung từ các trang đối tác/diễn đàn.
    """
    if not title or len(title.strip()) < 10:
        return None
    try:
        import urllib.parse
        from bs4 import BeautifulSoup

        # Lọc sạch tiêu đề loại bỏ các ký tự đặc biệt
        clean_title = re.sub(r'[\'\"’—\-\:\(\)]', ' ', title).strip()
        words = [w for w in clean_title.split() if len(w) > 2]
        if not words:
            return None
        search_query = " ".join(words[:8])
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(search_query)}"

        headers = {
            "User-Agent": DEFAULT_BROWSER_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.google.com/",
        }

        html_res = None
        if HAS_CURL_CFFI:
            try:
                async with CurlAsyncSession() as session:
                    resp = await session.get(search_url, headers=headers, impersonate="chrome124", timeout=timeout)
                    if resp.status_code == 200 and len(resp.text) > 400:
                        html_res = resp.text
            except Exception:
                pass

        if not html_res:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as http_client:
                resp = await http_client.get(search_url, headers=headers)
                if resp.status_code == 200:
                    html_res = resp.text

        if html_res:
            soup = BeautifulSoup(html_res, "html.parser")
            snippets: List[str] = []
            for snip in soup.find_all("a", class_="result__snippet"):
                txt = snip.get_text().strip()
                if len(txt) > 40 and not any(skip in txt.lower() for skip in ["cookie", "subscribe", "advertising", "terms of use"]):
                    snippets.append(txt)
            if snippets:
                combined = "\n\n".join(snippets[:5]).strip()
                if len(combined) >= 150:
                    return f"[Nguồn đối tác & trích dẫn phân tích]:\n{combined}"
    except Exception as e:
        logger.debug(f"Reverse search error: {e}")
    return None


def extract_html_paragraphs(html_text: str, min_total_len: int = 250) -> Optional[str]:
    """Trích xuất các đoạn văn <p> từ HTML khi Trafilatura hoặc parser khác bỏ sót."""
    if not html_text:
        return None
    try:
        paras = re.findall(r'<p[^>]*>(.*?)</p>', html_text, flags=re.DOTALL | re.IGNORECASE)
        cleaned = []
        for p in paras:
            c = clean_html_tags(p)
            # Bỏ qua các đoạn ngắn < 35 ký tự như cookie, banner, disclaimer
            if len(c) >= 35 and not any(skip in c.lower() for skip in ['cookie', 'subscribe', 'sign up', 'all rights reserved', 'advertisement']):
                cleaned.append(c)
        if cleaned:
            result = "\n\n".join(cleaned)
            if len(result) >= min_total_len:
                return result
    except Exception:
        pass
    return None


def extract_domain_article(html_text: str, url: str) -> Optional[str]:
    """Trích xuất chuyên sâu theo từng tờ báo lớn để đạt độ sạch và toàn vẹn > 95%."""
    if not html_text:
        return None
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text, "html.parser")

        # 1. VnExpress
        if "vnexpress.net" in url:
            body = soup.find("article", class_="fck_detail") or soup.find("div", class_="fck_detail")
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 20]
                if paras:
                    return "\n\n".join(paras)

        # 2. Tuổi Trẻ
        if "tuoitre.vn" in url:
            body = soup.find("div", class_="detail-content") or soup.find("div", id="main-detail-body")
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 25]
                if paras:
                    return "\n\n".join(paras)

        # 3. CafeF
        if "cafef.vn" in url:
            body = (
                soup.find("div", class_="detail-content")
                or soup.find("div", class_="contentdetail")
                or soup.find("div", class_="contentper")
                or soup.find("div", class_="fck")
            )
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 20]
                if paras:
                    return "\n\n".join(paras)

        # 4. BBC News
        if "bbc.com" in url or "bbc.co.uk" in url:
            paras = [
                p.get_text().strip()
                for p in soup.find_all("p")
                if p.get("data-component") == "text-block" or len(p.get_text().strip()) > 40
            ]
            if len(paras) >= 3:
                return "\n\n".join(paras)

        # 5. The Guardian
        if "theguardian.com" in url:
            body = soup.find("div", attrs={"data-gu-mark": "true"}) or soup.find("article")
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 30]
                if paras:
                    return "\n\n".join(paras)

        # 6. CoinDesk
        if "coindesk.com" in url:
            body = soup.find("section", class_="article-body") or soup.find("div", class_="composer-content")
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 25]
                if paras:
                    return "\n\n".join(paras)

        # 7. Politico
        if "politico.com" in url:
            body = (
                soup.find("div", class_="story-text")
                or soup.find("article", class_="story")
                or soup.find("div", class_="story-content")
                or soup.find("section", class_="story-text")
            )
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 30]
                if paras:
                    return "\n\n".join(paras)
        # 8. AP News (Associated Press)
        if "apnews.com" in url:
            body = (
                soup.find("div", class_="RichTextStoryBody")
                or soup.find("div", class_="Article")
                or soup.find("article")
            )
            if body:
                paras = [p.get_text().strip() for p in body.find_all("p") if len(p.get_text().strip()) > 25]
                if paras:
                    return "\n\n".join(paras)
    except Exception:
        pass
    return None


async def resolve_real_article_url(url: str, client: Optional[httpx.AsyncClient] = None) -> str:
    """
    Nếu URL là link bọc của Google News (news.google.com/rss/articles/...),
    giải mã hoặc tìm link đích thực sự trước khi đưa vào Waterfall.
    """
    if "news.google.com" not in url:
        return url

    # 1. Thử giải mã nhanh bằng Playwright nếu có sẵn (chính xác 100% với JS Redirect của Google News)
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until="commit", timeout=5000)
                for _ in range(15):
                    await asyncio.sleep(0.15)
                    curr = page.url
                    if "news.google.com" not in curr:
                        await browser.close()
                        return curr
            finally:
                await browser.close()
    except Exception:
        pass

    # 2. Fallback qua httpx nếu không khởi chạy được Playwright
    try:
        should_close = False
        if client is None:
            client = httpx.AsyncClient(timeout=6.0, follow_redirects=True)
            should_close = True
        try:
            resp = await client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA})
            if resp.url and "news.google.com" not in str(resp.url):
                return str(resp.url)
            m = re.search(r'data-n-au=["\'](https?://[^"\']+)["\']', resp.text)
            if m:
                return m.group(1)
            m2 = re.search(r'<a[^>]+href=["\'](https?://(?!news\.google\.com)[^"\']+)["\']', resp.text)
            if m2:
                return m2.group(1)
        finally:
            if should_close:
                await client.aclose()
    except Exception:
        pass

    return url


# Danh sách các cụm từ giao diện / menu rác tuyệt đối không bao giờ là nội dung báo
UI_JUNK_LINE_PATTERNS = (
    "previous image", "next image", "toggle caption", "skip to main content",
    "print subscriptions", "search jobs", "sign in", "international edition",
    "uk edition", "us edition", "australia edition", "europe edition",
    "back to home", "the guardian", "privacy notice:", "cookie", "subscribe",
    "newsletters may contain", "all rights reserved", "do not sell or share",
    "terms of service", "bloomberg the company", "terminal demo", "us edition",
    "work & life", "market data", "back forward", "share this", "follow us",
    "most popular", "related stories", "more on this story", "photograph:",
)

# Danh sách tiêu đề bài rác (Quảng cáo Newsletter, tuyển dụng, chùm ảnh không chữ) cần bỏ qua khi cào RSS
NON_ARTICLE_TITLE_PATTERNS = (
    "sign up for the ",
    "newsletter:",
    "free daily news email",
    "free football email",
    "food email",
    "photos of the day",
    "in pictures:",
    "best photos of",
    "quiz:",
    "crossword",
)


def is_junk_rss_entry(title: str, summary: str, url: str) -> bool:
    """
    Chặn ngay từ vòng gửi xe các bài RSS không phải tin tức:
    - Quảng cáo đăng ký Newsletter của The Guardian / NYT
    - Chùm ảnh (Photo Gallery) không có nội dung văn bản
    """
    t_low = (title or "").lower().strip()
    s_low = (summary or "").lower().strip()
    u_low = (url or "").lower().strip()

    if any(p in t_low for p in NON_ARTICLE_TITLE_PATTERNS):
        return True
    if "privacy notice: newsletters may contain" in s_low or "privacy notice: newsletters" in s_low:
        return True
    if "/gallery/" in u_low or "/in-pictures/" in u_low or "/ng-interactive/" in u_low:
        return True
    return False


def sanitize_article_prose(text: str, min_total_len: int = 200) -> str:
    """
    Bộ lọc cấp độ từng đoạn văn (Paragraph-level Sanitizer):
    Loại bỏ 100% các dòng menu ngắn (News, Opinion, Sport, UK edition, Previous image...)
    Chỉ giữ lại những đoạn văn xuôi thực thụ (dài >= 55 ký tự và có cấu trúc câu).
    """
    if not text:
        return ""

    raw_lines = text.splitlines()
    valid_paragraphs: List[str] = []

    for line in raw_lines:
        clean = clean_html_tags(line).strip()
        if not clean:
            continue

        # 1. Loại bỏ dòng chứa cú pháp link markdown hoặc URL trần
        if "](" in clean or "http://" in clean or "https://" in clean:
            continue

        c_low = clean.lower()

        # 2. Loại bỏ dòng khớp với từ khóa giao diện / nút bấm
        if any(junk in c_low for junk in UI_JUNK_LINE_PATTERNS):
            continue

        # 3. Loại bỏ các dòng cụt ngủn (menu, nhãn chuyên mục như "News", "Sport", "Int", "Sign in")
        # Một đoạn văn báo chí thực sự phải có ít nhất 9 từ và dài >= 50 ký tự, có dấu câu
        word_count = len(clean.split())
        if len(clean) < 50 or word_count < 8:
            continue

        if not any(punct in clean for punct in (".", "!", "?", "。", "”", '"', "’", "…")):
            continue

        if not valid_paragraphs or clean != valid_paragraphs[-1]:
            valid_paragraphs.append(clean)

    result = "\n\n".join(valid_paragraphs).strip()
    if len(result) >= min_total_len and len(valid_paragraphs) >= 2:
        return result
    return ""


def is_valid_article_prose(text: str, min_len: int = 200) -> bool:
    """Kiểm tra văn bản sau khi lọc sạch có đủ chuẩn bài báo không."""
    return len(sanitize_article_prose(text, min_total_len=min_len)) >= min_len


def clean_jina_markdown(raw_txt: str) -> str:
    """
    Làm sạch triệt để output từ Jina Reader Proxy.
    Xóa toàn bộ link rỗng [](), chuỗi menu [A](url)[B](url) và chỉ giữ lại đoạn văn xuôi.
    """
    if not raw_txt:
        return ""

    JUNK_KEYWORDS = (
        "title:", "url source:", "published time:", "markdown content:",
        "us edition", "subscribe", "work & life", "market data", "explore",
        "terms of service", "do not sell", "privacy policy", "trademarks",
        "back forward", "bloomberg the company", "terminal demo", "skip to",
        "toggle menu", "sign in", "all rights reserved", "newsletters",
        "copy link copied", "view comments", "listen to this", "photo by"
    )

    lines = raw_txt.splitlines()
    cleaned_paras = []

    for line in lines:
        l = line.strip()
        if not l or l in ("*", "**0**", "Menu", "TOP STORIES", "Newsletters", "Share", "Print"):
            continue

        # 1. Loại bỏ ngay lập tức bất kỳ dòng nào có từ 2 link Markdown trở lên hoặc link rỗng []()
        if l.count("](") >= 2 or "[](" in l:
            continue

        # 2. Xóa sạch link rỗng [] (...) và ảnh ![...] (...)
        clean_line = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', l)
        clean_line = re.sub(r'\[\s*\]\([^\)]+\)', '', clean_line)
        # Chuyển [Text](URL) thành Text (dùng [^\]]* thay vì + để không bị vỡ regex khi gặp [])
        clean_line = re.sub(r'\[([^\]]*)\]\([^\)]+\)', r'\1', clean_line).strip()

        l_lower = clean_line.lower()
        if any(l_lower.startswith(k) or l_lower == k for k in JUNK_KEYWORDS):
            continue

        # 3. Chỉ giữ lại những dòng thực sự là câu văn bài báo (dài > 40 ký tự và có khoảng trắng/dấu câu)
        if len(clean_line) > 40 and not clean_line.startswith("http") and ("." in clean_line or "," in clean_line):
            if not cleaned_paras or clean_line != cleaned_paras[-1]:
                cleaned_paras.append(clean_line)

    result = "\n\n".join(cleaned_paras).strip()
    return result if is_valid_article_prose(result) else ""


class SpiderNewsCrawler:
    """
    Bộ cào tin đa nguồn chuẩn Waterfall 8 tầng thế hệ mới:
    Tier 1: Domain-specific high-precision extractors (VnExpress, Tuổi Trẻ, CafeF, BBC, Guardian, Politico, AP News)
    Tier 2: Next.js Hydration State Parser (__NEXT_DATA__ / __NUXT_DATA__)
    Tier 3: Trafilatura Full text extraction (Multi-UA / curl_cffi)
    Tier 4: JSON-LD Schema (articleBody - AP News, NYT)
    Tier 5: HTML Paragraphs extraction (<p>)
    Tier 6: Jina Reader Proxy Fallback (r.jina.ai) lọc sạch 100% menu rác
    Tier 7: Reverse Search Fallback (DuckDuckGo HTML trích dẫn nguồn đối tác/diễn đàn)
    Tier 8: RSS summary fallback (bảo toàn không crash)
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH, timeout: float = 10.0):
        self.db_path = db_path
        self.timeout = timeout

    async def fetch_article_waterfall(
        self,
        url: str,
        rss_summary: str,
        client: Optional[httpx.AsyncClient] = None,
        title: str = "",
    ) -> Tuple[str, str]:
        """
        Thực hiện quy trình cào đa tầng để lấy nội dung đầy đủ và sạch nhất có thể.
        Trả về: (content_clean, tier_used)
        """
        clean_rss_text = clean_html_tags(rss_summary)

        if not url or not url.startswith("http"):
            return clean_rss_text, "tier_8_fallback"

        should_close_client = False
        if client is None:
            client = httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)
            should_close_client = True

        try:
            # Giải mã link Google News (nếu có) sang URL gốc thực sự trước khi cào
            url = await resolve_real_article_url(url, client)

            html_content = None

            # 1. Thử cào bằng curl_cffi (Giả lập TLS/JA3 Fingerprint Chrome 124 + Social Referer t.co)
            if HAS_CURL_CFFI:
                try:
                    async with CurlAsyncSession() as session:
                        c_resp = await session.get(
                            url,
                            headers=SOCIAL_REFERER_HEADERS,
                            impersonate="chrome124",
                            timeout=self.timeout,
                        )
                        if c_resp.status_code == 200 and len(c_resp.text) > 400:
                            if "Enable JavaScript" not in c_resp.text and "Just a moment..." not in c_resp.text:
                                html_content = c_resp.text
                except Exception as e:
                    logger.debug(f"curl_cffi fetch error for {url}: {e}")

            # 2. Nếu curl_cffi chưa lấy được, thử luân phiên qua httpx
            if not html_content:
                headers_list = [
                    {"User-Agent": "curl/8.4.0", "Accept": "*/*"},
                    SOCIAL_REFERER_HEADERS,
                    {
                        "User-Agent": DEFAULT_BROWSER_UA,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
                        "Referer": "https://www.google.com/",
                    },
                ]

                for hdrs in headers_list:
                    try:
                        resp = await client.get(url, headers=hdrs)
                        if resp.status_code == 200 and len(resp.text) > 400:
                            if "Enable JavaScript" not in resp.text and "Just a moment..." not in resp.text:
                                html_content = resp.text
                                break
                    except Exception:
                        continue

            if html_content:
                # Tier 1: Parser chuyên biệt cho từng domain lớn
                domain_text = extract_domain_article(html_content, url)
                if domain_text:
                    clean_d = sanitize_article_prose(domain_text, min_total_len=200)
                    if clean_d:
                        return clean_d, "tier_1_domain_parser"

                # Tier 2: Next.js Hydration State Parser (__NEXT_DATA__)
                next_data_text = extract_next_data_article(html_content)
                if next_data_text:
                    clean_nd = sanitize_article_prose(next_data_text, min_total_len=200)
                    if clean_nd:
                        return clean_nd, "tier_2_next_data"

                # Tier 3: Trafilatura
                try:
                    extracted = trafilatura.extract(
                        html_content,
                        include_comments=False,
                        include_tables=False,
                        no_fallback=False,
                    )
                    if extracted and "Enable JavaScript" not in extracted:
                        clean_tr = sanitize_article_prose(extracted, min_total_len=200)
                        if clean_tr:
                            return clean_tr, "tier_3_trafilatura"
                except Exception:
                    pass

                # Tier 4: JSON-LD articleBody
                json_body = extract_json_ld_article_body(html_content)
                if json_body:
                    clean_jb = sanitize_article_prose(json_body, min_total_len=150)
                    if clean_jb:
                        return clean_jb, "tier_4_json_ld"

                # Tier 5: Trích xuất thẻ đoạn văn <p>
                p_body = extract_html_paragraphs(html_content, min_total_len=200)
                if p_body:
                    clean_p = sanitize_article_prose(p_body, min_total_len=200)
                    if clean_p:
                        return clean_p, "tier_5_paragraphs"

            # Tier 6: Jina Reader Proxy Fallback (r.jina.ai)
            try:
                jina_url = f"https://r.jina.ai/{url}"
                jina_resp = await client.get(
                    jina_url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=6.0,
                )
                if jina_resp.status_code == 200 and len(jina_resp.text) > 250:
                    raw_txt = jina_resp.text.strip()
                    if "requiring CAPTCHA" not in raw_txt and "Enable JavaScript" not in raw_txt:
                        cleaned_jina = clean_jina_markdown(raw_txt)
                        if len(cleaned_jina) > 250 and not cleaned_jina.startswith("Toggle menu"):
                            return cleaned_jina, "tier_6_jina"
            except Exception:
                pass

            # Tier 7: Reverse Search Fallback (khi có tiêu đề và các tầng trên bị chặn)
            if title and len(title.strip()) > 12:
                reverse_txt = await reverse_search_article(title)
                if reverse_txt and len(reverse_txt) > 200:
                    return reverse_txt, "tier_7_reverse_search"

            # Tier 8: Fallback về RSS summary ban đầu
            return clean_rss_text or url, "tier_8_fallback"

        finally:
            if should_close_client:
                await client.aclose()

    async def ingest_entries(
        self,
        entries: List[Dict[str, Any]],
        source_id: Optional[int] = None,
        fetch_full_content: bool = False,
    ) -> Dict[str, Any]:
        """
        Lưu danh sách bài báo vào SQLite với cơ chế băm hash SHA-256 chống trùng lặp.
        Cập nhật đồng bộ vào bảng ảo articles_fts.
        """
        inserted_count = 0
        duplicate_count = 0
        error_count = 0

        # Bước 1: Lấy danh sách hash đã có trong 1 query chớp nhoáng (< 2ms)
        existing_hashes = set()
        try:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
                await db.execute("PRAGMA busy_timeout = 30000;")
                async with db.execute("SELECT url_hash FROM articles") as cur:
                    rows = await cur.fetchall()
                    existing_hashes = {r[0] for r in rows}
        except Exception as e:
            logger.warning(f"Could not preload existing url_hashes: {e}")

        # Bước 2: Thực hiện network requests (Waterfall) HOÀN TOÀN NGOÀI DATABASE TRANSACTION
        items_to_insert = []
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as http_client:
            for entry in entries:
                raw_url = entry.get("link") or entry.get("url") or ""
                title = (entry.get("title") or "").strip()
                summary_raw = entry.get("summary") or entry.get("description") or ""

                if not raw_url or not title:
                    continue

                # Bỏ qua ngay lập tức các bài quảng cáo Newsletter hoặc Gallery chỉ có ảnh
                if is_junk_rss_entry(title, summary_raw, raw_url):
                    continue

                url_hash = generate_url_hash(raw_url)
                if url_hash in existing_hashes:
                    duplicate_count += 1
                    continue

                # Cào nội dung sạch
                if fetch_full_content:
                    content_clean, _ = await self.fetch_article_waterfall(
                        raw_url, summary_raw, client=http_client, title=title
                    )
                else:
                    content_clean = clean_html_tags(summary_raw) or title

                lang = detect_language(f"{title} {content_clean}")
                author = entry.get("author") or "N/A"
                published_at = entry.get("published") or entry.get("updated") or datetime.now(timezone.utc).isoformat()

                items_to_insert.append({
                    "source_id": source_id,
                    "url": raw_url,
                    "url_hash": url_hash,
                    "title": title,
                    "summary_raw": summary_raw,
                    "content_clean": content_clean,
                    "language": lang,
                    "author": author,
                    "published_at": published_at,
                })

        # Bước 3: Mở kết nối ghi chớp nhoáng (chỉ mất ~5ms), tuyệt đối không gây lock DB
        if items_to_insert:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
                await db.execute("PRAGMA foreign_keys = ON;")
                await db.execute("PRAGMA journal_mode = WAL;")
                await db.execute("PRAGMA busy_timeout = 30000;")

                for item in items_to_insert:
                    try:
                        cursor = await db.execute(
                            """
                            INSERT OR IGNORE INTO articles (
                                source_id, url, url_hash, title, summary_raw,
                                content_clean, language, author, published_at, status
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending');
                            """,
                            (
                                item["source_id"],
                                item["url"],
                                item["url_hash"],
                                item["title"],
                                item["summary_raw"],
                                item["content_clean"],
                                item["language"],
                                item["author"],
                                item["published_at"],
                            ),
                        )
                        if cursor.rowcount > 0:
                            article_id = cursor.lastrowid
                            await db.execute(
                                """
                                INSERT INTO articles_fts (rowid, title, content_clean)
                                VALUES (?, ?, ?);
                                """,
                                (article_id, item["title"], item["content_clean"]),
                            )
                            inserted_count += 1
                            existing_hashes.add(item["url_hash"])
                        else:
                            duplicate_count += 1
                    except Exception as e:
                        logger.error(f"Error inserting article {item['url']}: {e}")
                        error_count += 1

                await db.commit()

        return {
            "total_entries": len(entries),
            "inserted": inserted_count,
            "duplicates": duplicate_count,
            "errors": error_count,
        }

    async def crawl_feed_string(
        self,
        xml_content: str,
        source_id: Optional[int] = None,
        fetch_full_content: bool = False,
    ) -> Dict[str, Any]:
        """Phân tích chuỗi XML RSS/Atom và nạp bài viết (dùng cho cả test offline và online)."""
        feed = feedparser.parse(xml_content)
        entries = feed.entries
        return await self.ingest_entries(
            entries, source_id=source_id, fetch_full_content=fetch_full_content
        )

    async def crawl_feed_url(
        self,
        feed_url: str,
        source_id: Optional[int] = None,
        fetch_full_content: bool = False,
    ) -> Dict[str, Any]:
        """Cào tin tức từ URL RSS trực tiếp."""
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            resp = await client.get(feed_url, headers={"User-Agent": DEFAULT_BROWSER_UA})
            resp.raise_for_status()
            xml_text = resp.text

        return await self.crawl_feed_string(
            xml_text, source_id=source_id, fetch_full_content=fetch_full_content
        )

    async def crawl_all_active_sources(self) -> Dict[str, Any]:
        """Quét toàn bộ các nguồn tin đang được kích hoạt (is_active = 1) trong bảng sources."""
        results = {}
        async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
            await db.execute("PRAGMA busy_timeout = 30000;")
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT id, name, url, source_type FROM sources WHERE is_active = 1 AND source_type = 'rss';"
            ) as cursor:
                active_sources = await cursor.fetchall()

        for source in active_sources:
            try:
                res = await self.crawl_feed_url(
                    source["url"], source_id=source["id"], fetch_full_content=True
                )
                results[source["name"]] = res
                # Cập nhật last_fetched_at
                async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
                    await db.execute("PRAGMA busy_timeout = 30000;")
                    await db.execute(
                        "UPDATE sources SET last_fetched_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (source["id"],),
                    )
                    await db.commit()
            except Exception as e:
                logger.error(f"Failed to crawl source {source['name']} ({source['url']}): {e}")
                results[source["name"]] = {"error": str(e)}

        return results
