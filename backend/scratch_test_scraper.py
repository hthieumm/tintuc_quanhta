import httpx
import re
import json

url = 'https://www.theguardian.com/society/2026/oct/09/vaccine-trial-begins-for-norovirus-superbug-which-causes-vomiting-and-diarrhoea'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

resp = httpx.get(url, headers=headers)
scripts = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', resp.text, re.DOTALL)
print(f'Found {len(scripts)} ld+json scripts')
for i, s in enumerate(scripts):
    try:
        data = json.loads(s.strip())
        items = data if isinstance(data, list) else [data]
        for it in items:
            if '@graph' in it:
                items.extend(it['@graph'])
            if 'articleBody' in it:
                print(f'Script {i} articleBody found! Len: {len(it["articleBody"])}')
                print(it['articleBody'][:200])
            elif 'description' in it:
                print(f'Script {i} description: {it["description"][:100]}')
    except Exception as e:
        print(f'Script {i} error: {e}')

# Check paragraph extraction
paragraphs = re.findall(r'<p[^>]*class=["\'][^"\']*dcr-[^"\']*["\'][^>]*>(.*?)</p>', resp.text)
if not paragraphs:
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', resp.text)
cleaned_p = [re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs if len(p) > 40]
print(f'\nExtracted {len(cleaned_p)} paragraphs from HTML!')
full_text = '\n\n'.join(cleaned_p)
print(f'Total HTML paragraph text len: {len(full_text)}')
print('Preview:\n', full_text[:400])
