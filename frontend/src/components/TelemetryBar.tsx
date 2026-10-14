import React from 'react';

interface TelemetryBarProps {
  latencyMs: number;
  avgLatencyMs?: number | null;
  activeFilaments: number;
  totalFilaments: number;
  pacingMode: 'sync' | 'chill';
  onPacingChange: (mode: 'sync' | 'chill') => void;
  onOpenFeeds: () => void;
  onOpenSkins: () => void;
  currentSkinName: string;
}

export const TelemetryBar: React.FC<TelemetryBarProps> = ({
  latencyMs,
  avgLatencyMs,
  activeFilaments,
  totalFilaments,
  pacingMode,
  onPacingChange,
  onOpenFeeds,
  onOpenSkins,
  currentSkinName
}) => {
  return (
    <footer style={{
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderTop: '1px solid #e8e6df',
      padding: '8px 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      fontSize: '12px',
      fontFamily: 'var(--font-mono)',
      color: '#44403c',
      zIndex: 100
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button
          onClick={onOpenFeeds}
          style={{
            background: '#f5f4ef',
            border: '1px solid #e2e0d8',
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '11px',
            cursor: 'pointer',
            fontWeight: 600
          }}
        >
          📰 Danh Sách Feeds
        </button>

        <button
          onClick={onOpenSkins}
          style={{
            background: 'rgba(124, 58, 237, 0.08)',
            border: '1px solid rgba(124, 58, 237, 0.25)',
            color: '#7c3aed',
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '11px',
            cursor: 'pointer',
            fontWeight: 600
          }}
        >
          🕷️ Skin: {currentSkinName}
        </button>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div>
          <span>ĐỘ TRỄ SYSTEM 1 TB: </span>
          <strong style={{ color: '#059669' }}>
            {avgLatencyMs != null ? `${avgLatencyMs.toFixed(1)}ms` : `${latencyMs.toFixed(1)}ms`}
          </strong>
        </div>

        <div>
          <span>TƠ ĐÃ GIĂNG: </span>
          <strong>{totalFilaments}</strong> (Hiện tại: {activeFilaments})
        </div>

        <div style={{ display: 'flex', gap: '6px' }}>
          <button
            onClick={() => onPacingChange('sync')}
            style={{
              background: pacingMode === 'sync' ? '#2d4a2b' : '#f5f4ef',
              color: pacingMode === 'sync' ? '#fff' : '#57534e',
              border: 'none',
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '11px',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            ⚡ Sync (400ms)
          </button>
          <button
            onClick={() => onPacingChange('chill')}
            style={{
              background: pacingMode === 'chill' ? '#2d4a2b' : '#f5f4ef',
              color: pacingMode === 'chill' ? '#fff' : '#57534e',
              border: 'none',
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '11px',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            ☕ Chill (1200ms)
          </button>
        </div>
      </div>
    </footer>
  );
};
