import React, { useState } from 'react';
import { ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';

interface Screen5TrendVaultProps {
  onNavigate: (tab: ScreenTab) => void;
}

export const Screen5TrendVault: React.FC<Screen5TrendVaultProps> = ({ onNavigate }) => {
  const [selectedEntity, setSelectedEntity] = useState<string>('usdvnd');
  const [isBookmarked, setIsBookmarked] = useState<boolean>(true);
  const [searchEntity, setSearchEntity] = useState<string>('');

  const entityDetails: Record<
    string,
    {
      name: string;
      badge: string;
      badgeColor: string;
      badgeBg: string;
      desc: string;
      topArticles: { title: string; meta: string }[];
    }
  > = {
    usdvnd: {
      name: 'TỶ GIÁ USD/VND',
      badge: 'GIẢM NHẸ (-0.3%)',
      badgeColor: '#1B5E20',
      badgeBg: '#E8F0E8',
      desc: 'Mức độ tác động vĩ mô: RẤT CAO • Tương quan âm với VN-Index và chi phí nhập khẩu nguyên liệu.',
      topArticles: [
        {
          title: '1. CafeF (11/10): SBV can thiệp thị trường mở, tỷ giá hạ nhiệt',
          meta: 'Độ tin cậy: 98% • Trọng số tác động: 0.89'
        },
        {
          title: '2. VnExpress (09/10): Doanh nghiệp xuất nhập khẩu bớt nỗi lo',
          meta: 'Độ tin cậy: 94% • Trọng số tác động: 0.82'
        },
        {
          title: '3. Tuổi Trẻ (06/10): Kiều hối quý 3 hỗ trợ nguồn cung ngoại tệ',
          meta: 'Độ tin cậy: 91% • Trọng số tác động: 0.76'
        }
      ]
    },
    fed: {
      name: 'FED LÃI SUẤT ĐIỀU HÀNH',
      badge: 'GIỮ NGUYÊN (5.25%)',
      badgeColor: '#1B5E20',
      badgeBg: '#E8F0E8',
      desc: 'Trục rễ nguyên nhân trung tâm điều tiết dòng vốn toàn cầu và chỉ số DXY.',
      topArticles: [
        {
          title: '1. Reuters (11/10): FOMC duy trì biên độ lãi suất 5.25%-5.50%',
          meta: 'Độ tin cậy: 99% • Trọng số tác động: 0.95'
        },
        {
          title: '2. Bloomberg (10/10): Kỳ vọng nới lỏng chu kỳ quý 4 được củng cố',
          meta: 'Độ tin cậy: 96% • Trọng số tác động: 0.88'
        }
      ]
    },
    vnindex: {
      name: 'VN-INDEX (1,280 ĐIỂM)',
      badge: 'TĂNG TRƯỞNG (+1.2%)',
      badgeColor: '#1B5E20',
      badgeBg: '#E8F0E8',
      desc: 'Thanh khoản bùng nổ 28.5k tỷ, dòng tiền nội lan tỏa sang nhóm xuất khẩu và ngân hàng.',
      topArticles: [
        {
          title: '1. Đầu Tư (11/10): VN-Index bứt phá ngưỡng cản tâm lý',
          meta: 'Độ tin cậy: 95% • Trọng số tác động: 0.84'
        }
      ]
    },
    sjc: {
      name: 'VÀNG SJC (88.5 TR/LƯỢNG)',
      badge: 'ĐỈNH MỚI (+2.1%)',
      badgeColor: '#8D6E63',
      badgeBg: '#FFF8E1',
      desc: 'Tài sản trú ẩn an toàn hưởng lợi từ bất ổn địa chính trị Trung Đông và vận tải biển.',
      topArticles: [
        {
          title: '1. Kitco (11/10): Nhu cầu vàng thỏi lập kỷ lục mới toàn cầu',
          meta: 'Độ tin cậy: 97% • Trọng số tác động: 0.91'
        }
      ]
    },
    fdi: {
      name: 'FDI BÁN DẪN & AI ($1.8B)',
      badge: 'TÍCH CỰC (+14%)',
      badgeColor: '#305A78',
      badgeBg: '#EAF1F7',
      desc: 'Dòng vốn chuyển dịch công nghệ cao từ Đạo luật Chips và hợp tác đối tác chiến lược toàn diện.',
      topArticles: [
        {
          title: '1. VTV (10/10): 3 tập đoàn bán dẫn cam kết mở rộng nhà máy tại VN',
          meta: 'Độ tin cậy: 98% • Trọng số tác động: 0.88'
        }
      ]
    }
  };

  const currentDetails = entityDetails[selectedEntity] || entityDetails.usdvnd;

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
            KHO TRI THỨC & THỜI GIAN
          </div>

          {/* Time horizons */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{ padding: '6px 10px', borderRadius: '6px', backgroundColor: '#F4F1EA', color: '#5A6B5C', fontSize: '11.5px' }}>
              ○ 24 Giờ Qua (42 tin)
            </div>
            <div style={{ padding: '6px 10px', borderRadius: '6px', backgroundColor: '#F4F1EA', color: '#5A6B5C', fontSize: '11.5px' }}>
              ○ 7 Ngày Qua (186 tin)
            </div>
            <div style={{ padding: '6px 10px', borderRadius: '6px', backgroundColor: '#2D4A2B', color: '#F4F1EA', fontSize: '11.5px', fontWeight: 700 }}>
              ● 30 Ngày Qua (TTL - 520 tin)
            </div>
            <div style={{ padding: '6px 10px', borderRadius: '6px', backgroundColor: '#FFF8E1', color: '#8D6E63', fontSize: '11.5px', fontWeight: 700, border: '1px solid #E5B869' }}>
              ★ Tech Vault (48 Đã Ghim)
            </div>
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* Entity Filters */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
              BỘ LỌC THỰC THỂ
            </div>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11.5px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Chính sách tiền tệ (FED, SBV)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11.5px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Chỉ số thị trường (VN-Index)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11.5px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Hàng hóa (Vàng SJC, Dầu)</span>
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11.5px', color: '#2D4A2B' }}>
              <input type="checkbox" defaultChecked />
              <span>Công nghệ & Bán dẫn (AI)</span>
            </label>
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* Search entity */}
          <div style={{ display: 'flex', alignItems: 'center', backgroundColor: '#FFFFFF', border: '1px solid #DCD5C5', borderRadius: '6px', padding: '6px 8px', gap: '6px' }}>
            <span>🔍</span>
            <input
              type="text"
              value={searchEntity}
              onChange={e => setSearchEntity(e.target.value)}
              placeholder="Tìm thực thể vĩ mô..."
              style={{ border: 'none', outline: 'none', width: '100%', fontSize: '11.5px', color: '#2D4A2B' }}
            />
          </div>
        </div>

        <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', color: '#8D6E63', lineHeight: '1.4' }}>
          Recursive CTE Engine<br />
          Organic Branch-Spine
        </div>
      </aside>

      {/* 2. MIDDLE BOTANICAL KNOWLEDGE GRAPH (1060px or flex-1) */}
      <section
        style={{
          flex: 1,
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '20px 24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)',
          overflowY: 'auto'
        }}
      >
        {/* Header & Legends */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #E8E2D5', paddingBottom: '10px' }}>
          <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: '15px', fontWeight: 700, color: '#2D4A2B' }}>
            CÂY TRI THỨC VĨ MÔ (ORGANIC BRANCH-SPINE) • LIÊN KẾT NHÂN QUẢ
          </h1>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', padding: '2px 8px', borderRadius: '4px', fontSize: '10px', fontWeight: 600 }}>
              ● Ổn định
            </span>
            <span style={{ backgroundColor: '#FDF2EE', color: '#C86D51', padding: '2px 8px', borderRadius: '4px', fontSize: '10px', fontWeight: 600 }}>
              ● Rủi ro biến động
            </span>
            <span style={{ backgroundColor: '#FFF8E1', color: '#E5B869', padding: '2px 8px', borderRadius: '4px', fontSize: '10px', fontWeight: 600 }}>
              ● Theo dõi
            </span>
          </div>
        </div>

        {/* Interactive Organic Botanical Graph Canvas */}
        <div
          style={{
            backgroundColor: '#FBF9F5',
            borderRadius: '10px',
            border: '1px solid #E8E2D5',
            padding: '24px 20px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '16px'
          }}
        >
          {/* ROOT TRUNK NODE: FED LÃI SUẤT */}
          <div
            onClick={() => {
              playSfx('click');
              setSelectedEntity('fed');
            }}
            style={{
              backgroundColor: selectedEntity === 'fed' ? '#1B3819' : '#2D4A2B',
              color: '#F4F1EA',
              borderRadius: '10px',
              padding: '12px 28px',
              textAlign: 'center',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(45, 74, 43, 0.18)',
              border: selectedEntity === 'fed' ? '2px solid #E5B869' : 'none',
              transform: selectedEntity === 'fed' ? 'scale(1.03)' : 'scale(1)',
              transition: 'all 0.2s ease'
            }}
          >
            <div style={{ fontSize: '13.5px', fontWeight: 700 }}>
              🏛️ FED LÃI SUẤT ĐIỀU HÀNH (5.25%)
            </div>
            <div style={{ fontSize: '10.5px', color: '#A8B6A8', marginTop: '2px', fontFamily: 'var(--font-mono)' }}>
              TRỤC RỄ NGUYÊN NHÂN TRUNG TÂM
            </div>
          </div>

          {/* Central Vertical Spine */}
          <div style={{ width: '2px', height: '24px', backgroundColor: '#B0A898' }} />

          {/* BRANCH ROW 1: Currency & Equity */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', width: '100%', justifyContent: 'center' }}>
            <div
              style={{
                backgroundColor: '#E8F0E8',
                color: '#1B5E20',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                border: '1px solid #C8E6C9'
              }}
            >
              💵 USD Index (DXY: 102.4)
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              onClick={() => {
                playSfx('click');
                setSelectedEntity('usdvnd');
              }}
              style={{
                backgroundColor: selectedEntity === 'usdvnd' ? '#2D4A2B' : '#E8F5E9',
                color: selectedEntity === 'usdvnd' ? '#F4F1EA' : '#1B5E20',
                borderRadius: '8px',
                padding: '8px 16px',
                fontSize: '12px',
                fontWeight: 700,
                cursor: 'pointer',
                border: selectedEntity === 'usdvnd' ? '2px solid #E5B869' : '1px solid #A5D6A7',
                transform: selectedEntity === 'usdvnd' ? 'scale(1.03)' : 'scale(1)',
                transition: 'all 0.2s ease'
              }}
            >
              🌿 TỶ GIÁ USD/VND (25.120) [ACTIVE]
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              onClick={() => {
                playSfx('click');
                setSelectedEntity('vnindex');
              }}
              style={{
                backgroundColor: selectedEntity === 'vnindex' ? '#2D4A2B' : '#E8F0E8',
                color: selectedEntity === 'vnindex' ? '#F4F1EA' : '#1B5E20',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                cursor: 'pointer',
                border: selectedEntity === 'vnindex' ? '2px solid #E5B869' : '1px solid #C8E6C9',
                transform: selectedEntity === 'vnindex' ? 'scale(1.03)' : 'scale(1)',
                transition: 'all 0.2s ease'
              }}
            >
              📈 VN-INDEX (1,280 ĐIỂM)
            </div>
          </div>

          {/* Central Vertical Spine */}
          <div style={{ width: '2px', height: '24px', backgroundColor: '#B0A898' }} />

          {/* BRANCH ROW 2: Inflation & Commodities */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', width: '100%', justifyContent: 'center' }}>
            <div
              style={{
                backgroundColor: '#FDF2EE',
                color: '#C86D51',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                border: '1px solid #F5C6BA'
              }}
            >
              📊 Lạm Phát CPI Mỹ (2.5%)
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              onClick={() => {
                playSfx('click');
                setSelectedEntity('sjc');
              }}
              style={{
                backgroundColor: selectedEntity === 'sjc' ? '#8D6E63' : '#FFF8E1',
                color: selectedEntity === 'sjc' ? '#FFFFFF' : '#8D6E63',
                borderRadius: '8px',
                padding: '8px 16px',
                fontSize: '12px',
                fontWeight: 700,
                cursor: 'pointer',
                border: selectedEntity === 'sjc' ? '2px solid #E5B869' : '1px solid #FFE082',
                transform: selectedEntity === 'sjc' ? 'scale(1.03)' : 'scale(1)',
                transition: 'all 0.2s ease'
              }}
            >
              🪙 Vàng SJC (88.5 tr/lượng)
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              style={{
                backgroundColor: '#FDF2EE',
                color: '#C86D51',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                border: '1px solid #F5C6BA'
              }}
            >
              🛢️ Dầu Thô Brent ($78/thùng)
            </div>
          </div>

          {/* Central Vertical Spine */}
          <div style={{ width: '2px', height: '24px', backgroundColor: '#B0A898' }} />

          {/* BRANCH ROW 3: Tech & FDI */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', width: '100%', justifyContent: 'center' }}>
            <div
              style={{
                backgroundColor: '#EAF1F7',
                color: '#4A6B82',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                border: '1px solid #BCD0DF'
              }}
            >
              ⚡ Đạo Luật Chips Hoa Kỳ
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              onClick={() => {
                playSfx('click');
                setSelectedEntity('fdi');
              }}
              style={{
                backgroundColor: selectedEntity === 'fdi' ? '#2D4A2B' : '#E8F0E8',
                color: selectedEntity === 'fdi' ? '#F4F1EA' : '#1B5E20',
                borderRadius: '8px',
                padding: '8px 16px',
                fontSize: '12px',
                fontWeight: 700,
                cursor: 'pointer',
                border: selectedEntity === 'fdi' ? '2px solid #E5B869' : '1px solid #A5D6A7',
                transform: selectedEntity === 'fdi' ? 'scale(1.03)' : 'scale(1)',
                transition: 'all 0.2s ease'
              }}
            >
              🏭 FDI Bán Dẫn VN ($1.8B)
            </div>

            <span style={{ color: '#B0A898', fontFamily: 'var(--font-mono)' }}>────────►</span>

            <div
              style={{
                backgroundColor: '#EAF1F7',
                color: '#4A6B82',
                borderRadius: '8px',
                padding: '8px 14px',
                fontSize: '11.5px',
                fontWeight: 600,
                border: '1px solid #BCD0DF'
              }}
            >
              🤖 AI System 1 Cục Bộ (Decision 3 Lite)
            </div>
          </div>
        </div>
      </section>

      {/* 3. RIGHT ENTITY INSPECTOR (420px) */}
      <aside
        style={{
          width: '420px',
          flexShrink: 0,
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >
        {/* Detail Box */}
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            border: '1px solid #DCD5C5',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
            boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
              THỰC THỂ: {currentDetails.name}
            </span>
            <span
              style={{
                backgroundColor: currentDetails.badgeBg,
                color: currentDetails.badgeColor,
                borderRadius: '999px',
                padding: '3px 8px',
                fontSize: '10px',
                fontFamily: 'var(--font-mono)',
                fontWeight: 700
              }}
            >
              {currentDetails.badge}
            </span>
          </div>

          <div style={{ fontSize: '12px', color: '#5A6B5C', lineHeight: '1.5' }}>
            {currentDetails.desc}
          </div>

          <div style={{ height: '1px', backgroundColor: '#EBE6DC' }} />

          <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#2D4A2B' }}>
            BÀI BÁO LIÊN QUAN TRỰC TIẾP (TOP 3):
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {currentDetails.topArticles.map((art, idx) => (
              <div
                key={idx}
                style={{
                  backgroundColor: '#FBF9F5',
                  borderRadius: '6px',
                  padding: '8px 10px',
                  border: '1px solid #E8E2D5',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }}
              >
                <div style={{ fontSize: '11.5px', fontWeight: 600, color: '#2D4A2B' }}>
                  {art.title}
                </div>
                <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#5A6B5C' }}>
                  {art.meta}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Actions Box */}
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            border: '1px solid #DCD5C5',
            padding: '14px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
          }}
        >
          <button
            onClick={() => {
              playSfx('click');
              setIsBookmarked(!isBookmarked);
            }}
            style={{
              backgroundColor: isBookmarked ? '#FFF8E1' : '#2D4A2B',
              border: isBookmarked ? '1px solid #E5B869' : 'none',
              color: isBookmarked ? '#8D6E63' : '#F4F1EA',
              borderRadius: '8px',
              padding: '9px 12px',
              fontSize: '11.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>{isBookmarked ? '★' : '☆'}</span>
            <span>{isBookmarked ? 'Đã Ghim Vào Tech Vault (Bảo Vệ Khỏi TTL)' : 'Ghim Vào Tech Vault'}</span>
          </button>

          <button
            onClick={() => alert(`Đang truy vấn đồ thị quan hệ cấp 2 cho thực thể: ${currentDetails.name}...`)}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #DCD5C5',
              color: '#2D4A2B',
              borderRadius: '8px',
              padding: '8px 12px',
              fontSize: '11.5px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>🔗</span>
            <span>Khám Phá Mạng Lưới Quan Hệ Cấp 2</span>
          </button>

          <button
            onClick={() => onNavigate('analytics')}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #DCD5C5',
              color: '#2D4A2B',
              borderRadius: '8px',
              padding: '8px 12px',
              fontSize: '11.5px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>📊</span>
            <span>Xem Ma Trận Nhiệt Từ Khóa (Screen 7) →</span>
          </button>
        </div>
      </aside>
    </div>
  );
};
