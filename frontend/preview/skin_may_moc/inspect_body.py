import xml.etree.ElementTree as ET

tree = ET.parse(r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg')
root = tree.getroot()

body = None
for el in root.iter():
    if el.get('id') == 'layer-body':
        body = el
        break

if body is not None:
    print('layer-body found, children:', len(body))
    for i, ch in enumerate(body):
        print(f'child {i} tag: {ch.tag}')
        d = ch.get('d', '')
        if d:
            print(f'  path len: {len(d)}, snippet: {d[:60]}...')
else:
    print('layer-body NOT found')
