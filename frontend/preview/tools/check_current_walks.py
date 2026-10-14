import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/preview/spider_showcase.html', encoding='utf-8') as f:
    c = f.read()

idx_m = c.find('function startMechaWalkAnimation')
idx_t = c.find('function startTribalWalkAnimation')
print('=== MECHA WALK ===')
print(c[idx_m:idx_m+2000])
print('=== TRIBAL WALK ===')
print(c[idx_t:idx_t+2000])
