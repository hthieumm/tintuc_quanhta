import os
import generate_tribal_paths

paths = generate_tribal_paths.paths

# Generate HTML
html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spider News Radar — Phòng Thí Nghiệm Gothic Tribal Neon Rig (24 Khớp)</title>
  <link rel="icon" href="data:,">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    :root {{
      --bg-dark: #08060f;
      --panel-bg: rgba(16, 12, 28, 0.85);
      --border-color: rgba(139, 92, 246, 0.25);
      --accent-neon: #a855f7;
      --accent-cyan: #06b6d4;
      --accent-pink: #ec4899;
      --text-main: #f3e8ff;
      --text-dim: #a89cb8;
      --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }}

    /* Top Telemetry Header */
    header {{
      background: rgba(12, 9, 22, 0.95);
      border-bottom: 1px solid var(--border-color);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 100;
    }}
    .logo-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-badge {{
      background: linear-gradient(135deg, #7c3aed, #ec4899);
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}
    .title-box h1 {{
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: #fff;
    }}
    .title-box p {{
      font-size: 11px;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }}
    .telemetry-pills {{
      display: flex;
      gap: 10px;
      font-family: var(--font-mono);
      font-size: 12px;
    }}
    .pill {{
      background: rgba(139, 92, 246, 0.1);
      border: 1px solid var(--border-color);
      padding: 6px 14px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .pill.active {{
      border-color: var(--accent-neon);
      color: #d8b4fe;
    }}
    .pill-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent-cyan);
      box-shadow: 0 0 8px var(--accent-cyan);
    }}

    /* Main Workspace Layout */
    .workspace {{
      display: flex;
      flex: 1;
      height: calc(100vh - 58px);
      position: relative;
    }}

    /* Left: Canvas Area */
    .canvas-panel {{
      flex: 1;
      position: relative;
      background: radial-gradient(circle at center, #170f2e 0%, #08060f 80%);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      user-select: none;
    }}

    /* Gothic Grid Background */
    .grid-overlay {{
      position: absolute;
      inset: 0;
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(139, 92, 246, 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(139, 92, 246, 0.05) 1px, transparent 1px);
      pointer-events: none;
    }}

    .viewport-container {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: grab;
      position: relative;
    }}
    .viewport-container:active {{
      cursor: grabbing;
    }}

    #tribal-svg-stage {{
      width: 640px;
      height: 860px;
      max-height: 92%;
      filter: drop-shadow(0 15px 35px rgba(0,0,0,0.8));
      transform-origin: center center;
      transition: transform 0.05s ease-out;
    }}

    /* Vector Chitin Styling */
    .tribal-chitin {{
      fill: #09070f;
      stroke: #2e1d4d;
      stroke-width: 0.8px;
      transition: fill 0.3s;
    }}
    .tribal-joint-dot {{
      fill: var(--accent-cyan);
      opacity: 0;
      transition: opacity 0.3s;
    }}
    .show-joints .tribal-joint-dot {{
      opacity: 0.85;
    }}

    /* Floating Viewport Controls */
    .canvas-controls {{
      position: absolute;
      bottom: 24px;
      left: 24px;
      display: flex;
      gap: 8px;
      z-index: 50;
    }}
    .ctrl-btn {{
      background: rgba(20, 15, 36, 0.9);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      width: 36px;
      height: 36px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
    }}
    .ctrl-btn:hover {{
      background: rgba(139, 92, 246, 0.3);
      border-color: var(--accent-neon);
      color: #fff;
    }}

    /* Right: Control Sidebar */
    .controls-panel {{
      width: 380px;
      background: var(--panel-bg);
      backdrop-filter: blur(12px);
      border-left: 1px solid var(--border-color);
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      z-index: 50;
    }}
    .controls-panel::-webkit-scrollbar {{
      width: 6px;
    }}
    .controls-panel::-webkit-scrollbar-thumb {{
      background: rgba(139, 92, 246, 0.3);
      border-radius: 3px;
    }}

    .section-title {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent-neon);
      font-family: var(--font-mono);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Presets Grid */
    .preset-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .preset-card {{
      background: rgba(26, 18, 48, 0.6);
      border: 1px solid rgba(139, 92, 246, 0.2);
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      text-align: left;
    }}
    .preset-card:hover {{
      border-color: var(--accent-neon);
      background: rgba(139, 92, 246, 0.15);
    }}
    .preset-card.active {{
      border-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.15);
      box-shadow: 0 0 12px rgba(6, 182, 212, 0.25);
    }}
    .preset-card h4 {{
      font-size: 13px;
      font-weight: 600;
      color: #fff;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .preset-card p {{
      font-size: 10px;
      color: var(--text-dim);
      line-height: 1.3;
    }}

    /* Speed Slider */
    .slider-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
      font-family: var(--font-mono);
    }}
    .slider-row input[type="range"] {{
      flex: 1;
      accent-color: var(--accent-cyan);
    }}

    /* Action Buttons */
    .action-btn {{
      background: linear-gradient(135deg, #7c3aed, #06b6d4);
      color: #fff;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
      width: 100%;
    }}
    .action-btn:hover {{
      opacity: 0.9;
      transform: translateY(-1px);
      box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }}

    /* Glow Color Pills */
    .glow-theme-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
    }}
    .theme-pill {{
      background: rgba(26, 18, 48, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 4px;
      padding: 6px;
      font-size: 10px;
      font-family: var(--font-mono);
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .theme-pill.active {{
      border-color: #fff;
      font-weight: 700;
    }}

    /* Manual Joints Accordion */
    .joints-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .leg-accordion {{
      background: rgba(22, 16, 42, 0.5);
      border: 1px solid rgba(139, 92, 246, 0.15);
      border-radius: 6px;
      overflow: hidden;
    }}
    .leg-header {{
      padding: 8px 12px;
      font-size: 11px;
      font-weight: 600;
      font-family: var(--font-mono);
      color: #d8b4fe;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.02);
    }}
    .leg-body {{
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .joint-ctrl {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 10px;
      font-family: var(--font-mono);
    }}
    .joint-label {{
      width: 50px;
      color: var(--text-dim);
    }}
    .joint-ctrl input[type="range"] {{
      flex: 1;
      height: 4px;
      accent-color: var(--accent-neon);
    }}
    .joint-val {{
      width: 32px;
      text-align: right;
      color: #fff;
    }}

    /* Silk Laser Canvas Overlay */
    #silk-canvas {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 40;
    }}
  </style>
</head>
<body>

  <!-- Top Telemetry Header -->
  <header>
    <div class="logo-group">
      <div class="logo-badge">🗡️</div>
      <div class="title-box">
        <h1>SPIDER RADAR — GOTHIC TRIBAL NEON RIG LABORATORY</h1>
        <p>Pure Vector Hierarchical Skeletal Rig • 24 Articulated Joints • 60 FPS GSAP</p>
      </div>
    </div>
    <div class="telemetry-pills">
      <div class="pill active">
        <div class="pill-dot"></div>
        <span id="telemetry-status">KINEMATICS: ACTIVE</span>
      </div>
      <div class="pill">
        <span>FPS:</span>
        <strong id="fps-display" style="color: var(--accent-cyan);">60.0</strong>
      </div>
      <div class="pill">
        <span>JOINTS: 24/24 RIGGED</span>
      </div>
      <a href="spider_showcase.html" style="text-decoration: none;">
        <div class="pill" style="cursor: pointer; background: rgba(139, 92, 246, 0.2);">
          <span>↗ Xem Showcase 6 Skin</span>
        </div>
      </a>
    </div>
  </header>

  <!-- Main Workspace -->
  <div class="workspace">
    <!-- Canvas Area -->
    <div class="canvas-panel" id="canvas-panel">
      <div class="grid-overlay"></div>
      <canvas id="silk-canvas"></canvas>

      <div class="viewport-container" id="viewport-container">
        <!-- SVG TRIBAL VECTOR RIG (24 JOINTS) -->
        <svg id="tribal-svg-stage" viewBox="200 20 560 860">
          <defs>
            <!-- Gothic Neon Aura Filter -->
            <filter id="tribal-neon-glow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="12" result="blur" />
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

            <!-- Cyan Glow Filter -->
            <filter id="cyan-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <!-- Ambient Neon Purple Aura -->
          <ellipse id="tribal-aura" cx="479" cy="500" rx="145" ry="185" fill="rgba(124, 58, 237, 0.16)" filter="url(#tribal-neon-glow)" />

          <!-- Master Skeleton Group -->
          <g id="tribal-spider-master" transform="translate(0, 0)">

            <!-- 8 HIERARCHICAL ARTICULATED LEGS (24 JOINTS) -->
            <g id="tribal-legs-group">

              <!-- === LEFT LEG 1 (Front Left) === -->
              <g id="tribal_L1_s1" data-rest="0" style="transform-origin: 440px 380px;">
                <path class="tribal-chitin" d="{paths['L1_s1']}" />
                <circle class="tribal-joint-dot" cx="440" cy="380" r="3.5" />
                <g id="tribal_L1_s2" data-rest="0" style="transform-origin: 418px 320px;">
                  <path class="tribal-chitin" d="{paths['L1_s2']}" />
                  <circle class="tribal-joint-dot" cx="418" cy="320" r="3.5" />
                  <g id="tribal_L1_s3" data-rest="0" style="transform-origin: 405px 245px;">
                    <path class="tribal-chitin" d="{paths['L1_s3']}" />
                    <circle class="tribal-joint-dot" cx="405" cy="245" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === RIGHT LEG 1 (Front Right) === -->
              <g id="tribal_R1_s1" data-rest="0" style="transform-origin: 518px 380px;">
                <path class="tribal-chitin" d="{paths['R1_s1']}" />
                <circle class="tribal-joint-dot" cx="518" cy="380" r="3.5" />
                <g id="tribal_R1_s2" data-rest="0" style="transform-origin: 540px 320px;">
                  <path class="tribal-chitin" d="{paths['R1_s2']}" />
                  <circle class="tribal-joint-dot" cx="540" cy="320" r="3.5" />
                  <g id="tribal_R1_s3" data-rest="0" style="transform-origin: 553px 245px;">
                    <path class="tribal-chitin" d="{paths['R1_s3']}" />
                    <circle class="tribal-joint-dot" cx="553" cy="245" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === LEFT LEG 2 (Upper-Lateral Left) === -->
              <g id="tribal_L2_s1" data-rest="0" style="transform-origin: 440px 425px;">
                <path class="tribal-chitin" d="{paths['L2_s1']}" />
                <circle class="tribal-joint-dot" cx="440" cy="425" r="3.5" />
                <g id="tribal_L2_s2" data-rest="0" style="transform-origin: 390px 415px;">
                  <path class="tribal-chitin" d="{paths['L2_s2']}" />
                  <circle class="tribal-joint-dot" cx="390" cy="415" r="3.5" />
                  <g id="tribal_L2_s3" data-rest="0" style="transform-origin: 320px 345px;">
                    <path class="tribal-chitin" d="{paths['L2_s3']}" />
                    <circle class="tribal-joint-dot" cx="320" cy="345" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === RIGHT LEG 2 (Upper-Lateral Right) === -->
              <g id="tribal_R2_s1" data-rest="0" style="transform-origin: 518px 425px;">
                <path class="tribal-chitin" d="{paths['R2_s1']}" />
                <circle class="tribal-joint-dot" cx="518" cy="425" r="3.5" />
                <g id="tribal_R2_s2" data-rest="0" style="transform-origin: 568px 415px;">
                  <path class="tribal-chitin" d="{paths['R2_s2']}" />
                  <circle class="tribal-joint-dot" cx="568" cy="415" r="3.5" />
                  <g id="tribal_R2_s3" data-rest="0" style="transform-origin: 638px 345px;">
                    <path class="tribal-chitin" d="{paths['R2_s3']}" />
                    <circle class="tribal-joint-dot" cx="638" cy="345" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === LEFT LEG 3 (Lower-Lateral Left) === -->
              <g id="tribal_L3_s1" data-rest="0" style="transform-origin: 440px 465px;">
                <path class="tribal-chitin" d="{paths['L3_s1']}" />
                <circle class="tribal-joint-dot" cx="440" cy="465" r="3.5" />
                <g id="tribal_L3_s2" data-rest="0" style="transform-origin: 360px 470px;">
                  <path class="tribal-chitin" d="{paths['L3_s2']}" />
                  <circle class="tribal-joint-dot" cx="360" cy="470" r="3.5" />
                  <g id="tribal_L3_s3" data-rest="0" style="transform-origin: 285px 520px;">
                    <path class="tribal-chitin" d="{paths['L3_s3']}" />
                    <circle class="tribal-joint-dot" cx="285" cy="520" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === RIGHT LEG 3 (Lower-Lateral Right) === -->
              <g id="tribal_R3_s1" data-rest="0" style="transform-origin: 518px 465px;">
                <path class="tribal-chitin" d="{paths['R3_s1']}" />
                <circle class="tribal-joint-dot" cx="518" cy="465" r="3.5" />
                <g id="tribal_R3_s2" data-rest="0" style="transform-origin: 598px 470px;">
                  <path class="tribal-chitin" d="{paths['R3_s2']}" />
                  <circle class="tribal-joint-dot" cx="598" cy="470" r="3.5" />
                  <g id="tribal_R3_s3" data-rest="0" style="transform-origin: 673px 520px;">
                    <path class="tribal-chitin" d="{paths['R3_s3']}" />
                    <circle class="tribal-joint-dot" cx="673" cy="520" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === LEFT LEG 4 (Rear Left) === -->
              <g id="tribal_L4_s1" data-rest="0" style="transform-origin: 440px 525px;">
                <path class="tribal-chitin" d="{paths['L4_s1']}" />
                <circle class="tribal-joint-dot" cx="440" cy="525" r="3.5" />
                <g id="tribal_L4_s2" data-rest="0" style="transform-origin: 395px 560px;">
                  <path class="tribal-chitin" d="{paths['L4_s2']}" />
                  <circle class="tribal-joint-dot" cx="395" cy="560" r="3.5" />
                  <g id="tribal_L4_s3" data-rest="0" style="transform-origin: 360px 640px;">
                    <path class="tribal-chitin" d="{paths['L4_s3']}" />
                    <circle class="tribal-joint-dot" cx="360" cy="640" r="3.5" />
                  </g>
                </g>
              </g>

              <!-- === RIGHT LEG 4 (Rear Right) === -->
              <g id="tribal_R4_s1" data-rest="0" style="transform-origin: 518px 525px;">
                <path class="tribal-chitin" d="{paths['R4_s1']}" />
                <circle class="tribal-joint-dot" cx="518" cy="525" r="3.5" />
                <g id="tribal_R4_s2" data-rest="0" style="transform-origin: 563px 560px;">
                  <path class="tribal-chitin" d="{paths['R4_s2']}" />
                  <circle class="tribal-joint-dot" cx="563" cy="560" r="3.5" />
                  <g id="tribal_R4_s3" data-rest="0" style="transform-origin: 598px 640px;">
                    <path class="tribal-chitin" d="{paths['R4_s3']}" />
                    <circle class="tribal-joint-dot" cx="598" cy="640" r="3.5" />
                  </g>
                </g>
              </g>

            </g> <!-- End Legs Group -->

            <!-- === BODY CORE (Cephalothorax & Gradient Neon Abdomen) === -->
            <g id="tribal-body-core" style="transform-origin: 479px 500px; will-change: transform;">
              <image href="assets/tribal_spider/body.png" x="400" y="343" width="161" height="329" />
              <!-- Chelicerae Fangs Snapper (Left & Right) -->
              <g id="tribal_fang_l" style="transform-origin: 470px 350px;">
                <polygon points="466,350 472,342 470,356" fill="#00f2fe" opacity="0.85" filter="url(#cyan-glow)" />
              </g>
              <g id="tribal_fang_r" style="transform-origin: 488px 350px;">
                <polygon points="492,350 486,342 488,356" fill="#00f2fe" opacity="0.85" filter="url(#cyan-glow)" />
              </g>
              <!-- Silk Nozzle at Head Top -->
              <circle id="silk-nozzle" cx="479" cy="342" r="3" fill="#00f2fe" filter="url(#cyan-glow)" />
            </g>

          </g> <!-- End Master Group -->
        </svg>
      </div>

      <!-- Canvas Navigation Controls -->
      <div class="canvas-controls">
        <button class="ctrl-btn" onclick="zoomIn()" title="Phóng to">＋</button>
        <button class="ctrl-btn" onclick="zoomOut()" title="Thu nhỏ">－</button>
        <button class="ctrl-btn" onclick="resetZoom()" title="Đặt lại góc nhìn">⟲</button>
        <button class="ctrl-btn" onclick="toggleJointDots()" title="Bật/Tắt điểm chốt khớp">🔴</button>
        <button class="ctrl-btn" onclick="toggleAura()" title="Bật/Tắt vầng hào quang">🔮</button>
      </div>
    </div>

    <!-- Right Controls Panel -->
    <div class="controls-panel">
      <!-- Presets Section -->
      <div>
        <div class="section-title">
          <span>1. Chế Độ Cử Động (Gothic Kinematics)</span>
          <span style="color: var(--accent-cyan);">60 FPS</span>
        </div>
        <div class="preset-grid">
          <div class="preset-card active" id="preset-idle" onclick="setPreset('idle')">
            <h4>🌿 Gothic Breathing</h4>
            <p>Nhịp thở ma mị của bụng & co duỗi khẽ các gai nhọn</p>
          </div>
          <div class="preset-card" id="preset-walk" onclick="setPreset('walk')">
            <h4>🏃 Tetrapod Prowl</h4>
            <p>Bò săn mồi 4 thì liên hoàn nhấc gối mượt mà</p>
          </div>
          <div class="preset-card" id="preset-strike" onclick="setPreset('strike')">
            <h4>⚡ Hunter Strike</h4>
            <p>Giương dàn gươm gai nhọn đe dọa con mồi</p>
          </div>
          <div class="preset-card" id="preset-coil" onclick="setPreset('coil')">
            <h4>🛡️ Shadow Coil</h4>
            <p>Thu gọn các chân bảo vệ cơ thể phòng thủ</p>
          </div>
        </div>
      </div>

      <!-- Speed Slider -->
      <div>
        <div class="section-title">Tốc Độ Cử Động (Speed)</div>
        <div class="slider-row">
          <input type="range" id="speed-slider" min="0.2" max="3.0" step="0.1" value="1.0" oninput="updateSpeed(this.value)">
          <span id="speed-val">1.0x</span>
        </div>
      </div>

      <!-- Silk & Reset Actions -->
      <div style="display: flex; gap: 10px;">
        <button class="action-btn" onclick="fireGothicSilk()">
          <span>⚡ BẮN TƠ GAI NEON</span>
        </button>
        <button class="action-btn" style="background: rgba(139, 92, 246, 0.2); border: 1px solid var(--border-color);" onclick="resetAllJoints()">
          <span>⟲ Đặt Lại Khớp</span>
        </button>
      </div>

      <!-- Optical Glow Themes -->
      <div>
        <div class="section-title">Màu Hào Quang Ma Mị (Aura FX)</div>
        <div class="glow-theme-grid">
          <div class="theme-pill active" id="theme-violet" onclick="setTheme('violet')">💜 VIOLET</div>
          <div class="theme-pill" id="theme-cyan" onclick="setTheme('cyan')">💙 CYAN</div>
          <div class="theme-pill" id="theme-crimson" onclick="setTheme('crimson')">❤️ CRIMSON</div>
          <div class="theme-pill" id="theme-emerald" onclick="setTheme('emerald')">💚 EMERALD</div>
        </div>
      </div>

      <!-- 24 Manual Joints Sliders -->
      <div>
        <div class="section-title">
          <span>2. Điều Khiển Từng Khớp Thủ Công</span>
          <span style="color: var(--accent-neon);">24 JOINTS</span>
        </div>
        <div class="joints-list" id="joints-container">
          <!-- Populated by JavaScript -->
        </div>
      </div>

    </div>
  </div>

  <script>
    // --- KINEMATICS ENGINE STATE ---
    let currentPreset = 'idle';
    let animSpeed = 1.0;
    let animRunning = true;
    let currentZoom = 1.0;
    let panX = 0, panY = 0;
    let isDragging = false, startX = 0, startY = 0;
    let showJoints = false;
    let showAura = true;

    // Joint Angle Values
    const joints = {{
      L1_s1: 0, L1_s2: 0, L1_s3: 0,
      R1_s1: 0, R1_s2: 0, R1_s3: 0,
      L2_s1: 0, L2_s2: 0, L2_s3: 0,
      R2_s1: 0, R2_s2: 0, R2_s3: 0,
      L3_s1: 0, L3_s2: 0, L3_s3: 0,
      R3_s1: 0, R3_s2: 0, R3_s3: 0,
      L4_s1: 0, L4_s2: 0, L4_s3: 0,
      R4_s1: 0, R4_s2: 0, R4_s3: 0
    }};

    // --- POPULATE MANUAL SLIDERS ---
    const legsMeta = [
      {{ id: 'L1', name: 'Chân Trước Trái (L1)', color: '#38bdf8' }},
      {{ id: 'R1', name: 'Chân Trước Phải (R1)', color: '#38bdf8' }},
      {{ id: 'L2', name: 'Chân Giữa-Trên Trái (L2)', color: '#c084fc' }},
      {{ id: 'R2', name: 'Chân Giữa-Trên Phải (R2)', color: '#c084fc' }},
      {{ id: 'L3', name: 'Chân Giữa-Dưới Trái (L3)', color: '#f472b6' }},
      {{ id: 'R3', name: 'Chân Giữa-Dưới Phải (R3)', color: '#f472b6' }},
      {{ id: 'L4', name: 'Chân Sau Trái (L4)', color: '#a78bfa' }},
      {{ id: 'R4', name: 'Chân Sau Phải (R4)', color: '#a78bfa' }}
    ];

    function buildJointSliders() {{
      const container = document.getElementById('joints-container');
      container.innerHTML = '';

      legsMeta.forEach(leg => {{
        const acc = document.createElement('div');
        acc.className = 'leg-accordion';
        acc.innerHTML = `
          <div class="leg-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
            <span style="color: ${{leg.color}}">🗡️ ${{leg.name}}</span>
            <span>▼</span>
          </div>
          <div class="leg-body">
            <div class="joint-ctrl">
              <span class="joint-label">Gốc s1</span>
              <input type="range" min="-45" max="45" value="0" id="slider_${{leg.id}}_s1" oninput="setManualJoint('${{leg.id}}_s1', this.value)">
              <span class="joint-val" id="val_${{leg.id}}_s1">0°</span>
            </div>
            <div class="joint-ctrl">
              <span class="joint-label">Gối s2</span>
              <input type="range" min="-45" max="45" value="0" id="slider_${{leg.id}}_s2" oninput="setManualJoint('${{leg.id}}_s2', this.value)">
              <span class="joint-val" id="val_${{leg.id}}_s2">0°</span>
            </div>
            <div class="joint-ctrl">
              <span class="joint-label">Móng s3</span>
              <input type="range" min="-45" max="45" value="0" id="slider_${{leg.id}}_s3" oninput="setManualJoint('${{leg.id}}_s3', this.value)">
              <span class="joint-val" id="val_${{leg.id}}_s3">0°</span>
            </div>
          </div>
        `;
        container.appendChild(acc);
      }});
    }}

    function setManualJoint(jointKey, val) {{
      val = parseFloat(val);
      joints[jointKey] = val;
      document.getElementById(`val_${{jointKey}}`).innerText = `${{Math.round(val)}}°`;
      applyJointTransform(jointKey, val);
    }}

    function applyJointTransform(jointKey, angle) {{
      const el = document.getElementById(`tribal_${{jointKey}}`);
      if (el) {{
        el.style.transform = `rotate(${{angle}}deg)`;
      }}
    }}

    function resetAllJoints() {{
      Object.keys(joints).forEach(k => {{
        joints[k] = 0;
        const slider = document.getElementById(`slider_${{k}}`);
        if (slider) slider.value = 0;
        const valTxt = document.getElementById(`val_${{k}}`);
        if (valTxt) valTxt.innerText = '0°';
        applyJointTransform(k, 0);
      }});
      gsap.to('#tribal-spider-master', {{ x: 0, y: 0, rotation: 0, duration: 0.4 }});
      gsap.to('#tribal-body-core', {{ scaleY: 1, duration: 0.4 }});
    }}

    // --- KINEMATICS UPDATE LOOP (60-120 FPS) ---
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsTime = performance.now();

    function updateKinematics(now) {{
      const dt = (now - lastTime) / 1000;
      lastTime = now;

      // FPS Counter
      frameCount++;
      if (now - fpsTime >= 500) {{
        const fps = (frameCount * 1000) / (now - fpsTime);
        document.getElementById('fps-display').innerText = fps.toFixed(1);
        frameCount = 0;
        fpsTime = now;
      }}

      if (animRunning) {{
        const t = (now * 0.003) * animSpeed;

        if (currentPreset === 'walk') {{
          // --- TETRAPOD PROWL WALK (QUADRATURE GAIT) ---
          const phi_A = t;
          const phi_B = t + Math.PI;

          const lift_A = Math.max(0, Math.cos(phi_A));
          const lift_B = Math.max(0, Math.cos(phi_B));

          // Alternating Tetrapod groups
          // Group A: L1, R2, L3, R4
          const L1_s1 = Math.sin(phi_A) * 15;
          const L1_s2 = -22 * lift_A;
          const L1_s3 = Math.sin(phi_A) * 12 + 8 * lift_A;

          const R2_s1 = Math.sin(phi_A) * 12;
          const R2_s2 = 18 * lift_A;
          const R2_s3 = -Math.sin(phi_A) * 10 - 6 * lift_A;

          const L3_s1 = Math.sin(phi_A) * 14;
          const L3_s2 = 18 * lift_A;
          const L3_s3 = -Math.sin(phi_A) * 12 - 8 * lift_A;

          const R4_s1 = Math.sin(phi_A) * 16;
          const R4_s2 = -22 * lift_A;
          const R4_s3 = Math.sin(phi_A) * 14 + 10 * lift_A;

          // Group B: R1, L2, R3, L4
          const R1_s1 = -Math.sin(phi_B) * 15;
          const R1_s2 = 22 * lift_B;
          const R1_s3 = -Math.sin(phi_B) * 12 - 8 * lift_B;

          const L2_s1 = -Math.sin(phi_B) * 12;
          const L2_s2 = -18 * lift_B;
          const L2_s3 = Math.sin(phi_B) * 10 + 6 * lift_B;

          const R3_s1 = -Math.sin(phi_B) * 14;
          const R3_s2 = -18 * lift_B;
          const R3_s3 = Math.sin(phi_B) * 12 + 8 * lift_B;

          const L4_s1 = -Math.sin(phi_B) * 16;
          const L4_s2 = 22 * lift_B;
          const L4_s3 = -Math.sin(phi_B) * 14 - 10 * lift_B;

          // Apply all joints
          applyJointTransform('L1_s1', L1_s1);
          applyJointTransform('L1_s2', L1_s2);
          applyJointTransform('L1_s3', L1_s3);

          applyJointTransform('R1_s1', R1_s1);
          applyJointTransform('R1_s2', R1_s2);
          applyJointTransform('R1_s3', R1_s3);

          applyJointTransform('L2_s1', L2_s1);
          applyJointTransform('L2_s2', L2_s2);
          applyJointTransform('L2_s3', L2_s3);

          applyJointTransform('R2_s1', R2_s1);
          applyJointTransform('R2_s2', R2_s2);
          applyJointTransform('R2_s3', R2_s3);

          applyJointTransform('L3_s1', L3_s1);
          applyJointTransform('L3_s2', L3_s2);
          applyJointTransform('L3_s3', L3_s3);

          applyJointTransform('R3_s1', R3_s1);
          applyJointTransform('R3_s2', R3_s2);
          applyJointTransform('R3_s3', R3_s3);

          applyJointTransform('L4_s1', L4_s1);
          applyJointTransform('L4_s2', L4_s2);
          applyJointTransform('L4_s3', L4_s3);

          applyJointTransform('R4_s1', R4_s1);
          applyJointTransform('R4_s2', R4_s2);
          applyJointTransform('R4_s3', R4_s3);

          // Body sway & heave
          const master = document.getElementById('tribal-spider-master');
          if (master) {{
            const bobY = Math.sin(t * 2) * 2.8;
            const roll = Math.sin(t) * 1.4;
            master.setAttribute('transform', `translate(0, ${{bobY}}) rotate(${{roll}}, 479, 500)`);
          }}

          // Abdomen breathing & Fangs twitch
          const body = document.getElementById('tribal-body-core');
          if (body) {{
            const scaleY = 1.0 + Math.sin(t * 0.8) * 0.035;
            body.style.transform = `scaleY(${{scaleY}})`;
          }}
          const fangL = document.getElementById('tribal_fang_l');
          const fangR = document.getElementById('tribal_fang_r');
          if (fangL && fangR) {{
            const fangAngle = Math.sin(t * 1.5) * 6;
            fangL.style.transform = `rotate(${{fangAngle}}deg)`;
            fangR.style.transform = `rotate(${{-fangAngle}}deg)`;
          }}

        }} else if (currentPreset === 'idle') {{
          // --- IDLE GOTHIC BREATHING ---
          const pulse = Math.sin(t * 0.7);
          const clawPulse = Math.sin(t * 0.5) * 3;

          applyJointTransform('L1_s1', Math.sin(t * 0.5) * 2);
          applyJointTransform('L1_s2', -pulse * 2.5);
          applyJointTransform('L1_s3', clawPulse);

          applyJointTransform('R1_s1', -Math.sin(t * 0.5) * 2);
          applyJointTransform('R1_s2', pulse * 2.5);
          applyJointTransform('R1_s3', -clawPulse);

          applyJointTransform('L4_s1', -Math.sin(t * 0.6) * 2);
          applyJointTransform('L4_s2', pulse * 3);
          applyJointTransform('L4_s3', -clawPulse);

          applyJointTransform('R4_s1', Math.sin(t * 0.6) * 2);
          applyJointTransform('R4_s2', -pulse * 3);
          applyJointTransform('R4_s3', clawPulse);

          // Abdomen rhythmic deep breath
          const body = document.getElementById('tribal-body-core');
          if (body) {{
            const scaleY = 1.0 + pulse * 0.045;
            body.style.transform = `scaleY(${{scaleY}})`;
          }}

          // Aura pulse
          const aura = document.getElementById('tribal-aura');
          if (aura && showAura) {{
            aura.setAttribute('rx', 145 + pulse * 6);
            aura.setAttribute('ry', 185 + pulse * 8);
          }}

        }} else if (currentPreset === 'strike') {{
          // --- HUNTER STRIKE PRESET ---
          const tremor = Math.sin(t * 8) * 1.2;
          applyJointTransform('L1_s1', -28 + tremor);
          applyJointTransform('L1_s2', -34 + tremor);
          applyJointTransform('L1_s3', 25 + tremor);

          applyJointTransform('R1_s1', 28 - tremor);
          applyJointTransform('R1_s2', 34 - tremor);
          applyJointTransform('R1_s3', -25 - tremor);

          applyJointTransform('L2_s1', -18);
          applyJointTransform('L2_s2', -24);
          applyJointTransform('L2_s3', 18);

          applyJointTransform('R2_s1', 18);
          applyJointTransform('R2_s2', 24);
          applyJointTransform('R2_s3', -18);

          // Rear legs braced for attack
          applyJointTransform('L4_s1', 14);
          applyJointTransform('L4_s2', 22);
          applyJointTransform('L4_s3', -18);

          applyJointTransform('R4_s1', -14);
          applyJointTransform('R4_s2', -22);
          applyJointTransform('R4_s3', 18);

          const master = document.getElementById('tribal-spider-master');
          if (master) {{
            master.setAttribute('transform', `translate(0, ${{Math.sin(t * 3) * 1.5}})`);
          }}

        }} else if (currentPreset === 'coil') {{
          // --- SHADOW DEFENSIVE COIL ---
          const breathe = Math.sin(t * 0.4) * 1.5;
          applyJointTransform('L1_s1', 18 + breathe);
          applyJointTransform('L1_s2', 25);
          applyJointTransform('L1_s3', -20);

          applyJointTransform('R1_s1', -18 - breathe);
          applyJointTransform('R1_s2', -25);
          applyJointTransform('R1_s3', 20);

          applyJointTransform('L2_s1', 15);
          applyJointTransform('L2_s2', 20);
          applyJointTransform('L2_s3', -16);

          applyJointTransform('R2_s1', -15);
          applyJointTransform('R2_s2', -20);
          applyJointTransform('R2_s3', 16);

          applyJointTransform('L4_s1', -18);
          applyJointTransform('L4_s2', -25);
          applyJointTransform('L4_s3', 22);

          applyJointTransform('R4_s1', 18);
          applyJointTransform('R4_s2', 25);
          applyJointTransform('R4_s3', -22);
        }}
      }}

      requestAnimationFrame(updateKinematics);
    }}
    requestAnimationFrame(updateKinematics);

    // --- PRESETS SELECTION ---
    function setPreset(presetName) {{
      currentPreset = presetName;
      document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
      const activeCard = document.getElementById(`preset-${{presetName}}`);
      if (activeCard) activeCard.classList.add('active');

      if (presetName === 'strike') {{
        // Snap attack fangs
        gsap.to('#tribal_fang_l', {{ rotation: 18, duration: 0.15, yoyo: true, repeat: 3 }});
        gsap.to('#tribal_fang_r', {{ rotation: -18, duration: 0.15, yoyo: true, repeat: 3 }});
      }}
    }}

    function updateSpeed(val) {{
      animSpeed = parseFloat(val);
      document.getElementById('speed-val').innerText = `${{animSpeed.toFixed(1)}}x`;
    }}

    // --- GOTHIC SILK FIRING FX ---
    function fireGothicSilk() {{
      const canvas = document.getElementById('silk-canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

      const stage = document.getElementById('tribal-svg-stage');
      const rect = stage.getBoundingClientRect();
      const parentRect = canvas.getBoundingClientRect();

      // Start at head fangs
      const startX = rect.left + rect.width * (479 - 200) / 560 - parentRect.left;
      const startY = rect.top + rect.height * (342 - 20) / 860 - parentRect.top;

      // Target top-right
      const endX = startX + 320;
      const endY = startY - 260;

      // Flash recoil on front legs
      gsap.to(['#tribal_L1_s2', '#tribal_R1_s2'], {{
        rotation: '-=15',
        duration: 0.1,
        yoyo: true,
        repeat: 1
      }});

      // Draw spiked neon filament
      let progress = 0;
      const startTime = performance.now();
      const duration = 500;

      function renderSilk(now) {{
        const elapsed = now - startTime;
        progress = Math.min(1, elapsed / duration);

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const curX = startX + (endX - startX) * progress;
        const curY = startY + (endY - startY) * progress;

        // Neon Glow Beam
        ctx.shadowColor = '#a855f7';
        ctx.shadowBlur = 15;
        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = 2.5;

        ctx.beginPath();
        ctx.moveTo(startX, startY);
        // Bezier arch
        const midX = (startX + curX) / 2 + 30;
        const midY = (startY + curY) / 2 - 40;
        ctx.quadraticCurveTo(midX, midY, curX, curY);
        ctx.stroke();

        // Spikes along silk
        if (progress > 0.3) {{
          ctx.strokeStyle = '#06b6d4';
          ctx.lineWidth = 1.2;
          for (let i = 0.2; i <= progress; i += 0.15) {{
            const px = startX + (endX - startX) * i;
            const py = startY + (endY - startY) * i;
            ctx.beginPath();
            ctx.moveTo(px - 6, py - 4);
            ctx.lineTo(px + 6, py + 4);
            ctx.stroke();
          }}
        }}

        if (progress < 1) {{
          requestAnimationFrame(renderSilk);
        }} else {{
          // Fade out
          gsap.to(canvas, {{
            opacity: 0,
            duration: 0.6,
            onComplete: () => {{
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              canvas.style.opacity = 1;
            }}
          }});
        }}
      }}
      requestAnimationFrame(renderSilk);
    }}

    // --- GLOW THEME SETTINGS ---
    function setTheme(theme) {{
      document.querySelectorAll('.theme-pill').forEach(p => p.classList.remove('active'));
      const activePill = document.getElementById(`theme-${{theme}}`);
      if (activePill) activePill.classList.add('active');

      const aura = document.getElementById('tribal-aura');
      if (!aura) return;

      if (theme === 'violet') {{
        aura.setAttribute('fill', 'rgba(124, 58, 237, 0.18)');
      }} else if (theme === 'cyan') {{
        aura.setAttribute('fill', 'rgba(6, 182, 212, 0.22)');
      }} else if (theme === 'crimson') {{
        aura.setAttribute('fill', 'rgba(239, 68, 68, 0.22)');
      }} else if (theme === 'emerald') {{
        aura.setAttribute('fill', 'rgba(16, 185, 129, 0.22)');
      }}
    }}

    // --- VIEWPORT CONTROLS ---
    function zoomIn() {{
      currentZoom = Math.min(2.5, currentZoom + 0.15);
      applyViewportTransform();
    }}
    function zoomOut() {{
      currentZoom = Math.max(0.6, currentZoom - 0.15);
      applyViewportTransform();
    }}
    function resetZoom() {{
      currentZoom = 1.0;
      panX = 0; panY = 0;
      applyViewportTransform();
    }}
    function applyViewportTransform() {{
      const stage = document.getElementById('tribal-svg-stage');
      stage.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{currentZoom}})`;
    }}

    function toggleJointDots() {{
      showJoints = !showJoints;
      document.getElementById('tribal-svg-stage').classList.toggle('show-joints', showJoints);
    }}

    function toggleAura() {{
      showAura = !showAura;
      const aura = document.getElementById('tribal-aura');
      if (aura) aura.style.display = showAura ? 'block' : 'none';
    }}

    // Drag to Pan
    const vpContainer = document.getElementById('viewport-container');
    vpContainer.addEventListener('mousedown', (e) => {{
      if (e.target.tagName !== 'BUTTON') {{
        isDragging = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
      }}
    }});
    window.addEventListener('mousemove', (e) => {{
      if (isDragging) {{
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        applyViewportTransform();
      }}
    }});
    window.addEventListener('mouseup', () => {{
      isDragging = false;
    }});

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {{
      buildJointSliders();
    }});
  </script>
</body>
</html>
'''

with open('frontend/preview/test_tribal_vector_rig.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Created test_tribal_vector_rig.html successfully! Size: {len(html_content)} bytes")
