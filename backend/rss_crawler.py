"""
Spider News Radar - RSS & Multi-Source Crawler Module
Implements 4-tier Waterfall scraping pipeline, deduplication by SHA-256 URL hash,
language tagging, and SQLite WAL ingestion.
"""

import os
import asyncio
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
    from curl_cffi import requests as c_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    c_requests = None

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

# Ký tự đặc trưng thuần Việt (hỏi, ngã, nặng, nón, râu, đ - không trùng với tiếng Pháp hay Tây Ban Nha)
VIETNAMESE_UNIQUE_CHARS = re.compile(
    r"[ăâđêôơưảãạẳẵặẩẫậẻẽẹểễệỉĩịỏõọổỗộởỡợủũụửữựỳỷỹỵ]",
    re.IGNORECASE,
)
VIETNAMESE_STOPWORDS = {"và", "của", "các", "trong", "được", "người", "không", "có", "này", "đã", "cho", "với", "về", "khi", "những", "theo", "tại", "một", "từ"}
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")
JAPANESE_PATTERN = re.compile(r"[\u3040-\u309f\u30a0-\u30ff]")


def detect_language(text: str) -> str:
    """
    Phát hiện ngôn ngữ của bài viết dựa trên đặc trưng văn bản:
    'vi' (Tiếng Việt), 'zh' (Tiếng Trung), 'ja' (Tiếng Nhật), hoặc 'en' (Mặc định).
    Loại bỏ triệt để lỗi nhận diện nhầm do từ mượn tiếng Pháp/Tây Ban Nha (như lycées, café, résumé).
    """
    if not text:
        return "en"
    
    t_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', t_lower))
    vn_stopwords_count = len(words.intersection(VIETNAMESE_STOPWORDS))
    vn_chars_count = len(VIETNAMESE_UNIQUE_CHARS.findall(t_lower))

    if vn_stopwords_count >= 2 or vn_chars_count >= 5:
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
                        # WSJ / Substack / Next.js: Đoạn văn chia thành mảng các text/link fragment
                        # Bắt buộc ghép toàn bộ các mảnh lại thành câu hoàn chỉnh trước khi đo độ dài
                        if "content" in obj and isinstance(obj["content"], list):
                            if any(isinstance(x, dict) and "text" in x for x in obj["content"]):
                                full_p = "".join(str(x.get("text") or "") for x in obj["content"] if isinstance(x, dict))
                                c = clean_html_tags(full_p).strip()
                                if len(c) > 40 and not any(skip in c.lower() for skip in ["subscribe", "newsletter", "sign in", "all rights reserved"]):
                                    collected_paras.append(c)
                                return

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


def clean_and_extract_paragraphs(html_content: str) -> str:
    """
    Trích xuất toàn văn các đoạn văn <p> sạch sẽ từ HTML:
    - Bóc tách và giữ 100% nội dung chữ bên trong các thẻ liên kết <a> bằng phương thức unwrap().
    - Loại bỏ triệt để các thẻ rác hệ thống (script, style, nav, footer, aside, form, figure).
    - Chuẩn hóa khoảng trắng và loại bỏ các thông báo paywall / subscription ngắn.
    """
    if not html_content:
        return ""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # 1. Chỉ xóa các thẻ rác thực sự, TUYỆT ĐỐI KHÔNG xóa thẻ <a>, <span>, <em>, <strong>
        for junk in soup(["script", "style", "nav", "footer", "aside", "noscript", "iframe", "form", "figure", "figcaption", "button"]):
            junk.decompose()

        # 2. Giữ lại chữ bên trong thẻ <a> và thẻ inline bằng cách gỡ bỏ vỏ thẻ (unwrap)
        for inline_tag in soup.find_all(["a", "span", "em", "strong", "b", "i", "mark"]):
            inline_tag.unwrap()

        # 3. Trích xuất các đoạn văn <p> với khoảng trắng chuẩn xác
        paragraphs = []
        seen_norm = set()
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            text = re.sub(r'\s+([.,!?;:])', r'\1', text)
            text = clean_html_tags(text).strip()
            low = text.lower()
            if len(text) > 40 and not any(skip in low for skip in [
                "subscription to keep reading",
                "distribution and use of this material are governed",
                "dow jones reprints",
                "copyright ©",
                "all rights reserved",
                "to continue reading",
                "sign in to continue",
                "djreprints.com",
                "subscriber agreement",
                "please enable js",
            ]):
                norm = text[:60].lower()
                if norm not in seen_norm:
                    seen_norm.add(norm)
                    paragraphs.append(text)

        result = "\n\n".join(paragraphs).strip()
        return sanitize_article_prose(result, min_total_len=200) or result
    except Exception as e:
        logger.debug(f"clean_and_extract_paragraphs error: {e}")
        return ""


