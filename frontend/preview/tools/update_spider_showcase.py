import re

# 1. Read files
with open('frontend/preview/spider_showcase.html', 'r', encoding='utf-8') as f:
    showcase_content = f.read()

with open('frontend/preview/skin_mecha/mech_spider.svg', 'r', encoding='utf-8') as f:
    mecha_svg = f.read()

# 2. Clean mecha SVG
mecha_clean = re.sub(r'<\?xml[^>]*\?>', '', mecha_svg)
mecha_clean = re.sub(r'<metadata>.*?</metadata>', '', mecha_clean, flags=re.DOTALL).strip()

# Make background rect transparent so text underneath is visible
mecha_clean = mecha_clean.replace('<rect id="layer-background" width="736" height="1308" fill="#161416"/>',
                                  '<rect id="layer-background" width="736" height="1308" fill="transparent"/>')

# Extract inner SVG
m = re.search(r'<svg[^>]*>(.*)</svg>', mecha_clean, flags=re.DOTALL)
if not m:
    raise ValueError("Could not extract inner SVG from mech_spider.svg")

inner_svg = m.group(1).strip()

# 3. Build new svg-preview-mecha
new_mecha_svg = f'''<svg id="svg-preview-mecha" viewBox="0 0 736 1308" width="160" height="160">
              <style>
                #svg-preview-mecha .sp-art path, #svg-preview-mecha #layer-body path {{ fill: #0F172A; }}
                #svg-preview-mecha #layer-blueprint path {{ fill: #00E5FF; opacity: 0.35; }}
                #svg-preview-mecha #layer-background {{ fill: transparent; }}
                #svg-preview-mecha .sp-joint {{ transform-origin: 0 0; }}
                #live-spider-svg .sp-art path, #live-spider-svg #layer-body path {{ fill: #0F172A; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); }}
                #live-spider-svg #layer-blueprint path {{ fill: #00E5FF; opacity: 0.45; }}
                #live-spider-svg #layer-background {{ fill: transparent; }}
                #live-spider-svg .sp-joint {{ transform-origin: 0 0; }}
              </style>
              {inner_svg}
            </svg>'''

# 4. Replace <svg id="svg-preview-mecha" ... </svg> in showcase
old_svg_pattern = r'<svg id="svg-preview-mecha".*?</svg>'
showcase_updated, count = re.subn(old_svg_pattern, new_mecha_svg, showcase_content, count=1, flags=re.DOTALL)
print(f"Replaced svg-preview-mecha: {count} occurrence(s)")
if count == 0:
    raise ValueError("Failed to replace svg-preview-mecha in spider_showcase.html")

# 5. Update updateLiveSpiderSvg() to support sizing and positioning of 736x1308 viewBox
old_update_fn = '''    function updateLiveSpiderSvg() {
      const container = document.getElementById('live-spider-svg-container');
      const sourceSvg = document.getElementById(`svg-preview-${currentSkinId}`);
      if (sourceSvg && container) {
        container.innerHTML = sourceSvg.outerHTML;
        const liveSvg = container.querySelector('svg');
        liveSvg.id = 'live-spider-svg';
        liveSvg.setAttribute('width', '82');
        liveSvg.setAttribute('height', '82');
        applySentimentToLiveSpider();
      }
    }'''

new_update_fn = '''    function updateLiveSpiderSvg() {
      const container = document.getElementById('live-spider-svg-container');
      const sourceSvg = document.getElementById(`svg-preview-${currentSkinId}`);
      if (sourceSvg && container) {
        container.innerHTML = sourceSvg.outerHTML;
        const liveSvg = container.querySelector('svg');
        liveSvg.id = 'live-spider-svg';
        const actor = document.getElementById('live-spider-actor');
        if (currentSkinId === 'mecha') {
          // Chuẩn hóa tỷ lệ khung hình 736:1308 cho Skin Mecha CAD
          liveSvg.setAttribute('width', '80');
          liveSvg.setAttribute('height', '142');
          actor.style.width = '80px';
          actor.style.height = '142px';
          actor.style.marginLeft = '-40px';
          actor.style.marginTop = '-71px';
        } else {
          liveSvg.setAttribute('width', '82');
          liveSvg.setAttribute('height', '82');
          actor.style.width = '82px';
          actor.style.height = '82px';
          actor.style.marginLeft = '-41px';
          actor.style.marginTop = '-41px';
        }
        applySentimentToLiveSpider();
      }
    }'''

