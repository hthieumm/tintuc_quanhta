import React from 'react';
import { ScreenTab, PacingMode } from '../../types';

interface BottomTelemetryBarProps {
  activeTab: ScreenTab;
  latencyMs: number;
  avgLatencyMs: number | null;
  totalFilaments: number;
  pacingMode: PacingMode;
  onPacingChange: (mode: PacingMode) => void;
  onOpenFeeds: () => void;
  onOpenSkins: () => void;
  currentSkinName: string;
  feedCount?: number;
}

export const BottomTelemetryBar: React.FC<BottomTelemetryBarProps> = ({
  activeTab,
  latencyMs,
  avgLatencyMs,
  totalFilaments,
  pacingMode,
  onPacingChange,
  onOpenFeeds,
  onOpenSkins,
  currentSkinName,
  feedCount = 25
}) => {
  const currentLatency = avgLatencyMs !== null ? avgLatencyMs.toFixed(1) : latencyMs.toFixed(1);

  // Render contextual telemetry matching spider_radar.pen for each screen
  const renderScreenTelemetry = () => {
    switch (activeTab) {
      case 'arena':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              ⚡ ĐỘ TRỄ DECISION 3 LITE: {currentLatency}ms (SINGLE-PASS)
            </span>
            <span style={{ color: '#2D4A2B' }}>
              🕸️ TƠ ĐÃ GIĂNG: {totalFilaments} / 14 THỰC THỂ
            </span>
            <span style={{ color: '#C86D51' }}>
              🧮 TOKEN MATRIX: [●●●●●●○○○○○○○○]
            </span>
            <span style={{ color: '#5A6B5C' }}>
              ⏱️ FPS: 60.0 • RAM: 24MB • TAURI v2 NATIVE
            </span>
          </>
        );
      case 'feeds':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              ⚡ ĐỘ TRỄ DECISION 3 LITE: {currentLatency}ms • SYSTEM 2 TRANSLATED
            </span>
            <span style={{ color: '#2D4A2B' }}>
              📊 ĐÃ LỌC: 42 BÀI VĨ MÔ • BỎ QUA 182 TIN RÁC
            </span>
            <span style={{ color: '#5A6B5C' }}>
              ⏱️ FPS: 60.0 • RAM: 24MB • TAURI v2 NATIVE
            </span>
          </>
        );
      case 'digest':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              ⚡ ĐỘNG CƠ TỔNG HỢP: GEMINI 2.5 FLASH • TỔNG TIN PHÂN TÍCH: 42 BÀI
            </span>
            <span style={{ color: '#5A6B5C' }}>
              BẢN TIN ĐIỀU HÀNH TỰ ĐỘNG CẬP NHẬT 06:00 VÀ 18:00 MỖI NGÀY
            </span>
            <span style={{ color: '#2D4A2B' }}>
              DATABASE RETENTION: 30 DAYS TTL • 48 BOOKMARKS VAULT
            </span>
          </>
        );
      case 'github':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              🐙 GITHUB SCRAPER: QUÉT 15 PHÚT/LẦN • CACHE TTL: 24 GIỜ
            </span>
            <span style={{ color: '#5A6B5C' }}>
              REPOSITORY DATABASE: decision-ai/decision-3-lite (Apache 2.0)
            </span>
            <span style={{ color: '#2D4A2B' }}>
              BOOKMARK STATUS: TECH VAULT ACTIVE
            </span>
          </>
        );
      case 'vault':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              🌳 GRAPH ENGINE: SQLITE CTE RECURSIVE • BỘ NHỚ ĐỆM GRAPH: 3.2MB
            </span>
            <span style={{ color: '#5A6B5C' }}>
              ALGORITHM: FORCE-DIRECTED RELAXATION (ORGANIC SPINE)
            </span>
            <span style={{ color: '#2D4A2B' }}>
              DATA RETENTION: 30 DAYS SYNC
            </span>
          </>
        );
      case 'settings':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              ⚙️ CẤU HÌNH ĐÃ LƯU TRONG SQLITE 'system_settings' • BẢO MẬT AES-GCM
            </span>
            <span style={{ color: '#5A6B5C' }}>
              BACKEND: FASTAPI PORT 8001 • TAURI V2 LOCALHOST
            </span>
            <span style={{ color: '#2D4A2B' }}>
              STATUS: ALL SYSTEMS OPERATIONAL
            </span>
          </>
        );
      case 'analytics':
        return (
          <>
            <span style={{ color: '#1B5E20' }}>
              📊 ANALYTICS ENGINE: SQLITE CTE AGGREGATES • TỔNG HỢP 30 NGÀY
            </span>
            <span style={{ color: '#5A6B5C' }}>
              BỘ ĐỆM DỮ LIỆU: IN-MEMORY CACHE (2.4MB) • TỰ ĐỘNG LÀM MỚI
            </span>
            <span style={{ color: '#2D4A2B' }}>
              STATUS: ALL 6 CHARTS SYNCHRONIZED • ZERO VRAM OVERHEAD
            </span>
          </>
        );
    }
  };

  return (
    <footer
      style={{
        height: '44px',
        backgroundColor: '#F0F5EA',
        border: '1px solid #DCD5C5',
        borderRadius: '12px',
        margin: '6px 12px 10px 12px',
        padding: '0 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexShrink: 0,
        fontFamily: 'var(--font-mono)',
        fontSize: '11px',
        fontWeight: 700,
        color: '#2D4A2B',
        zIndex: 60
      }}
    >
      {/* Telemetry info row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px', overflow: 'hidden' }}>
        {renderScreenTelemetry()}
      </div>

      {/* Quick Action controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
        {/* Pacing Toggle Pill */}
        <div
          style={{
            display: 'flex',
            backgroundColor: '#EBE6DC',
            borderRadius: '999px',
            padding: '2px',
            border: '1px solid #DCD5C5'
          }}
        >
          <button
            onClick={() => onPacingChange('sync')}
            style={{
              border: 'none',
              background: pacingMode === 'sync' ? '#2D4A2B' : 'transparent',
              color: pacingMode === 'sync' ? '#FFFFFF' : '#5A6B5C',
              padding: '2px 8px',
              borderRadius: '999px',
              fontSize: '10px',
              fontWeight: 700,
              cursor: 'pointer'
            }}
            title="Đồng bộ Decision 3 Lite (400ms)"
          >
            ⚡ SYNC (400ms)
          </button>
          <button
            onClick={() => onPacingChange('chill')}
            style={{
              border: 'none',
              background: pacingMode === 'chill' ? '#2D4A2B' : 'transparent',
              color: pacingMode === 'chill' ? '#FFFFFF' : '#5A6B5C',
              padding: '2px 8px',
              borderRadius: '999px',
              fontSize: '10px',
              fontWeight: 700,
              cursor: 'pointer'
            }}
            title="Chế độ thư giãn (1200ms)"
          >
            ☕ CHILL (1.2s)
          </button>
        </div>

        {/* Skin Selector Pill */}
        <button
          onClick={onOpenSkins}
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #DCD5C5',
            borderRadius: '999px',
            padding: '3px 9px',
            fontSize: '10.5px',
            color: '#2D4A2B',
            cursor: 'pointer',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}
          title="Đổi Skin Con Nhện"
        >
          <span>🕷️</span>
          <span>{currentSkinName.split(' ')[0]}</span>
        </button>

        {/* Feeds Drawer Trigger */}
        <button
          onClick={onOpenFeeds}
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #DCD5C5',
            borderRadius: '999px',
            padding: '3px 9px',
            fontSize: '10.5px',
            color: '#2D4A2B',
            cursor: 'pointer',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}
          title="Mở Hàng Đợi Nguồn Tin (Feeds)"
        >
          <span>📑</span>
          <span>FEEDS ({feedCount})</span>
        </button>
      </div>
    </footer>
  );
};