def extract_domain_article(html_text: str, url: str) -> Optional[str]:
    """
    Trích xuất chuyên sâu theo từng tờ báo lớn (VN & Quốc tế).
    Loại bỏ triệt để các khối 'Tin liên quan', 'Đọc thêm', 'Form khảo sát', 'Chú thích ảnh' nằm xen giữa bài.
    """
    if not html_text:
        return None
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text, "html.parser")

        # Xóa trước toàn bộ các thẻ rác phổ biến nằm bên trong thân bài của mọi tờ báo
        for junk_tag in soup.select(
            "script, style, nav, header, footer, aside, form, figure, figcaption, "
            "iframe, button, .related-news, .box-tinlienquan, .tinlienquan, "
            "[type='RelatedOneNews'], .story-interrupt, .ad-slot, .sub-meta"
        ):
            junk_tag.decompose()

        body = None

        # 1. VnExpress
        if "vnexpress.net" in url:
            body = soup.find("article", class_="fck_detail") or soup.find("div", class_="fck_detail")
            if body:
                for p_junk in body.select("p.Image, p.author_mail, div.box_brief_info"):
                    p_junk.decompose()

        # 2. Tuổi Trẻ
        elif "tuoitre.vn" in url:
            body = soup.find("div", class_="detail-content") or soup.find("div", id="main-detail-body")

        # 3. CafeF (Lấy cả Sapo mở đầu + Nội dung chính)
        elif "cafef.vn" in url:
            sapo = soup.find("h2", class_="sapo")
            sapo_txt = clean_html_tags(sapo.get_text()) if sapo else ""
            body = (
                soup.find("div", class_="detail-content")
                or soup.find("div", class_="contentdetail")
                or soup.find("div", class_="fck")
            )
            if body:
                paras = [clean_html_tags(p.get_text()) for p in body.find_all("p") if len(p.get_text().strip()) > 25]
                if sapo_txt and len(sapo_txt) > 30:
                    paras.insert(0, sapo_txt)
                if paras:
                    return "\n\n".join(paras)

        # 4. BBC News (Chỉ lấy từ article text-block, bỏ qua trang video không có chữ)
        elif "bbc.com" in url or "bbc.co.uk" in url:
            if "/news/videos/" in url or "/news/av/" in url:
                return None
            paras = [
                clean_html_tags(p.get_text())
                for div in soup.find_all("div", attrs={"data-component": "text-block"})
                for p in div.find_all("p")
                if len(p.get_text().strip()) > 35
            ]
            if not paras:
                art = soup.find("article")
                if art:
                    paras = [clean_html_tags(p.get_text()) for p in art.find_all("p") if len(p.get_text().strip()) > 40]
            if len(paras) >= 3:
                return "\n\n".join(paras)

        # 5. The Guardian (Chỉ lấy vùng văn bản chính data-gu-name="body" hoặc #maincontent)
        elif "theguardian.com" in url:
            body = (
                soup.find("div", attrs={"data-gu-name": "body"})
                or soup.find("div", id="maincontent")
                or soup.find("div", class_="article-body-commercial-selector")
            )

        # 6. CoinDesk (Hỗ trợ cả DOM cũ lẫn DOM Next.js mới)
        elif "coindesk.com" in url:
            body = (
                soup.find("div", attrs={"data-module-name": "article-body"})
                or soup.find("div", class_="at-body")
                or soup.find("section", class_="article-body")
                or soup.find("div", class_="composer-content")
            )

        # 7. Politico
        elif "politico.com" in url:
            body = (
                soup.find("div", class_="story-text")
                or soup.find("section", class_="story-text")
                or soup.find("article", class_="story-main-content")
            )

        # 8. AP News
        elif "apnews.com" in url:
            body = soup.find("div", class_="RichTextStoryBody") or soup.find("div", class_="Article")

        # 9. CNBC (Mới bổ sung)
        elif "cnbc.com" in url:
            body = soup.find("div", class_="ArticleBody-articleBody") or soup.find("div", class_="RenderKeyPoints-list")

        # 10. Yahoo Finance (Mới bổ sung - Rất quan trọng khi cào bài đối tác Bloomberg/Economist)
        elif "yahoo.com" in url:
            body = soup.find("div", class_="caas-body") or soup.find("div", class_="atoms-wrapper")

        # 11. Reuters (Mới bổ sung)
        elif "reuters.com" in url:
            body = soup.find("div", attrs={"data-testid": "ArticleBody"}) or soup.find("article")

        # 12. The Wall Street Journal (WSJ)
        elif "wsj.com" in url:
            body = (
                soup.find("section", class_="article-body")
                or soup.find("div", class_="article-content")
                or soup.find("div", attrs={"data-module-name": "article-body"})
                or soup.find("article")
            )

        if body:
            # Gỡ bỏ vỏ thẻ nội tuyến (unwrap) để không làm rơi rụng chữ nằm trong các thẻ liên kết <a>
            for inline_tag in body.find_all(["a", "span", "em", "strong", "b", "i", "mark"]):
                inline_tag.unwrap()

            seen_p = set()
            clean_paras = []
            for p in body.find_all("p"):
                txt = p.get_text(" ", strip=True)
                txt = re.sub(r'\s+([.,!?;:])', r'\1', txt)
                txt = clean_html_tags(txt).strip()
                if len(txt) < 35:
                    continue
                low = txt.lower()
                # Lọc bỏ các câu rác cuối bài của AP, Guardian, Reuters, WSJ
                if any(k in low for k in (
                    "please include as much detail", "please tell us using the form",
                    "follow ap’s coverage", "contributed to this report",
                    "sign up for our newsletter", "reporting by ", "editing by ",
                    "subscription to keep reading", "dow jones reprints",
                    "subscriber agreement", "copyright ©",
                )):
                    continue
                if low not in seen_p:
                    seen_p.add(low)
                    clean_paras.append(txt)

            if len(clean_paras) >= 2:
                return "\n\n".join(clean_paras)
    except Exception as e:
        logger.debug(f"Domain parser error for {url}: {e}")
    return None


