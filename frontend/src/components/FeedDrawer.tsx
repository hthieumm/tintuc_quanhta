import React, { useState, useEffect } from 'react';
import { apiFetch } from '../utils/api';
import { playSfx } from '../utils/audio';

export interface SourceItem {
  id: number;
  name: string;
  url: string;
  category: string;
  source_type: string;
  is_active: number;
  fetch_interval_min: number;
  last_fetched_at: string | null;
  created_at: string;
  article_count?: number;
}

interface FeedDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenAddFeed?: () => void;
}

const CATEGORY_META: Record<string, { label: string; color: string; bg: string }> = {
  kinh_te: { label: 'Vĩ Mô', color: '#166534', bg: '#DCFCE7' },
  chung_khoan: { label: 'Chứng Khoán', color: '#1E40AF', bg: '#DBEAFE' },
  vang: { label: 'Vàng & Tỷ Giá', color: '#92400E', bg: '#FEF3C7' },
  crypto: { label: 'Crypto', color: '#C2410C', bg: '#FFEDD5' },
  quoc_te: { label: 'Quốc Tế', color: '#991B1B', bg: '#FEE2E2' },
  chinh_tri: { label: 'Chính Trị', color: '#6B21A8', bg: '#F3E8FF' },
  github: { label: 'Tech AI', color: '#0F766E', bg: '#CCFBF1' }
};

