import xml.etree.ElementTree as ET
import re

tree = ET.parse(r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg')
root = tree.getroot()

for el in root.iter():
    if el.get('id') == 'layer-body':
        d = el[0].get('d', '')
        coords = re.findall(r'([-\d.]+),([-\d.]+)', d)
        xs = [float(x) for x, y in coords]
        ys = [float(y) for x, y in coords]
        print(f'Body X range: {min(xs)} to {max(xs)}, center: {(min(xs)+max(xs))/2}')
        print(f'Body Y range: {min(ys)} to {max(ys)}, center: {(min(ys)+max(ys))/2}')