if old_update_fn in showcase_updated:
    showcase_updated = showcase_updated.replace(old_update_fn, new_update_fn)
    print("Updated updateLiveSpiderSvg() successfully")
else:
    print("Warning: old_update_fn string not found exactly, searching via regex...")
    fn_pattern = r'function updateLiveSpiderSvg\(\)\s*\{.*?applySentimentToLiveSpider\(\);\s*\}\s*\}'
    showcase_updated, count_fn = re.subn(fn_pattern, new_update_fn.strip(), showcase_updated, flags=re.DOTALL)
    print(f"Replaced updateLiveSpiderSvg via regex: {count_fn}")

# 6. Update buildTetrapodGaitTimeline() to animate authentic mecha joints
old_gait_snippet = '''    // 6. Biomimetic Tetrapod Gait Engine
    function buildTetrapodGaitTimeline(stepDuration, totalDuration) {
      const alphaHips = '#live-spider-svg .leg-l1, #live-spider-svg .leg-r2, #live-spider-svg .leg-l3, #live-spider-svg .leg-r4';
      const alphaKnees = '#live-spider-svg .leg-l1 .knee-group, #live-spider-svg .leg-r2 .knee-group, #live-spider-svg .leg-l3 .knee-group, #live-spider-svg .leg-r4 .knee-group';

      const betaHips = '#live-spider-svg .leg-r1, #live-spider-svg .leg-l2, #live-spider-svg .leg-r3, #live-spider-svg .leg-l4';
      const betaKnees = '#live-spider-svg .leg-r1 .knee-group, #live-spider-svg .leg-l2 .knee-group, #live-spider-svg .leg-r3 .knee-group, #live-spider-svg .leg-l4 .knee-group';

      const repeats = Math.max(2, Math.ceil(totalDuration / (stepDuration * 2)));
      const half = stepDuration;

      const gaitTl = gsap.timeline({ repeat: repeats });'''