export const FeedDrawer: React.FC<FeedDrawerProps> = ({ isOpen, onClose, onOpenAddFeed }) => {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const loadSources = async () => {
    setIsLoading(true);
    try {
      const res = await apiFetch('/api/v1/sources');
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data)) {
          setSources(data);
        }
      }
    } catch (e) {
      console.error('Lỗi nạp nguồn tin từ SQLite:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadSources();
      setStatusMsg(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleToggle = async (id: number, currentActive: number) => {
    playSfx('click');
    // Optimistic UI update
    setSources(prev =>
      prev.map(s => (s.id === id ? { ...s, is_active: currentActive === 1 ? 0 : 1 } : s))
    );

    try {
      const res = await apiFetch(`/api/v1/sources/${id}/toggle`, { method: 'PATCH' });
      if (!res.ok) {
        // Rollback if failed
        loadSources();
      } else {
        const json = await res.json();
        setStatusMsg(`Đã ${json.is_active === 1 ? 'kích hoạt' : 'tạm dừng'} nguồn tin.`);
        setTimeout(() => setStatusMsg(null), 2500);
      }
    } catch {
      loadSources();
    }
  };

  const handleDelete = async (id: number, name: string) => {
    playSfx('paper_rustle');
    if (!confirm(`Bạn có chắc chắn muốn xóa nguồn "${name}" khỏi cơ sở dữ liệu SQLite?`)) {
      return;
    }

    setSources(prev => prev.filter(s => s.id !== id));
    try {
      const res = await apiFetch(`/api/v1/sources/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setStatusMsg(`Đã xóa nguồn "${name}" khỏi database.`);
        setTimeout(() => setStatusMsg(null), 2500);
      } else {
        loadSources();
      }
    } catch {
      loadSources();
    }
  };

  const filteredSources = sources.filter(s => {
    const matchesCat = filterCategory === 'all' || s.category === filterCategory;
    const matchesQuery = !searchQuery.trim() ||
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.url.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesQuery;
  });

  const activeCount = sources.filter(s => s.is_active === 1).length;
  const totalArticles = sources.reduce((acc, s) => acc + (s.article_count || 0), 0);

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.45)',
        backdropFilter: 'blur(3px)',
        zIndex: 200,
        display: 'flex',
        justifyContent: 'flex-start'
      }}
    >
      {/* Slide-over Drawer Pane */}
      <div
        style={{
          width: '420px',
          maxWidth: '90vw',
          backgroundColor: '#FAF8F5',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '4px 0 24px rgba(0, 0, 0, 0.2)',
          borderRight: '1px solid #DCD5C5',
          animation: 'slideInLeft 0.22s ease-out'
        }}
      >
        {/* Drawer Header */}
        <div
          style={{
            padding: '18px 20px',
            backgroundColor: '#FFFFFF',
            borderBottom: '1px solid #E8E2D5',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '18px' }}>📡</span>
              <div>
                <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#1B5E20', margin: 0 }}>
                  Quản Lý Nguồn Tin (Feeds)
                </h3>
                <span style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', color: '#78716C' }}>
                  Đồng bộ trực tiếp SQLite Database ({sources.length} Nguồn)
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              style={{
                background: '#F4F1EA',
                border: 'none',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                fontSize: '13px',
                cursor: 'pointer',
                color: '#5F7D58',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              title="Đóng (Esc)"
            >
              ✕
            </button>
          </div>

          {/* Quick Stats Pills */}
          <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
            <div
              style={{
                flex: 1,
                padding: '5px 10px',
                borderRadius: '6px',
                backgroundColor: '#E8F5E9',
                border: '1px solid #C8E6C9',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '11px',
                color: '#1B5E20'
              }}
            >
              <span>Đang quét:</span>
              <strong style={{ fontFamily: 'var(--font-mono)' }}>{activeCount}/{sources.length}</strong>
            </div>
            <div
              style={{
                flex: 1,
                padding: '5px 10px',
                borderRadius: '6px',
                backgroundColor: '#F5F5F4',
                border: '1px solid #E7E5E4',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '11px',
                color: '#44403C'
              }}
            >
              <span>Tổng bài:</span>
              <strong style={{ fontFamily: 'var(--font-mono)' }}>{totalArticles} bài</strong>
            </div>
          </div>
        </div>

        {/* Action Controls & Search Bar */}
        <div
          style={{
            padding: '12px 18px',
            backgroundColor: '#F4F1EA',
            borderBottom: '1px solid #E8E2D5',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
        >
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="🔍 Tìm theo tên hoặc URL nguồn..."
              style={{
                flex: 1,
                padding: '6px 10px',
                borderRadius: '6px',
                border: '1px solid #DCD5C5',
                fontSize: '11.5px',
                backgroundColor: '#FFFFFF',
                outline: 'none'
              }}
            />
            {onOpenAddFeed && (
              <button
                onClick={() => {
                  playSfx('click');
                  onOpenAddFeed();
                }}
                style={{
                  backgroundColor: '#1B5E20',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '6px 12px',
                  fontSize: '11.5px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  whiteSpace: 'nowrap'
                }}
              >
                <span>+ Thêm Nguồn</span>
              </button>
            )}
            <button
              onClick={loadSources}
              title="Làm mới danh sách"
              style={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #DCD5C5',
                borderRadius: '6px',
                padding: '6px 10px',
                fontSize: '12px',
                cursor: 'pointer',
                color: '#5F7D58'
              }}
            >
              🔄
            </button>
          </div>

          {/* Category Filter Scroll */}
          <div style={{ display: 'flex', gap: '5px', overflowX: 'auto', paddingBottom: '2px' }}>
            {[
              { id: 'all', label: 'Tất Cả' },
              { id: 'kinh_te', label: 'Vĩ Mô' },
              { id: 'chung_khoan', label: 'Chứng Khoán' },
              { id: 'vang', label: 'Vàng & FX' },
              { id: 'crypto', label: 'Crypto' },
              { id: 'quoc_te', label: 'Quốc Tế' },
              { id: 'chinh_tri', label: 'Chính Trị' }
            ].map(cat => {
              const isSelected = filterCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => setFilterCategory(cat.id)}
                  style={{
                    backgroundColor: isSelected ? '#2D4A2B' : '#FFFFFF',
                    color: isSelected ? '#FAF8F5' : '#5F7D58',
                    border: '1px solid',
                    borderColor: isSelected ? '#2D4A2B' : '#DCD5C5',
                    borderRadius: '12px',
                    padding: '2px 8px',
                    fontSize: '10px',
                    fontWeight: isSelected ? 700 : 500,
                    cursor: 'pointer',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {cat.label}
                </button>
              );
            })}
          </div>

          {statusMsg && (
            <div style={{ fontSize: '11px', color: '#1B5E20', fontWeight: 600, padding: '2px 0' }}>
              ✓ {statusMsg}
            </div>
          )}
        </div>

        {/* Sources List Pane */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '14px 18px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
        >
          {isLoading && sources.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 0', fontSize: '12px', color: '#78716C' }}>
              ⏳ Đang nạp danh sách nguồn tin từ SQLite...
            </div>
          ) : filteredSources.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 0', fontSize: '12px', color: '#78716C' }}>
              Không tìm thấy nguồn tin nào phù hợp.
            </div>
          ) : (
            filteredSources.map(s => {
              const catMeta = CATEGORY_META[s.category] || { label: s.category, color: '#57534E', bg: '#F5F5F4' };
              const isActive = s.is_active === 1;

              return (
                <div
                  key={s.id}
                  style={{
                    backgroundColor: '#FFFFFF',
                    border: isActive ? '1px solid #DCD5C5' : '1px dashed #D6D3D1',
                    borderRadius: '8px',
                    padding: '10px 12px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    opacity: isActive ? 1 : 0.65,
                    transition: 'all 0.15s ease',
                    boxShadow: isActive ? '0 1px 3px rgba(0,0,0,0.03)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', maxWidth: '240px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span style={{ fontSize: '12.5px', fontWeight: 700, color: '#1A2E19' }}>
                          {s.name}
                        </span>
                        <span
                          style={{
                            fontSize: '9px',
                            fontFamily: 'var(--font-mono)',
                            color: catMeta.color,
                            backgroundColor: catMeta.bg,
                            padding: '1px 5px',
                            borderRadius: '4px',
                            fontWeight: 600
                          }}
                        >
                          {catMeta.label}
                        </span>
                      </div>
                      <span
                        title={s.url}
                        style={{
                          fontSize: '10px',
                          fontFamily: 'var(--font-mono)',
                          color: '#A8A29E',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {s.url.replace(/^https?:\/\//, '')}
                      </span>
                    </div>

                    {/* Toggle Button */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <button
                        onClick={() => handleToggle(s.id, s.is_active)}
                        style={{
                          fontSize: '9.5px',
                          fontFamily: 'var(--font-mono)',
                          fontWeight: 700,
                          backgroundColor: isActive ? '#DCFCE7' : '#F5F5F4',
                          color: isActive ? '#166534' : '#78716C',
                          border: isActive ? '1px solid #86EFAC' : '1px solid #D6D3D1',
                          padding: '3px 8px',
                          borderRadius: '12px',
                          cursor: 'pointer'
                        }}
                      >
                        {isActive ? '● ACTIVE' : '○ PAUSED'}
                      </button>
                      <button
                        onClick={() => handleDelete(s.id, s.name)}
                        title="Xóa nguồn này"
                        style={{
                          background: 'none',
                          border: 'none',
                          color: '#EF4444',
                          cursor: 'pointer',
                          fontSize: '12px',
                          padding: '2px 4px'
                        }}
                      >
                        🗑️
                      </button>
                    </div>
                  </div>

                  {/* Footer metadata */}
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontSize: '10px',
                      fontFamily: 'var(--font-mono)',
                      color: '#78716C',
                      borderTop: '1px solid #F5F5F4',
                      paddingTop: '4px'
                    }}
                  >
                    <span>📊 <strong>{s.article_count ?? 0}</strong> bài trong SQLite</span>
                    <span>🕒 {s.last_fetched_at ? s.last_fetched_at.split('T')[0] : 'Đang chờ quét'}</span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Drawer Footer */}
        <div
          style={{
            padding: '12px 18px',
            backgroundColor: '#FFFFFF',
            borderTop: '1px solid #E8E2D5',
            fontSize: '11px',
            color: '#78716C',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span>Đường dẫn DB: <code>backend/data/spider_radar.db</code></span>
          <button
            onClick={onClose}
            style={{
              backgroundColor: '#F4F1EA',
              border: '1px solid #DCD5C5',
              borderRadius: '6px',
              padding: '4px 12px',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              color: '#2D4A2B'
            }}
          >
            Đóng
          </button>
        </div>
      </div>

      {/* Backdrop clickable zone */}
      <div style={{ flex: 1 }} onClick={onClose} />
    </div>
  );
};
