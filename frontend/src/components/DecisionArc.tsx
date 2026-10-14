import React from 'react';
import { DecisionNode } from '../types';

interface DecisionArcProps {
  nodes: DecisionNode[];
}

export const DecisionArc: React.FC<DecisionArcProps> = ({ nodes }) => {
  return (
    <div style={{
      flex: '0 0 35%',
      background: 'rgba(255, 255, 255, 0.7)',
      backdropFilter: 'blur(8px)',
      borderLeft: '1px solid #e8e6df',
      padding: '32px 24px',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px'
    }}>
      <div>
        <h3 style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: '#78716c', fontFamily: 'var(--font-mono)' }}>
          LAYA NEURAL ROUTING ARC
        </h3>
        <p style={{ fontSize: '12px', color: '#a8a29e' }}>Mỗi thực thể, một nhánh rẽ quyết định Laya</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {nodes.map(n => (
          <div
            key={n.id}
            id={n.id}
            style={{
              background: '#fff',
              border: '1px solid #e8e6df',
              borderRadius: '12px',
              padding: '14px 18px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              boxShadow: '0 2px 6px rgba(0,0,0,0.03)',
              transition: 'all 0.3s'
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: '14px', color: '#1c1917' }}>{n.label}</div>
              <div style={{ fontSize: '11px', color: '#78716c', fontFamily: 'var(--font-mono)' }}>{n.subText}</div>
            </div>
            <div style={{
              background: 'rgba(45, 74, 43, 0.08)',
              color: '#2d4a2b',
              padding: '4px 10px',
              borderRadius: '8px',
              fontSize: '11px',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)'
            }}>
              {n.silkCount} TƠ
            </div>
          </div>
        ))}
      </div>

      <div style={{
        marginTop: 'auto',
        background: '#fbfaf6',
        border: '1px solid #e8e6df',
        borderRadius: '10px',
        padding: '14px',
        fontSize: '12px',
        color: '#57534e',
        lineHeight: '1.5'
      }}>
        <strong>Tơ Tự Tiêu Biến (Transient Filament):</strong> Chu kỳ 1.2s — Tơ tự động phóng từ chân nhện, kích hoạt xung chớp sáng đích và tự mờ dần khỏi DOM.
      </div>
    </div>
  );
};
