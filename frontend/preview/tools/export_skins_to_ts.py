import os

os.makedirs('frontend/src/assets/skins', exist_ok=True)

# 1. Export Tribal paths from frontend/preview/tools/generate_tribal_paths.py
import sys
sys.path.append('frontend/preview/tools')
import generate_tribal_paths

paths = generate_tribal_paths.paths

tribal_ts = f'''export const tribalPaths = {repr(paths)};

export const tribalSvgTemplate = `
<svg id="live-spider-svg" viewBox="49 20 860 860" width="104" height="104">
  <defs>
    <filter id="tribal-neon-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur" />
      <feColorMatrix type="matrix" values="
        0.5 0 0 0 0.5
        0 0.2 0 0 0.2
        0.8 0 1 0 0.9
        0 0 0 1 0" in="blur" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="tribal-cyan-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <ellipse id="tribal-aura" cx="479" cy="500" rx="145" ry="185" fill="rgba(124, 58, 237, 0.22)" filter="url(#tribal-neon-glow)" />

  <g id="tribal-spider-master" transform="translate(0, 0)">
    <g id="tribal-legs-group">
      <!-- L1 -->
      <g class="sp-tribal-joint" id="tribal_L1_s1" data-rest="0" style="transform-origin: 440px 380px;">
        <path class="tribal-chitin" d="{paths['L1_s1']}" />
        <g class="sp-tribal-joint" id="tribal_L1_s2" data-rest="0" style="transform-origin: 418px 320px;">
          <path class="tribal-chitin" d="{paths['L1_s2']}" />
          <g class="sp-tribal-joint" id="tribal_L1_s3" data-rest="0" style="transform-origin: 405px 245px;">
            <path class="tribal-chitin" d="{paths['L1_s3']}" />
          </g>
        </g>
      </g>
      <!-- R1 -->
      <g class="sp-tribal-joint" id="tribal_R1_s1" data-rest="0" style="transform-origin: 518px 380px;">
        <path class="tribal-chitin" d="{paths['R1_s1']}" />
        <g class="sp-tribal-joint" id="tribal_R1_s2" data-rest="0" style="transform-origin: 540px 320px;">
          <path class="tribal-chitin" d="{paths['R1_s2']}" />
          <g class="sp-tribal-joint" id="tribal_R1_s3" data-rest="0" style="transform-origin: 553px 245px;">
            <path class="tribal-chitin" d="{paths['R1_s3']}" />
          </g>
        </g>
      </g>
      <!-- L2 -->
      <g class="sp-tribal-joint" id="tribal_L2_s1" data-rest="0" style="transform-origin: 440px 425px;">
        <path class="tribal-chitin" d="{paths['L2_s1']}" />
        <g class="sp-tribal-joint" id="tribal_L2_s2" data-rest="0" style="transform-origin: 390px 415px;">
          <path class="tribal-chitin" d="{paths['L2_s2']}" />
          <g class="sp-tribal-joint" id="tribal_L2_s3" data-rest="0" style="transform-origin: 320px 345px;">
            <path class="tribal-chitin" d="{paths['L2_s3']}" />
          </g>
        </g>
      </g>
      <!-- R2 -->
      <g class="sp-tribal-joint" id="tribal_R2_s1" data-rest="0" style="transform-origin: 518px 425px;">
        <path class="tribal-chitin" d="{paths['R2_s1']}" />
        <g class="sp-tribal-joint" id="tribal_R2_s2" data-rest="0" style="transform-origin: 568px 415px;">
          <path class="tribal-chitin" d="{paths['R2_s2']}" />
          <g class="sp-tribal-joint" id="tribal_R2_s3" data-rest="0" style="transform-origin: 638px 345px;">
            <path class="tribal-chitin" d="{paths['R2_s3']}" />
          </g>
        </g>
      </g>
      <!-- L3 -->
      <g class="sp-tribal-joint" id="tribal_L3_s1" data-rest="0" style="transform-origin: 440px 465px;">
        <path class="tribal-chitin" d="{paths['L3_s1']}" />
        <g class="sp-tribal-joint" id="tribal_L3_s2" data-rest="0" style="transform-origin: 360px 470px;">
          <path class="tribal-chitin" d="{paths['L3_s2']}" />
          <g class="sp-tribal-joint" id="tribal_L3_s3" data-rest="0" style="transform-origin: 285px 520px;">
            <path class="tribal-chitin" d="{paths['L3_s3']}" />
          </g>
        </g>
      </g>
      <!-- R3 -->
      <g class="sp-tribal-joint" id="tribal_R3_s1" data-rest="0" style="transform-origin: 518px 465px;">
        <path class="tribal-chitin" d="{paths['R3_s1']}" />
        <g class="sp-tribal-joint" id="tribal_R3_s2" data-rest="0" style="transform-origin: 598px 470px;">
          <path class="tribal-chitin" d="{paths['R3_s2']}" />
          <g class="sp-tribal-joint" id="tribal_R3_s3" data-rest="0" style="transform-origin: 673px 520px;">
            <path class="tribal-chitin" d="{paths['R3_s3']}" />
          </g>
        </g>
      </g>
      <!-- L4 -->
      <g class="sp-tribal-joint" id="tribal_L4_s1" data-rest="0" style="transform-origin: 440px 525px;">
        <path class="tribal-chitin" d="{paths['L4_s1']}" />
        <g class="sp-tribal-joint" id="tribal_L4_s2" data-rest="0" style="transform-origin: 395px 560px;">
          <path class="tribal-chitin" d="{paths['L4_s2']}" />
          <g class="sp-tribal-joint" id="tribal_L4_s3" data-rest="0" style="transform-origin: 360px 640px;">
            <path class="tribal-chitin" d="{paths['L4_s3']}" />
          </g>
        </g>
      </g>
      <!-- R4 -->
      <g class="sp-tribal-joint" id="tribal_R4_s1" data-rest="0" style="transform-origin: 518px 525px;">
        <path class="tribal-chitin" d="{paths['R4_s1']}" />
        <g class="sp-tribal-joint" id="tribal_R4_s2" data-rest="0" style="transform-origin: 563px 560px;">
          <path class="tribal-chitin" d="{paths['R4_s2']}" />
          <g class="sp-tribal-joint" id="tribal_R4_s3" data-rest="0" style="transform-origin: 598px 640px;">
            <path class="tribal-chitin" d="{paths['R4_s3']}" />
          </g>
        </g>
      </g>
    </g>

    <g class="spider-abdomen" id="tribal-body-core" style="transform-origin: 479px 500px; will-change: transform;">
      <image href="/preview/assets/tribal_spider/body.png" x="400" y="343" width="161" height="329" />
      <g id="tribal_fang_l" style="transform-origin: 470px 350px;">
        <polygon points="466,350 472,342 470,356" fill="#00f2fe" opacity="0.85" filter="url(#tribal-cyan-glow)" />
      </g>
      <g id="tribal_fang_r" style="transform-origin: 488px 350px;">
        <polygon points="492,350 486,342 488,356" fill="#00f2fe" opacity="0.85" filter="url(#tribal-cyan-glow)" />
      </g>
      <circle id="silk-nozzle" cx="479" cy="342" r="3.5" fill="#00f2fe" filter="url(#tribal-cyan-glow)" />
    </g>
  </g>
</svg>
`;
'''

with open('frontend/src/assets/skins/tribalVectorSvg.ts', 'w', encoding='utf-8') as f:
    f.write(tribal_ts)

# 2. Extract Mecha SVG template from preview
with open('frontend/preview/test_mecha_vector_rig.html', 'r', encoding='utf-8') as f:
    mecha_html = f.read()

idx_m = mecha_html.find('<svg id="mecha-cad-rig"')
idx_m_end = mecha_html.find('</svg>', idx_m) + 6
mecha_svg_inner = mecha_html[idx_m:idx_m_end]

mecha_ts = f'''export const mechaSvgTemplate = `{mecha_svg_inner}`;
'''

with open('frontend/src/assets/skins/mechaVectorSvg.ts', 'w', encoding='utf-8') as f:
    f.write(mecha_ts)

print("Exported skins to frontend/src/assets/skins/ successfully!")
