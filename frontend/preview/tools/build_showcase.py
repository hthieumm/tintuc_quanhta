import os
import re

# Read SVG
with open('frontend/preview/skin_mecha/mech_spider.svg', 'r', encoding='utf-8') as f:
    svg_raw = f.read()

# Clean XML declaration & metadata
svg_clean = re.sub(r'<\?xml[^>]*\?>', '', svg_raw).strip()
svg_clean = re.sub(r'<metadata>.*?</metadata>', '', svg_clean, flags=re.DOTALL).strip()

# Ensure SVG has responsive style and appropriate attributes
# Change width/height to 100% inside container while keeping viewBox 0 0 736 1308
svg_clean = re.sub(r'width="736"', 'width="100%"', svg_clean, count=1)
svg_clean = re.sub(r'height="1308"', 'height="100%"', svg_clean, count=1)

html_template = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mecha Spider Skin Showcase — Spider News Radar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0A0D12;
      --bg-surface: #121822;
      --bg-card: #182230;
      --border: #223246;
      --border-accent: #00E5FF;
      --text-main: #E2E8F0;
      --text-muted: #8295AD;
      --accent-cyan: #00E5FF;
      --accent-emerald: #00E676;
      --accent-coral: #FF5252;
      --accent-amber: #FFB300;
      --spider-stroke: #EAEFF5;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      user-select: none;
    }}

    /* TOP HEADER */
    .app-header {{
      height: 56px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 100;
    }}

    .header-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .status-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--accent-cyan);
      box-shadow: 0 0 10px var(--accent-cyan);
      animation: pulseDot 2s infinite ease-in-out;
    }}

    @keyframes pulseDot {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(0.7); opacity: 0.5; }}
    }}

    .brand-title {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.95rem;
      letter-spacing: 0.8px;
      color: #FFFFFF;
    }}

    .brand-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 6px;
      background: rgba(0, 229, 255, 0.12);
      border: 1px solid rgba(0, 229, 255, 0.35);
      color: var(--accent-cyan);
    }}

    .header-telemetry {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
    }}

    .telem-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-muted);
    }}
    .telem-val {{
      color: var(--text-main);
      font-weight: 600;
    }}

    /* WORKSPACE LAYOUT */
    .workspace {{
      flex: 1;
      display: grid;
      grid-template-columns: 320px 1fr 340px;
      height: calc(100vh - 56px);
      overflow: hidden;
    }}

    /* SIDEBARS */
    .sidebar {{
      background: var(--bg-surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 16px;
      gap: 20px;
      z-index: 20;
    }}

    .sidebar.right {{
      border-right: none;
      border-left: 1px solid var(--border);
    }}

    .panel-block {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .panel-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--accent-cyan);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 8px;
    }}

    /* BUTTONS & CONTROLS */
    .btn-group {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .btn {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 500;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-surface);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .btn:hover {{
      border-color: var(--accent-cyan);
      background: rgba(0, 229, 255, 0.08);
      color: #FFFFFF;
      transform: translateY(-1px);
    }}

    .btn.active {{
      background: rgba(0, 229, 255, 0.2);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      box-shadow: 0 0 12px rgba(0, 229, 255, 0.25);
    }}

    .btn-full {{
      grid-column: span 2;
    }}

    .btn-primary {{
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.25) 0%, rgba(0, 150, 255, 0.35) 100%);
      border-color: var(--accent-cyan);
      color: #FFFFFF;
      font-weight: 600;
    }}
    .btn-primary:hover {{
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.4) 0%, rgba(0, 150, 255, 0.5) 100%);
      box-shadow: 0 0 16px rgba(0, 229, 255, 0.4);
    }}

    .toggle-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
      color: var(--text-main);
    }}

    .switch {{
      position: relative;
      display: inline-block;
      width: 36px;
      height: 20px;
    }}
    .switch input {{
      opacity: 0;
      width: 0;
      height: 0;
    }}
    .slider {{
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: var(--border);
      transition: .3s;
      border-radius: 20px;
    }}
    .slider:before {{
      position: absolute;
      content: "";
      height: 14px;
      width: 14px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }}
    input:checked + .slider {{
      background-color: var(--accent-cyan);
    }}
    input:checked + .slider:before {{
      transform: translateX(16px);
      background-color: #0A0D12;
    }}

    /* SLIDER CONTROL */
    .slider-box {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .slider-label {{
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}
    input[type=range] {{
      -webkit-appearance: none;
      width: 100%;
      background: var(--border);
      height: 5px;
      border-radius: 4px;
      outline: none;
    }}
    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: var(--accent-cyan);
      cursor: pointer;
      box-shadow: 0 0 8px var(--accent-cyan);
    }}

    /* VIEWPORT CANVAS STAGE */
    .canvas-viewport {{
      position: relative;
      background: #11141A;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: grab;
    }}

    .canvas-viewport:active {{
      cursor: grabbing;
    }}

    /* Grid background */
    .canvas-viewport::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-size: 32px 32px;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      pointer-events: none;
    }}

    /* Radar sweep circle */
    .radar-circle {{
      position: absolute;
      width: 500px;
      height: 500px;
      border: 1px dashed rgba(0, 229, 255, 0.15);
      border-radius: 50%;
      pointer-events: none;
    }}
    .radar-circle.outer {{
      width: 750px;
      height: 750px;
      border: 1px solid rgba(0, 229, 255, 0.08);
    }}

    /* SVG WRAPPER ZOOM & PAN */
    .spider-container {{
      position: relative;
      transform-origin: center center;
      transition: transform 0.05s ease-out;
      width: 680px;
      height: 880px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .spider-container svg {{
      width: 100%;
      height: 100%;
      display: block;
      filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.7));
    }}

    /* THEMES */
    /* 1. Cyan Glow */
    body.theme-cyan .sp-art path,
    body.theme-cyan #layer-body path {{
      fill: #FFFFFF !important;
      filter: drop-shadow(0 0 3px rgba(0, 229, 255, 0.6));
    }}
    body.theme-cyan #layer-blueprint path {{
      fill: #00E5FF !important;
      opacity: 0.65;
    }}

    /* 2. Emerald Matrix */
    body.theme-emerald {{
      --accent-cyan: #00E676;
    }}
    body.theme-emerald .sp-art path,
    body.theme-emerald #layer-body path {{
      fill: #E8F5E9 !important;
      filter: drop-shadow(0 0 3px rgba(0, 230, 118, 0.6));
    }}
    body.theme-emerald #layer-blueprint path {{
      fill: #00E676 !important;
      opacity: 0.65;
    }}

    /* 3. White CAD Paper */
    body.theme-paper {{
      --bg-dark: #F5F7FA;
      --bg-surface: #FFFFFF;
      --bg-card: #F8FAFC;
      --border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #64748B;
    }}
    body.theme-paper .canvas-viewport {{
      background: #FDFBF7;
    }}
    body.theme-paper .canvas-viewport::before {{
      background-image: 
        linear-gradient(to right, rgba(15, 23, 42, 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(15, 23, 42, 0.05) 1px, transparent 1px);
    }}
    body.theme-paper #layer-background {{
      fill: #FDFBF7 !important;
    }}
    body.theme-paper .sp-art path,
    body.theme-paper #layer-body path,
    body.theme-paper #layer-blueprint path {{
      fill: #0F172A !important;
    }}

    /* HUD OVERLAY FLOATING CONTROLS */
    .hud-controls {{
      position: absolute;
      bottom: 20px;
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(18, 24, 34, 0.85);
      backdrop-filter: blur(12px);
      padding: 6px 12px;
      border-radius: 30px;
      border: 1px solid var(--border);
      z-index: 50;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }}

    .hud-btn {{
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 1rem;
      cursor: pointer;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: all 0.2s;
    }}
    .hud-btn:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: var(--accent-cyan);
    }}

    /* TARGET NEWS CARD (SIMULATION) */
    .target-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      position: relative;
      transition: all 0.3s;
    }}
    .target-card.highlight {{
      border-color: var(--accent-cyan);
      box-shadow: 0 0 16px rgba(0, 229, 255, 0.25);
    }}
    .badge-meta {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: var(--accent-cyan);
      background: rgba(0, 229, 255, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 6px;
    }}
    .card-title {{
      font-size: 0.82rem;
      font-weight: 600;
      line-height: 1.35;
      margin-bottom: 4px;
    }}
    .card-source {{
      font-size: 0.72rem;
      color: var(--text-muted);
    }}

    /* LASER FILAMENT SVG CANVAS */
    #laser-overlay {{
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      z-index: 30;
    }}

    /* JOINTS MONITOR TABLE */
    .joint-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
    }}
    .joint-tag {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      padding: 4px;
      border-radius: 4px;
      text-align: center;
    }}
    .joint-tag.active {{
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }}
  </style>
