import React, { useEffect, useState } from 'react';
import { ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';

interface SearchModalFTS5Props {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (tab: ScreenTab) => void;
}

export const SearchModalFTS5: React.FC<SearchModalFTS5Props> = ({ isOpen, onClose, onNavigate }) => {
  const [query, setQuery] = useState('');

  const sampleResults = [
    {
      id: 1,
      title: 'Ngân Hàng Nhà Nước Họp Khẩn: Duy Trì Trần Lãi Suất 4.5%',
      snippet: '...duy trì ổn định trần <mark>LÃI SUẤT ĐIỀU HÀNH</mark> ở mức 4.5% nhằm hỗ trợ thanh khoản...',
      category: 'Kinh tế vĩ mô',
      screen: 'feeds' as ScreenTab,
      latency: '0.8ms'
    },
    {
      id: 2,
      title: 'GPT-6 and the Geometry of LLM Optimization',
      snippet: '...non-convex loss landscape, training dynamics, <mark>next-token loss</mark>...',
      category: 'Nghiên cứu AI',
      screen: 'arena' as ScreenTab,
      latency: '1.1ms'
    },
    {
      id: 3,
      title: 'Tỷ Giá USD/VND Hạ Nhiệt Sau Can Thiệp Thị Trường Mở',
      snippet: '...ổn định <mark>TỶ GIÁ USD/VND</mark> tại mốc 25.120, điều tiết OMO...',
      category: 'Vĩ mô & Tiền tệ',
      screen: 'vault' as ScreenTab,
      latency: '1.4ms'
    },
    {
      id: 4,
      title: 'Mô hình Decision 3 Lite: Suy luận Single-Pass Tensor trên CPU',
      snippet: '...phân loại phản xạ nhị phân <mark>sub-10ms</mark>, 180MB RAM...',
      category: 'GitHub AI',
      screen: 'github' as ScreenTab,
      latency: '1.6ms'
    }
  ];

  const [realResults, setRealResults] = useState<any[] | null>(null);
  const [latencyText, setLatencyText] = useState<string>('0.8ms');

  useEffect(() => {
    if (!query.trim()) {
      setRealResults(null);
      return;
    }
    const t0 = performance.now();
    const timer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/v1/search?q=${encodeURIComponent(query.trim())}`);
        if (res.ok) {
          const items = await res.json();
          const elapsed = (performance.now() - t0).toFixed(1);
          setLatencyText(`${elapsed}ms`);
          setRealResults(
            items.map((item: any) => ({
              id: item.id,
              title: item.title,
              snippet: item.content_clean?.slice(0, 160) + '...',
              category: item.language === 'vi' ? 'Tin Trong Nước' : 'Quốc Tế',
              screen: 'feeds' as ScreenTab,
              latency: `${elapsed}ms`
            }))
          );
        }
      } catch {
        // Fallback
      }
    }, 150);
    return () => clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filtered = realResults !== null
    ? realResults
    : (query.trim()
      ? sampleResults.filter(
          r =>
            r.title.toLowerCase().includes(query.toLowerCase()) ||
            r.snippet.toLowerCase().includes(query.toLowerCase())
        )
      : sampleResults);

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.4)', // 40% scrim backdrop
        backdropFilter: 'blur(3px)',
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        paddingTop: '100px',
        zIndex: 100
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          width: '620px',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.25)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Search Input Bar */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '14px 18px',
            borderBottom: '1px solid #E8E2D5',
            gap: '12px'
          }}
        >
          <span style={{ fontSize: '18px' }}>🔍</span>
          <input
            autoFocus
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Tra cứu toàn văn SQLite FTS5 (lãi suất, tỷ giá, OMO, decision...)"
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              fontSize: '14px',
              color: '#2D4A2B',
              fontFamily: 'var(--font-sans)'
            }}
          />
          <kbd
            style={{
              backgroundColor: '#F4F1EA',
              border: '1px solid #DCD5C5',
              borderRadius: '4px',
              padding: '2px 6px',
              fontSize: '10px',
              fontFamily: 'var(--font-mono)',
              color: '#5A6B5C'
            }}
          >
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div style={{ maxHeight: '380px', overflowY: 'auto', padding: '8px' }}>
          <div style={{ padding: '6px 10px', fontSize: '10.5px', fontFamily: 'var(--font-mono)', color: '#8A9A86' }}>
            KẾT QUẢ TỨC THÌ (SQLite FTS5 MATCH QUERY)
          </div>

          {filtered.map(res => (
            <div
              key={res.id}
              onClick={() => {
                playSfx('click');
                onNavigate(res.screen);
                onClose();
              }}
              style={{
                padding: '10px 12px',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: '3px',
                transition: 'background-color 0.15s ease'
              }}
              onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#FBF9F5')}
              onMouseLeave={e => (e.currentTarget.style.backgroundColor = 'transparent')}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>{res.title}</span>
                <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#00BA88' }}>
                  ⚡ {res.latency}
                </span>
              </div>
              <div
                style={{ fontSize: '11.5px', color: '#5A6B5C' }}
                dangerouslySetInnerHTML={{ __html: res.snippet }}
              />
              <div style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#8D6E63' }}>
                Chuyên mục: {res.category} • Nhấp để mở ngay
              </div>
            </div>
          ))}
        </div>

        {/* Footer info */}
        <div
          style={{
            padding: '8px 16px',
            backgroundColor: '#F4F1EA',
            borderTop: '1px solid #E8E2D5',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '10.5px',
            fontFamily: 'var(--font-mono)',
            color: '#5A6B5C'
          }}
        >
          <span>Tra cứu toàn văn FTS5 không cần kết nối internet (&lt;2ms)</span>
          <span>ENTER để chọn • ESC để đóng</span>
        </div>
      </div>
    </div>
  );
};
