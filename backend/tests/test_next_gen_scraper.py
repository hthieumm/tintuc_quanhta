"""
Tests for Next-Gen Scraping Techniques:
1. __NEXT_DATA__ JSON extraction
2. curl_cffi with Social Referrer
3. Reverse search fallback
"""

import pytest
import json
from backend.rss_crawler import extract_next_data_article, extract_json_ld_article_body, detect_language

def test_extract_next_data_article():
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <script id="__NEXT_DATA__" type="application/json">
      {
        "props": {
          "pageProps": {
            "story": {
              "headline": "Global Market Surge",
              "paragraphs": [
                "The Federal Reserve held benchmark interest rates steady while signaling a cautious approach toward upcoming rate cuts in late 2026.",
                "Global stock indices reacted positively to the central bank's statement, with technology and financial shares leading gains across Asia and Europe.",
                "Bond yields ticked lower as fixed income traders factored in moderate monetary easing over the next four quarters."
              ]
            }
          }
        }
      }
      </script>
    </head>
    <body><div>Placeholder</div></body>
    </html>
    """
    extracted = extract_next_data_article(sample_html)
    assert extracted is not None
    assert "Federal Reserve" in extracted
    assert "Global stock indices" in extracted
    assert len(extracted) > 150

def test_extract_next_data_empty():
    assert extract_next_data_article("<html><body>No script</body></html>") is None
    assert extract_next_data_article("") is None
