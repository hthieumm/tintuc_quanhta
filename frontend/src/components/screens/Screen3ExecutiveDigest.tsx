import React, { useState } from 'react';
import { ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';

interface Screen3ExecutiveDigestProps {
  onNavigate: (tab: ScreenTab) => void;
}

export const Screen3ExecutiveDigest: React.FC<Screen3ExecutiveDigestProps> = ({ onNavigate }) => {
  const [selectedDate, setSelectedDate] = useState<string>('2026-10-11');
  const [filterMacro, setFilterMacro] = useState<boolean>(true);
  const [filterGeopolitics, setFilterGeopolitics] = useState<boolean>(true);
  const [filterTech, setFilterTech] = useState<boolean>(true);
  const [copiedNotice, setCopiedNotice] = useState<boolean>(false);

  const dates = [
    { id: '2026-10-11', label: '11/10/2026 (42 tin)' },
    { id: '2026-10-10', label: '10/10/2026 (38 tin)' },
    { id: '2026-10-09', label: '09/10/2026 (45 tin)' },
    { id: '2026-10-08', label: '08/10/2026 (29 tin)' },
    { id: '2026-10-07', label: '07/10/2026 (51 tin)' },
    { id: 'w40-2026', label: 'W40/2026 (Tổng hợp tuần)' }
  ];

  const handleCopyMarkdown = () => {
    playSfx('paper_rustle');
    const content = `# BẢN TIN VĨ MÔ ĐIỀU HÀNH NGÀY 11/10/2026\n\n- Tâm lý thị trường: 0.68 (Tích cực / Risk-On)\n- Độ tin cậy tổng hợp: 96.4%\n- Tỷ lệ phân bổ: 45% Kinh tế, 30% Địa chính trị, 25% Công nghệ AI\n\n## 1. Vĩ Mô & Dòng Tiền\n- FED phát tín hiệu giữ nguyên lãi suất 5.25%\n- Tỷ giá USD/VND hạ nhiệt về mốc 25.120\n- Dòng vốn FDI bán dẫn đạt 1.8 tỷ USD\n\n## 2. Địa Chính Trị\n- Tiêu chuẩn carbon mới của EU\n- Cước vận tải biển Á-Âu tăng 12%\n\n## 3. Đột Phá AI\n- Decision 3 Lite suy luận 5.4ms\n- Giảm 84.6% chi phí token API`;
    navigator.clipboard.writeText(content);
    setCopiedNotice(true);
    setTimeout(() => setCopiedNotice(false), 2000);
  };

  const handleExportPdf = () => {
    playSfx('click');
    alert('Đang kết xuất báo cáo vĩ mô PDF chuẩn định dạng A4 báo cáo điều hành...');
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
            LỊCH SỬ BẢN TIN
          </div>

          {/* Dates list */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {dates.map(d => {
              const isActive = selectedDate === d.id;
              return (
                <div
                  key={d.id}
                  onClick={() => {
                    playSfx('click');
                    setSelectedDate(d.id);
                  }}
                  style={{
                    padding: '7px 10px',
                    borderRadius: '8px',
                    backgroundColor: isActive ? '#2D4A2B' : '#F4F1EA',
                    color: isActive ? '#F4F1EA' : '#5A6B5C',
                    cursor: 'pointer',
                    fontSize: '12px',
                    fontWeight: isActive ? 700 : 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <span>{isActive ? '●' : '○'}</span>
                  <span>{d.label}</span>
                </div>
              );
            })}
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          <div
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '12px',
              fontWeight: 700,
              color: '#2D4A2B'
            }}
          >
            BỘ LỌC CHỦ ĐỀ
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px' }}>
            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                backgroundColor: '#F4F1EA',
                padding: '6px 10px',
                borderRadius: '6px',
                cursor: 'pointer',
                color: '#2D4A2B'
              }}
            >
              <input
                type="checkbox"
                checked={filterMacro && filterGeopolitics && filterTech}
                onChange={e => {
                  setFilterMacro(e.target.checked);
                  setFilterGeopolitics(e.target.checked);
                  setFilterTech(e.target.checked);
                }}
              />
              <span>Tất cả chuyên mục (42)</span>
            </label>

            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                backgroundColor: '#F4F1EA',
                padding: '6px 10px',
                borderRadius: '6px',
                cursor: 'pointer',
                color: '#2D4A2B'
              }}
            >
              <input
                type="checkbox"
                checked={filterMacro}
                onChange={e => setFilterMacro(e.target.checked)}
              />
              <span>Vĩ mô & Tiền tệ (19)</span>
            </label>

            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                backgroundColor: '#F4F1EA',
                padding: '6px 10px',
                borderRadius: '6px',
                cursor: 'pointer',
                color: '#2D4A2B'
              }}
            >
              <input
                type="checkbox"
                checked={filterGeopolitics}
                onChange={e => setFilterGeopolitics(e.target.checked)}
              />
              <span>Địa chính trị quốc tế (13)</span>
            </label>

            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                backgroundColor: '#F4F1EA',
                padding: '6px 10px',
                borderRadius: '6px',
                cursor: 'pointer',
                color: '#2D4A2B'
              }}
            >
              <input
                type="checkbox"
                checked={filterTech}
                onChange={e => setFilterTech(e.target.checked)}
              />
              <span>AI & Bán dẫn (10)</span>
            </label>
          </div>
        </div>

        {/* Sidebar Export Actions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button
            onClick={handleExportPdf}
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
            <span>Xuất Báo Cáo PDF</span>
          </button>

          <button
            onClick={handleCopyMarkdown}
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
            <span>📑</span>
            <span>{copiedNotice ? 'Đã Sao Chép!' : 'Sao chép Markdown'}</span>
          </button>
        </div>
      </aside>

      {/* 2. RIGHT DIGEST CONTAINER (1640px or flex-1) */}
      <main
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          overflowY: 'auto'
        }}
      >
        {/* Hero Banner: Executive Briefing */}
        <section
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            border: '1px solid #DCD5C5',
            padding: '16px 24px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)',
            flexShrink: 0
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <h1
              style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '20px',
                fontWeight: 700,
                color: '#2D4A2B'
              }}
            >
              BẢN TIN VĨ MÔ ĐIỀU HÀNH NGÀY 11/10/2026
            </h1>
            <div style={{ fontSize: '11.5px', color: '#5A6B5C' }}>
              Tổng hợp từ 42 bài báo chọn lọc • Lọc phản xạ Decision 3 Lite (System 1) + Gemini 2.5 Flash
            </div>
            <div style={{ display: 'flex', gap: '8px', marginTop: '2px' }}>
              <span
                style={{
                  backgroundColor: '#E8F0E8',
                  color: '#1B5E20',
                  padding: '3px 9px',
                  borderRadius: '999px',
                  fontSize: '10.5px',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600
                }}
              >
                📊 Tâm lý thị trường: 0.68 (Tích cực vừa phải / Risk-On)
              </span>
              <span
                style={{
                  backgroundColor: '#F2EBE5',
                  color: '#8C4830',
                  padding: '3px 9px',
                  borderRadius: '999px',
                  fontSize: '10.5px',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600
                }}
              >
                🎯 Độ tin cậy tổng hợp: 96.4%
              </span>
              <span
                style={{
                  backgroundColor: '#EAEFF4',
                  color: '#305A78',
                  padding: '3px 9px',
                  borderRadius: '999px',
                  fontSize: '10.5px',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600
                }}
              >
                ⏱️ Thời gian tổng hợp: 1.8s
              </span>
            </div>
          </div>

          {/* Ratio bar & Link to Screen 7 */}
          <div style={{ width: '380px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', fontWeight: 600 }}>
              <span style={{ color: '#2D4A2B' }}>TỶ LỆ PHÂN BỔ ĐỀ MỤC</span>
              <span style={{ color: '#5A6B5C', fontFamily: 'var(--font-mono)' }}>45% • 30% • 25%</span>
            </div>
            {/* Horizontal segmented bar */}
            <div style={{ display: 'flex', height: '10px', borderRadius: '5px', overflow: 'hidden' }}>
              <div style={{ width: '45%', backgroundColor: '#2D4A2B' }} title="Kinh tế vĩ mô 45%" />
              <div style={{ width: '30%', backgroundColor: '#C86D51' }} title="Địa chính trị 30%" />
              <div style={{ width: '25%', backgroundColor: '#4A6B82' }} title="Công nghệ AI 25%" />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#5A6B5C' }}>
              <span>● Kinh tế (45%)</span>
              <span>● Địa chính trị (30%)</span>
              <span>● AI (25%)</span>
            </div>
            <button
              onClick={() => onNavigate('analytics')}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#2D4A2B',
                fontSize: '11px',
                fontFamily: 'var(--font-mono)',
                fontWeight: 600,
                cursor: 'pointer',
                textAlign: 'right',
                marginTop: '2px'
              }}
            >
              📊 Xem Chi Tiết 6 Biểu Đồ Định Lượng (Screen 7) →
            </button>
          </div>
        </section>

        {/* 3 Modular Deep Dive Panels */}
        <section style={{ display: 'flex', gap: '12px', flex: 1 }}>
          {/* Panel 1: Macro & Cashflow */}
          {filterMacro && (
            <div
              style={{
                flex: 1,
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #DCD5C5',
                padding: '18px 20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '14.5px', fontWeight: 700, color: '#2D4A2B' }}>
                  VĨ MÔ & DÒNG TIỀN
                </span>
                <span
                  style={{
                    backgroundColor: '#E8F0E8',
                    color: '#1B5E20',
                    borderRadius: '999px',
                    padding: '2px 8px',
                    fontSize: '9.5px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  KINH TẾ & TIỀN TỆ
                </span>
              </div>

              {/* Highlights */}
              <div style={{ backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '10px', border: '1px solid #E8E2D5' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#2D4A2B', marginBottom: '6px' }}>
                  ĐIỂM NHẤN CỐT LÕI (HIGHLIGHTS):
                </div>
                <ul style={{ paddingLeft: '16px', fontSize: '11.5px', color: '#3D4E3D', lineHeight: '1.6' }}>
                  <li>FED phát tín hiệu giữ nguyên lãi suất 5.25% trong phiên họp</li>
                  <li>Tỷ giá USD/VND hạ nhiệt về mốc 25.120 sau can thiệp thị trường mở</li>
                  <li>Dòng vốn FDI cam kết vào mảng bán dẫn quý 3 đạt 1.8 tỷ USD</li>
                </ul>
              </div>

              {/* Narrative Digest */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#5A6B5C' }}>
                  PHÂN TÍCH CHUYÊN SÂU (NARRATIVE DIGEST):
                </div>
                <p style={{ fontSize: '12px', color: '#2C3E2C', lineHeight: '1.6' }}>
                  Áp lực tỷ giá hạ nhiệt rõ rệt sau động thái điều tiết thanh khoản qua OMO của Ngân hàng Nhà nước. Mặt bằng lãi suất huy động tiếp tục duy trì ở mức hợp lý, tạo điều kiện thuận lợi cho thanh khoản hệ thống ngân hàng thương mại trước thềm cao điểm tín dụng cuối năm.
                </p>
              </div>

              {/* Macro Impact Box */}
              <div
                style={{
                  backgroundColor: '#E8F0E8',
                  borderRadius: '8px',
                  padding: '10px',
                  marginTop: 'auto',
                  border: '1px solid #C8E6C9'
                }}
              >
                <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#1B5E20', marginBottom: '2px' }}>
                  ĐÁNH GIÁ TÁC ĐỘNG VĨ MÔ & KHUYẾN NGHỊ:
                </div>
                <div style={{ fontSize: '11.5px', color: '#2D3E2D', lineHeight: '1.45' }}>
                  Tác động tích cực tới chi phí vốn doanh nghiệp; tỷ giá ổn định mở ra cơ hội giải ngân vốn đầu tư công và thu hút dòng vốn ngoại trở lại thị trường chứng khoán.
                </div>
              </div>
            </div>
          )}

          {/* Panel 2: Geopolitics */}
          {filterGeopolitics && (
            <div
              style={{
                flex: 1,
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #DCD5C5',
                padding: '18px 20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '14.5px', fontWeight: 700, color: '#2D4A2B' }}>
                  TOÀN CẢNH ĐỊA CHÍNH TRỊ
                </span>
                <span
                  style={{
                    backgroundColor: '#FDF2EE',
                    color: '#C86D51',
                    borderRadius: '999px',
                    padding: '2px 8px',
                    fontSize: '9.5px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  ĐỊA CHÍNH TRỊ QUỐC TẾ
                </span>
              </div>

              {/* Highlights */}
              <div style={{ backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '10px', border: '1px solid #E8E2D5' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#2D4A2B', marginBottom: '6px' }}>
                  ĐIỂM NHẤN CỐT LÕI (HIGHLIGHTS):
                </div>
                <ul style={{ paddingLeft: '16px', fontSize: '11.5px', color: '#3D4E3D', lineHeight: '1.6' }}>
                  <li>EU ban hành tiêu chuẩn carbon mới cho linh kiện điện tử và hàng dệt may</li>
                  <li>Cước vận tải biển Á - Âu tiếp tục leo thang 12% do hạn chế kênh đào</li>
                  <li>Khối ASEAN ký hiệp định hợp tác hành lang kinh tế số xuyên biên giới</li>
                </ul>
              </div>

              {/* Narrative Digest */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#5A6B5C' }}>
                  PHÂN TÍCH CHUYÊN SÂU (NARRATIVE DIGEST):
                </div>
                <p style={{ fontSize: '12px', color: '#2C3E2C', lineHeight: '1.6' }}>
                  Căng thẳng chuỗi cung ứng logistics quốc tế vẫn tiềm ẩn rủi ro lạm phát chi phí đẩy. Tuy nhiên, việc ký kết hiệp định kinh tế số ASEAN mở ra không gian thương mại dịch vụ số bù đắp cho các rào cản thương mại hàng hóa truyền thống.
                </p>
              </div>

              {/* Macro Impact Box */}
              <div
                style={{
                  backgroundColor: '#FDF2EE',
                  borderRadius: '8px',
                  padding: '10px',
                  marginTop: 'auto',
                  border: '1px solid #F5C6BA'
                }}
              >
                <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#C86D51', marginBottom: '2px' }}>
                  ĐÁNH GIÁ TÁC ĐỘNG VĨ MÔ & KHUYẾN NGHỊ:
                </div>
                <div style={{ fontSize: '11.5px', color: '#2D3E2D', lineHeight: '1.45' }}>
                  Cần chủ động phòng ngừa rủi ro chi phí vận tải biển quý 4; đồng thời đẩy nhanh chuyển đổi xanh sản xuất linh kiện xuất khẩu để đáp ứng chuẩn mực mới của châu Âu.
                </div>
              </div>
            </div>
          )}

          {/* Panel 3: AI & GitHub Tech */}
          {filterTech && (
            <div
              style={{
                flex: 1,
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #DCD5C5',
                padding: '18px 20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '14.5px', fontWeight: 700, color: '#2D4A2B' }}>
                  ĐỘT PHÁ CÔNG NGHỆ AI
                </span>
                <span
                  style={{
                    backgroundColor: '#EAF1F7',
                    color: '#4A6B82',
                    borderRadius: '999px',
                    padding: '2px 8px',
                    fontSize: '9.5px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  AI SYSTEM 1 & EDGE
                </span>
              </div>

              {/* Highlights */}
              <div style={{ backgroundColor: '#FBF9F5', borderRadius: '8px', padding: '10px', border: '1px solid #E8E2D5' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#2D4A2B', marginBottom: '6px' }}>
                  ĐIỂM NHẤN CỐT LÕI (HIGHLIGHTS):
                </div>
                <ul style={{ paddingLeft: '16px', fontSize: '11.5px', color: '#3D4E3D', lineHeight: '1.6' }}>
                  <li>decision-ai/decision-3-lite phát hành bản System 1 suy luận nhị phân 5.4ms</li>
                  <li>Kiến trúc Sparse Attention mới giảm 40% chi phí VRAM khi chạy cục bộ</li>
                  <li>Spider Radar hoàn tất tích hợp dual-system: Decision 3 Lite + Gemini 2.5 Flash</li>
                </ul>
              </div>

              {/* Narrative Digest */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#5A6B5C' }}>
                  PHÂN TÍCH CHUYÊN SÂU (NARRATIVE DIGEST):
                </div>
                <p style={{ fontSize: '12px', color: '#2C3E2C', lineHeight: '1.6' }}>
                  Bước tiến quan trọng của kiến trúc mô hình phân loại phản xạ trực giác (Reflexive Classifiers). Bằng cách phân định rành mạch giữa System 1 (nhanh, rẻ, cục bộ) và System 2 (suy luận sâu), hệ sinh thái đã chứng minh khả năng cắt giảm 84.6% chi phí token.
                </p>
              </div>

              {/* Macro Impact Box */}
              <div
                style={{
                  backgroundColor: '#EAF1F7',
                  borderRadius: '8px',
                  padding: '10px',
                  marginTop: 'auto',
                  border: '1px solid #BCD0DF'
                }}
              >
                <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#4A6B82', marginBottom: '2px' }}>
                  ĐÁNH GIÁ TÁC ĐỘNG VĨ MÔ & KHUYẾN NGHỊ:
                </div>
                <div style={{ fontSize: '11.5px', color: '#2D3E2D', lineHeight: '1.45' }}>
                  Tối ưu hóa chi phí vận hành AI ứng dụng trong các doanh nghiệp tài chính; loại bỏ hoàn toàn rủi ro vượt ngân sách API cloud trong bối cảnh nhu cầu AI tăng vọt.
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
};
