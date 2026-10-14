import React, { useState } from 'react';

interface ArticleReaderProps {
  onKeywordClick: (index: number, word: string, category: string, el: HTMLElement) => void;
}

export const ArticleReader: React.FC<ArticleReaderProps> = ({ onKeywordClick }) => {
  const [isVietnamese, setIsVietnamese] = useState(true);

  const handleClick = (e: React.MouseEvent<HTMLElement>, index: number, word: string, category: string) => {
    e.stopPropagation();
    onKeywordClick(index, word, category, e.currentTarget);
  };

  return (
    <div style={{ flex: '0 0 65%', padding: '32px 40px', overflowY: 'auto' }}>
      {/* Top Metadata Bar & Bilingual Switcher */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div style={{ fontSize: '11px', color: '#78716c', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', letterSpacing: '1px' }}>
          BLOOMBERG / CAFÉF VĨ MÔ • 10/10/2026 • 2 PHÚT TRƯỚC
        </div>
        {/* Bilingual View Switcher */}
        <div style={{ display: 'flex', background: '#f5f4ef', padding: '3px', borderRadius: '20px', border: '1px solid #e2e0d8', fontSize: '12px' }}>
          <button
            onClick={() => setIsVietnamese(true)}
            style={{
              padding: '4px 12px',
              borderRadius: '16px',
              border: 'none',
              background: isVietnamese ? '#2d4a2b' : 'transparent',
              color: isVietnamese ? '#fff' : '#57534e',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            ● 🇻🇳 Tiếng Việt
          </button>
          <button
            onClick={() => setIsVietnamese(false)}
            style={{
              padding: '4px 12px',
              borderRadius: '16px',
              border: 'none',
              background: !isVietnamese ? '#2d4a2b' : 'transparent',
              color: !isVietnamese ? '#fff' : '#57534e',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            ○ 🌐 Bản Gốc
          </button>
        </div>
      </div>

      {/* Article Title */}
      <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: '28px', lineHeight: '1.35', color: '#1c1917', marginBottom: '24px' }}>
        {isVietnamese 
          ? "Ngân Hàng Nhà Nước Họp Khẩn: Duy Trì Trần Lãi Suất & Ổn Định Tỷ Giá Dòng Tiền"
          : "State Bank of Vietnam Emergency Briefing: Interest Rate Caps Sustained & FX Liquidity Stabilized"}
      </h1>

      {/* Article Body */}
      <div style={{ fontSize: '16px', lineHeight: '1.8', color: '#44403c' }}>
        <p style={{ marginBottom: '20px' }}>
          {isVietnamese ? (
            <>
              Sáng nay, Thống đốc Ngân hàng Nhà nước đã chủ trì hội nghị điều hành chính sách tiền tệ quý 4. Theo định hướng xuyên suốt, cơ quan quản lý quyết tâm duy trì ổn định trần{' '}
              <mark
                className="spider-target"
                data-spider-index="0"
                data-word="Lãi suất"
                data-cat="kinh_te"
                onClick={(e) => handleClick(e, 0, "Lãi suất", "kinh_te")}
              >
                LÃI SUẤT ĐIỀU HÀNH
              </mark>{' '}
              ở mức 4.5% nhằm hỗ trợ cộng đồng doanh nghiệp và kích cầu tín dụng cuối năm.
            </>
          ) : (
            <>
              This morning, the SBV Governor chaired the monetary policy conference for Q4. Management confirmed its firm stance on maintaining stability for benchmark{' '}
              <mark
                className="spider-target"
                data-spider-index="0"
                data-word="Interest Rates"
                data-cat="kinh_te"
                onClick={(e) => handleClick(e, 0, "Interest Rates", "kinh_te")}
              >
                POLICY INTEREST RATES
              </mark>{' '}
              at 4.5% to stimulate corporate credit growth.
            </>
          )}
        </p>

        <p style={{ marginBottom: '20px' }}>
          {isVietnamese ? (
            <>
              Đồng thời, cơ quan quản lý cam kết theo dõi chặt chẽ diễn biến{' '}
              <mark
                className="spider-target"
                data-spider-index="1"
                data-word="Tỷ giá & Giá vàng"
                data-cat="vang"
                onClick={(e) => handleClick(e, 1, "Tỷ giá & Giá vàng", "vang")}
              >
                TỶ GIÁ USD/VND & GIÁ VÀNG
              </mark>
              , sẵn sàng can thiệp bán ngoại tệ kỳ hạn để triệt tiêu tình trạng đầu cơ. Thanh khoản liên ngân hàng được giữ dồi dào, tạo động lực tâm lý tích cực giúp chỉ số{' '}
              <mark
                className="spider-target"
                data-spider-index="2"
                data-word="VN-Index"
                data-cat="chung_khoan"
                onClick={(e) => handleClick(e, 2, "VN-Index", "chung_khoan")}
              >
                VN-INDEX BỨT PHÁ 1.300 ĐIỂM
              </mark>{' '}
              với khối lượng khớp lệnh kỷ lục.
            </>
          ) : (
            <>
              Simultaneously, the regulator closely monitors{' '}
              <mark
                className="spider-target"
                data-spider-index="1"
                data-word="FX & Gold"
                data-cat="vang"
                onClick={(e) => handleClick(e, 1, "FX & Gold", "vang")}
              >
                USD/VND RATES & GOLD PRICES
              </mark>
              , prepared for foreign currency market interventions, driving confidence as{' '}
              <mark
                className="spider-target"
                data-spider-index="2"
                data-word="VN-Index"
                data-cat="chung_khoan"
                onClick={(e) => handleClick(e, 2, "VN-Index", "chung_khoan")}
              >
                VN-INDEX SURGES PAST 1,300
              </mark>{' '}
              with historic liquidity.
            </>
          )}
        </p>
      </div>
    </div>
  );
};
