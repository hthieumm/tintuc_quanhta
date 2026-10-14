import xml.etree.ElementTree as ET
import re

tree = ET.parse(r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg')
root = tree.getroot()

spider_root = None
for el in root.iter():
    if el.get('id') == 'spider-root':
        spider_root = el
        break

all_xs = []
all_ys = []
for p in spider_root.iter('{http://www.w3.org/2000/svg}path'):
    d = p.get('d', '')
    coords = re.findall(r'([-\d.]+),([-\d.]+)', d)
    for x, y in coords:
        all_xs.append(float(x))
        all_ys.append(float(y))

print(f'Total paths in spider-root: {len(list(spider_root.iter("{http://www.w3.org/2000/svg}path")))}')
print(f'Overall raw coords X: {min(all_xs)} to {max(all_xs)}, center: {(min(all_xs)+max(all_xs))/2}')
print(f'Overall raw coords Y: {min(all_ys)} to {max(all_ys)}, center: {(min(all_ys)+max(all_ys))/2}')