</head>
<body class="theme-default">

  <!-- TOP APP HEADER -->
  <header class="app-header">
    <div class="header-brand">
      <div class="status-dot"></div>
      <div class="brand-title">SPIDER RADAR // MECHA SKIN MK-VI</div>
      <span class="brand-tag">PURE VECTOR RIG</span>
    </div>
    <div class="header-telemetry">
      <div class="telem-item">ENGINE: <span class="telem-val" style="color:var(--accent-cyan)">LAYA 8ms</span></div>
      <div class="telem-item">RIGGED JOINTS: <span class="telem-val">28 AXES</span></div>
      <div class="telem-item">VECTOR FORMAT: <span class="telem-val">SVG 2D (511 KB)</span></div>
      <div class="telem-item">ZOOM: <span class="telem-val" id="zoom-readout">100%</span></div>
    </div>
  </header>

  <!-- MAIN WORKSPACE -->
  <main class="workspace">

    <!-- LEFT SIDEBAR: CONTROLS & SKINS -->
    <aside class="sidebar">
      
      <!-- MOTION MODES -->
      <div class="panel-block">
        <div class="panel-header">Chuyển Động & Rig</div>
        <div class="btn-group">
          <button class="btn active" id="btn-walk" onclick="setMode('walk')">▶️ Bò Tetrapod</button>
          <button class="btn" id="btn-idle" onclick="setMode('idle')">🧘 Nhún Thở</button>
          <button class="btn" id="btn-attack" onclick="setMode('attack')">🎯 Ngắm Săn Mồi</button>
          <button class="btn" id="btn-stop" onclick="setMode('stop')">⏸️ Đứng Yên</button>
          <button class="btn btn-full btn-primary" onclick="shootLaserDemo()">🕸️ Bắn Tơ Laser Vào Thẻ Tin</button>
        </div>
        <div class="slider-box" style="margin-top:4px;">
          <div class="slider-label">
            <span>TỐC ĐỘ DI CHUYỂN:</span>
            <span id="speed-val">1.0x</span>
          </div>
          <input type="range" id="speed-slider" min="0.2" max="3" step="0.1" value="1" oninput="updateSpeed(this.value)">
        </div>
      </div>

      <!-- SKIN THEMES -->
      <div class="panel-block">
        <div class="panel-header">Giao Diện Skin (Themes)</div>
        <div class="btn-group">
          <button class="btn active" onclick="setTheme('default')">🌑 Obsidian CAD</button>
          <button class="btn" onclick="setTheme('cyan')">⚡ Cyan Neon</button>
          <button class="btn" onclick="setTheme('emerald')">🟢 Emerald Radar</button>
          <button class="btn" onclick="setTheme('paper')">📄 Giấy Kỹ Thuật</button>
        </div>
      </div>

      <!-- LAYER TOGGLES -->
      <div class="panel-block">
        <div class="panel-header">Quản Lý Các Lớp (Layers)</div>
        <div class="toggle-row">
          <span>Lưới Blueprint & Thước CAD</span>
          <label class="switch">
            <input type="checkbox" id="chk-blueprint" checked onchange="toggleBlueprint(this.checked)">
            <span class="slider"></span>
          </label>
        </div>
        <div class="toggle-row">
          <span>Thân Khung Thủy Lực</span>
          <label class="switch">
            <input type="checkbox" id="chk-body" checked onchange="toggleBody(this.checked)">
            <span class="slider"></span>
          </label>
        </div>
        <div class="toggle-row">
          <span>Vòng Tròn Tọa Độ Radar</span>
          <label class="switch">
            <input type="checkbox" id="chk-radar" checked onchange="toggleRadar(this.checked)">
            <span class="slider"></span>
          </label>
        </div>
      </div>

      <!-- SPECS INFO -->
      <div class="panel-block">
        <div class="panel-header">Đặc Tả Kỹ Thuật</div>
        <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.6;">
          • <b>Chân L1/R1:</b> 3 đoạn vươn dài (550px).<br>
          • <b>Chân L2/R2, L3/R3:</b> 3 đoạn giáp titan gián cách.<br>
          • <b>Chân L4/R4:</b> 5 đoạn siêu dài uốn cong phía sau.<br>
          • <b>Ăng-ten ANT:</b> 1 đoạn dò sóng.<br>
          • <b>Công nghệ:</b> 100% SVG 2D không tiêu hao VRAM 3D.
        </div>
      </div>

    </aside>

    <!-- CENTER CANVAS VIEWPORT -->
    <section class="canvas-viewport" id="viewport" onwheel="handleZoom(event)" onmousedown="startDrag(event)">
      
      <div class="radar-circle" id="radar-c1"></div>
      <div class="radar-circle outer" id="radar-c2"></div>

      <!-- SVG Laser Overlay -->
      <svg id="laser-overlay"></svg>

      <!-- Spider SVG Container -->
      <div class="spider-container" id="spider-wrapper">
        {svg_clean}
      </div>

      <!-- FLOATING HUD CONTROLS -->
      <div class="hud-controls">
        <button class="hud-btn" title="Phóng to" onclick="zoomDelta(0.15)">＋</button>
        <button class="hud-btn" title="Thu nhỏ" onclick="zoomDelta(-0.15)">－</button>
        <button class="hud-btn" title="Căn giữa 100%" onclick="resetView()">⟲</button>
        <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:var(--text-muted); padding:0 8px;">Kéo chuột để di chuyển canvas</span>
      </div>

    </section>

    <!-- RIGHT SIDEBAR: LIVE TELEMETRY & TARGET FEEDS -->
    <aside class="sidebar right">

      <div class="panel-block">
        <div class="panel-header">Mục Tiêu Radar Nhận Tơ</div>
        
        <div class="target-card" id="card-1">
          <span class="badge-meta">#KINH_TE_VI_MO</span>
          <div class="card-title">FED Giữ Nguyên Lãi Suất: Dòng Vốn Toàn Cầu Chuyển Dịch Mạnh</div>
          <div class="card-source">CaféF • 2 phút trước • Độ tin cậy: 98%</div>
        </div>

        <div class="target-card" id="card-2" style="margin-top:8px;">
          <span class="badge-meta" style="color:var(--accent-amber); background:rgba(255,179,0,0.1)">#THI_TRUONG_VANG</span>
          <div class="card-title">Giá Vàng Lập Đỉnh Mới Trong Phiên Khai Mạc Sáng Nay</div>
          <div class="card-source">VnExpress • 5 phút trước • Tác động: Cao</div>
        </div>

        <div class="target-card" id="card-3" style="margin-top:8px;">
          <span class="badge-meta" style="color:var(--accent-emerald); background:rgba(0,230,118,0.1)">#GITHUB_TECH</span>
          <div class="card-title">NandhaKishorM/laya: Single-pass Tensor Engine 8ms Latency</div>
          <div class="card-source">GitHub Trending • Laya Verified</div>
        </div>
      </div>

      <!-- LIVE JOINTS MATRIX -->
      <div class="panel-block">
        <div class="panel-header">Góc Khớp Thời Gian Thực (Deg)</div>
        <div class="joint-grid">
          <div class="joint-tag" id="tag-L1">L1: 0°</div>
          <div class="joint-tag" id="tag-L2">L2: 0°</div>
          <div class="joint-tag" id="tag-L3">L3: 0°</div>
          <div class="joint-tag" id="tag-L4">L4: 0°</div>
          <div class="joint-tag" id="tag-R1">R1: 0°</div>
          <div class="joint-tag" id="tag-R2">R2: 0°</div>
          <div class="joint-tag" id="tag-R3">R3: 0°</div>
          <div class="joint-tag" id="tag-R4">R4: 0°</div>
        </div>
      </div>

      <!-- CONTROLLER SHORTCUTS -->
      <div class="panel-block">
        <div class="panel-header">Hướng Dẫn Thử Nghiệm</div>
        <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.5;">
          • <b>Cuộn chuột (Wheel):</b> Zoom phóng to cực đại không vỡ nét.<br>
          • <b>Click & Drag:</b> Kéo di chuyển toàn bộ sân đấu.<br>
          • <b>Nút Bắn Tơ:</b> Thử nghiệm bắn tia laser vector nối từ càng nhện sang card tin tức!
        </div>
      </div>

    </aside>

  </main>

  <script>
    /* ============================================================== */
    /* 1. KINEMATIC RIG ENGINE                                        */
    /* ============================================================== */
    const rest = id => {{
      const el = document.getElementById(id);
      return el && el.dataset.rest ? parseFloat(el.dataset.rest) : 0;
    }};

    const setJoint = (id, d) => {{
      const el = document.getElementById(id);
      if (el) {{
        el.setAttribute('transform', `rotate(${{rest(id) + d}})`);
      }}
    }};

    const n_seg = {{ 1: 3, 2: 3, 3: 3, 4: 5 }};
    const amp_walk = {{
      1: [6, 12, 10],
      2: [7, 10, 8],
      3: [5, 8, 6],
      4: [4, 4, 3, 2, 2]
    }};
    const amp_idle = {{
      1: [2, 3, 2],
      2: [2, 3, 2],
      3: [1.5, 2, 1.5],
      4: [1, 1, 1, 0.5, 0.5]
    }};

    const root = document.getElementById('spider-root');
    let currentMode = 'walk';
    let speedMult = 1.0;
    let animFrame = null;
    let t_accum = 0;
    let lastTime = performance.now();

    function tick(now) {{
      const dt = (now - lastTime) / 1000;
      lastTime = now;
      t_accum += dt * speedMult;
      const t = t_accum * 1.4;

      if (currentMode === 'walk') {{
        for (const n in n_seg) {{
          for (let i = 0; i < n_seg[n]; i++) {{
            const ph = (n % 2 ? 0 : Math.PI);
            const a = amp_walk[n][i];
            const w = Math.sin(t + i * 0.5 + ph);
            setJoint(`L${{n}}_s${{i + 1}}`, a * w);
            setJoint(`R${{n}}_s${{i + 1}}`, -a * Math.sin(t + i * 0.5 + ph + Math.PI));
          }}
        }}
        setJoint('ANT_s1', 3 * Math.sin(t * 0.8));
        if (root) root.setAttribute('transform', `translate(0, ${{4 * Math.sin(t * 2)}})`);

        // Update Readouts
        updateJointTags(
          (amp_walk[1][0] * Math.sin(t)).toFixed(1),
          (amp_walk[2][0] * Math.sin(t + Math.PI)).toFixed(1),
          (amp_walk[3][0] * Math.sin(t)).toFixed(1),
          (amp_walk[4][0] * Math.sin(t + Math.PI)).toFixed(1)
        );

      }} else if (currentMode === 'idle') {{
        for (const n in n_seg) {{
          for (let i = 0; i < n_seg[n]; i++) {{
            const a = amp_idle[n][i];
            const w = Math.sin(t * 0.6 + i * 0.3);
            setJoint(`L${{n}}_s${{i + 1}}`, a * w);
            setJoint(`R${{n}}_s${{i + 1}}`, -a * w);
          }}
        }}
        setJoint('ANT_s1', 1.5 * Math.sin(t * 0.5));
        if (root) root.setAttribute('transform', `translate(0, ${{2 * Math.sin(t * 0.8)}})`);

      }} else if (currentMode === 'attack') {{
        // Raising front legs L1 & R1, spreading back legs
        setJoint('L1_s1', -18 + 4 * Math.sin(t * 4));
        setJoint('L1_s2', -25 + 6 * Math.sin(t * 4));
        setJoint('R1_s1', 18 - 4 * Math.sin(t * 4));
        setJoint('R1_s2', 25 - 6 * Math.sin(t * 4));
        setJoint('L4_s1', 6 * Math.sin(t));
        setJoint('R4_s1', -6 * Math.sin(t));
        if (root) root.setAttribute('transform', `translate(0, ${{ -8 + 3 * Math.sin(t * 3)}})`);
      }}

      animFrame = requestAnimationFrame(tick);
    }}

    requestAnimationFrame(tick);

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.btn-group .btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`btn-${{mode}}`);
      if (activeBtn) activeBtn.classList.add('active');

      if (mode === 'stop') {{
        // Reset all to rest
        for (const n in n_seg) {{
          for (let i = 0; i < n_seg[n]; i++) {{
            setJoint(`L${{n}}_s${{i + 1}}`, 0);
            setJoint(`R${{n}}_s${{i + 1}}`, 0);
          }}
        }}
        setJoint('ANT_s1', 0);
        if (root) root.setAttribute('transform', 'translate(0, 0)');
      }}
    }}

    function updateSpeed(val) {{
      speedMult = parseFloat(val);
      document.getElementById('speed-val').innerText = `${{speedMult.toFixed(1)}}x`;
    }}

    function updateJointTags(l1, l2, l3, l4) {{
      document.getElementById('tag-L1').innerText = `L1: ${{l1}}°`;
      document.getElementById('tag-L2').innerText = `L2: ${{l2}}°`;
      document.getElementById('tag-L3').innerText = `L3: ${{l3}}°`;
      document.getElementById('tag-L4').innerText = `L4: ${{l4}}°`;
      document.getElementById('tag-R1').innerText = `R1: ${{-l1}}°`;
      document.getElementById('tag-R2').innerText = `R2: ${{-l2}}°`;
      document.getElementById('tag-R3').innerText = `R3: ${{-l3}}°`;
      document.getElementById('tag-R4').innerText = `R4: ${{-l4}}°`;
    }}

    /* ============================================================== */
    /* 2. THEMES & LAYERS                                             */
    /* ============================================================== */
    function setTheme(theme) {{
      document.body.className = `theme-${{theme}}`;
      document.querySelectorAll('.panel-block:nth-child(2) .btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
    }}

    function toggleBlueprint(show) {{
      const el = document.getElementById('layer-blueprint');
      if (el) el.style.display = show ? 'inline' : 'none';
    }}

    function toggleBody(show) {{
      const el = document.getElementById('layer-body');
      const rootEl = document.getElementById('spider-root');
      if (el) el.style.display = show ? 'inline' : 'none';
      if (rootEl) rootEl.style.display = show ? 'inline' : 'none';
    }}

    function toggleRadar(show) {{
      document.getElementById('radar-c1').style.display = show ? 'block' : 'none';
      document.getElementById('radar-c2').style.display = show ? 'block' : 'none';
    }}

    /* ============================================================== */
    /* 3. ZOOM & PAN                                                  */
    /* ============================================================== */
    let currentScale = 1.0;
    let panX = 0;
    let panY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const wrapper = document.getElementById('spider-wrapper');
    const zoomReadout = document.getElementById('zoom-readout');

    function applyTransform() {{
      wrapper.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{currentScale}})`;
      zoomReadout.innerText = `${{Math.round(currentScale * 100)}}%`;
    }}

    function handleZoom(e) {{
      e.preventDefault();
      const delta = e.deltaY < 0 ? 0.08 : -0.08;
      currentScale = Math.min(Math.max(0.4, currentScale + delta), 3.5);
      applyTransform();
    }}

    function zoomDelta(d) {{
      currentScale = Math.min(Math.max(0.4, currentScale + d), 3.5);
      applyTransform();
    }}

    function resetView() {{
      currentScale = 1.0;
      panX = 0;
      panY = 0;
      applyTransform();
    }}

    function startDrag(e) {{
      if (e.target.closest('.hud-controls')) return;
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
      window.addEventListener('mousemove', onDrag);
      window.addEventListener('mouseup', endDrag);
    }}

    function onDrag(e) {{
      if (!isDragging) return;
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      applyTransform();
    }}

    function endDrag() {{
      isDragging = false;
      window.removeEventListener('mousemove', onDrag);
      window.removeEventListener('mouseup', endDrag);
    }}

    /* ============================================================== */
    /* 4. LASER FILAMENT DEMO                                         */
    /* ============================================================== */
    function shootLaserDemo() {{
      setMode('attack');
      const card = document.getElementById('card-1');
      card.classList.add('highlight');

      const overlay = document.getElementById('laser-overlay');
      const vpRect = document.getElementById('viewport').getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();

      // Start: Spider head center
      const startX = vpRect.width / 2;
      const startY = vpRect.height / 2 - 120;

      // End: Right side of viewport near target card
      const endX = vpRect.width;
      const endY = cardRect.top - vpRect.top + cardRect.height / 2;

      // Draw SVG Bezier Laser Line
      const pathD = `M ${{startX}} ${{startY}} Q ${{startX + 180}} ${{startY - 50}}, ${{endX}} ${{endY}}`;
      
      overlay.innerHTML = `
        <defs>
          <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <path d="${{pathD}}" stroke="#00E5FF" stroke-width="2.5" fill="none" opacity="1" filter="url(#laser-glow)">
          <animate attributeName="stroke-dasharray" from="0, 1000" to="1000, 0" dur="0.25s" fill="freeze" />
        </path>
        <circle cx="${{startX}}" cy="${{startY}}" r="5" fill="#FFFFFF" filter="url(#laser-glow)">
          <animate attributeName="r" values="3; 8; 3" dur="0.4s" repeatCount="indefinite"/>
        </circle>
      `;

      setTimeout(() => {{
        overlay.style.transition = 'opacity 0.6s';
        overlay.style.opacity = '0';
        setTimeout(() => {{
          overlay.innerHTML = '';
          overlay.style.opacity = '1';
          card.classList.remove('highlight');
          setMode('walk');
        }}, 600);
      }}, 1200);
    }}
  </script>
</body>
</html>
'''

with open('frontend/preview/show_skin_mecha.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Success: Generated frontend/preview/show_skin_mecha.html (Size:', len(html_template), 'bytes)')
