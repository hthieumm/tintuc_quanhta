with open('frontend/preview/test_tribal_vector_rig.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('id="tribal-svg-stage" viewBox="200 20 560 860"', 'id="tribal-svg-stage" viewBox="49 20 860 860"')
c = c.replace('rotate(${roll}, 479, 500)', 'rotate(${roll}, 479, 450)')

with open('frontend/preview/test_tribal_vector_rig.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated test_tribal_vector_rig.html viewBox to square 1:1!')
