import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/preview/test_mecha_vector_rig.html', 'r', encoding='utf-8') as f:
    mecha_lab = f.read()

idx_m = mecha_lab.find("currentPreset === 'walk'")
print("=== MECHA LAB WALK BLOCK ===")
print(mecha_lab[idx_m:idx_m+1800])

with open('frontend/preview/test_tribal_vector_rig.html', 'r', encoding='utf-8') as f:
    tribal_lab = f.read()

idx_t = tribal_lab.find("currentPreset === 'walk'")
print("=== TRIBAL LAB WALK BLOCK ===")
print(tribal_lab[idx_t:idx_t+1800])
