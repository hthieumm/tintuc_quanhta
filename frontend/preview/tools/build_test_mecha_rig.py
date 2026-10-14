import os
import re

svg_path = r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\skin_mecha\mech_spider.svg'
out_path = r'D:\code_tienich_forme\tintuc_quanhta\frontend\preview\test_mecha_vector_rig.html'

with open(svg_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()

# Add glowing filters and sensor eye to the SVG if not present
# Let's inspect the defs or insert defs after <svg ...>
defs_to_add = """
<defs>
  <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6" result="blur1" />
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
</defs>
"""

# Insert defs right after the opening <svg ...> tag
svg_with_defs = re.sub(r'(<svg[^>]*>)', r'\1' + defs_to_add, svg_content, count=1)

# Add glowing sensor optics to the cephalothorax/cockpit (around 368, 220) and antenna tip (368, 140)
cockpit_enhancement = """
<g id="mecha-cockpit-optics" style="pointer-events:none;">
  <!-- Optical Visor Sensor Core -->
  <circle id="mecha-eye-left" cx="352" cy="225" r="4.5" fill="#00E5FF" filter="url(#sensor-glow)" />
  <circle id="mecha-eye-center" cx="368" cy="216" r="6.5" fill="#00E5FF" filter="url(#sensor-glow)" />
  <circle id="mecha-eye-right" cx="384" cy="225" r="4.5" fill="#00E5FF" filter="url(#sensor-glow)" />
  <!-- Center Core Pulsing Arc -->
  <circle cx="368" cy="216" r="2.5" fill="#FFFFFF" />
  <!-- Silk Laser Emitter Nozzle -->
  <circle id="silk-nozzle" cx="368" cy="142" r="3.5" fill="#00E5FF" filter="url(#sensor-glow)" />
  <!-- In-SVG Laser Silk Layer -->
  <path id="laser-silk-path" d="" fill="none" stroke="#00E5FF" stroke-width="2.8" filter="url(#laser-glow)" opacity="0" />
  <circle id="laser-target-dot" cx="0" cy="0" r="8" fill="#00E5FF" filter="url(#laser-glow)" opacity="0" />
</g>
"""

# Insert cockpit enhancement before the closing </g> of spider-root
svg_enhanced = svg_with_defs.replace('</g>\n</svg>', cockpit_enhancement + '</g>\n</svg>')
if '</g>\n</svg>' not in svg_with_defs:
    svg_enhanced = svg_with_defs.replace('</svg>', cockpit_enhancement + '</svg>')

html_template = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spider News Radar — Phòng Thí Nghiệm Mecha Vector Rigging (29 Khớp)</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0a0b10;
      --bg-panel: #11131a;
      --bg-card: #181b24;
      --border-subtle: #232836;
      --border-focus: #00E5FF;
      --cyan-neon: #00E5FF;
      --cyan-dim: rgba(0, 229, 255, 0.15);
      --red-alert: #FF1744;
      --amber-warn: #F59E0B;
      --text-main: #E2E8F0;
      --text-muted: #94A3B8;
      --font-mono: 'JetBrains Mono', monospace;
      --font-sans: 'Plus Jakarta Sans', sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* TOP HEADER BAR */
    header {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 100;
      flex-shrink: 0;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--cyan-dim);
      border: 1px solid var(--cyan-neon);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      box-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
    }
    .brand-title {
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: #fff;
    }
    .brand-subtitle {
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .header-pills {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .pill {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 4px 10px;
      border-radius: 6px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .pill.active {
      border-color: var(--cyan-neon);
      color: var(--cyan-neon);
      background: var(--cyan-dim);
    }
    .pulse-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--cyan-neon);
      box-shadow: 0 0 8px var(--cyan-neon);
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }

    /* MAIN CONTAINER: VIEWPORT + SIDEBAR */
    .main-layout {
      display: flex;
      flex: 1;
      height: calc(100vh - 53px);
      overflow: hidden;
    }

    /* CENTER VIEWPORT */
    .viewport {
      flex: 1;
      position: relative;
      background: #0d0e14;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      cursor: grab;
      user-select: none;
    }
    .viewport:active { cursor: grabbing; }

    /* BACKGROUND CAD GRID */
    .grid-layer {
      position: absolute;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 50%, rgba(0, 229, 255, 0.04) 0%, transparent 70%),
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 100% 100%, 40px 40px, 40px 40px;
      pointer-events: none;
    }

    /* HUD OVERLAY CROSSHAIRS */
    .hud-overlay {
      position: absolute;
      inset: 20px;
      border: 1px solid rgba(0, 229, 255, 0.08);
      pointer-events: none;
      border-radius: 8px;
    }
    .hud-corner {
      position: absolute;
      width: 14px;
      height: 14px;
      border-color: var(--cyan-neon);
      border-style: solid;
      opacity: 0.5;
    }
    .hud-corner.tl { top: -1px; left: -1px; border-width: 2px 0 0 2px; }
    .hud-corner.tr { top: -1px; right: -1px; border-width: 2px 2px 0 0; }
    .hud-corner.bl { bottom: -1px; left: -1px; border-width: 0 0 2px 2px; }
    .hud-corner.br { bottom: -1px; right: -1px; border-width: 0 2px 2px 0; }

    /* SPIDER CONTAINER TRANSFORM STAGE */
    #stage-container {
      position: relative;
      transform-origin: center center;
      transition: transform 0.05s ease-out;
      will-change: transform;
    }

    #mech-spider {
      display: block;
      height: 82vh;
      width: auto;
      max-height: 850px;
      filter: drop-shadow(0 15px 35px rgba(0, 0, 0, 0.7));
    }

    /* SVG LASER SILK OVERLAY */
    #laser-silk-canvas {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 50;
    }

    /* VIEWPORT FLOATING TOOLBAR */
    .viewport-controls {
      position: absolute;
      bottom: 20px;
      left: 20px;
      display: flex;
      gap: 8px;
      z-index: 60;
    }
    .btn-vp {
      background: rgba(17, 19, 26, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
    }
    .btn-vp:hover {
      border-color: var(--cyan-neon);
      color: var(--cyan-neon);
      transform: translateY(-2px);
    }

    /* RIGHT CONTROL SIDEBAR */
    .sidebar {
      width: 440px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      z-index: 90;
    }
    .sidebar::-webkit-scrollbar { width: 6px; }
    .sidebar::-webkit-scrollbar-thumb { background: #232836; border-radius: 3px; }

    .panel-section {
      padding: 18px 20px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .section-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .section-title span.badge {
      font-family: var(--font-mono);
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--bg-card);
      color: var(--cyan-neon);
      border: 1px solid rgba(0, 229, 255, 0.2);
    }

    /* PRESET BUTTONS GRID */
    .preset-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .btn-preset {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 12px 14px;
      border-radius: 8px;
      text-align: left;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
      overflow: hidden;
    }
    .btn-preset:hover {
      border-color: rgba(0, 229, 255, 0.4);
      background: #1c202c;
    }
    .btn-preset.active {
      border-color: var(--cyan-neon);
      background: var(--cyan-dim);
      box-shadow: 0 0 14px rgba(0, 229, 255, 0.2);
    }
    .btn-preset .preset-icon { font-size: 18px; margin-bottom: 4px; }
    .btn-preset .preset-name { font-size: 13px; font-weight: 700; color: #fff; }
    .btn-preset .preset-sub { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

    /* SPEED & MASTER CONTROLS */
    .control-row {
      margin-top: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .control-label {
      font-size: 12px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      min-width: 90px;
    }
    .slider-container {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    input[type=range] {
      flex: 1;
      height: 5px;
      border-radius: 3px;
      background: #232836;
      outline: none;
      -webkit-appearance: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: var(--cyan-neon);
      cursor: pointer;
      box-shadow: 0 0 8px var(--cyan-neon);
    }
    .val-display {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--cyan-neon);
      min-width: 40px;
      text-align: right;
    }

    /* ACTION BUTTONS (FIRE SILK / TOGGLES) */
    .action-btn-row {
      display: flex;
      gap: 10px;
      margin-top: 14px;
    }
    .btn-action {
      flex: 1;
      padding: 10px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border-subtle);
      background: var(--bg-card);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .btn-action:hover { border-color: var(--cyan-neon); color: var(--cyan-neon); }
    .btn-action.primary {
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.2), rgba(0, 229, 255, 0.05));
      border-color: var(--cyan-neon);
      color: #fff;
    }
    .btn-action.primary:hover {
      box-shadow: 0 0 16px rgba(0, 229, 255, 0.35);
      transform: translateY(-1px);
    }

    /* COLOR THEME SELECTOR */
    .theme-chips {
      display: flex;
      gap: 8px;
    }
    .chip {
      flex: 1;
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-family: var(--font-mono);
      text-align: center;
      cursor: pointer;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      transition: all 0.2s;
    }
    .chip.active {
      border-color: var(--cyan-neon);
      color: #fff;
      background: rgba(0, 229, 255, 0.1);
    }

    /* ACCORDION JOINT LIST */
    .joint-group-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      margin-bottom: 8px;
      overflow: hidden;
    }
    .joint-group-header {
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.02);
      transition: background 0.2s;
    }
    .joint-group-header:hover { background: rgba(0, 229, 255, 0.04); }
    .joint-group-title {
      font-size: 12px;
      font-weight: 700;
      color: #E2E8F0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .joint-group-content {
      padding: 10px 14px 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      display: none;
    }
    .joint-group-card.open .joint-group-content { display: block; }
    .joint-group-card.open .joint-group-header { border-bottom: 1px solid rgba(255, 255, 255, 0.05); }

    .single-joint-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }
    .single-joint-name {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      width: 50px;
    }

    /* TELEMETRY MATRIX BAR (BOTTOM) */
    .telemetry-matrix {
      background: rgba(10, 11, 16, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px;
      font-family: var(--font-mono);
      font-size: 11px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .telem-item {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
    }
    .telem-val { color: var(--cyan-neon); font-weight: 700; }
  </style>
</head>
<body>

  <!-- TOP HEADER -->
  <header>
    <div class="brand">
      <div class="brand-icon">⚙️</div>
      <div>
        <div class="brand-title">SPIDER RADAR — MECHA VECTOR RIG LABORATORY</div>
        <div class="brand-subtitle">Pure Vector Nested Mount Points • 29 Mechanical Joints • 60 FPS GSAP</div>
      </div>
    </div>
    <div class="header-pills">
      <div class="pill active" id="pill-engine"><div class="pulse-dot"></div> KINEMATICS ENGINE: ACTIVE</div>
      <div class="pill" id="pill-fps">FPS: <span id="fps-val" style="color:var(--cyan-neon)">60.0</span></div>
      <div class="pill">JOINTS: 29/29 RIGGED</div>
      <a href="./spider_showcase.html" style="text-decoration:none" class="pill" target="_blank">↗ Xem Showcase 6 Skin</a>
    </div>
  </header>

  <!-- MAIN DUAL-PANE LAYOUT -->
  <div class="main-layout">

    <!-- CENTER INTERACTIVE VIEWPORT -->
    <div class="viewport" id="viewport">
      <div class="grid-layer"></div>
      
      <!-- HUD CORNER RULERS -->
      <div class="hud-overlay">
        <div class="hud-corner tl"></div>
        <div class="hud-corner tr"></div>
        <div class="hud-corner bl"></div>
        <div class="hud-corner br"></div>
        <div style="position:absolute; top:8px; left:12px; font-family:var(--font-mono); font-size:10px; color:rgba(0,229,255,0.4);">
          CAD COORD: 736 x 1308 • TOP-DOWN VIEW (0° FORWARD)
        </div>
      </div>

      <!-- SPIDER STAGE -->
      <div id="stage-container">
        """ + svg_enhanced + """

      </div>

      <!-- VIEWPORT TOOLBAR (ZOOM / PAN / RESET) -->
      <div class="viewport-controls">
        <button class="btn-vp" onclick="zoomIn()" title="Phóng to (Zoom In)">＋</button>
        <button class="btn-vp" onclick="zoomOut()" title="Thu nhỏ (Zoom Out)">－</button>
        <button class="btn-vp" onclick="resetZoom()" title="Về chuẩn 100% (Reset Zoom)">⟲</button>
        <button class="btn-vp" onclick="toggleHeading()" id="btn-heading" title="Đảo chiều đầu (0° / 180°)">⬆</button>
        <button class="btn-vp" onclick="toggleBlueprint()" id="btn-bp" title="Ẩn/Hiện CAD Blueprint Layer">📐</button>
      </div>
    </div>

    <!-- RIGHT CONTROL SIDEBAR -->
    <div class="sidebar">

      <!-- SECTION 1: ANIMATION PRESETS -->
      <div class="panel-section">
        <div class="section-title">
          1. Chế Độ Chuyển Động (Kinematic Presets)
          <span class="badge">60 FPS</span>
        </div>
        <div class="preset-grid">
          <button class="btn-preset active" id="btn-preset-idle" onclick="setPreset('idle')">
            <div class="preset-icon">🌿</div>
            <div class="preset-name">Idle Breathing</div>
            <div class="preset-sub">Nhịp thở pít-tông & sóng ăng-ten</div>
          </button>
          <button class="btn-preset" id="btn-preset-walk" onclick="setPreset('walk')">
            <div class="preset-icon">🏃</div>
            <div class="preset-name">Tetrapod Walk</div>
            <div class="preset-sub">4 thì liên hoàn không gãy khớp</div>
          </button>
          <button class="btn-preset" id="btn-preset-strike" onclick="setPreset('strike')">
            <div class="preset-icon">⚡</div>
            <div class="preset-name">Combat Strike</div>
            <div class="preset-sub">Giương càng săn mồi đe dọa</div>
          </button>
          <button class="btn-preset" id="btn-preset-shock" onclick="setPreset('shock')">
            <div class="preset-icon">🛡️</div>
            <div class="preset-name">Hydraulic Shock</div>
            <div class="preset-sub">Nhún giảm xóc tiếp đất đàn hồi</div>
          </button>
        </div>

        <!-- SPEED SLIDER -->
        <div class="control-row">
          <span class="control-label">TỐC ĐỘ (SPEED)</span>
          <div class="slider-container">
            <input type="range" id="speed-slider" min="0.2" max="2.5" step="0.1" value="1.0" oninput="updateSpeed(this.value)">
            <span class="val-display" id="speed-val">1.0x</span>
          </div>
        </div>

        <!-- FIRE LASER SILK ACTION -->
        <div class="action-btn-row">
          <button class="btn-action primary" onclick="fireLaserSilk()">
            <span>⚡ BẮN TƠ LASER CYAN</span>
          </button>
          <button class="btn-action" onclick="resetAllJoints()">
            <span>⟲ Reset Góc Nghỉ</span>
          </button>
        </div>
      </div>

      <!-- SECTION 2: SENSOR COLOR & BLUEPRINT TOGGLE -->
      <div class="panel-section">
        <div class="section-title">
          2. Hiệu Ứng Cảm Biến & Lớp Bản Vẽ (CAD FX)
        </div>
        
        <div style="margin-bottom:12px;">
          <div style="font-size:11px; color:var(--text-muted); margin-bottom:6px; font-family:var(--font-mono)">MÀU ĐÈN CẢM BIẾN (OPTICAL VISOR):</div>
          <div class="theme-chips">
            <div class="chip active" onclick="setOpticsColor('#00E5FF', this)">CYAN HUD</div>
            <div class="chip" onclick="setOpticsColor('#FF1744', this)">ALERT RED</div>
            <div class="chip" onclick="setOpticsColor('#FFD600', this)">SOLAR GOLD</div>
            <div class="chip" onclick="setOpticsColor('#10B981', this)">EMERALD</div>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px;">
          <div>
            <div style="font-size:12px; font-weight:700;">Hiện Đường Gióng CAD Blueprint</div>
            <div style="font-size:11px; color:var(--text-muted);">Đường kích thước, vòng tròn tiêu cự CAD</div>
          </div>
          <input type="checkbox" id="check-blueprint" checked onchange="toggleBlueprint(this.checked)" style="width:18px; height:18px; accent-color:var(--cyan-neon); cursor:pointer;">
        </div>
      </div>

      <!-- SECTION 3: 29 INDIVIDUAL JOINT SLIDERS -->
      <div class="panel-section" style="flex:1;">
        <div class="section-title">
          3. Điều Khiển Từng Khớp Thủ Công (Manual Rig)
          <span class="badge">29 JOINTS</span>
        </div>

        <!-- ANTENNA -->
        <div class="joint-group-card open">
          <div class="joint-group-header" onclick="toggleAccordion(this)">
            <div class="joint-group-title">📡 Ăng-ten Ra-đa (ANT)</div>
            <span style="font-size:11px; color:var(--text-muted);">▼</span>
          </div>
          <div class="joint-group-content">
            <div class="single-joint-row">
              <span class="single-joint-name">ANT_s1</span>
              <input type="range" class="joint-slider" data-id="ANT_s1" min="-30" max="30" value="0" oninput="manualJointSlide('ANT_s1', this.value)">
              <span class="val-display" id="val-ANT_s1">0°</span>
            </div>
          </div>
        </div>

        <!-- LEGS L1 & R1 (FORELEGS - 3 SEGMENTS) -->
        <div class="joint-group-card">
          <div class="joint-group-header" onclick="toggleAccordion(this)">
            <div class="joint-group-title">🎯 Cặp Chân Trước Săn Mồi (L1 & R1)</div>
            <span style="font-size:11px; color:var(--text-muted);">▼</span>
          </div>
          <div class="joint-group-content">
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin-bottom:4px;">Chân Trái L1 (3 Đốt):</div>
            <div class="single-joint-row"><span class="single-joint-name">L1_s1</span><input type="range" class="joint-slider" data-id="L1_s1" min="-45" max="45" value="0" oninput="manualJointSlide('L1_s1', this.value)"><span class="val-display" id="val-L1_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L1_s2</span><input type="range" class="joint-slider" data-id="L1_s2" min="-45" max="45" value="0" oninput="manualJointSlide('L1_s2', this.value)"><span class="val-display" id="val-L1_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L1_s3</span><input type="range" class="joint-slider" data-id="L1_s3" min="-45" max="45" value="0" oninput="manualJointSlide('L1_s3', this.value)"><span class="val-display" id="val-L1_s3">0°</span></div>
            
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin:10px 0 4px;">Chân Phải R1 (3 Đốt):</div>
            <div class="single-joint-row"><span class="single-joint-name">R1_s1</span><input type="range" class="joint-slider" data-id="R1_s1" min="-45" max="45" value="0" oninput="manualJointSlide('R1_s1', this.value)"><span class="val-display" id="val-R1_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R1_s2</span><input type="range" class="joint-slider" data-id="R1_s2" min="-45" max="45" value="0" oninput="manualJointSlide('R1_s2', this.value)"><span class="val-display" id="val-R1_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R1_s3</span><input type="range" class="joint-slider" data-id="R1_s3" min="-45" max="45" value="0" oninput="manualJointSlide('R1_s3', this.value)"><span class="val-display" id="val-R1_s3">0°</span></div>
          </div>
        </div>

        <!-- LEGS L2 & R2 (MID-FRONT - 3 SEGMENTS) -->
        <div class="joint-group-card">
          <div class="joint-group-header" onclick="toggleAccordion(this)">
            <div class="joint-group-title">📐 Cặp Chân Ngang Vai (L2 & R2)</div>
            <span style="font-size:11px; color:var(--text-muted);">▼</span>
          </div>
          <div class="joint-group-content">
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin-bottom:4px;">Chân Trái L2:</div>
            <div class="single-joint-row"><span class="single-joint-name">L2_s1</span><input type="range" class="joint-slider" data-id="L2_s1" min="-45" max="45" value="0" oninput="manualJointSlide('L2_s1', this.value)"><span class="val-display" id="val-L2_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L2_s2</span><input type="range" class="joint-slider" data-id="L2_s2" min="-45" max="45" value="0" oninput="manualJointSlide('L2_s2', this.value)"><span class="val-display" id="val-L2_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L2_s3</span><input type="range" class="joint-slider" data-id="L2_s3" min="-45" max="45" value="0" oninput="manualJointSlide('L2_s3', this.value)"><span class="val-display" id="val-L2_s3">0°</span></div>
            
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin:10px 0 4px;">Chân Phải R2:</div>
            <div class="single-joint-row"><span class="single-joint-name">R2_s1</span><input type="range" class="joint-slider" data-id="R2_s1" min="-45" max="45" value="0" oninput="manualJointSlide('R2_s1', this.value)"><span class="val-display" id="val-R2_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R2_s2</span><input type="range" class="joint-slider" data-id="R2_s2" min="-45" max="45" value="0" oninput="manualJointSlide('R2_s2', this.value)"><span class="val-display" id="val-R2_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R2_s3</span><input type="range" class="joint-slider" data-id="R2_s3" min="-45" max="45" value="0" oninput="manualJointSlide('R2_s3', this.value)"><span class="val-display" id="val-R2_s3">0°</span></div>
          </div>
        </div>

        <!-- LEGS L3 & R3 (MID-REAR - 3 SEGMENTS) -->
        <div class="joint-group-card">
          <div class="joint-group-header" onclick="toggleAccordion(this)">
            <div class="joint-group-title">⚖️ Cặp Chân Trụ Sau (L3 & R3)</div>
            <span style="font-size:11px; color:var(--text-muted);">▼</span>
          </div>
          <div class="joint-group-content">
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin-bottom:4px;">Chân Trái L3:</div>
            <div class="single-joint-row"><span class="single-joint-name">L3_s1</span><input type="range" class="joint-slider" data-id="L3_s1" min="-45" max="45" value="0" oninput="manualJointSlide('L3_s1', this.value)"><span class="val-display" id="val-L3_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L3_s2</span><input type="range" class="joint-slider" data-id="L3_s2" min="-45" max="45" value="0" oninput="manualJointSlide('L3_s2', this.value)"><span class="val-display" id="val-L3_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L3_s3</span><input type="range" class="joint-slider" data-id="L3_s3" min="-45" max="45" value="0" oninput="manualJointSlide('L3_s3', this.value)"><span class="val-display" id="val-L3_s3">0°</span></div>
            
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin:10px 0 4px;">Chân Phải R3:</div>
            <div class="single-joint-row"><span class="single-joint-name">R3_s1</span><input type="range" class="joint-slider" data-id="R3_s1" min="-45" max="45" value="0" oninput="manualJointSlide('R3_s1', this.value)"><span class="val-display" id="val-R3_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R3_s2</span><input type="range" class="joint-slider" data-id="R3_s2" min="-45" max="45" value="0" oninput="manualJointSlide('R3_s2', this.value)"><span class="val-display" id="val-R3_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R3_s3</span><input type="range" class="joint-slider" data-id="R3_s3" min="-45" max="45" value="0" oninput="manualJointSlide('R3_s3', this.value)"><span class="val-display" id="val-R3_s3">0°</span></div>
          </div>
        </div>

        <!-- LEGS L4 & R4 (HINDLEGS - 5 SEGMENTS KHỔNG LỒ) -->
        <div class="joint-group-card">
          <div class="joint-group-header" onclick="toggleAccordion(this)">
            <div class="joint-group-title">💥 Cặp Pít-tông Khổng Lồ Đáy (L4 & R4 - 5 Đốt)</div>
            <span style="font-size:11px; color:var(--text-muted);">▼</span>
          </div>
          <div class="joint-group-content">
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin-bottom:4px;">Chân Trái L4 (5 Đốt Lồng Nhau):</div>
            <div class="single-joint-row"><span class="single-joint-name">L4_s1</span><input type="range" class="joint-slider" data-id="L4_s1" min="-40" max="40" value="0" oninput="manualJointSlide('L4_s1', this.value)"><span class="val-display" id="val-L4_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L4_s2</span><input type="range" class="joint-slider" data-id="L4_s2" min="-40" max="40" value="0" oninput="manualJointSlide('L4_s2', this.value)"><span class="val-display" id="val-L4_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L4_s3</span><input type="range" class="joint-slider" data-id="L4_s3" min="-40" max="40" value="0" oninput="manualJointSlide('L4_s3', this.value)"><span class="val-display" id="val-L4_s3">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L4_s4</span><input type="range" class="joint-slider" data-id="L4_s4" min="-40" max="40" value="0" oninput="manualJointSlide('L4_s4', this.value)"><span class="val-display" id="val-L4_s4">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">L4_s5</span><input type="range" class="joint-slider" data-id="L4_s5" min="-40" max="40" value="0" oninput="manualJointSlide('L4_s5', this.value)"><span class="val-display" id="val-L4_s5">0°</span></div>
            
            <div style="font-size:11px; color:var(--cyan-neon); font-family:var(--font-mono); margin:10px 0 4px;">Chân Phải R4 (5 Đốt Lồng Nhau):</div>
            <div class="single-joint-row"><span class="single-joint-name">R4_s1</span><input type="range" class="joint-slider" data-id="R4_s1" min="-40" max="40" value="0" oninput="manualJointSlide('R4_s1', this.value)"><span class="val-display" id="val-R4_s1">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R4_s2</span><input type="range" class="joint-slider" data-id="R4_s2" min="-40" max="40" value="0" oninput="manualJointSlide('R4_s2', this.value)"><span class="val-display" id="val-R4_s2">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R4_s3</span><input type="range" class="joint-slider" data-id="R4_s3" min="-40" max="40" value="0" oninput="manualJointSlide('R4_s3', this.value)"><span class="val-display" id="val-R4_s3">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R4_s4</span><input type="range" class="joint-slider" data-id="R4_s4" min="-40" max="40" value="0" oninput="manualJointSlide('R4_s4', this.value)"><span class="val-display" id="val-R4_s4">0°</span></div>
            <div class="single-joint-row"><span class="single-joint-name">R4_s5</span><input type="range" class="joint-slider" data-id="R4_s5" min="-40" max="40" value="0" oninput="manualJointSlide('R4_s5', this.value)"><span class="val-display" id="val-R4_s5">0°</span></div>
          </div>
        </div>

      </div>

      <!-- SECTION 4: REALTIME TELEMETRY MATRIX -->
      <div class="panel-section">
        <div class="section-title">
          4. Bảng Giám Sát Đo Từ Xa (Telemetry Matrix)
        </div>
        <div class="telemetry-matrix">
          <div class="telem-item"><span>RIG ARCHITECTURE:</span><span class="telem-val">NESTED 29-JOINT</span></div>
          <div class="telem-item"><span>JOINT DISCONNECTION:</span><span class="telem-val" style="color:#10B981">0.00% (SEAMLESS)</span></div>
          <div class="telem-item"><span>HYDRAULIC PRESSURE:</span><span class="telem-val" id="telem-psi">3,420 PSI</span></div>
          <div class="telem-item"><span>HEADING:</span><span class="telem-val" id="telem-heading">0° (FORWARD)</span></div>
          <div class="telem-item"><span>ACTIVE FILAMENTS:</span><span class="telem-val" id="telem-filaments">0 / 2 MAX</span></div>
          <div class="telem-item"><span>GSAP STATUS:</span><span class="telem-val" style="color:#10B981">SYNCED 60FPS</span></div>
        </div>
      </div>

    </div>

  </div>

  <!-- JAVASCRIPT KINEMATICS & CONTROL ENGINE -->
  <script>
    // 1. Core Rig Data & Functions
    const restAngle = {};
    document.querySelectorAll('.sp-joint').forEach(el => {
      restAngle[el.id] = parseFloat(el.dataset.rest) || 0;
    });

    const setJoint = (id, delta) => {
      const el = document.getElementById(id);
      if (el && restAngle[id] !== undefined) {
        el.setAttribute('transform', `rotate(${restAngle[id] + delta})`);
      }
    };

    const n_seg = { 1: 3, 2: 3, 3: 3, 4: 5 };
    const amp_idle = { 1: [3, 6, 5], 2: [4, 6, 5], 3: [3, 4, 3], 4: [2, 2, 2, 1.5, 1.5] };
    const amp_walk = { 1: [14, 20, 16], 2: [15, 22, 18], 3: [12, 16, 14], 4: [10, 10, 8, 7, 6] };

    const spiderRoot = document.getElementById('spider-root');
    const stageContainer = document.getElementById('stage-container');

    let currentPreset = 'idle';
    let animSpeed = 1.0;
    let manualMode = false;
    let headingAngle = 0;
    let zoomLevel = 1.0;
    let panX = 0, panY = 0;
    let isDragging = false, startMouseX = 0, startMouseY = 0;

    // 2. Main Animation Loop (rAF + GSAP hybrid)
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsTimer = 0;

    function tick(now) {
      // Calculate real FPS
      frameCount++;
      if (now - fpsTimer >= 500) {
        const fps = (frameCount * 1000) / (now - fpsTimer);
        document.getElementById('fps-val').innerText = fps.toFixed(1);
        frameCount = 0;
        fpsTimer = now;
      }

      if (!manualMode) {
        const t = (now / 600) * animSpeed;

        if (currentPreset === 'idle') {
          // Preset 1: Idle core breathing
          for (const n in n_seg) {
            for (let i = 0; i < n_seg[n]; i++) {
              const ph = (n % 2 ? 0 : Math.PI);
              const a = amp_idle[n][i];
              const w = Math.sin(t + i * 0.4 + ph);
              setJoint(`L${n}_s${i+1}`, a * w);
              setJoint(`R${n}_s${i+1}`, -a * Math.sin(t + i * 0.4 + ph + Math.PI));
            }
          }
          setJoint('ANT_s1', 3.5 * Math.sin(t * 0.9));
          spiderRoot.setAttribute('transform', `translate(0, ${2.5 * Math.sin(t * 1.8)})`);
          document.getElementById('telem-psi').innerText = `${(3200 + 150 * Math.sin(t)).toFixed(0)} PSI`;

        } else if (currentPreset === 'walk') {
          // Preset 2: Tetrapod walk cycle (Alpha tetrapod: L1, R2, L3, R4 / Beta: R1, L2, R3, L4)
          for (const n in n_seg) {
            for (let i = 0; i < n_seg[n]; i++) {
              // Group alpha: legs 1, 3 left vs 2, 4 right
              const isAlphaLeg = (n == 1 || n == 3);
              const phaseLeg = isAlphaLeg ? 0 : Math.PI;
              const a = amp_walk[n][i];
              const wL = Math.sin(t + phaseLeg + i * 0.35);
              const wR = Math.sin(t + (Math.PI - phaseLeg) + i * 0.35);

              setJoint(`L${n}_s${i+1}`, a * wL);
              setJoint(`R${n}_s${i+1}`, -a * wR);
            }
          }
          setJoint('ANT_s1', 8 * Math.sin(t * 1.2));
          spiderRoot.setAttribute('transform', `translate(0, ${4 * Math.sin(t * 2)})`);
          document.getElementById('telem-psi').innerText = `${(3500 + 400 * Math.sin(t * 2)).toFixed(0)} PSI`;
        }
      }

      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    // 3. Switch Presets
    function setPreset(preset) {
      currentPreset = preset;
      manualMode = false;
      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      document.getElementById(`btn-preset-${preset}`).classList.add('active');

      if (preset === 'strike') {
        manualMode = true;
        // Front legs strike upwards aggressively
        gsap.to({}, { duration: 0.6, ease: "power2.out", onUpdate: function() {
          const p = this.progress();
          setJoint('L1_s1', -25 * p); setJoint('L1_s2', -35 * p); setJoint('L1_s3', -20 * p);
          setJoint('R1_s1', 25 * p);  setJoint('R1_s2', 35 * p);  setJoint('R1_s3', 20 * p);
          setJoint('L4_s1', 15 * p);  setJoint('L4_s2', 12 * p);
          setJoint('R4_s1', -15 * p); setJoint('R4_s2', -12 * p);
          setJoint('ANT_s1', -10 * p);
        }});
        gsap.to(spiderRoot, { transform: 'translate(0, -12px)', duration: 0.6, ease: "back.out(2)" });
        document.getElementById('telem-psi').innerText = '4,850 PSI (STRIKE)';

      } else if (preset === 'shock') {
        manualMode = true;
        // Deep hydraulic shock compression & elastic rebound
        const tl = gsap.timeline();
        tl.to({}, { duration: 0.2, ease: "power3.in", onUpdate: function() {
          const p = this.progress();
          setJoint('L1_s1', 20 * p); setJoint('R1_s1', -20 * p);
          setJoint('L4_s1', -25 * p); setJoint('R4_s1', 25 * p);
          setJoint('L4_s2', -15 * p); setJoint('R4_s2', 15 * p);
        }})
        .to(spiderRoot, { transform: 'translate(0, 16px)', duration: 0.2, ease: "power3.in" }, 0)
        .to({}, { duration: 0.8, ease: "elastic.out(1.4, 0.3)", onUpdate: function() {
          const p = 1 - this.progress();
          setJoint('L1_s1', 20 * p); setJoint('R1_s1', -20 * p);
          setJoint('L4_s1', -25 * p); setJoint('R4_s1', 25 * p);
          setJoint('L4_s2', -15 * p); setJoint('R4_s2', 15 * p);
        }})
        .to(spiderRoot, { transform: 'translate(0, 0px)', duration: 0.8, ease: "elastic.out(1.4, 0.3)" }, 0.2)
        .add(() => { setPreset('idle'); });
      }
    }

    // 4. Update Speed
    function updateSpeed(val) {
      animSpeed = parseFloat(val);
      document.getElementById('speed-val').innerText = `${animSpeed.toFixed(1)}x`;
    }

    // 5. Manual Joint Slider Handling
    function manualJointSlide(id, val) {
      manualMode = true;
      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      const delta = parseFloat(val);
      setJoint(id, delta);
      const disp = document.getElementById(`val-${id}`);
      if (disp) disp.innerText = `${delta > 0 ? '+' : ''}${delta}°`;
    }

    function resetAllJoints() {
      manualMode = false;
      document.querySelectorAll('.joint-slider').forEach(sl => {
        sl.value = 0;
        const id = sl.dataset.id;
        const disp = document.getElementById(`val-${id}`);
        if (disp) disp.innerText = '0°';
        setJoint(id, 0);
      });
      spiderRoot.setAttribute('transform', 'translate(0, 0)');
      setPreset('idle');
    }

    // 6. Laser Silk Ejection Effect
    let activeFilamentsCount = 0;
    function fireLaserSilk() {
      const pathEl = document.getElementById('laser-silk-path');
      const targetDot = document.getElementById('laser-target-dot');
      const nozzle = document.getElementById('silk-nozzle');

      // Random target point on the CAD arena
      const targetX = 120 + Math.random() * 500;
      const targetY = 150 + Math.random() * 300;

      // Start nozzle coordinates (cockpit top: 368, 142)
      const startX = 368;
      const startY = 142;

      // Bezier curve with mechanical tension
      const midX = (startX + targetX) / 2 + (Math.random() - 0.5) * 80;
      const midY = (startY + targetY) / 2 - 60;
      const d = `M ${startX} ${startY} Q ${midX} ${midY} ${targetX} ${targetY}`;

      pathEl.setAttribute('d', d);
      targetDot.setAttribute('cx', targetX);
      targetDot.setAttribute('cy', targetY);

      activeFilamentsCount = Math.min(2, activeFilamentsCount + 1);
      document.getElementById('telem-filaments').innerText = `${activeFilamentsCount} / 2 MAX`;

      // Filament Animation: Shoot (0.3s) -> Flare target (0.2s) -> Dissipate (0.7s)
      const tl = gsap.timeline({
        onComplete: () => {
          activeFilamentsCount = Math.max(0, activeFilamentsCount - 1);
          document.getElementById('telem-filaments').innerText = `${activeFilamentsCount} / 2 MAX`;
        }
      });

      tl.fromTo(pathEl, { opacity: 0, strokeDasharray: 800, strokeDashoffset: 800 }, {
        opacity: 0.9, strokeDashoffset: 0, duration: 0.32, ease: "power3.out"
      })
      .fromTo(targetDot, { opacity: 0, scale: 0.3, transformOrigin: `${targetX}px ${targetY}px` }, {
        opacity: 1, scale: 1.6, duration: 0.2, ease: "back.out(2)"
      }, "-=0.1")
      .to(pathEl, { opacity: 0, duration: 0.75, ease: "power1.in" }, "+=0.15")
      .to(targetDot, { opacity: 0, scale: 0.5, duration: 0.5 }, "-=0.5");
    }

    // 7. Sensor Optics Color
    function setOpticsColor(color, chipEl) {
      document.querySelectorAll('.theme-chips .chip').forEach(c => c.classList.remove('active'));
      if (chipEl) chipEl.classList.add('active');

      const eyes = document.querySelectorAll('#mecha-cockpit-optics circle');
      eyes.forEach(e => {
        if (e.getAttribute('fill') !== '#FFFFFF') {
          gsap.to(e, { fill: color, duration: 0.3 });
        }
      });
      document.getElementById('laser-silk-path').setAttribute('stroke', color);
      document.getElementById('laser-target-dot').setAttribute('fill', color);
    }

    // 8. Toggle Blueprint Lines Layer
    function toggleBlueprint(show) {
      const bp = document.getElementById('layer-blueprint');
      const chk = document.getElementById('check-blueprint');
      if (show === undefined) show = bp.style.display === 'none';
      bp.style.display = show ? 'block' : 'none';
      if (chk) chk.checked = show;
      document.getElementById('btn-bp').style.borderColor = show ? 'var(--cyan-neon)' : 'var(--border-subtle)';
    }

    // 9. Heading Inversion (0° Forward vs 180° Inverted)
    function toggleHeading() {
      headingAngle = (headingAngle === 0) ? 180 : 0;
      gsap.to(stageContainer, { rotation: headingAngle, duration: 0.4, ease: "power2.out" });
      document.getElementById('telem-heading').innerText = `${headingAngle}° ${headingAngle === 0 ? '(FORWARD)' : '(INVERTED)'}`;
      document.getElementById('btn-heading').innerText = (headingAngle === 0) ? '⬆' : '⬇';
    }

    // 10. Zoom and Pan Controls
    function applyTransform() {
      stageContainer.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomLevel}) rotate(${headingAngle}deg)`;
    }

    function zoomIn() {
      zoomLevel = Math.min(2.5, zoomLevel + 0.15);
      applyTransform();
    }
    function zoomOut() {
      zoomLevel = Math.max(0.4, zoomLevel - 0.15);
      applyTransform();
    }
    function resetZoom() {
      zoomLevel = 1.0;
      panX = 0; panY = 0;
      applyTransform();
    }

    const vp = document.getElementById('viewport');
    vp.addEventListener('mousedown', e => {
      if (e.target.closest('.viewport-controls')) return;
      isDragging = true;
      startMouseX = e.clientX - panX;
      startMouseY = e.clientY - panY;
    });
    window.addEventListener('mousemove', e => {
      if (!isDragging) return;
      panX = e.clientX - startMouseX;
      panY = e.clientY - startMouseY;
      applyTransform();
    });
    window.addEventListener('mouseup', () => { isDragging = false; });
    vp.addEventListener('wheel', e => {
      e.preventDefault();
      const zoomDelta = e.deltaY * -0.001;
      zoomLevel = Math.min(2.5, Math.max(0.4, zoomLevel + zoomDelta));
      applyTransform();
    }, { passive: false });

    // 11. Accordion Toggle
    function toggleAccordion(header) {
      const card = header.closest('.joint-group-card');
      card.classList.toggle('open');
      const arrow = header.querySelector('span');
      if (arrow) arrow.innerText = card.classList.contains('open') ? '▲' : '▼';
    }
  </script>
</body>
</html>
"""

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Created {out_path} successfully!")
print(f"File size: {os.path.getsize(out_path):,} bytes")
