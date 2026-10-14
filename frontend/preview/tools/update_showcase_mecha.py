import re
import os

showcase_path = r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\spider_showcase.html'
svg_path = r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg'

with open(showcase_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(svg_path, 'r', encoding='utf-8') as f:
    raw_svg = f.read()

# Build the enhanced mecha SVG for the preview and live actor
# Defs for laser glow and sensor glow
defs_block = """
  <defs>
    <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur1" />
      <feGaussianBlur stdDeviation="2" result="blur2" />
      <feMerge>
        <feMergeNode in="blur1" />
        <feMergeNode in="blur2" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="sensor-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="laser-cyan-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="30%" stop-color="#00E5FF" />
      <stop offset="100%" stop-color="#00B4D8" />
    </linearGradient>
  </defs>
"""

cockpit_optics = """
  <g id="mecha-cockpit-optics" style="pointer-events:none;">
    <!-- Optical Visor Sensors -->
    <circle class="spider-eye mecha-sensor" id="mecha-eye-left" cx="352" cy="225" r="4.5" fill="#00E5FF" filter="url(#sensor-glow)" />
    <circle class="spider-eye mecha-sensor" id="mecha-eye-center" cx="368" cy="216" r="6.5" fill="#00E5FF" filter="url(#sensor-glow)" />
    <circle class="spider-eye mecha-sensor" id="mecha-eye-right" cx="384" cy="225" r="4.5" fill="#00E5FF" filter="url(#sensor-glow)" />
    <!-- Center Core Arc Light -->
    <circle cx="368" cy="216" r="2.5" fill="#FFFFFF" />
    <!-- Silk Laser Emitter Nozzle -->
    <circle id="silk-nozzle" cx="368" cy="142" r="3" fill="#00E5FF" filter="url(#sensor-glow)" />
  </g>
"""

# Extract the body of raw_svg (between <svg ...> and </svg>)
svg_match = re.search(r'<svg[^>]*>([\s\S]*?)</svg>', raw_svg)
if not svg_match:
    print("Could not find svg in raw_svg!")
    exit(1)

inner_svg = svg_match.group(1)

# Ensure cockpit optics is inserted inside spider-root
if '</g>' in inner_svg:
    # insert before last </g> which closes spider-root
    last_g_pos = inner_svg.rfind('</g>')
    inner_svg = inner_svg[:last_g_pos] + cockpit_optics + inner_svg[last_g_pos:]

# Complete mecha preview SVG
new_mecha_svg = f"""<svg id="svg-preview-mecha" viewBox="0 0 736 1308" width="160" height="160">
  <style>
    #svg-preview-mecha .sp-art path, #svg-preview-mecha #layer-body path {{ fill: #0F172A; }}
    #svg-preview-mecha #layer-blueprint path {{ fill: #00E5FF; opacity: 0.35; }}
    #svg-preview-mecha #layer-background {{ fill: transparent; }}
    #svg-preview-mecha .sp-joint {{ transform-origin: 0 0; }}
    #live-spider-svg .sp-art path, #live-spider-svg #layer-body path {{ fill: #0F172A; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.4)); }}
    #live-spider-svg #layer-blueprint {{ display: none; }}
    #live-spider-svg #layer-background {{ fill: transparent; }}
    #live-spider-svg .sp-joint {{ transform-origin: 0 0; }}
  </style>
{defs_block}
{inner_svg}
</svg>"""

# Replace svg-preview-mecha in spider_showcase.html
pattern = r'<svg id="svg-preview-mecha"[\s\S]*?</svg>'
if re.search(pattern, content):
    content = re.sub(pattern, new_mecha_svg, content, count=1)
    print("Replaced svg-preview-mecha in spider_showcase.html")
else:
    print("Could not find svg-preview-mecha in spider_showcase.html!")

# Now add Mecha Kinematics Engine into spider_showcase.html
mecha_engine_code = """
    // ==========================================
    // ⚙️ MECHA 29-JOINT KINEMATICS WALK ENGINE
    // ==========================================
    let mechaWalkRaf = null;
    let mechaWalkStartTime = 0;

    function startMechaWalkAnimation() {
      if (mechaWalkRaf) cancelAnimationFrame(mechaWalkRaf);
      mechaWalkStartTime = performance.now();

      const restAngles = {};
      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      liveSvg.querySelectorAll('.sp-joint').forEach(el => {
        restAngles[el.id] = parseFloat(el.dataset.rest) || 0;
      });

      const n_seg = { 1: 3, 2: 3, 3: 3, 4: 5 };
      const amp_walk = { 1: [14, 20, 16], 2: [15, 22, 18], 3: [12, 16, 14], 4: [10, 10, 8, 7, 6] };
      const spiderRoot = liveSvg.querySelector('#spider-root');
      const isSync = (currentPacingMode === 'sync');
      const speed = isSync ? 1.8 : 1.1;

      function step(now) {
        if (!isCrawling) return;
        const t = ((now - mechaWalkStartTime) / 450) * speed;

        for (const n in n_seg) {
          for (let i = 0; i < n_seg[n]; i++) {
            const isAlphaLeg = (n == 1 || n == 3);
            const phaseLeg = isAlphaLeg ? 0 : Math.PI;
            const a = amp_walk[n][i];
            const wL = Math.sin(t + phaseLeg + i * 0.35);
            const wR = Math.sin(t + (Math.PI - phaseLeg) + i * 0.35);

            const lEl = liveSvg.querySelector(`#L${n}_s${i+1}`);
            const rEl = liveSvg.querySelector(`#R${n}_s${i+1}`);
            if (lEl && restAngles[`L${n}_s${i+1}`] !== undefined) {
              lEl.setAttribute('transform', `rotate(${restAngles[`L${n}_s${i+1}`] + a * wL})`);
            }
            if (rEl && restAngles[`R${n}_s${i+1}`] !== undefined) {
              rEl.setAttribute('transform', `rotate(${restAngles[`R${n}_s${i+1}`] - a * wR})`);
            }
          }
        }

        const antEl = liveSvg.querySelector('#ANT_s1');
        if (antEl && restAngles['ANT_s1'] !== undefined) {
          antEl.setAttribute('transform', `rotate(${restAngles['ANT_s1'] + 7 * Math.sin(t * 1.3)})`);
        }

        if (spiderRoot) {
          spiderRoot.setAttribute('transform', `translate(0, ${3.5 * Math.sin(t * 2)})`);
        }

        mechaWalkRaf = requestAnimationFrame(step);
      }

      mechaWalkRaf = requestAnimationFrame(step);
    }

    function stopMechaWalkAnimation() {
      if (mechaWalkRaf) {
        cancelAnimationFrame(mechaWalkRaf);
        mechaWalkRaf = null;
      }
      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      // Reset all 29 joints back to rest angle smoothly with elastic rebound
      liveSvg.querySelectorAll('.sp-joint').forEach(el => {
        const rest = parseFloat(el.dataset.rest) || 0;
        gsap.to(el, {
          attr: { transform: `rotate(${rest})` },
          duration: 0.28,
          ease: "power2.out"
        });
      });

      const spiderRoot = liveSvg.querySelector('#spider-root');
      if (spiderRoot) {
        gsap.to(spiderRoot, { attr: { transform: 'translate(0, 0)' }, duration: 0.28 });
      }
    }
"""

# Check where crawlSpiderTo calls buildTetrapodGaitTimeline
# In crawlSpiderTo:
# if (activeGaitTimeline) activeGaitTimeline.kill();
# activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);
# We can wrap it:
# if (currentSkinId === 'mecha') {
#   startMechaWalkAnimation();
# } else {
#   if (activeGaitTimeline) activeGaitTimeline.kill();
#   activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);
# }

crawl_patch_target = """      if (activeGaitTimeline) activeGaitTimeline.kill();
      activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);"""

crawl_patch_replacement = """      if (currentSkinId === 'mecha') {
        startMechaWalkAnimation();
      } else {
        if (activeGaitTimeline) activeGaitTimeline.kill();
        activeGaitTimeline = buildTetrapodGaitTimeline(stepDuration, moveDuration);
      }"""

if crawl_patch_target in content:
    content = content.replace(crawl_patch_target, crawl_patch_replacement, 1)
    print("Patched start of walk in crawlSpiderTo!")
else:
    print("Warning: crawl_patch_target not found!")

# Now patch masterTl onComplete:
complete_patch_target = """        onComplete: () => {
          if (activeGaitTimeline) {
            activeGaitTimeline.kill();
            activeGaitTimeline = null;
          }
          gsap.to('#live-spider-svg .leg, #live-spider-svg .knee-group', {
            rotation: 0, duration: 0.2, ease: "power1.out"
          });
          gsap.to('#live-spider-body-carrier', { y: 0, duration: 0.2 });"""

complete_patch_replacement = """        onComplete: () => {
          if (currentSkinId === 'mecha') {
            stopMechaWalkAnimation();
          } else {
            if (activeGaitTimeline) {
              activeGaitTimeline.kill();
              activeGaitTimeline = null;
            }
            gsap.to('#live-spider-svg .leg, #live-spider-svg .knee-group', {
              rotation: 0, duration: 0.2, ease: "power1.out"
            });
            gsap.to('#live-spider-body-carrier', { y: 0, duration: 0.2 });
          }"""

if complete_patch_target in content:
    content = content.replace(complete_patch_target, complete_patch_replacement, 1)
    print("Patched onComplete in crawlSpiderTo!")
else:
    print("Warning: complete_patch_target not found!")

# Insert mecha_engine_code right before crawlSpiderTo
if "function crawlSpiderTo" in content:
    content = content.replace("function crawlSpiderTo", mecha_engine_code + "\n    function crawlSpiderTo", 1)
    print("Inserted mecha_engine_code before crawlSpiderTo!")
else:
    print("Warning: function crawlSpiderTo not found!")

# Update applySentimentToLiveSpider to support mecha sensors
sentiment_target = """      eyes.forEach(eye => {
        gsap.to(eye, { fill: color, duration: 0.3 });
      });"""

sentiment_replacement = """      eyes.forEach(eye => {
        gsap.to(eye, { fill: color, duration: 0.3 });
      });
      const mechaSensors = document.querySelectorAll('#live-spider-svg .mecha-sensor');
      mechaSensors.forEach(s => {
        gsap.to(s, { fill: color, duration: 0.3 });
      });"""

if sentiment_target in content:
    content = content.replace(sentiment_target, sentiment_replacement, 1)
    print("Patched applySentimentToLiveSpider for mecha sensors!")

with open(showcase_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {showcase_path} successfully!")
print(f"New file size: {os.path.getsize(showcase_path):,} bytes")