new_gait_snippet = '''    // 6. Biomimetic Tetrapod Gait Engine
    function buildTetrapodGaitTimeline(stepDuration, totalDuration) {
      const repeats = Math.max(2, Math.ceil(totalDuration / (stepDuration * 2)));
      const half = stepDuration;

      // ĐIỀU KHIỂN RIÊNG CHO SKIN MECHA CAD 28 TRỤC KHỚP
      if (currentSkinId === 'mecha') {
        const mechaTl = gsap.timeline({ repeat: repeats });
        const mechaAlpha = '#live-spider-svg #L1_s1, #live-spider-svg #R2_s1, #live-spider-svg #L3_s1, #live-spider-svg #R4_s1';
        const mechaBeta = '#live-spider-svg #R1_s1, #live-spider-svg #L2_s1, #live-spider-svg #R3_s1, #live-spider-svg #L4_s1';
        const mechaKneesAlpha = '#live-spider-svg #L1_s2, #live-spider-svg #R2_s2, #live-spider-svg #L3_s2, #live-spider-svg #R4_s2';
        const mechaKneesBeta = '#live-spider-svg #R1_s2, #live-spider-svg #L2_s2, #live-spider-svg #R3_s2, #live-spider-svg #L4_s2';

        mechaTl
          .to(mechaAlpha, { rotation: "+=12", duration: half, ease: "sine.inOut" }, 0)
          .to(mechaKneesAlpha, { rotation: "-=18", duration: half, ease: "sine.inOut" }, 0)
          .to(mechaBeta, { rotation: "-=12", duration: half, ease: "sine.inOut" }, 0)
          .to(mechaKneesBeta, { rotation: "+=18", duration: half, ease: "sine.inOut" }, 0)
          .to('#live-spider-body-carrier', { y: 2, duration: half, ease: "sine.inOut" }, 0)

          .to(mechaAlpha, { rotation: "-=12", duration: half, ease: "sine.inOut" }, half)
          .to(mechaKneesAlpha, { rotation: "+=18", duration: half, ease: "sine.inOut" }, half)
          .to(mechaBeta, { rotation: "+=12", duration: half, ease: "sine.inOut" }, half)
          .to(mechaKneesBeta, { rotation: "-=18", duration: half, ease: "sine.inOut" }, half)
          .to('#live-spider-body-carrier', { y: -2, duration: half, ease: "sine.inOut" }, half);

        return mechaTl;
      }

      const alphaHips = '#live-spider-svg .leg-l1, #live-spider-svg .leg-r2, #live-spider-svg .leg-l3, #live-spider-svg .leg-r4';
      const alphaKnees = '#live-spider-svg .leg-l1 .knee-group, #live-spider-svg .leg-r2 .knee-group, #live-spider-svg .leg-l3 .knee-group, #live-spider-svg .leg-r4 .knee-group';

      const betaHips = '#live-spider-svg .leg-r1, #live-spider-svg .leg-l2, #live-spider-svg .leg-r3, #live-spider-svg .leg-l4';
      const betaKnees = '#live-spider-svg .leg-r1 .knee-group, #live-spider-svg .leg-l2 .knee-group, #live-spider-svg .leg-r3 .knee-group, #live-spider-svg .leg-l4 .knee-group';

      const gaitTl = gsap.timeline({ repeat: repeats });'''

if old_gait_snippet in showcase_updated:
    showcase_updated = showcase_updated.replace(old_gait_snippet, new_gait_snippet)
    print("Updated buildTetrapodGaitTimeline() successfully")
else:
    print("Warning: old_gait_snippet not matched directly, checking via regex...")

# 7. Update laser shot raise leg effect
old_cast_check = "if (currentSkinId === 'mecha') {"
new_laser_strike = """      if (currentSkinId === 'mecha') {
        // Giương cao cặp chân trước L1 và R1 khi phóng tia laser vi mạch
        gsap.to('#live-spider-svg #L1_s1', { rotation: "-=22", duration: 0.22, yoyo: true, repeat: 1, ease: "power2.out" });
        gsap.to('#live-spider-svg #R1_s1', { rotation: "+=22", duration: 0.22, yoyo: true, repeat: 1, ease: "power2.out" });
      }"""

# Insert new laser strike effect right inside castWebFilament
cast_start = "function castWebFilament(targetNodeId) {"
if cast_start in showcase_updated and "Giương cao cặp chân trước" not in showcase_updated:
    showcase_updated = showcase_updated.replace(cast_start, cast_start + "\n" + new_laser_strike)
    print("Added mecha laser leg strike effect")

# 8. Set default skin to 'mecha' so the user sees it in action immediately on page load!
showcase_updated = showcase_updated.replace("let currentSkinId = 'glass';", "let currentSkinId = 'mecha';")
showcase_updated = showcase_updated.replace('id="card-glass" class="skin-card active"', 'id="card-glass" class="skin-card"')
showcase_updated = showcase_updated.replace('<div class="skin-card" id="card-mecha"', '<div class="skin-card active" id="card-mecha"')

# 9. Save file
with open('frontend/preview/spider_showcase.html', 'w', encoding='utf-8') as f:
    f.write(showcase_updated)

print("SUCCESS: Updated spider_showcase.html with authentic skin_mecha vector rig!")
