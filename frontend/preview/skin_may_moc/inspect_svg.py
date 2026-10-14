import re

with open(r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg', 'r', encoding='utf-8') as f:
    text = f.read()

ids = re.findall(r'id="([^"]+)"', text)
print('Total IDs:', len(ids))
joints = [i for i in ids if re.match(r'^[LR]\d_s\d', i)]
print('Joints count:', len(joints))
print('Joints:', joints)
layers = [i for i in ids if 'layer' in i or 'spider' in i or 'body' in i]
print('Layers / Roots:', layers)
