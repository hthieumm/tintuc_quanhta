import React from 'react';
import { SpiderSkinId } from '../types';

interface SkinSelectorProps {
  isOpen: boolean;
  currentSkin: SpiderSkinId;
  onSelectSkin: (skinId: SpiderSkinId) => void;
  onClose: () => void;
}

export const SkinSelector: React.FC<SkinSelectorProps> = ({
  isOpen,
  currentSkin,
  onSelectSkin,
  onClose
}) => {
  if (!isOpen) return null;

  const skins: { id: SpiderSkinId; title: string; subtitle: string; desc: string; badge: string }[] = [
    {
      id: 'tribal',
      title: 'Gothic Tribal Neon',
      subtitle: 'SKELETAL RIG 24 KHỚP (MẶC ĐỊNH)',
      desc: 'Skeletal Rigging 24 khớp vector lồng nhau; nhện đen gothic bóng bẩy; bụng gradient tím neon; vết cào gai nhọn phát quang; dáng bò rình rập và săn mồi uy lực.',
      badge: '#GothicNeon'
    },
    {
      id: 'mecha',
      title: 'Mecha CAD Vector (Phong Cách A)',
      subtitle: 'PURE VECTOR CAD RIG 29 KHỚP',
      desc: 'Bản vẽ CAD Vector cơ khí than chì; giáp titan sáng bóng; đầu ngực xoay chuẩn 0°; piston thủy lực kép; vòng tròn định vị ngắm bắn CAD Reticle; tơ laser Cyan.',
      badge: '#StyleA_Titanium'
    }
  ];

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0,0,0,0.5)',
      backdropFilter: 'blur(5px)',
      zIndex: 200,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: '#fff',
        borderRadius: '16px',
        maxWidth: '720px',
        width: '100%',
        padding: '24px',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Chọn Skin Con Nhện (2 Mẫu Thẩm Mỹ Tuyệt Đỉnh)</h2>
            <p style={{ fontSize: '12px', color: '#78716c' }}>Hệ thống động học & hiệu ứng tơ thích ứng theo từng phong cách</p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>✕</button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          {skins.map(s => {
            const isSelected = currentSkin === s.id;
            return (
              <div
                key={s.id}
                onClick={() => { onSelectSkin(s.id); onClose(); }}
                style={{
                  border: isSelected ? '2px solid #7c3aed' : '1px solid #e8e6df',
                  borderRadius: '12px',
                  padding: '16px',
                  background: isSelected ? 'rgba(124, 58, 237, 0.04)' : '#fbfaf6',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  position: 'relative'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1c1917' }}>{s.title}</h4>
                  <span style={{ fontSize: '10px', background: isSelected ? '#7c3aed' : '#e2e0d8', color: isSelected ? '#fff' : '#57534e', padding: '2px 8px', borderRadius: '10px', fontWeight: 700 }}>
                    {s.badge}
                  </span>
                </div>
                <div style={{ fontSize: '10px', color: '#78716c', fontFamily: 'var(--font-mono)', marginBottom: '8px' }}>
                  {s.subtitle}
                </div>
                <p style={{ fontSize: '12px', color: '#57534e', lineHeight: '1.4' }}>
                  {s.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