async def resolve_real_article_url(url: str, client: Optional[httpx.AsyncClient] = None) -> str:
    """
    Tự động chuyển hướng URL trung gian / URL Video sang URL bài báo Text chính thức:
    1. BBC Video (/news/videos/...) -> BBC Article (/news/articles/...)
    2. VnExpress Video (video.vnexpress.net/...) -> Bài báo VnExpress chuẩn
    3. Google News RSS (news.google.com/rss/articles/...) -> Báo gốc
    """
    if not url:
        return url

    u_low = url.lower()
    should_close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=6.0, follow_redirects=True)
        should_close_client = True

    try:
        # 1. BBC Video / Audio-Visual -> Tìm link bài báo chữ '/news/articles/...'
        if "bbc.com/news/videos/" in u_low or "bbc.co.uk/news/videos/" in u_low or "bbc.com/news/av/" in u_low:
            try:
                resp = await client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA}, follow_redirects=True, timeout=6.0)
                if resp.status_code == 200:
                    m_art = re.search(
                        r'href=["\']((?:https?://(?:www\.)?bbc\.(?:com|co\.uk))?/news/articles/[a-zA-Z0-9]+)["\']',
                        resp.text,
                    )
                    if m_art:
                        found = m_art.group(1)
                        return f"https://www.bbc.com{found}" if found.startswith("/") else found
            except Exception:
                pass

        # 2. VnExpress Video -> Tìm link bài báo chữ gốc nếu có đính kèm
        if "video.vnexpress.net" in u_low:
            try:
                resp = await client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA}, follow_redirects=True, timeout=6.0)
                if resp.status_code == 200:
                    m_vne = re.search(r'href=["\'](https://vnexpress\.net/[a-zA-Z0-9\-]+-\d+\.html)["\']', resp.text)
                    if m_vne:
                        return m_vne.group(1)
            except Exception:
                pass

        # 3. Google News Wrapper -> Giải mã batchexecute / Base64
        if "news.google.com" in u_low:
            # 3.1. Thử giải mã batchexecute (chuẩn mới Google News CBMi)
            try:
                resp = await client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA}, follow_redirects=True, timeout=6.0)
                if resp.url and "news.google.com" not in str(resp.url):
                    return str(resp.url)
                sg_m = re.search(r'data-n-a-sg="([^"]+)"', resp.text)
                ts_m = re.search(r'data-n-a-ts="([^"]+)"', resp.text)
                if sg_m and ts_m:
                    import urllib.parse
                    art_id = urllib.parse.urlparse(url).path.split("/")[-1]
                    if art_id:
                        _GARTURLREQ_CTX = [
                            ["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1],
                            "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0,
                        ]
                        inner = ["garturlreq", _GARTURLREQ_CTX, art_id, int(ts_m.group(1)), sg_m.group(1)]
                        envelope = [["Fbv4je", json.dumps(inner, separators=(",", ":")), None, "1"]]
                        body = "f.req=" + urllib.parse.quote(json.dumps([envelope], separators=(",", ":")))
                        b_resp = await client.post(
                            "https://news.google.com/_/DotsSplashUi/data/batchexecute",
                            headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
                            content=body,
                            timeout=6.0,
                        )
                        if b_resp.status_code == 200:
                            found = [u.rstrip("\\") for u in re.findall(r'"(https?://[^"]+)"', b_resp.text) if "google" not in u]
                            if found:
                                return found[0]
            except Exception:
                pass

            # 3.2. Giải mã Base64 cho định dạng URL cũ
            try:
                import base64
                m_b64 = re.search(r'/articles/([A-Za-z0-9_-]+)', url)
                if m_b64:
                    encoded = m_b64.group(1)
                    pad = encoded + "=" * ((4 - len(encoded) % 4) % 4)
                    decoded_str = base64.urlsafe_b64decode(pad).decode("latin1", errors="ignore")
                    http_match = re.search(r'(https?://[^\x00-\x1f\x7f-\xff"\'\s<>]+)', decoded_str)
                    if http_match and "google.com" not in http_match.group(1):
                        return http_match.group(1)
            except Exception:
                pass

            # 3.3. Fallback qua regex thẻ HTML
            try:
                resp = await client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA}, follow_redirects=True, timeout=6.0)
                if resp.url and "news.google.com" not in str(resp.url):
                    return str(resp.url)
                m = re.search(r'data-n-au=["\'](https?://[^"\']+)["\']', resp.text)
                if m:
                    return m.group(1)
                m2 = re.search(r'<a[^>]+href=["\'](https?://(?!news\.google\.com)[^"\']+)["\']', resp.text)
                if m2:
                    return m2.group(1)
            except Exception:
                pass

    finally:
        if should_close_client:
            await client.aclose()

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
    "please include as much detail as possible",
    "tell us using the form below",
    "you can share your response using this form",
    "your responses are secure and encrypted",
    "a journalist will contact you",
    "guardian community team",
    "share your story",
    "share your thoughts",
    "guardian callout",
)

