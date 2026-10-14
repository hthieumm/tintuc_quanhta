import xml.etree.ElementTree as ET

tree = ET.parse(r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg')
root = tree.getroot()

def dump_tree(elem, depth=0):
    elem_id = elem.get('id', '')
    elem_cls = elem.get('class', '')
    elem_rest = elem.get('data-rest', '')
    elem_tr = elem.get('transform', '')
    tag = elem.tag.split('}')[-1]
    if elem_id or 'sp-' in elem_cls:
        info = f"{tag} id='{elem_id}' class='{elem_cls}'"
        if elem_rest:
            info += f" rest={elem_rest}"
        if elem_tr and len(elem_tr) < 40:
            info += f" tr={elem_tr}"
        print('  ' * depth + info)
    for ch in elem:
        dump_tree(ch, depth + 1)

dump_tree(root)
