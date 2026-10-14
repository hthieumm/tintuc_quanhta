import os
import re
import generate_tribal_paths

paths = generate_tribal_paths.paths

# Read spider_showcase.html
with open('frontend/preview/spider_showcase.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Build the new tribal SVG string for Card 6
tribal_svg_new = f'''<svg id="svg-preview-tribal" viewBox="200 20 560 860" width="160" height="160">
              <defs>
                <!-- Neon Purple/Cyan Glow Filter -->
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

              <!-- Bóng Đổ Ma Mị Neon Tím Dưới Thân -->
              <ellipse id="tribal-aura" cx="479" cy="500" rx="145" ry="185" fill="rgba(124, 58, 237, 0.22)" filter="url(#tribal-neon-glow)" />

              <!-- Master Skeleton Group -->
              <g id="tribal-spider-master" transform="translate(0, 0)">

                <!-- 8 HIERARCHICAL ARTICULATED LEGS (24 JOINTS) -->
                <g id="tribal-legs-group">

                  <!-- === LEFT LEG 1 (Front Left) === -->
                  <g class="sp-tribal-joint" id="tribal_L1_s1" data-rest="0" style="transform-origin: 440px 380px;">
                    <path class="tribal-chitin" d="{paths['L1_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_L1_s2" data-rest="0" style="transform-origin: 418px 320px;">
                      <path class="tribal-chitin" d="{paths['L1_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_L1_s3" data-rest="0" style="transform-origin: 405px 245px;">
                        <path class="tribal-chitin" d="{paths['L1_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === RIGHT LEG 1 (Front Right) === -->
                  <g class="sp-tribal-joint" id="tribal_R1_s1" data-rest="0" style="transform-origin: 518px 380px;">
                    <path class="tribal-chitin" d="{paths['R1_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_R1_s2" data-rest="0" style="transform-origin: 540px 320px;">
                      <path class="tribal-chitin" d="{paths['R1_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_R1_s3" data-rest="0" style="transform-origin: 553px 245px;">
                        <path class="tribal-chitin" d="{paths['R1_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === LEFT LEG 2 === -->
                  <g class="sp-tribal-joint" id="tribal_L2_s1" data-rest="0" style="transform-origin: 440px 425px;">
                    <path class="tribal-chitin" d="{paths['L2_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_L2_s2" data-rest="0" style="transform-origin: 390px 415px;">
                      <path class="tribal-chitin" d="{paths['L2_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_L2_s3" data-rest="0" style="transform-origin: 320px 345px;">
                        <path class="tribal-chitin" d="{paths['L2_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === RIGHT LEG 2 === -->
                  <g class="sp-tribal-joint" id="tribal_R2_s1" data-rest="0" style="transform-origin: 518px 425px;">
                    <path class="tribal-chitin" d="{paths['R2_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_R2_s2" data-rest="0" style="transform-origin: 568px 415px;">
                      <path class="tribal-chitin" d="{paths['R2_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_R2_s3" data-rest="0" style="transform-origin: 638px 345px;">
                        <path class="tribal-chitin" d="{paths['R2_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === LEFT LEG 3 === -->
                  <g class="sp-tribal-joint" id="tribal_L3_s1" data-rest="0" style="transform-origin: 440px 465px;">
                    <path class="tribal-chitin" d="{paths['L3_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_L3_s2" data-rest="0" style="transform-origin: 360px 470px;">
                      <path class="tribal-chitin" d="{paths['L3_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_L3_s3" data-rest="0" style="transform-origin: 285px 520px;">
                        <path class="tribal-chitin" d="{paths['L3_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === RIGHT LEG 3 === -->
                  <g class="sp-tribal-joint" id="tribal_R3_s1" data-rest="0" style="transform-origin: 518px 465px;">
                    <path class="tribal-chitin" d="{paths['R3_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_R3_s2" data-rest="0" style="transform-origin: 598px 470px;">
                      <path class="tribal-chitin" d="{paths['R3_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_R3_s3" data-rest="0" style="transform-origin: 673px 520px;">
                        <path class="tribal-chitin" d="{paths['R3_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === LEFT LEG 4 === -->
                  <g class="sp-tribal-joint" id="tribal_L4_s1" data-rest="0" style="transform-origin: 440px 525px;">
                    <path class="tribal-chitin" d="{paths['L4_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_L4_s2" data-rest="0" style="transform-origin: 395px 560px;">
                      <path class="tribal-chitin" d="{paths['L4_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_L4_s3" data-rest="0" style="transform-origin: 360px 640px;">
                        <path class="tribal-chitin" d="{paths['L4_s3']}" />
                      </g>
                    </g>
                  </g>

                  <!-- === RIGHT LEG 4 === -->
                  <g class="sp-tribal-joint" id="tribal_R4_s1" data-rest="0" style="transform-origin: 518px 525px;">
                    <path class="tribal-chitin" d="{paths['R4_s1']}" />
                    <g class="sp-tribal-joint" id="tribal_R4_s2" data-rest="0" style="transform-origin: 563px 560px;">
                      <path class="tribal-chitin" d="{paths['R4_s2']}" />
                      <g class="sp-tribal-joint" id="tribal_R4_s3" data-rest="0" style="transform-origin: 598px 640px;">
                        <path class="tribal-chitin" d="{paths['R4_s3']}" />
                      </g>
                    </g>
                  </g>

                </g> <!-- End Legs Group -->

                <!-- === THÂN & BỤNG GRADIENT XANH TÍM NEON === -->
                <g class="spider-abdomen" id="tribal-body-core" style="transform-origin: 479px 500px; will-change: transform;">
                  <image href="assets/tribal_spider/body.png" x="400" y="343" width="161" height="329" />
                  <g id="tribal_fang_l" style="transform-origin: 470px 350px;">
                    <polygon points="466,350 472,342 470,356" fill="#00f2fe" opacity="0.85" filter="url(#tribal-cyan-glow)" />
                  </g>
                  <g id="tribal_fang_r" style="transform-origin: 488px 350px;">
                    <polygon points="492,350 486,342 488,356" fill="#00f2fe" opacity="0.85" filter="url(#tribal-cyan-glow)" />
                  </g>
                  <circle id="silk-nozzle" cx="479" cy="342" r="3.5" fill="#00f2fe" filter="url(#tribal-cyan-glow)" />
                </g>

              </g>
            </svg>'''

# Replace old svg-preview-tribal
idx_start = content.find('<svg id="svg-preview-tribal"')
idx_end = content.find('</svg>', idx_start) + 6
if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + tribal_svg_new + content[idx_end:]
    print("Replaced svg-preview-tribal in spider_showcase.html successfully!")
else:
    print("Error: Could not find svg-preview-tribal")

# Update Card 6 description
old_desc = 'Mô phỏng 100% ảnh gốc bằng Skeletal Rigging; bụng gradient tím neon; tơ gai nhọn rực sáng.'
new_desc = 'Skeletal Rigging 24 khớp vector lồng nhau; nhện đen gothic bóng bẩy; bụng gradient tím neon; dáng bò rình rập và săn mồi uy lực.'
content = content.replace(old_desc, new_desc)

# Add CSS for tribal chitin
if '.tribal-chitin' not in content:
    css_insert = '''
    .tribal-chitin {
      fill: #09070f;
      stroke: rgba(168, 85, 247, 0.55);
      stroke-width: 0.9px;
      transition: fill 0.3s;
    }
    .tribal-mode {
      filter: drop-shadow(0 6px 18px rgba(124, 58, 237, 0.45));
    }
'''
    content = content.replace('/* 4. Skin Selection Logic */', css_insert + '\n    /* 4. Skin Selection Logic */')

# Update updateLiveSpiderSvg() to handle tribal
old_skin_switch = '''        if (currentSkinId === 'mecha') {
          // Mecha CAD Vector sử dụng khung vuông đối xứng tâm (-547 -532 1830 1830)
          actor.classList.add('mecha-mode');
          liveSvg.setAttribute('width', '104');
          liveSvg.setAttribute('height', '104');
          actor.style.width = '104px';
          actor.style.height = '104px';
          actor.style.marginLeft = '-52px';
          actor.style.marginTop = '-52px';
          setTimeout(startMechaIdleAnimation, 120);
        } else {
          actor.classList.remove('mecha-mode');
          stopMechaIdleAnimation();
          liveSvg.setAttribute('width', '82');
          liveSvg.setAttribute('height', '82');
          actor.style.width = '82px';
          actor.style.height = '82px';
          actor.style.marginLeft = '-41px';
          actor.style.marginTop = '-41px';
        }'''

new_skin_switch = '''        if (currentSkinId === 'mecha') {
          actor.classList.remove('tribal-mode');
          stopTribalIdleAnimation();
          actor.classList.add('mecha-mode');
          liveSvg.setAttribute('width', '104');
          liveSvg.setAttribute('height', '104');
          actor.style.width = '104px';
          actor.style.height = '104px';
          actor.style.marginLeft = '-52px';
          actor.style.marginTop = '-52px';
          setTimeout(startMechaIdleAnimation, 120);
        } else if (currentSkinId === 'tribal') {
          actor.classList.remove('mecha-mode');
          stopMechaIdleAnimation();
          actor.classList.add('tribal-mode');
          liveSvg.setAttribute('width', '100');
          liveSvg.setAttribute('height', '100');
          actor.style.width = '100px';
          actor.style.height = '100px';
          actor.style.marginLeft = '-50px';
          actor.style.marginTop = '-50px';
          setTimeout(startTribalIdleAnimation, 120);
        } else {
          actor.classList.remove('mecha-mode');
          actor.classList.remove('tribal-mode');
          stopMechaIdleAnimation();
          stopTribalIdleAnimation();
          liveSvg.setAttribute('width', '82');
          liveSvg.setAttribute('height', '82');
          actor.style.width = '82px';
          actor.style.height = '82px';
          actor.style.marginLeft = '-41px';
          actor.style.marginTop = '-41px';
        }'''

content = content.replace(old_skin_switch, new_skin_switch)

# Add Tribal Idle and Walk Kinematics handlers
tribal_handlers = '''
    // --- TRIBAL KINEMATICS ENGINE (24 JOINTS) ---
    let tribalIdleRaf = null;
    let tribalIdleStartTime = 0;
    let tribalWalkRaf = null;
    let tribalWalkStartTime = 0;

    function startTribalIdleAnimation() {
      if (isCrawling || currentSkinId !== 'tribal') return;
      if (tribalIdleRaf) cancelAnimationFrame(tribalIdleRaf);
      tribalIdleStartTime = performance.now();

      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      const setJ = (id, delta) => {
        const el = liveSvg.querySelector(`#${id}`);
        if (el) el.style.transform = `rotate(${delta}deg)`;
      };

      function idleStep(now) {
        if (isCrawling || currentSkinId !== 'tribal') return;
        const t = (now - tribalIdleStartTime) / 1000;
        const pulse = Math.sin(t * 1.2);
        const clawPulse = Math.sin(t * 0.8) * 3;

        setJ('tribal_L1_s1', Math.sin(t * 0.7) * 2);
        setJ('tribal_L1_s2', -pulse * 2.5);
        setJ('tribal_L1_s3', clawPulse);

        setJ('tribal_R1_s1', -Math.sin(t * 0.7) * 2);
        setJ('tribal_R1_s2', pulse * 2.5);
        setJ('tribal_R1_s3', -clawPulse);

        setJ('tribal_L4_s1', -Math.sin(t * 0.8) * 2);
        setJ('tribal_L4_s2', pulse * 3);
        setJ('tribal_L4_s3', -clawPulse);

        setJ('tribal_R4_s1', Math.sin(t * 0.8) * 2);
        setJ('tribal_R4_s2', -pulse * 3);
        setJ('tribal_R4_s3', clawPulse);

        // Abdomen breathing & Aura pulse
        const body = liveSvg.querySelector('#tribal-body-core');
        if (body) {
          body.style.transform = `scaleY(${1.0 + pulse * 0.04})`;
        }
        const aura = liveSvg.querySelector('#tribal-aura');
        if (aura) {
          aura.setAttribute('rx', 145 + pulse * 6);
          aura.setAttribute('ry', 185 + pulse * 8);
        }

        tribalIdleRaf = requestAnimationFrame(idleStep);
      }

      tribalIdleRaf = requestAnimationFrame(idleStep);
    }

    function stopTribalIdleAnimation() {
      if (tribalIdleRaf) {
        cancelAnimationFrame(tribalIdleRaf);
        tribalIdleRaf = null;
      }
    }

    function startTribalWalkAnimation() {
      stopTribalIdleAnimation();
      if (tribalWalkRaf) cancelAnimationFrame(tribalWalkRaf);
      tribalWalkStartTime = performance.now();

      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      const setJ = (id, delta) => {
        const el = liveSvg.querySelector(`#${id}`);
        if (el) el.style.transform = `rotate(${delta}deg)`;
      };

      const isSync = (currentPacingMode === 'sync');
      const strideSpeed = isSync ? 2.4 : 1.35;

      function walkStep(now) {
        if (!isCrawling) return;
        const t = ((now - tribalWalkStartTime) / 380) * strideSpeed;

        const phi_A = t;
        const phi_B = t + Math.PI;

        const lift_A = Math.max(0, Math.cos(phi_A));
        const lift_B = Math.max(0, Math.cos(phi_B));

        // Group A: L1, R2, L3, R4
        setJ('tribal_L1_s1', Math.sin(phi_A) * 15);
        setJ('tribal_L1_s2', -22 * lift_A);
        setJ('tribal_L1_s3', Math.sin(phi_A) * 12 + 8 * lift_A);

        setJ('tribal_R2_s1', Math.sin(phi_A) * 12);
        setJ('tribal_R2_s2', 18 * lift_A);
        setJ('tribal_R2_s3', -Math.sin(phi_A) * 10 - 6 * lift_A);

        setJ('tribal_L3_s1', Math.sin(phi_A) * 14);
        setJ('tribal_L3_s2', 18 * lift_A);
        setJ('tribal_L3_s3', -Math.sin(phi_A) * 12 - 8 * lift_A);

        setJ('tribal_R4_s1', Math.sin(phi_A) * 16);
        setJ('tribal_R4_s2', -22 * lift_A);
        setJ('tribal_R4_s3', Math.sin(phi_A) * 14 + 10 * lift_A);

        // Group B: R1, L2, R3, L4
        setJ('tribal_R1_s1', -Math.sin(phi_B) * 15);
        setJ('tribal_R1_s2', 22 * lift_B);
        setJ('tribal_R1_s3', -Math.sin(phi_B) * 12 - 8 * lift_B);

        setJ('tribal_L2_s1', -Math.sin(phi_B) * 12);
        setJ('tribal_L2_s2', -18 * lift_B);
        setJ('tribal_L2_s3', Math.sin(phi_B) * 10 + 6 * lift_B);

        setJ('tribal_R3_s1', -Math.sin(phi_B) * 14);
        setJ('tribal_R3_s2', -18 * lift_B);
        setJ('tribal_R3_s3', Math.sin(phi_B) * 12 + 8 * lift_B);

        setJ('tribal_L4_s1', -Math.sin(phi_B) * 16);
        setJ('tribal_L4_s2', 22 * lift_B);
        setJ('tribal_L4_s3', -Math.sin(phi_B) * 14 - 10 * lift_B);

        // Body bob
        const master = liveSvg.querySelector('#tribal-spider-master');
        if (master) {
          const bobY = Math.sin(t * 2) * 2.8;
          const roll = Math.sin(t) * 1.4;
          master.setAttribute('transform', `translate(0, ${bobY}) rotate(${roll}, 479, 500)`);
        }

        // Fangs twitch
        const fangL = liveSvg.querySelector('#tribal_fang_l');
        const fangR = liveSvg.querySelector('#tribal_fang_r');
        if (fangL && fangR) {
          const fangAngle = Math.sin(t * 1.5) * 6;
          fangL.style.transform = `rotate(${fangAngle}deg)`;
          fangR.style.transform = `rotate(${-fangAngle}deg)`;
        }

        tribalWalkRaf = requestAnimationFrame(walkStep);
      }

      tribalWalkRaf = requestAnimationFrame(walkStep);
    }

    function stopTribalWalkAnimation() {
      if (tribalWalkRaf) {
        cancelAnimationFrame(tribalWalkRaf);
        tribalWalkRaf = null;
      }
      const liveSvg = document.getElementById('live-spider-svg');
      if (liveSvg) {
        liveSvg.querySelectorAll('.sp-tribal-joint').forEach(el => {
          gsap.to(el, { transform: 'rotate(0deg)', duration: 0.25, ease: 'power1.out' });
        });
        const master = liveSvg.querySelector('#tribal-spider-master');
        if (master) gsap.to(master, { attr: { transform: 'translate(0,0)' }, duration: 0.25 });
      }
    }
'''

content = content.replace('function startMechaWalkAnimation()', tribal_handlers + '\n    function startMechaWalkAnimation()')

# Hook startTribalWalkAnimation & stop into crawlSpiderTo
old_crawl_start = '''      if (currentSkinId === 'mecha') {
        startMechaWalkAnimation();
      } else {
        if (activeGaitTimeline) activeGaitTimeline.kill();
        activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);
      }'''

new_crawl_start = '''      if (currentSkinId === 'mecha') {
        startMechaWalkAnimation();
      } else if (currentSkinId === 'tribal') {
        startTribalWalkAnimation();
      } else {
        if (activeGaitTimeline) activeGaitTimeline.kill();
        activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);
      }'''

content = content.replace(old_crawl_start, new_crawl_start)

old_crawl_end = '''        onComplete: () => {
          if (currentSkinId === 'mecha') {
            stopMechaWalkAnimation();
          } else {
            if (activeGaitTimeline) {
              activeGaitTimeline.kill();
              activeGaitTimeline = null;
            }'''

new_crawl_end = '''        onComplete: () => {
          if (currentSkinId === 'mecha') {
            stopMechaWalkAnimation();
          } else if (currentSkinId === 'tribal') {
            stopTribalWalkAnimation();
          } else {
            if (activeGaitTimeline) {
              activeGaitTimeline.kill();
              activeGaitTimeline = null;
            }'''

content = content.replace(old_crawl_end, new_crawl_end)

# In crawlSpiderTo onComplete, re-trigger idle animation
old_retrigger = '''          if (currentSkinId === 'mecha') {
            setTimeout(startMechaIdleAnimation, 80);
          }'''

new_retrigger = '''          if (currentSkinId === 'mecha') {
            setTimeout(startMechaIdleAnimation, 80);
          } else if (currentSkinId === 'tribal') {
            setTimeout(startTribalIdleAnimation, 80);
          }'''

content = content.replace(old_retrigger, new_retrigger)

with open('frontend/preview/spider_showcase.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated spider_showcase.html successfully! Total size: {len(content)} bytes")