# Danh sách đường dẫn URL phi văn bản của toàn bộ các báo VN & Quốc tế
MEDIA_ONLY_URL_PATTERNS = (
    # Quốc tế (Guardian, AP, Politico, CoinDesk, Bloomberg, CNBC, Economist)
    "/video/", "/videos/", "/audio/", "/podcasts/", "/podcast/",
    "/gallery/", "/in-pictures/", "/photo-gallery/", "/photography/",
    "/ng-interactive/", "/interactive/", "/cartoons/", "/crosswords/",
    "/coindesk-tv/", "/tv/", "/watch/", "/films/", "/hub/",
    "youtube.com/watch", "youtu.be/",
    # Báo Việt Nam (VnExpress, Tuổi Trẻ, CafeF)
    "video.vnexpress.net", "tv.tuoitre.vn", "/infographics/", "/infographic/",
    "/megastory/", "/photo/", "/anh-360/", "/tuong-thuat-",
)

# Danh sách mẫu tiêu đề không phải bài phân tích/tin tức văn bản
NON_ARTICLE_TITLE_PATTERNS = (
    # Newsletter & Khảo sát độc giả (The Guardian, Politico, NYT)
    "sign up for the ", "newsletter:", "free daily news email",
    "free football email", "food email", "tell us:", "send us your questions",
    "corrections and clarifications", "first edition:", "morning briefing:",
    "share your experience", "share your story", "tell us about", "callout:",
    # Chùm ảnh / Đố vui / Video / Audio
    "photos of the day", "in pictures:", "best photos of", "photo gallery:",
    "quiz:", "crossword", "watch:", "listen:", "(video)", "[video]",
    "(podcast)", "[podcast]", "video:", "podcast:",
    # Bảng giá tự động / Ticker chứng khoán & vàng địa phương
    "gold rate today in ", "gold and silver price today",
    "check live 22 and 24 carat", "stock price, news, quote & history",
)

