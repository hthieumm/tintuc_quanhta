import React from 'react';
import { ScreenTab } from '../../types';

interface TopHeaderBarProps {
  activeTab: ScreenTab;
  onTabChange: (tab: ScreenTab) => void;
  avgLatencyMs: number | null;
  engineName?: string;
  isSfxEnabled: boolean;
  volumePercent?: number;
  onToggleSfx: () => void;
  onOpenSearch: () => void;
}

export const TopHeaderBar: React.FC<TopHeaderBarProps> = ({
  activeTab,
  onTabChange,
  avgLatencyMs,
  engineName = 'Decision 3 Lite',
  isSfxEnabled,
  volumePercent = 70,
  onToggleSfx,
  onOpenSearch
}) => {
  const tabs: { id: ScreenTab; label: string; icon: string }[] = [
    { id: 'arena', label: 'ARENA', icon: '🕸️' },
    { id: 'feeds', label: 'BÀI BÁO', icon: '📑' },
    { id: 'digest', label: 'DIGEST', icon: '📰' },
    { id: 'analytics', label: 'CHỈ SỐ', icon: '📊' },
    { id: 'github', label: 'GITHUB', icon: '🐙' },
    { id: 'vault', label: 'VAULT', icon: '🌳' },
    { id: 'settings', label: 'CÀI ĐẶT', icon: '⚙️' }
  ];

  return (
    <header
      style={{
        height: '46px',
        backgroundColor: '#EBE6DC',
        border: '1px solid #DCD5C5',
        borderRadius: '12px',
        margin: '6px 12px 6px 12px',
        padding: '0 12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexShrink: 0,
        zIndex: 60,
        gap: '8px',
        whiteSpace: 'nowrap'
      }}
    >
      {/* Top Left: Window Dots & App Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '5px', backgroundColor: '#E06C75' }} title="Close" />
          <div style={{ width: '10px', height: '10px', borderRadius: '5px', backgroundColor: '#E5C07B' }} title="Minimize" />
          <div style={{ width: '10px', height: '10px', borderRadius: '5px', backgroundColor: '#98C379' }} title="Maximize" />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '13.5px',
              fontWeight: 700,
              color: '#2D4A2B',
              letterSpacing: '0.4px'
            }}
          >
            SPIDER RADAR
          </span>
          <span style={{ color: '#8A9A86', fontSize: '10.5px' }}>//</span>
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '10px',
              color: '#5A6B5C',
              fontWeight: 600
            }}
          >
            MACRO & LLM LAB
          </span>
        </div>
      </div>

      {/* Center: 7 Global Navigation Tabs */}
      <nav
        style={{
          display: 'flex',
          backgroundColor: '#DFD9CC',
          padding: '2.5px',
          borderRadius: '8px',
          gap: '2px',
          flexShrink: 0
        }}
      >
        {tabs.map(tab => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              style={{
                border: 'none',
                background: isActive ? '#2D4A2B' : 'transparent',
                color: isActive ? '#F4F1EA' : '#5A6B5C',
                padding: '4px 8px',
                borderRadius: '6px',
                fontSize: '11px',
                fontWeight: isActive ? 700 : 500,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                transition: 'all 0.15s ease',
                fontFamily: 'var(--font-sans)',
                whiteSpace: 'nowrap'
              }}
              onMouseEnter={e => {
                if (!isActive) e.currentTarget.style.backgroundColor = '#E2DCD0';
              }}
              onMouseLeave={e => {
                if (!isActive) e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              <span style={{ fontSize: '9px', opacity: isActive ? 1 : 0.6 }}>{isActive ? '●' : '○'}</span>
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Top Right: Badges & Telemetry */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
        {/* Instant Search trigger */}
        <button
          onClick={onOpenSearch}
          style={{
            background: '#FAF8F5',
            border: '1px solid #DCD5C5',
            borderRadius: '999px',
            padding: '3px 8px',
            fontSize: '10.5px',
            color: '#2D4A2B',
            fontFamily: 'var(--font-mono)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontWeight: 600,
            whiteSpace: 'nowrap'
          }}
          title="Tra cứu toàn văn FTS5 (Cmd+K / Ctrl+K)"
        >
          <span>🔍</span>
          <span>Cmd+K</span>
        </button>

        {/* Engine status badge */}
        <div
          style={{
            backgroundColor: '#E8F5E9',
            border: '1px solid #C8E6C9',
            borderRadius: '999px',
            padding: '3px 8px',
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            whiteSpace: 'nowrap'
          }}
        >
          <div style={{ width: '7px', height: '7px', borderRadius: '50%', backgroundColor: '#00BA88', flexShrink: 0 }} />
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '10px',
              color: '#1B5E20',
              fontWeight: 700
            }}
          >
            {engineName === 'Decision 3 Lite' ? 'D3 LITE' : engineName.toUpperCase()}: {avgLatencyMs !== null ? `${avgLatencyMs.toFixed(1)}ms` : '8.5ms'}
          </span>
        </div>

        {/* SFX Pill */}
        <button
          onClick={onToggleSfx}
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #DCD5C5',
            borderRadius: '999px',
            padding: '3px 8px',
            fontSize: '10.5px',
            color: isSfxEnabled && volumePercent > 0 ? '#2D4A2B' : '#8A9A86',
            fontFamily: 'var(--font-mono)',
            fontWeight: 600,
            cursor: 'pointer',
            whiteSpace: 'nowrap'
          }}
          title={isSfxEnabled && volumePercent > 0 ? `Âm lượng SFX: ${volumePercent}% (Nhấp để bật/tắt)` : 'Âm thanh đang tắt (Nhấp để bật)'}
        >
          {isSfxEnabled && volumePercent > 0 ? (volumePercent > 50 ? `🔊 ${volumePercent}%` : `🔉 ${volumePercent}%`) : '🔇 TẮT'}
        </button>

        {/* Status Pill */}
        <div
          style={{
            backgroundColor: '#EBE6DC',
            border: '1px solid #DCD5C5',
            borderRadius: '999px',
            padding: '3px 7px',
            fontSize: '10px',
            color: '#5A6B5C',
            fontFamily: 'var(--font-mono)',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '3px',
            whiteSpace: 'nowrap'
          }}
        >
          <span style={{ fontSize: '7px' }}>🟢</span>
          <span>LIVE</span>
        </div>
      </div>
    </header>
  );
};
