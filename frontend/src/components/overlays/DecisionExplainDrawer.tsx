import React from 'react';
import { playSfx } from '../../utils/audio';

interface DecisionExplainDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DecisionExplainDrawer: React.FC<DecisionExplainDrawerProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.35)',
        backdropFilter: 'blur(2px)',
        display: 'flex',
        justifyContent: 'flex-end',
        zIndex: 95
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          width: '460px',
          height: '100%',
          backgroundColor: '#FFFFFF',
          borderLeft: '1px solid #DCD5C5',
          boxShadow: '-4px 0 24px rgba(0, 0, 0, 0.15)',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflowY: 'auto'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #E8E2D5', paddingBottom: '12px' }}>
            <div>
              <div style={{ fontFamily: 'var(--font-serif)', fontSize: '16px', fontWeight: 700, color: '#2D4A2B' }}>
                GIẢI TRÌNH QUYẾT ĐỊNH DECISION 3 LITE
              </div>
              <div style={{ fontSize: '11px', color: '#5A6B5C', marginTop: '2px' }}>
                Single-Pass Tensor Attribution & Attention Weights
              </div>
            </div>
            <button
              onClick={onClose}
              style={{
                border: 'none',
                backgroundColor: '#F4F1EA',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                cursor: 'pointer',
                fontSize: '12px',
                color: '#2D4A2B'
              }}
            >
              ✕
            </button>
          </div>

          {/* Verdict Card */}
          <div
            style={{
              backgroundColor: '#FBF9F5',
              border: '1.5px solid #2D4A2B',
              borderRadius: '8px',
              padding: '12px',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px'
            }}
          >
            <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#8D6E63', fontWeight: 700 }}>
              KẾT QUẢ SUY LUẬN NHỊ PHÂN (SYSTEM 1)
            </div>
            <div style={{ fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
              PASS THRESHOLD: VĨ MÔ TRỌNG ĐIỂM (CHẤP THUẬN)
            </div>
            <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: '#1B5E20' }}>
              Confidence Score: 0.942 / 1.000 • Latency: 5.4ms
            </div>
          </div>

          {/* Token Weights Table */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#2D4A2B' }}>
              TRỌNG SỐ TỪ KHÓA (ATTENTION ATTRIBUTION):
            </div>

            {[
              { token: 'Thanh khoản OMO', weight: '+0.92', impact: 'Kích hoạt bơm ròng ngân hàng nhà nước', color: '#1B5E20' },
              { token: 'Trần Lãi Suất 4.5%', weight: '+0.88', impact: 'Chính sách tiền tệ ổn định vĩ mô', color: '#1B5E20' },
              { token: 'Tỷ giá USD/VND', weight: '+0.79', impact: 'Tác động trực tiếp tới thị trường mở', color: '#1B5E20' },
              { token: 'Chỉ số CPI', weight: '+0.64', impact: 'Đo lường kỳ vọng lạm phát', color: '#2D4A2B' },
              { token: 'Tin đồn mạng', weight: '-0.45', impact: 'Lọc giảm trọng số tin tức không kiểm chứng', color: '#C86D51' }
            ].map((item, idx) => (
              <div
                key={idx}
                style={{
                  backgroundColor: '#FAF8F5',
                  border: '1px solid #E8E2D5',
                  borderRadius: '6px',
                  padding: '8px 10px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#2D4A2B' }}>{item.token}</div>
                  <div style={{ fontSize: '10px', color: '#5A6B5C' }}>{item.impact}</div>
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', fontWeight: 700, color: item.color }}>
                  {item.weight}
                </span>
              </div>
            ))}
          </div>

          {/* Architectural Notes */}
          <div
            style={{
              backgroundColor: '#E8F5E9',
              borderRadius: '8px',
              padding: '12px',
              border: '1px solid #C8E6C9',
              fontSize: '11.5px',
              color: '#1B5E20',
              lineHeight: '1.5'
            }}
          >
            <strong>Cơ chế định tuyến:</strong> Bài báo này vượt ngưỡng tin cậy 0.75, thỏa mãn điều kiện chuyển tiếp sang LLM System 2 (Gemini 2.5 Flash) để sinh bản dịch và phân tích tác động vĩ mô chi tiết.
          </div>
        </div>

        {/* Close button */}
        <button
          onClick={() => {
            playSfx('click');
            onClose();
          }}
          style={{
            backgroundColor: '#2D4A2B',
            color: '#FAF8F5',
            border: 'none',
            borderRadius: '8px',
            padding: '10px',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            textAlign: 'center',
            marginTop: '16px'
          }}
        >
          Đóng Ngăn Kéo Giải Trình
        </button>
      </div>
    </div>
  );
};