# Danh sách từ khóa chặn tin rác đời sống / hôn nhân / giải trí / thể thao thuần túy
NOISE_REJECT_KEYWORDS = (
    # Đời sống, Hôn nhân, Sinh sản, Tâm sự, Thám hiểm
    "froze your eggs", "egg freezing", "fertility", "called off a wedding",
    "wedding", "dating", "boyfriend", "girlfriend", "divorce", "pregnancy",
    "horoscope", "zodiac", "recipe", "cooking", "fashion", "skincare",
    "beauty", "workout", "weight loss", "amelia earhart", "archaeology",
    "dinosaur", "fossil", "pet dog", "pet cat",
    # Thể thao & Giải trí thuần túy
    "premier league", "champions league", "la liga", "serie a", "world cup",
    "ballon d'or", "manchester united", "arsenal", "chelsea", "liverpool",
    "real madrid", "barcelona", "nba", "nfl", "tennis", "golf",
    "box office", "hollywood", "grammy", "oscars", "red carpet",
    "hoa hậu", "showbiz", "scandal tình ái", "ngoại tình", "v-league",
)

COMPILED_NOISE_REJECT = [
    re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)
    for k in NOISE_REJECT_KEYWORDS
]


def is_junk_rss_entry(title: str, summary: str, url: str) -> bool:
    """
    Bộ lọc tổng lực trước khi nạp RSS cho toàn bộ các trang báo trong dự án:
    Chỉ cho phép bài báo dạng Text đi vào hệ thống.
    (Ngoại lệ: BBC Video và VnExpress Video được phép đi vào resolve_real_article_url để thử bóc link bài Text).
    """
    t_raw = title or ""
    s_raw = summary or ""
    t_low = t_raw.lower().strip()
    s_low = s_raw.lower().strip()
    u_low = (url or "").lower().strip()

    if any(p in t_low for p in NON_ARTICLE_TITLE_PATTERNS):
        return True
    if any(p.search(t_raw) or p.search(s_raw) for p in COMPILED_NOISE_REJECT):
        return True
    if "privacy notice: newsletters may contain" in s_low or "privacy notice: newsletters" in s_low:
        return True
    if "please tell us using the form below" in s_low or "please tell us using the form" in s_low:
        return True
    if "guardian community team" in s_low or "share your response" in s_low:
        return True

    # Ngoại lệ cho những trang Video có nhúng kèm link bài viết Text bên trong
    if any(vh in u_low for vh in ("bbc.com/news/videos/", "bbc.co.uk/news/videos/", "bbc.com/news/av/", "video.vnexpress.net")):
        return False

    if any(p in u_low for p in MEDIA_ONLY_URL_PATTERNS):
        return True

    return False


def sanitize_article_prose(text: str, min_total_len: int = 200) -> str:
    """
    Bộ lọc cấp độ từng đoạn văn (Paragraph-level Sanitizer):
    Loại bỏ 100% các dòng menu ngắn (News, Opinion, Sport, UK edition, Previous image...)
    Chỉ giữ lại những đoạn văn xuôi thực thụ (dài >= 50 ký tự và có cấu trúc câu).
    Khử trùng lặp toàn cục (Global Deduplication) nhằm loại bỏ triệt để các câu form lặp lại nhiều lần.
    """
    if not text:
        return ""

    raw_lines = text.splitlines()
    valid_paragraphs: List[str] = []
    seen_hashes: set = set()

    for line in raw_lines:
        clean = clean_html_tags(line).strip()
        if not clean:
            continue

        # 1. Loại bỏ dòng chứa cú pháp link markdown hoặc URL trần
        if "](" in clean or "http://" in clean or "https://" in clean:
            continue

        c_low = clean.lower()

        # 2. Loại bỏ dòng khớp với từ khóa giao diện / nút bấm / hướng dẫn form
        if any(junk in c_low for junk in UI_JUNK_LINE_PATTERNS):
            continue

        # 3. Loại bỏ các dòng cụt ngủn (menu, nhãn chuyên mục như "News", "Sport", "Int", "Sign in")
        # Một đoạn văn báo chí thực sự phải có ít nhất 8 từ và dài >= 45 ký tự, có dấu câu
        word_count = len(clean.split())
        if len(clean) < 45 or word_count < 7:
            continue

        if not any(punct in clean for punct in (".", "!", "?", "。", "”", '"', "’", "…")):
            continue

        # 4. Khử trùng lặp toàn cục (Global Deduplication)
        norm_key = re.sub(r'\s+', ' ', c_low)
        if norm_key in seen_hashes:
            continue
        seen_hashes.add(norm_key)

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
PAYWALL_DOMAINS = [
    "wsj.com",
    "bloomberg.com",
    "ft.com",
    "nytimes.com",
    "economist.com",
    "theinformation.com",
    "barrons.com",
]


