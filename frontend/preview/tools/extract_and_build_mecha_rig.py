import cv2
import numpy as np
import os

def process_mecha():
    src_path = r'C:\Users\d7jhhhhhhu9ldweqtuid\.gemini\antigravity\brain\61cfbf20-c564-4109-95ab-7d2249703c87\.user_uploaded\media_1791709370425_738c60cc.png'
    out_dir = r'frontend/preview/assets/mecha_cad_master'
    os.makedirs(out_dir, exist_ok=True)

    img = cv2.imread(src_path)
    h, w, c = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. CLEANING MASKS: Loai bo 100% duong giong CAD va text ngoai ria
    clean_mask = np.ones((h, w), dtype=np.uint8)
    clean_mask[:, :26] = 0
    clean_mask[:, 552:] = 0
    clean_mask[:35, :170] = 0
    clean_mask[:250, 455:] = 0
    clean_mask[985:, :] = 0
    clean_mask[935:, 230:350] = 0
    clean_mask[525:940, 285:291] = 0
    clean_mask[515:555, 245:330] = 0
    clean_mask[60:90, :100] = 0
    clean_mask[60:90, 470:] = 0
    clean_mask[165:180, :180] = 0
    clean_mask[165:180, 400:] = 0
    clean_mask[320:335, :90] = 0
    clean_mask[320:335, 480:] = 0

    cleaned_gray = cv2.bitwise_and(gray, gray, mask=clean_mask)

    alpha = np.zeros((h, w), dtype=np.uint8)
    alpha[cleaned_gray > 28] = np.clip((cleaned_gray[cleaned_gray > 28].astype(float) - 25) * 1.35, 0, 255).astype(np.uint8)
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])

    # 2. ANATOMICAL PARTS VỚI TỌA ĐỘ CHUẨN XÁC THEO BẢN VẼ
    parts_meta = {
        "body_chassis": {
            "bbox": (180, 20, 396, 520),
            "pivot": (288, 280)
        },
        "leg_l1_femur": {
            "bbox": (110, 110, 230, 240),
            "pivot": (215, 180)
        },
        "leg_l1_tibia": {
            "bbox": (120, 10, 215, 185),
            "pivot": (140, 170)
        },
        "leg_r1_femur": {
            "bbox": (345, 110, 465, 240),
            "pivot": (360, 180)
        },
        "leg_r1_tibia": {
            "bbox": (360, 10, 455, 185),
            "pivot": (435, 170)
        },
        "leg_l2_femur": {
            "bbox": (100, 235, 215, 315),
            "pivot": (195, 260)
        },
        "leg_l2_tibia": {
            "bbox": (50, 265, 130, 400),
            "pivot": (115, 280)
        },
        "leg_r2_femur": {
            "bbox": (360, 235, 475, 315),
            "pivot": (380, 260)
        },
        "leg_r2_tibia": {
            "bbox": (445, 265, 525, 400),
            "pivot": (460, 280)
        },
        "leg_l3_femur": {
            "bbox": (95, 320, 245, 670),
            "pivot": (200, 390)
        },
        "leg_l3_tibia": {
            "bbox": (100, 650, 180, 835),
            "pivot": (135, 660)
        },
        "leg_l3_claw": {
            "bbox": (110, 815, 160, 995),
            "pivot": (125, 825)
        },
        "leg_r3_femur": {
            "bbox": (330, 320, 480, 670),
            "pivot": (375, 390)
        },
        "leg_r3_tibia": {
            "bbox": (395, 650, 475, 835),
            "pivot": (440, 660)
        },
        "leg_r3_claw": {
            "bbox": (415, 815, 465, 995),
            "pivot": (450, 825)
        }
    }

    for part_name, info in parts_meta.items():
        x1, y1, x2, y2 = info["bbox"]
        part_crop = rgba[y1:y2, x1:x2].copy()
        out_part_path = os.path.join(out_dir, f"{part_name}.png")
        cv2.imwrite(out_part_path, part_crop)

    # 3. SVG MASTER
    svg_content = f'''<svg id="mecha-cad-master-svg" viewBox="0 0 576 1024" width="576" height="1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="cad-laser-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="pivot-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- LƯỚI TỌA ĐỘ CAD HUD -->
  <g class="cad-grid-layer" opacity="0.45" stroke="#00E5FF" stroke-width="0.7" stroke-dasharray="2 4">
    <circle cx="288" cy="300" r="260" fill="none" />
    <circle cx="288" cy="300" r="180" fill="none" />
    <circle cx="288" cy="300" r="90" fill="none" />
    <line x1="288" y1="20" x2="288" y2="1000" />
    <line x1="30" y1="300" x2="546" y2="300" />
    <line x1="30" y1="180" x2="546" y2="180" />
    <line x1="30" y1="660" x2="546" y2="660" />
    <line x1="30" y1="825" x2="546" y2="825" />
  </g>

  <!-- ==================== HIERARCHICAL SKELETAL RIG ==================== -->

  <!-- CHÂN PISTON KHỔNG LỒ L3 -->
  <g id="rig-leg-l3" class="leg-l3-root" style="transform-origin: 200px 390px; will-change: transform;">
    <g class="femur-housing">
      <image href="assets/mecha_cad_master/leg_l3_femur.png" x="95" y="320" width="150" height="350" />
    </g>
    <g id="rig-knee-l3" class="knee-group knee-l3" style="transform-origin: 135px 660px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_l3_tibia.png" x="100" y="650" width="80" height="185" />
      <g id="rig-claw-l3" class="claw-group claw-l3" style="transform-origin: 125px 825px; will-change: transform;">
        <image href="assets/mecha_cad_master/leg_l3_claw.png" x="110" y="815" width="50" height="180" />
      </g>
    </g>
  </g>

  <!-- CHÂN PISTON KHỔNG LỒ R3 -->
  <g id="rig-leg-r3" class="leg-r3-root" style="transform-origin: 375px 390px; will-change: transform;">
    <g class="femur-housing">
      <image href="assets/mecha_cad_master/leg_r3_femur.png" x="330" y="320" width="150" height="350" />
    </g>
    <g id="rig-knee-r3" class="knee-group knee-r3" style="transform-origin: 440px 660px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_r3_tibia.png" x="395" y="650" width="80" height="185" />
      <g id="rig-claw-r3" class="claw-group claw-r3" style="transform-origin: 450px 825px; will-change: transform;">
        <image href="assets/mecha_cad_master/leg_r3_claw.png" x="415" y="815" width="50" height="180" />
      </g>
    </g>
  </g>

  <!-- CHÂN NGANG L2 -->
  <g id="rig-leg-l2" class="leg-l2-root" style="transform-origin: 195px 260px; will-change: transform;">
    <image href="assets/mecha_cad_master/leg_l2_femur.png" x="100" y="235" width="115" height="80" />
    <g id="rig-knee-l2" class="knee-group knee-l2" style="transform-origin: 115px 280px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_l2_tibia.png" x="50" y="265" width="80" height="135" />
    </g>
  </g>

  <!-- CHÂN NGANG R2 -->
  <g id="rig-leg-r2" class="leg-r2-root" style="transform-origin: 380px 260px; will-change: transform;">
    <image href="assets/mecha_cad_master/leg_r2_femur.png" x="360" y="235" width="115" height="80" />
    <g id="rig-knee-r2" class="knee-group knee-r2" style="transform-origin: 460px 280px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_r2_tibia.png" x="445" y="265" width="80" height="135" />
    </g>
  </g>

  <!-- CHÂN TRƯỚC L1 -->
  <g id="rig-leg-l1" class="leg-l1-root" style="transform-origin: 215px 180px; will-change: transform;">
    <image href="assets/mecha_cad_master/leg_l1_femur.png" x="110" y="110" width="120" height="130" />
    <g id="rig-knee-l1" class="knee-group knee-l1" style="transform-origin: 140px 170px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_l1_tibia.png" x="120" y="10" width="95" height="175" />
    </g>
  </g>

  <!-- CHÂN TRƯỚC R1 -->
  <g id="rig-leg-r1" class="leg-r1-root" style="transform-origin: 360px 180px; will-change: transform;">
    <image href="assets/mecha_cad_master/leg_r1_femur.png" x="345" y="110" width="120" height="130" />
    <g id="rig-knee-r1" class="knee-group knee-r1" style="transform-origin: 435px 170px; will-change: transform;">
      <image href="assets/mecha_cad_master/leg_r1_tibia.png" x="360" y="10" width="95" height="175" />
    </g>
  </g>

  <!-- KHUNG GẦM BUỒNG LÁI TRUNG TÂM -->
  <g id="rig-chassis-core" style="transform-origin: 288px 280px; will-change: transform;">
    <image href="assets/mecha_cad_master/body_chassis.png" x="180" y="20" width="216" height="500" />
    <circle class="spider-eye eye-l" cx="268" cy="190" r="5" fill="#00E5FF" filter="url(#cad-laser-glow)" />
    <circle class="spider-eye eye-r" cx="308" cy="190" r="5" fill="#00E5FF" filter="url(#cad-laser-glow)" />
    <circle cx="288" cy="120" r="3" fill="#00E5FF" filter="url(#cad-laser-glow)" />
  </g>

  <!-- TẦNG TÂM KHỚP PIVOTS -->
  <g id="cad-pivots-layer" style="display: none;">
    <circle cx="215" cy="180" r="8" fill="none" stroke="#EF4444" stroke-width="2.5" filter="url(#pivot-glow)" />
    <circle cx="360" cy="180" r="8" fill="none" stroke="#EF4444" stroke-width="2.5" filter="url(#pivot-glow)" />
    <circle cx="140" cy="170" r="7" fill="none" stroke="#F59E0B" stroke-width="2" />
    <circle cx="435" cy="170" r="7" fill="none" stroke="#F59E0B" stroke-width="2" />

    <circle cx="195" cy="260" r="8" fill="none" stroke="#EF4444" stroke-width="2.5" filter="url(#pivot-glow)" />
    <circle cx="380" cy="260" r="8" fill="none" stroke="#EF4444" stroke-width="2.5" filter="url(#pivot-glow)" />
    <circle cx="115" cy="280" r="7" fill="none" stroke="#F59E0B" stroke-width="2" />
    <circle cx="460" cy="280" r="7" fill="none" stroke="#F59E0B" stroke-width="2" />

    <circle cx="200" cy="390" r="9" fill="none" stroke="#EF4444" stroke-width="3" filter="url(#pivot-glow)" />
    <circle cx="375" cy="390" r="9" fill="none" stroke="#EF4444" stroke-width="3" filter="url(#pivot-glow)" />
    <circle cx="135" cy="660" r="8" fill="none" stroke="#F59E0B" stroke-width="2.5" />
    <circle cx="440" cy="660" r="8" fill="none" stroke="#F59E0B" stroke-width="2.5" />
    <circle cx="125" cy="825" r="7" fill="none" stroke="#10B981" stroke-width="2" />
    <circle cx="450" cy="825" r="7" fill="none" stroke="#10B981" stroke-width="2" />
  </g>
</svg>
'''

    svg_path = os.path.join(out_dir, "mecha_cad_rig_master.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Updated SVG Master at:", svg_path)

if __name__ == "__main__":
    process_mecha()
