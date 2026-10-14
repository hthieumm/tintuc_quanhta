import httpx
import re
import base64
import trafilatura

url = 'https://news.google.com/rss/articles/CBMijAFBVV95cUxNQjdzXzdVOVh5OVVkeXRrSlNpQXBuMTBWQzhqRDUtbG9uY1ZET0trR0xXNmlIQUhBY1hRS1BsVm8yRENMUE1MZTRxaEtsUmFoaEFUSXFuTXpqeVpqMHd5a1ZYOEtnT3ZvV1NhNmZYMUg0WnlGenFVal82aFp3c2psT25Fc0dRSUNWbkNobw?oc=5'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)

matches = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', resp.text)
ap_matches = [m for m in matches if 'apnews.com' in m]
print('AP Matches:', ap_matches[:3])

# Google News 2024 new decoding algorithm:
# Google News CBM URLs can be decoded or parsed via the data attributes or jina reader:
jina_url = f"https://r.jina.ai/{url}"
jina_resp = httpx.get(jina_url, timeout=12.0)
print('Jina Status for GNews:', jina_resp.status_code, 'Length:', len(jina_resp.text))
if jina_resp.status_code == 200:
    print('Jina text sample:', jina_resp.text[:400])
