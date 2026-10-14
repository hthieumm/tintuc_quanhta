import sqlite3

conn = sqlite3.connect('backend/data/spider_radar.db')
c = conn.cursor()

c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='github_repos'")
print('Schema:', c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM github_repos")
print('Row count:', c.fetchone()[0])

c.execute("SELECT * FROM github_repos LIMIT 5")
rows = c.fetchall()
print('Sample rows:', len(rows))
for r in rows:
    print(r)