def fetch_full_article_with_bypass(url: str, title: str = "", rss_summary: str = "") -> str:
    """
    Pipeline 3 bước lấy full bài báo, tự động vượt Paywall khi bài bị cắt cụt.
    Tầng 1: Thử tải trực tiếp với Header / Referer Google + unwrap thẻ link.
    Tầng 2: Tìm bản đăng lại hợp pháp trên MSN / Yahoo Finance / Mirror theo Tiêu đề.
    Tầng 3: Kéo bản chụp từ Archive.ph / Wayback Machine.
    Fallback cuối: Ghép Summary và Content thông minh để tránh lặp câu.
    """
    if not url or not url.startswith("http"):
        return clean_html_tags(rss_summary).strip()

    is_paywall_site = any(domain in url.lower() for domain in PAYWALL_DOMAINS)
    content = ""

    # Giải mã Google News nếu cần
    target_url = url
    if "news.google.com" in url.lower():
        try:
            with httpx.Client(follow_redirects=True, timeout=6.0) as client:
                resp = client.get(url, headers={"User-Agent": DEFAULT_BROWSER_UA})
                if resp.url and "news.google.com" not in str(resp.url):
                    target_url = str(resp.url)
                else:
                    sg_m = re.search(r'data-n-a-sg="([^"]+)"', resp.text)
                    ts_m = re.search(r'data-n-a-ts="([^"]+)"', resp.text)
                    if sg_m and ts_m:
                        import urllib.parse
                        art_id = urllib.parse.urlparse(url).path.split("/")[-1]
                        if art_id:
                            _ctx = [
                                ["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1],
                                "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0,
                            ]
                            inner = ["garturlreq", _ctx, art_id, int(ts_m.group(1)), sg_m.group(1)]
                            envelope = [["Fbv4je", json.dumps(inner, separators=(",", ":")), None, "1"]]
                            body = "f.req=" + urllib.parse.quote(json.dumps([envelope], separators=(",", ":")))
                            b_resp = client.post(
                                "https://news.google.com/_/DotsSplashUi/data/batchexecute",
                                headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
                                content=body,
                                timeout=6.0,
                            )
                            if b_resp.status_code == 200:
                                found = [u.rstrip("\\") for u in re.findall(r'"(https?://[^"]+)"', b_resp.text) if "google" not in u]
                                if found:
                                    target_url = found[0]
        except Exception:
            pass

    # --- TẦNG 1: Thử tải trực tiếp với Header / Referer Google + unwrap thẻ link ---
    headers = {
        "Referer": "https://www.google.com/",
        "User-Agent": DEFAULT_BROWSER_UA,
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    }
    try:
        if HAS_CURL_CFFI and c_requests:
            resp = c_requests.get(target_url, headers=headers, impersonate="chrome120", timeout=12)
            if resp.status_code == 200 and len(resp.text) > 1000:
                # 1.1. Thử extract_domain_article đã unwrap thẻ <a>
                dom_txt = extract_domain_article(resp.text, target_url)
                if dom_txt and len(dom_txt) > 600:
                    content = dom_txt
                else:
                    # 1.2. Thử Next.js Hydration state đã sửa không bị rụng chữ
                    nd_txt = extract_next_data_article(resp.text)
                    if nd_txt and len(nd_txt) > 800:
                        content = nd_txt
                    else:
                        content = clean_and_extract_paragraphs(resp.text)
                        if not content:
                            raw_ext = trafilatura.extract(resp.text, include_links=False, include_comments=False)
                            content = sanitize_article_prose(raw_ext or "", min_total_len=200)

                # Nếu lấy được bài dài (> 1200 ký tự) thì trả về luôn
                if content and len(content) > 1200:
                    return content
    except Exception as e:
        logger.debug(f"[Tầng 1] Lỗi tải trực tiếp {target_url}: {e}")

    # Nếu bài quá ngắn (< 1200 ký tự) hoặc thuộc trang Paywall -> Kích hoạt Bypass
    if is_paywall_site or len(content or "") < 1200:
        # --- TẦNG 2: Tìm bản đăng lại hợp pháp trên MSN / Yahoo Finance / Mirror theo Tiêu đề ---
        if title:
            try:
                import urllib.parse
                clean_title = re.sub(r'[\'\"’—\-\:\(\)]', ' ', title).strip()
                clean_title = re.sub(r'\b(WSJ|The Wall Street Journal|Bloomberg|Reuters|FT|Financial Times|The Economist)\b', '', clean_title, flags=re.IGNORECASE).strip()
                words = [w for w in clean_title.split() if len(w) > 1]
                query = " ".join(words[:10])

                results = []
                try:
                    from duckduckgo_search import DDGS
                    with DDGS() as ddgs:
                        results = list(ddgs.text(f'"{query}" (site:msn.com OR site:finance.yahoo.com OR site:squawknews.com)', max_results=3))
                        if not results:
                            results = list(ddgs.text(query, max_results=3))
                except Exception:
                    pass

                # Nếu DDGS không ra, thử fallback qua DDG HTML search
                if not results and HAS_CURL_CFFI and c_requests:
                    try:
                        from bs4 import BeautifulSoup
                        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
                        ddg_r = c_requests.get(search_url, headers=headers, impersonate="chrome120", timeout=8)
                        if ddg_r.status_code == 200:
                            s = BeautifulSoup(ddg_r.text, "html.parser")
                            for a_tag in s.find_all("a", class_="result__url"):
                                h = a_tag.get("href", "").strip()
                                m_tar = re.search(r'uddg=([^&]+)', h)
                                m_url = urllib.parse.unquote(m_tar.group(1)) if m_tar else h
                                if m_url and not any(p in m_url for p in PAYWALL_DOMAINS):
                                    results.append({"href": m_url})
                                    if len(results) >= 3:
                                        break
                    except Exception:
                        pass

                for r in results:
                    mirror_url = r.get("href")
                    if mirror_url and not any(p in mirror_url for p in PAYWALL_DOMAINS):
                        try:
                            m_resp = c_requests.get(mirror_url, impersonate="chrome120", timeout=12) if (HAS_CURL_CFFI and c_requests) else None
                            if m_resp and m_resp.status_code == 200:
                                m_content = clean_and_extract_paragraphs(m_resp.text)
                                if not m_content:
                                    raw_m = trafilatura.extract(m_resp.text, include_links=False)
                                    m_content = sanitize_article_prose(raw_m or "", min_total_len=300)
                                if m_content and len(m_content) > 1000:
                                    logger.info(f"[Tầng 2] Đã lấy full bài qua Mirror: {mirror_url}")
                                    return m_content
                        except Exception:
                            continue
            except Exception as e:
                logger.debug(f"[Tầng 2] Lỗi tìm Mirror: {e}")

        # --- TẦNG 3: Kéo bản chụp từ Archive.ph / Wayback Machine ---
        archive_urls = [
            f"https://archive.ph/newest/{target_url}",
            f"https://web.archive.org/web/2/{target_url}"
        ]
        for arch_url in archive_urls:
            try:
                a_resp = c_requests.get(arch_url, impersonate="chrome120", timeout=15) if (HAS_CURL_CFFI and c_requests) else None
                if a_resp and a_resp.status_code == 200:
                    a_content = clean_and_extract_paragraphs(a_resp.text)
                    if not a_content:
                        raw_a = trafilatura.extract(a_resp.text, include_links=False)
                        a_content = sanitize_article_prose(raw_a or "", min_total_len=300)
                    if a_content and len(a_content) > 1000:
                        logger.info(f"[Tầng 3] Đã lấy full bài qua Archive: {arch_url}")
                        return a_content
            except Exception as e:
                logger.debug(f"[Tầng 3] Lỗi kéo Archive {arch_url}: {e}")

    # --- FALLBACK CUỐI: Ghép Summary và Content thông minh để tránh lặp câu ---
    clean_c = sanitize_article_prose(content, min_total_len=100) if content else ""
    if clean_c and len(clean_c) >= 600:
        return clean_c

    clean_summary = clean_html_tags(rss_summary).strip()
    if not clean_c:
        return clean_summary

    if not clean_summary:
        return clean_c

    # Kiểm tra tránh lặp câu giữa summary và đoạn đầu của content
    summary_words = set(clean_summary.lower().split()[:12])
    first_p = clean_c.split("\n\n")[0]
    first_words = set(first_p.lower().split()[:12])
    overlap = len(summary_words.intersection(first_words))

    if overlap >= 5:
        return clean_c

    return f"{clean_summary}\n\n{clean_c}".strip()


async def fetch_full_article_with_bypass_async(url: str, title: str = "", rss_summary: str = "") -> str:
    """Phiên bản non-blocking async của fetch_full_article_with_bypass."""
    return await asyncio.to_thread(fetch_full_article_with_bypass, url, title, rss_summary)


def fetch_article_content_robust(url: str, title: Optional[str] = None) -> Optional[str]:
    """
    Sử dụng curl_cffi và multi-stage bypass để cào sạch bài gốc không bị chặn bot hay paywall.
    """
    res = fetch_full_article_with_bypass(url, title=title or "")
    return res if res and len(res) > 250 else None


async def fetch_article_content_robust_async(url: str, title: Optional[str] = None) -> Optional[str]:
    """Phiên bản non-blocking async của fetch_article_content_robust cho FastAPI."""
    return await asyncio.to_thread(fetch_article_content_robust, url, title)


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

            # Nếu là trang trong danh mục Paywall cứng (WSJ, Bloomberg, FT, NYT, Economist...),
            # kích hoạt trực tiếp pipeline lách paywall 3 tầng (Chrome TLS unwrap -> MSN/Yahoo Syndication -> Archive)
            if any(domain in url.lower() for domain in PAYWALL_DOMAINS):
                bp_content = await fetch_full_article_with_bypass_async(url, title=title, rss_summary=rss_summary)
                if bp_content and len(bp_content) > 300:
                    clean_bp = sanitize_article_prose(bp_content, min_total_len=200)
                    if clean_bp and len(clean_bp) > 250:
                        return clean_bp, "tier_paywall_bypass"

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

            # Tier 6.5: Robust TLS Impersonation & Syndication Wire (Reuters, Bloomberg, AP)
            try:
                robust_txt = await fetch_article_content_robust_async(url, title=title)
                if robust_txt and len(robust_txt) > 250:
                    return robust_txt, "tier_robust_curl_cffi"
            except Exception as e:
                logger.debug(f"Tier robust curl_cffi error: {e}")

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
        source_category = None
        try:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
                await db.execute("PRAGMA busy_timeout = 30000;")
                async with db.execute("SELECT url_hash FROM articles") as cur:
                    rows = await cur.fetchall()
                    existing_hashes = {r[0] for r in rows}
                if source_id:
                    async with db.execute("SELECT category FROM sources WHERE id = ?", (source_id,)) as cur:
                        s_row = await cur.fetchone()
                        if s_row:
                            source_category = s_row[0]
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

                # Tự động giải mã / chuyển hướng URL trung gian sang bài báo chữ thực sự
                if any(k in raw_url.lower() for k in ("bbc.com/news/videos", "bbc.co.uk/news/videos", "bbc.com/news/av", "video.vnexpress.net", "news.google.com")):
                    raw_url = await resolve_real_article_url(raw_url, client=http_client)
                    # Nếu là BBC Video hoặc VnExpress Video thuần túy không có link bài chữ đính kèm thì bỏ qua
                    if any(vh in raw_url.lower() for vh in ("bbc.com/news/videos/", "bbc.co.uk/news/videos/", "bbc.com/news/av/", "video.vnexpress.net")):
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

                # Chốt kiểm duyệt System 1 (D3 Lite Rule Gate) & Phân loại chuyên mục
                try:
                    from .app import evaluate_article_system1_gate
                    passed, detected_cat = evaluate_article_system1_gate(
                        title, content_clean, source_category=source_category
                    )
                    if not passed:
                        logger.info(f"System 1 rejected noise article: '{title}'")
                        continue
                except Exception as e:
                    logger.debug(f"System 1 evaluation fallback: {e}")
                    detected_cat = None

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
                    "category": detected_cat or source_category or "kinh_te",
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
                                content_clean, language, author, published_at, status, category
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?);
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
                                item.get("category", "kinh_te"),
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
