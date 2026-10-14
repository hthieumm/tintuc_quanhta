import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "spider_radar.db")
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("PRAGMA table_info(articles)")
cols = [r[1] for r in cur.fetchall()]
if "is_bookmarked" not in cols:
    cur.execute("ALTER TABLE articles ADD COLUMN is_bookmarked INTEGER DEFAULT 0")
    con.commit()
    print("Added is_bookmarked to articles")
else:
    print("is_bookmarked already in articles")

# Check current bookmarked count
cur.execute("SELECT count(*) FROM articles WHERE is_bookmarked = 1")
cnt = cur.fetchone()[0]
if cnt == 0:
    cur.execute("SELECT id FROM articles ORDER BY id DESC LIMIT 10")
    ids = [str(r[0]) for r in cur.fetchall()[:5]]
    if ids:
        cur.execute(f"UPDATE articles SET is_bookmarked = 1 WHERE id IN ({','.join(ids)})")
        con.commit()
        print(f"Bookmarked {len(ids)} articles as initial starred vault items")

cur.execute("SELECT count(*) FROM articles")
total = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM articles WHERE is_bookmarked = 1")
bm = cur.fetchone()[0]
print(f"Total articles: {total}, Starred articles: {bm}, Unstarred articles: {total - bm}")
con.close()
