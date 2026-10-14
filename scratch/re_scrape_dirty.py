import asyncio
import sqlite3
from backend.rss_crawler import SpiderNewsCrawler
from backend.database import DEFAULT_DB_PATH

async def run_clean():
    crawler = SpiderNewsCrawler(db_path=DEFAULT_DB_PATH)
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    c = conn.cursor()
    
    # 1. Tìm các bài bị dính menu rác hoặc bài 2915
    query = """
        SELECT id, url, summary_raw, title
        FROM articles
        WHERE content_clean LIKE '%Toggle menu%' 
           OR content_clean LIKE '%* 1st item%' 
           OR content_clean LIKE '%search for any story%'
           OR id = 2915
    """
    c.execute(query)
    dirty_articles = c.fetchall()
    print(f'Phat hien {len(dirty_articles)} bai bao can lam sach / cao lai toan van.')
    
    fixed_count = 0
    for aid, url, summary, title in dirty_articles:
        full_text, tier = await crawler.fetch_article_waterfall(url, summary or '')
        if full_text and not full_text.startswith('Toggle menu') and len(full_text) > 200:
            c.execute('UPDATE articles SET content_clean = ? WHERE id = ?', (full_text, aid))
            try:
                c.execute('UPDATE articles_fts SET content_clean = ? WHERE rowid = ?', (full_text, aid))
            except Exception:
                pass
            fixed_count += 1
            print(f'  [OK] Bai #{aid}: {title[:35]} -> {tier} (Len: {len(full_text)})')
        else:
            print(f'  [FAIL] Bai #{aid}: {title[:35]} -> fallback (Len: {len(full_text)})')
            
    conn.commit()
    conn.close()
    print(f'Hoan tat! Da sua thanh cong {fixed_count} / {len(dirty_articles)} bai bao!')

if __name__ == '__main__':
    asyncio.run(run_clean())
