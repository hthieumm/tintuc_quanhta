import json
import sqlite3

with open('C:/Users/d7jhhhhhhu9ldweqtuid/.gemini/antigravity/brain/ad45a830-6351-43ff-9e4f-85bd2f102129/.system_generated/steps/1929/output.txt', 'r', encoding='utf-8') as f:
    text = f.read().strip()

# Clean quotes
if text.startswith('"') and text.endswith('"'):
    try:
        text = json.loads(text)
    except Exception:
        text = text[1:-1]

print('Text length:', len(text))
print('Sample:\n', text[:300])

conn = sqlite3.connect('backend/data/spider_radar.db')
c = conn.cursor()
c.execute('UPDATE articles SET content_clean = ? WHERE id = 2915', (text,))
c.execute('UPDATE articles_fts SET content_clean = ? WHERE rowid = 2915', (text,))
conn.commit()
conn.close()
print('Updated article 2915 successfully!')
