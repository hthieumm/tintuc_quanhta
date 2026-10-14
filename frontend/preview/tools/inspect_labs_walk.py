import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Inspect test_mecha_vector_rig.html
with open('frontend/preview/test_mecha_vector_rig.html', 'r', encoding='utf-8') as f:
    mecha_lab = f.read()

idx_m = mecha_lab.find("currentPreset === 'walk'")
print("Found mecha lab walk preset at:", idx_m)

# 2. Inspect test_tribal_vector_rig.html
with open('frontend/preview/test_tribal_vector_rig.html', 'r', encoding='utf-8') as f:
    tribal_lab = f.read()

idx_t = tribal_lab.find("currentPreset === 'walk'")
print("Found tribal lab walk preset at:", idx_t)
