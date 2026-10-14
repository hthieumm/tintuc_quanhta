import React, { useState } from 'react';
import { ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';

interface Screen7AnalyticsProps {
  onNavigate: (tab: ScreenTab) => void;
}

export const Screen7Analytics: React.FC<Screen7AnalyticsProps> = ({ onNavigate }) => {
  const [timeHorizon, setTimeHorizon] = useState<string>('30d');
  const [refreshNotice, setRefreshNotice] = useState<boolean>(false);

  const handleRefresh = () => {
    playSfx('click');
    setRefreshNotice(true);
    setTimeout(() => setRefreshNotice(false), 2000);
  };

  const handleExportData = () => {
    playSfx('paper_rustle');
    alert('Đang kết xuất tệp CSV/JSON toàn bộ chuỗi số liệu 30 ngày từ SQLite CTE...');
  };

  return (
    <div
      style={{
        display: 'flex',
        flex: 1,
        gap: '12px',
        padding: '0 12px',
        overflow: 'hidden',
        height: 'calc(100vh - 114px)',
        position: 'relative'
      }}
    >
      {/* 1. LEFT SIDEBAR (240px) */}
      <aside
        style={{
          width: '240px',
          flexShrink: 0,
          backgroundColor: '#EBE6DC',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '14px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflowY: 'auto'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '12.5px',
              fontWeight: 700,
              color: '#2D4A2B',
              letterSpacing: '0.3px'
            }}
          >
            BỘ LỌC PHÂN TÍCH
          </div>

          {/* Time horizons */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {[
              { id: '24h', label: '○ 24 Giờ Qua (42 tin)' },
              { id: '7d', label: '○ 7 Ngày Qua (186 tin)' },
              { id: '30d', label: '● 30 Ngày Qua (1,842 tin)' },
              { id: 'q4', label: '○ Quý 4/2026 (Toàn cảnh)' }
            ].map(item => {
              const isActive = timeHorizon === item.id;
              return (
                <div
                  key={item.id}
                  onClick={() => {
                    playSfx('click');
                    setTimeHorizon(item.id);
                  }}
                  style={{
                    padding: '6px 10px',
                    borderRadius: '6px',
                    backgroundColor: isActive ? '#2D4A2B' : '#F4F1EA',
                    color: isActive ? '#F4F1EA' : '#5A6B5C',
                    fontSize: '11.5px',
                    fontWeight: isActive ? 700 : 500,
                    cursor: 'pointer'
                  }}
                >
                  {item.label}
                </div>
              );
            })}
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* Tracking Indicators */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
              CHỈ SỐ THEO DÕI
            </div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Tâm lý thị trường (Sentiment)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Tỷ lệ lọc sạch Decision 3 (76%)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Ma trận từ khóa (Heatmap)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Độ trễ suy luận (P50 8.5ms)</span>
            </label>
          </div>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button
            onClick={handleExportData}
            style={{
              backgroundColor: '#2D4A2B',
              border: 'none',
              borderRadius: '8px',
              padding: '9px 12px',
              color: '#F4F1EA',
              fontSize: '11.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>📥</span>
            <span>Xuất Báo Cáo Dữ Liệu</span>
          </button>

          <button
            onClick={handleRefresh}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #DCD5C5',
              borderRadius: '8px',
              padding: '8px 12px',
              color: '#2D4A2B',
              fontSize: '11.5px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>🔄</span>
            <span>{refreshNotice ? 'Đã Đồng Bộ Mới!' : 'Làm Mới Số Liệu'}</span>
          </button>
        </div>
      </aside>

      {/* 2. RIGHT CHARTS DASHBOARD (1640px or flex-1, 2-COLUMN BENTO GRID) */}
      <main
        style={{
          flex: 1,
          display: 'flex',
          gap: '12px',
          overflowY: 'auto'
        }}
      >
        {/* Left Column (Cards 1, 2, 3) */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Card 1: Sentiment 30 days */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                XU HƯỚNG TÂM LÝ THỊ TRƯỜNG 30 NGÀY
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                TRUNG BÌNH: +0.68 (RISK-ON NHẸ)
              </span>
            </div>

            <div style={{ fontSize: '11px', color: '#5A6B5C' }}>
              Tổng hợp từ 1,842 bài báo phân tích • Biên độ dao động -1.0 đến +1.0
            </div>

            {/* Sentiment Graph Box */}
            <div style={{ backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '12px', border: '1px solid #E8E2D5', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#1B5E20', fontWeight: 700 }}>
                <span>+1.0 [VÙNG RISK-ON / LẠC QUAN]</span>
                <span>ĐỈNH: +0.72 (08/10)</span>
              </div>

              {/* Bar visualization of sentiment progression */}
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '6px', height: '90px', padding: '6px 0', borderBottom: '1px solid #DCD5C5' }}>
                {[35, 42, 28, 48, 55, 62, 50, 70, 85, 98, 92, 104, 95, 90].map((h, i) => (
                  <div
                    key={i}
                    style={{
                      flex: 1,
                      height: `${h * 0.75}%`,
                      backgroundColor: h > 80 ? '#1B5E20' : h > 50 ? '#4D804D' : '#A8CAA8',
                      borderRadius: '3px 3px 0 0'
                    }}
                    title={`Ngày ${i * 2 + 1}: +${(h / 120).toFixed(2)}`}
                  />
                ))}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9.5px', fontFamily: 'var(--font-mono)', color: '#8A9A86' }}>
                <span>12/09 (Khởi điểm +0.22)</span>
                <span>25/09 (Điều chỉnh OMO)</span>
                <span style={{ color: '#2D4A2B', fontWeight: 700 }}>11/10 (Hiện tại +0.68)</span>
              </div>
            </div>

            <div style={{ fontSize: '11px', color: '#2D4A2B', fontStyle: 'italic' }}>
              • Nhận định AI: Thị trường chuyển biến tích cực rõ nét từ tuần 40 khi tỷ giá hạ nhiệt.
            </div>
          </div>

          {/* Card 2: Clean ratio */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                TỶ LỆ LỌC SẠCH & KHỬ TIN RÁC CỦA DECISION 3 LITE
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                LOẠI BỎ 76.4% TIN RÁC
              </span>
            </div>

            <div style={{ fontSize: '11px', color: '#5A6B5C' }}>
              So sánh tổng bài cào thô (Xám) vs Bài báo tinh hoa giữ lại (Xanh)
            </div>

            {/* Daily comparison bars */}
            <div style={{ backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '10px 14px', border: '1px solid #E8E2D5', display: 'flex', justifyContent: 'space-between' }}>
              {[
                { day: 'T2 (05/10)', raw: 85, clean: 22 },
                { day: 'T3 (06/10)', raw: 92, clean: 26 },
                { day: 'T4 (07/10)', raw: 105, clean: 32 },
                { day: 'T5 (08/10)', raw: 78, clean: 20 },
                { day: 'T6 (09/10)', raw: 110, clean: 35 },
                { day: 'T7 (10/10)', raw: 88, clean: 24 },
                { day: 'CN (11/10)', raw: 95, clean: 28 }
              ].map((d, i) => (
                <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-end', gap: '3px', height: '65px' }}>
                    <div style={{ width: '12px', height: `${(d.raw / 120) * 100}%`, backgroundColor: '#DCD5C5', borderRadius: '2px' }} title={`Thô: ${d.raw}`} />
                    <div style={{ width: '12px', height: `${(d.clean / 120) * 100}%`, backgroundColor: '#2D4A2B', borderRadius: '2px' }} title={`Sạch: ${d.clean}`} />
                  </div>
                  <span style={{ fontSize: '9px', fontFamily: 'var(--font-mono)', color: '#5A6B5C' }}>{d.day}</span>
                </div>
              ))}
            </div>

            <div style={{ fontSize: '11px', color: '#1B5E20', fontWeight: 600 }}>
              • Tiết kiệm trung bình: 4.2 giờ đọc tin rác/ngày cho người dùng.
            </div>
          </div>

          {/* Card 3: Latency Histogram */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                PHÂN PHỐI ĐỘ TRỄ SUY LUẬN Decision 3 Lite (System 1)
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                P50: 8.5ms • P95: 14.2ms
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#2D4A2B' }}>&lt; 5.0ms (Cực nhanh):</span>
                <div style={{ width: '240px', height: '8px', backgroundColor: '#EBE6DC', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '35%', height: '100%', backgroundColor: '#1B5E20' }} />
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', color: '#1B5E20', fontWeight: 700 }}>35% (35k req)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#2D4A2B' }}>5ms - 10ms (Chuẩn):</span>
                <div style={{ width: '240px', height: '8px', backgroundColor: '#EBE6DC', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '48%', height: '100%', backgroundColor: '#2D4A2B' }} />
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', color: '#2D4A2B', fontWeight: 700 }}>48% (48k req)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#2D4A2B' }}>10ms - 20ms (Chậm nhẹ):</span>
                <div style={{ width: '240px', height: '8px', backgroundColor: '#EBE6DC', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '14%', height: '100%', backgroundColor: '#E5B869' }} />
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', color: '#8D6E63', fontWeight: 700 }}>14% (14k req)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#2D4A2B' }}>&gt; 20ms (Biên ngoài):</span>
                <div style={{ width: '240px', height: '8px', backgroundColor: '#EBE6DC', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '3%', height: '100%', backgroundColor: '#C86D51' }} />
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', color: '#C86D51', fontWeight: 700 }}>3% (3k req)</span>
              </div>
            </div>

            <div style={{ fontSize: '10.5px', color: '#1B5E20', fontWeight: 600 }}>
              • 100% request hoàn thành &lt; 25ms. Không có hiện tượng nghẽn luồng.
            </div>
          </div>
        </div>

        {/* Right Column (Cards 4, 5, 6) */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Card 4: Topic Allocation */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                CƠ CẤU CHỦ ĐỀ & TỶ TRỌNG DÒNG TIỀN VĨ MÔ
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                TOP 1: KINH TẾ (45%)
              </span>
            </div>

            {/* Segmented bar */}
            <div style={{ display: 'flex', height: '14px', borderRadius: '6px', overflow: 'hidden' }}>
              <div style={{ width: '45%', backgroundColor: '#2D4A2B' }} />
              <div style={{ width: '30%', backgroundColor: '#C86D51' }} />
              <div style={{ width: '25%', backgroundColor: '#4A6B82' }} />
            </div>

            {/* 3 Columns breakdown */}
            <div style={{ display: 'flex', backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '10px', border: '1px solid #E8E2D5', justifyContent: 'space-between', fontSize: '11px' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                <span style={{ fontWeight: 700, color: '#2D4A2B' }}>● Kinh Tế & Tiền Tệ (45%)</span>
                <span style={{ color: '#5A6B5C' }}>• Lãi suất điều hành: 28%</span>
                <span style={{ color: '#5A6B5C' }}>• Tỷ giá USD/VND: 17%</span>
                <span style={{ color: '#5A6B5C' }}>• Tín dụng & OMO: 15%</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                <span style={{ fontWeight: 700, color: '#C86D51' }}>● Địa Chính Trị (30%)</span>
                <span style={{ color: '#5A6B5C' }}>• Kênh đào Suez: 18%</span>
                <span style={{ color: '#5A6B5C' }}>• Tiêu chuẩn Carbon EU: 12%</span>
                <span style={{ color: '#5A6B5C' }}>• Hiệp định số ASEAN: 10%</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                <span style={{ fontWeight: 700, color: '#4A6B82' }}>● Công Nghệ AI (25%)</span>
                <span style={{ color: '#5A6B5C' }}>• System 1 Fast Pass: 15%</span>
                <span style={{ color: '#5A6B5C' }}>• Đạo luật Chips & FDI: 10%</span>
                <span style={{ color: '#5A6B5C' }}>• Edge AI Wasm: 8%</span>
              </div>
            </div>

            <div style={{ fontSize: '11px', color: '#2D4A2B', fontStyle: 'italic' }}>
              • Dự báo dòng tiền: Nhóm cổ phiếu xuất khẩu và khu công nghiệp hưởng lợi lớn nhất.
            </div>
          </div>

          {/* Card 5: Heatmap 4x3 */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                MA TRẬN NHIỆT TỪ KHÓA NÓNG TRONG TUẦN (HEATMAP)
              </span>
              <span style={{ backgroundColor: '#E2DCD0', color: '#2D4A2B', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                TỔNG 142 TỪ KHÓA
              </span>
            </div>

            {/* 4x3 Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px' }}>
              {[
                { word: 'LÃI SUẤT', count: '412 lần', bg: '#2D4A2B', color: '#F4F1EA' },
                { word: 'TỶ GIÁ USD', count: '385 lần', bg: '#385E36', color: '#F4F1EA' },
                { word: 'VÀNG SJC', count: '310 lần', bg: '#C86D51', color: '#F4F1EA' },
                { word: 'BÁN DẪN', count: '280 lần', bg: '#4A6B82', color: '#F4F1EA' },
                { word: 'FED RATE', count: '265 lần', bg: '#527550', color: '#F4F1EA' },
                { word: 'SBV OMO', count: '240 lần', bg: '#6D8F6B', color: '#F4F1EA' },
                { word: 'Decision 3', count: '215 lần', bg: '#8EA98C', color: '#1B2E1A' },
                { word: 'VN-INDEX', count: '198 lần', bg: '#E5B869', color: '#2D4A2B' },
                { word: 'LẠM PHÁT', count: '175 lần', bg: '#E2A999', color: '#2D4A2B' },
                { word: 'FDI CHIPS', count: '160 lần', bg: '#A0B8C8', color: '#1A2E3B' },
                { word: 'DẦU BRENT', count: '145 lần', bg: '#E8D0C8', color: '#4A2B20' },
                { word: 'SUEZ LOGISTICS', count: '130 lần', bg: '#F0E0D8', color: '#5A3B30' }
              ].map((cell, idx) => (
                <div
                  key={idx}
                  style={{
                    backgroundColor: cell.bg,
                    color: cell.color,
                    padding: '8px 6px',
                    borderRadius: '6px',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '2px'
                  }}
                >
                  <span style={{ fontSize: '11px', fontWeight: 700 }}>{cell.word}</span>
                  <span style={{ fontSize: '9px', fontFamily: 'var(--font-mono)', opacity: 0.9 }}>{cell.count}</span>
                </div>
              ))}
            </div>

            <div style={{ fontSize: '10.5px', color: '#2D4A2B', fontWeight: 600 }}>
              • 3 thực thể biến động mạnh nhất tuần: [LÃI SUẤT (+24%)] • [TỶ GIÁ USD (+18%)] • [BÁN DẪN (+28%)].
            </div>
          </div>

          {/* Card 6: Cost Efficiency */}
          <div
            style={{
              backgroundColor: '#E8F0E8',
              borderRadius: '12px',
              border: '1px solid #C8E6C9',
              padding: '14px 18px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#1B5E20' }}>
                ⚡ HIỆU QUẢ VẬN HÀNH DUAL-SYSTEM (TIẾT KIỆM TỐI ĐA)
              </span>
              <span style={{ backgroundColor: '#FFFFFF', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                TIẾT KIỆM 84.6% TOKEN
              </span>
            </div>

            <div style={{ display: 'flex', gap: '8px' }}>
              <div style={{ flex: 1, backgroundColor: '#FFFFFF', borderRadius: '6px', padding: '8px', fontSize: '11px', color: '#1B5E20', fontWeight: 600 }}>
                💰 Tiết kiệm chi phí API: -84.6%
              </div>
              <div style={{ flex: 1, backgroundColor: '#FFFFFF', borderRadius: '6px', padding: '8px', fontSize: '11px', color: '#2D4A2B', fontWeight: 600 }}>
                🖥️ VRAM Chiếm Dụng: 0 MB
              </div>
              <div style={{ flex: 1, backgroundColor: '#FFFFFF', borderRadius: '6px', padding: '8px', fontSize: '11px', color: '#4A6B82', fontWeight: 600 }}>
                💾 Tốc độ FTS5: 1.2ms
              </div>
            </div>

            <div style={{ fontSize: '11px', color: '#2D3E2D', lineHeight: '1.4' }}>
              Spider Radar đạt hiệu năng xử lý tin tức vĩ mô tương đương trạm tài chính Bloomberg với chi phí token và phần cứng tối ưu bậc nhất.
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
