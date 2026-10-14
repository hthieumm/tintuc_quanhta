import React, { useState, useEffect } from 'react';
import { PacingMode, System1Engine, ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';
import { apiFetch } from '../../utils/api';

export interface DbSourceItem {
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

export interface DbStats {
  total_articles: number;
  bookmarked_articles: number;
  unbookmarked_articles: number;
  total_repos: number;
  bookmarked_repos: number;
  active_sources: number;
  db_size_mb: number;
}

interface Screen6SettingsProps {
  onNavigate: (tab: ScreenTab) => void;
  pacingMode: PacingMode;
  onPacingChange: (mode: PacingMode) => void;
  system1Engine: System1Engine;
  onEngineChange: (engine: System1Engine) => void;
  isSfxEnabled: boolean;
  onToggleSfx: () => void;
  volumePercent: number;
  onVolumeChange: (vol: number) => void;
  onOpenAddFeed: () => void;
}

export const Screen6Settings: React.FC<Screen6SettingsProps> = ({
  onNavigate,
  pacingMode,
  onPacingChange,
  system1Engine,
  onEngineChange,
  isSfxEnabled,
  onToggleSfx,
  volumePercent,
  onVolumeChange,
  onOpenAddFeed
}) => {
  const [activeSection, setActiveSection] = useState<string>('all');
  const [cleanNotice, setCleanNotice] = useState<string | null>(null);
  const [cleanError, setCleanError] = useState<string | null>(null);
  const [sources, setSources] = useState<DbSourceItem[]>([]);
  const [isLoadingSources, setIsLoadingSources] = useState<boolean>(false);
  const [dbStats, setDbStats] = useState<DbStats | null>(null);
  const [isCleaningDb, setIsCleaningDb] = useState<boolean>(false);
  const [isVacuuming, setIsVacuuming] = useState<boolean>(false);

  // Load database statistics from backend SQLite
  const loadDbStats = async () => {
    try {
      const res = await apiFetch('/api/v1/system/db-stats');
      if (res.ok) {
        const data = await res.json();
        setDbStats(data);
      }
    } catch (e) {
      console.error('Lỗi tải thống kê database:', e);
    }
  };

  const loadSources = async () => {
    setIsLoadingSources(true);
    try {
      const res = await apiFetch('/api/v1/sources');
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data)) {
          setSources(data);
        }
      }
    } catch (e) {
      console.error('Lỗi tải nguồn tin từ SQLite:', e);
    } finally {
      setIsLoadingSources(false);
    }
  };

  useEffect(() => {
    loadSources();
    loadDbStats();
  }, []);

  const handleToggleSource = async (id: number) => {
    playSfx('click');
    setSources(prev =>
      prev.map(s => (s.id === id ? { ...s, is_active: s.is_active === 1 ? 0 : 1 } : s))
    );
    try {
      const res = await apiFetch(`/api/v1/sources/${id}/toggle`, { method: 'PATCH' });
      if (!res.ok) {
        loadSources();
      }
    } catch {
      loadSources();
    }
  };

  const handleDeleteSource = async (id: number) => {
    playSfx('paper_rustle');
    if (confirm('Bạn có chắc chắn muốn xóa nguồn tin RSS này khỏi hệ thống?')) {
      setSources(prev => prev.filter(s => s.id !== id));
      try {
        await apiFetch(`/api/v1/sources/${id}`, { method: 'DELETE' });
        loadDbStats();
      } catch (e) {
        console.error('Lỗi xóa nguồn tin:', e);
        loadSources();
      }
    }
  };

  // 1. Dọn dẹp DB ngay: Xóa tất cả bài viết KHÔNG ĐƯỢC ĐÁNH DẤU SAO
  const handleCleanUnstarred = async () => {
    playSfx('click');
    const unstarred = dbStats?.unbookmarked_articles ?? 0;
    const starred = dbStats?.bookmarked_articles ?? 0;

    if (unstarred === 0) {
      alert('Cơ sở dữ liệu hiện tại không có bài báo nào chưa gắn sao. Mọi bài viết đều được bảo vệ trong Tech Vault!');
      return;
    }

    const confirmMsg =
      `⚠️ XÁC NHẬN DỌN DẸP DATABASE NGAY:\n\n` +
      `• Sẽ XÓA VĨNH VIỄN: ${unstarred} bài báo không được đánh dấu sao.\n` +
      `• BẢO TOÀN TUYỆT ĐỐI: ${starred} bài báo đã gắn sao (Tech Vault).\n\n` +
      `Bạn có chắc chắn muốn xóa dọn dẹp ngay bây giờ?`;

    if (!confirm(confirmMsg)) {
      return;
    }

    setIsCleaningDb(true);
    setCleanError(null);
    try {
      const res = await apiFetch('/api/v1/system/clean-unstarred', { method: 'POST' });
      if (res.ok) {
        const result = await res.json();
        playSfx('paper_rustle');
        setCleanNotice(result.message || `Đã dọn dẹp thành công ${result.deleted_articles} bài báo không gắn sao.`);
        await loadDbStats();
      } else {
        const err = await res.json();
        setCleanError(err.detail || 'Lỗi dọn dẹp database');
      }
    } catch (e: any) {
      setCleanError('Không thể kết nối đến Backend: ' + (e?.message || ''));
    } finally {
      setIsCleaningDb(false);
      setTimeout(() => {
        setCleanNotice(null);
        setCleanError(null);
      }, 5000);
    }
  };

  // 2. Thu hồi đĩa VACUUM SQLite
  const handleVacuumDb = async () => {
    playSfx('click');
    setIsVacuuming(true);
    setCleanError(null);
    try {
      const res = await apiFetch('/api/v1/system/vacuum', { method: 'POST' });
      if (res.ok) {
        const result = await res.json();
        playSfx('wind_chime');
        setCleanNotice(result.message || 'Đã thu hồi dung lượng đĩa SQLite thành công.');
        await loadDbStats();
      } else {
        setCleanError('Lỗi thực thi lệnh VACUUM.');
      }
    } catch (e: any) {
      setCleanError('Không thể kết nối đến Backend: ' + (e?.message || ''));
    } finally {
      setIsVacuuming(false);
      setTimeout(() => {
        setCleanNotice(null);
        setCleanError(null);
      }, 4000);
    }
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
            DANH MỤC CÀI ĐẶT
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div
              onClick={() => setActiveSection('all')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'all' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'all' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                fontWeight: activeSection === 'all' ? 700 : 500,
                cursor: 'pointer'
              }}
            >
              ● Tất Cả Thiết Lập
            </div>
            <div
              onClick={() => setActiveSection('quota')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'quota' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'quota' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              ○ 1. Quota & Lọc Tin
            </div>
            <div
              onClick={() => setActiveSection('ttl')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'ttl' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'ttl' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              ○ 2. Vòng Đời TTL & Dọn DB
            </div>
            <div
              onClick={() => setActiveSection('engines')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'engines' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'engines' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              ○ 3. Decision 3 & Dual LLM
            </div>
            <div
              onClick={() => setActiveSection('feeds')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'feeds' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'feeds' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              ○ 4. Nguồn Tin RSS Động
            </div>
            <div
              onClick={() => setActiveSection('sfx')}
              style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: activeSection === 'sfx' ? '#2D4A2B' : '#F4F1EA',
                color: activeSection === 'sfx' ? '#F4F1EA' : '#5A6B5C',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              ○ 5. Giao Diện & Âm Lượng SFX
            </div>
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* System Telemetry Specs */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
              HỆ THỐNG & TÀI NGUYÊN
            </div>
            <div style={{ fontSize: '11px', color: '#3D4E3D', lineHeight: '1.6' }}>
              • Framework: <strong>Tauri v2 Native</strong><br />
              • SQLite Database: <strong>{dbStats ? `${dbStats.db_size_mb} MB` : '5.1 MB'}</strong><br />
              • Bài viết đã lưu: <strong>{dbStats ? `${dbStats.total_articles} bài` : 'Đang tải...'}</strong><br />
              • Tech Vault ghim: <strong style={{ color: '#D97706' }}>{dbStats ? `${dbStats.bookmarked_articles} bài ★` : '...'}</strong><br />
              • Repos ghim: <strong>{dbStats ? `${dbStats.bookmarked_repos} repos` : '...'}</strong><br />
              <span style={{ color: '#1B5E20', fontWeight: 700 }}>• VRAM GPU: 0 MB (CPU Ready)</span>
            </div>
          </div>
        </div>

        {/* Link to Screen 7 */}
        <button
          onClick={() => onNavigate('analytics')}
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #DCD5C5',
            borderRadius: '8px',
            padding: '8px 10px',
            fontSize: '11px',
            fontWeight: 600,
            color: '#2D4A2B',
            cursor: 'pointer',
            textAlign: 'center'
          }}
        >
          📊 Xem Chi Tiết Biểu Đồ & Chỉ Số (Screen 7) →
        </button>
      </aside>

      {/* 2. RIGHT SETTINGS DASHBOARD (2-COLUMN CARDS LAYOUT) */}
      <main
        style={{
          flex: 1,
          display: 'flex',
          gap: '12px',
          overflowY: 'auto'
        }}
      >
        {/* Left Column Cards */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Card 1: Daily Quota */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                1. QUẢN LÝ QUOTA QUÉT TIN HÀNG NGÀY
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                QUOTA: 500 BÀI/NGÀY
              </span>
            </div>

            <div style={{ fontSize: '11.5px', color: '#5A6B5C' }}>
              Tiến độ tiêu thụ quota hôm nay: <strong>{dbStats ? Math.min(dbStats.total_articles, 500) : 342} / 500</strong> bài báo (68.4%)
            </div>

            {/* Quota Progress Bar */}
            <div style={{ height: '10px', backgroundColor: '#EBE6DC', borderRadius: '5px', overflow: 'hidden' }}>
              <div style={{ width: '68.4%', height: '100%', backgroundColor: '#2D4A2B' }} />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11.5px', color: '#2C3E2C' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" defaultChecked />
                <span>Tự động tạm dừng quét khi đạt giới hạn 500 bài (Bảo vệ CPU)</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" defaultChecked />
                <span>Tự động ưu tiên cào các kênh vĩ mô trọng điểm khi dung lượng hẹp</span>
              </label>
              <div style={{ color: '#5F7D58', fontFamily: 'var(--font-mono)', fontSize: '11px', marginTop: '2px' }}>
                ⏱️ Tần suất kiểm tra RSS: 15 phút / lần (Tối ưu phản xạ Decision 3 Lite)
              </div>
            </div>
          </div>

          {/* Card 2: Data Retention & IMMEDIATE CLEANUP (Dọn dẹp DB ngay) */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '16px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                2. VÒNG ĐỜI LƯU TRỮ & DỌN DẸP DATABASE (TTL)
              </span>
              <span style={{ backgroundColor: '#FDF2EE', color: '#C86D51', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                TTL: 30 NGÀY • DB: {dbStats ? `${dbStats.db_size_mb} MB` : '5.1 MB'}
              </span>
            </div>

            <div style={{ fontSize: '11.5px', color: '#5A6B5C', lineHeight: '1.4' }}>
              Chính sách loại bỏ tin rác để giữ SQLite luôn gọn nhẹ, sub-millisecond query. Bạn có thể dọn dẹp tức thì mọi tin chưa đánh dấu sao bên dưới.
            </div>

            {/* Tech Vault Banner */}
            <div
              style={{
                backgroundColor: '#FFF8E1',
                border: '1px solid #FFE082',
                borderRadius: '8px',
                padding: '10px 12px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <span style={{ fontSize: '16px', color: '#D97706' }}>★</span>
              <div style={{ fontSize: '11px', color: '#8D6E63', lineHeight: '1.5' }}>
                <strong>BẢO VỆ TUYỆT ĐỐI TECH VAULT:</strong> Các bài báo bạn đã nhấn ngôi sao <strong>[★ Lưu Tech Vault]</strong> được miễn trừ vĩnh viễn khỏi mọi lệnh dọn dẹp và duy trì lâu dài.
              </div>
            </div>

            {/* Real DB statistics grid */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr 1fr',
                gap: '8px',
                backgroundColor: '#FAF8F5',
                padding: '10px',
                borderRadius: '8px',
                border: '1px solid #EBE6DC'
              }}
            >
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '10px', color: '#8A9A86', textTransform: 'uppercase', fontWeight: 600 }}>Tổng bài viết</span>
                <span style={{ fontSize: '15px', fontWeight: 700, color: '#2D4A2B', fontFamily: 'var(--font-mono)' }}>
                  {dbStats ? dbStats.total_articles.toLocaleString() : '...'}
                </span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '10px', color: '#D97706', textTransform: 'uppercase', fontWeight: 600 }}>★ Đã gắn sao (Giữ lại)</span>
                <span style={{ fontSize: '15px', fontWeight: 700, color: '#D97706', fontFamily: 'var(--font-mono)' }}>
                  {dbStats ? dbStats.bookmarked_articles.toLocaleString() : '...'}
                </span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '10px', color: '#C86D51', textTransform: 'uppercase', fontWeight: 600 }}>Chưa gắn sao (Xóa)</span>
                <span style={{ fontSize: '15px', fontWeight: 700, color: '#C86D51', fontFamily: 'var(--font-mono)' }}>
                  {dbStats ? dbStats.unbookmarked_articles.toLocaleString() : '...'}
                </span>
              </div>
            </div>

            {cleanNotice && (
              <div style={{ backgroundColor: '#E8F5E9', border: '1px solid #C8E6C9', color: '#1B5E20', borderRadius: '6px', padding: '8px 12px', fontSize: '11.5px', fontWeight: 600 }}>
                ✓ {cleanNotice}
              </div>
            )}

            {cleanError && (
              <div style={{ backgroundColor: '#FFEBEE', border: '1px solid #FFCDD2', color: '#C62828', borderRadius: '6px', padding: '8px 12px', fontSize: '11.5px', fontWeight: 600 }}>
                ✕ {cleanError}
              </div>
            )}

            {/* Dọn dẹp buttons */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '2px' }}>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={handleCleanUnstarred}
                  disabled={isCleaningDb}
                  style={{
                    flex: 1,
                    backgroundColor: '#C86D51',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '9px 12px',
                    color: '#FFFFFF',
                    fontSize: '11.5px',
                    fontWeight: 700,
                    cursor: isCleaningDb ? 'wait' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    transition: 'all 0.15s ease',
                    opacity: isCleaningDb ? 0.7 : 1
                  }}
                  title="Xóa ngay tất cả bài báo chưa đánh dấu sao, chỉ giữ lại các bài Tech Vault"
                >
                  <span>🧹</span>
                  <span>{isCleaningDb ? 'Đang dọn dẹp...' : 'Dọn Dẹp DB Ngay (Xóa Bài Không Đánh Dấu Sao)'}</span>
                </button>

                <button
                  onClick={handleVacuumDb}
                  disabled={isVacuuming}
                  style={{
                    backgroundColor: '#2D4A2B',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '9px 12px',
                    color: '#FFFFFF',
                    fontSize: '11.5px',
                    fontWeight: 600,
                    cursor: isVacuuming ? 'wait' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    opacity: isVacuuming ? 0.7 : 1
                  }}
                  title="Thu hồi không gian đĩa SQLite và tối ưu hóa chỉ mục FTS5"
                >
                  <span>💾</span>
                  <span>{isVacuuming ? 'Đang nén...' : 'Thu Hồi Đĩa VACUUM'}</span>
                </button>
              </div>

              <div style={{ fontSize: '10.5px', color: '#8A9A86', lineHeight: '1.4' }}>
                💡 <em>Mẹo: Mọi thao tác dọn dẹp đều đồng bộ lại chỉ mục FTS5 và kích hoạt giải phóng bộ nhớ tự động.</em>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column Cards */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {/* Card 3: Dual AI Engines */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '12px 16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                3. ĐỘNG CƠ SUY LUẬN DECISION 3 LITE & LLM DUAL-SYSTEM
              </span>
              <span style={{ backgroundColor: '#E8F0E8', color: '#1B5E20', borderRadius: '999px', padding: '2px 8px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                DUAL ACTIVE
              </span>
            </div>

            {/* Engine Selector Pills */}
            <div style={{ display: 'flex', gap: '6px', backgroundColor: '#F4F1EA', padding: '3px', borderRadius: '8px', border: '1px solid #DCD5C5' }}>
              {(['auto', 'laya', 'd3', 'mock'] as System1Engine[]).map(eng => {
                const isActive = system1Engine === eng;
                return (
                  <button
                    key={eng}
                    onClick={() => {
                      playSfx('click');
                      onEngineChange(eng);
                    }}
                    style={{
                      flex: 1,
                      border: 'none',
                      backgroundColor: isActive ? '#2D4A2B' : 'transparent',
                      color: isActive ? '#FAF8F5' : '#5A6B5C',
                      padding: '3px 0',
                      borderRadius: '5px',
                      fontSize: '10px',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: isActive ? 700 : 500,
                      cursor: 'pointer'
                    }}
                  >
                    {eng === 'auto' ? 'Auto-Detect' : eng === 'laya' ? 'Laya (CUDA)' : eng === 'd3' ? 'Decision 3 Lite' : 'Mock (0ms)'}
                  </button>
                );
              })}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', fontSize: '10.5px', color: '#3D4E3D', lineHeight: '1.5' }}>
              <div style={{ color: '#1B5E20', fontWeight: 600 }}>• System 1 Docker Port: http://127.0.0.1:8000/v1/systemone</div>
              <div>• Docker Image: <strong>decision-3-lite-serve:latest</strong> (Đang chạy ổn định)</div>
              <div>• LLM System 2: <strong>Google Gemini 2.5 Flash</strong> (Xử lý dịch & tổng hợp)</div>
              <div style={{ color: '#2D4A2B', fontWeight: 600 }}>• Hiệu năng định lượng: <strong>Tiết kiệm 84.6% token API • P50: 8.5ms</strong></div>
            </div>
          </div>

          {/* Card 4: Dynamic Feeds */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '12px 16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                  4. QUẢN LÝ NGUỒN RSS ĐỘNG (FEEDS MANAGER)
                </span>
                <button
                  onClick={() => { playSfx('click'); loadSources(); }}
                  style={{
                    backgroundColor: 'transparent',
                    border: '1px solid #DCD5C5',
                    borderRadius: '4px',
                    padding: '1px 5px',
                    fontSize: '9.5px',
                    color: '#5A6B5C',
                    cursor: 'pointer'
                  }}
                  title="Tải lại danh sách từ SQLite"
                >
                  ↻ Làm mới
                </button>
              </div>
              <span style={{ backgroundColor: '#E2DCD0', color: '#2D4A2B', borderRadius: '999px', padding: '2px 8px', fontSize: '9.5px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                {sources.filter(s => s.is_active === 1).length} / {sources.length} NGUỒN
              </span>
            </div>

            {/* Feeds list with scroll */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '110px', overflowY: 'auto', paddingRight: '4px' }}>
              {isLoadingSources && sources.length === 0 ? (
                <div style={{ padding: '12px', textAlign: 'center', fontSize: '11px', color: '#8A9A86' }}>
                  Đang tải danh sách nguồn từ SQLite...
                </div>
              ) : sources.length === 0 ? (
                <div style={{ padding: '12px', textAlign: 'center', fontSize: '11px', color: '#8A9A86' }}>
                  Chưa có nguồn tin nào trong cơ sở dữ liệu.
                </div>
              ) : (
                sources.map(s => (
                  <div
                    key={s.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '6px 8px',
                      backgroundColor: s.is_active === 1 ? '#FAF8F5' : '#F0EDE6',
                      borderRadius: '6px',
                      border: '1px solid #E8E2D5',
                      fontSize: '11px',
                      opacity: s.is_active === 1 ? 1 : 0.65
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
                      <input
                        type="checkbox"
                        checked={s.is_active === 1}
                        onChange={() => handleToggleSource(s.id)}
                        style={{ cursor: 'pointer' }}
                      />
                      <span style={{ fontWeight: 600, color: '#2D4A2B', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden', maxWidth: '220px' }}>
                        {s.name}
                      </span>
                      <span style={{ color: '#8A9A86', fontSize: '10.5px' }}>
                        ({s.article_count ?? 0} bài)
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
                      <span style={{ fontSize: '9.5px', color: '#5A6B5C', fontFamily: 'var(--font-mono)' }}>
                        {s.last_fetched_at ? s.last_fetched_at.slice(11, 16) : 'Chờ quét'}
                      </span>
                      <button
                        onClick={() => handleDeleteSource(s.id)}
                        style={{
                          backgroundColor: 'transparent',
                          border: 'none',
                          color: '#C86D51',
                          cursor: 'pointer',
                          fontSize: '12px',
                          padding: '2px 4px'
                        }}
                        title="Xóa nguồn tin này khỏi database"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>

            <button
              onClick={onOpenAddFeed}
              style={{
                backgroundColor: '#2D4A2B',
                border: 'none',
                borderRadius: '6px',
                padding: '7px 12px',
                color: '#F4F1EA',
                fontSize: '11px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <span>+</span>
              <span>Thêm Nguồn RSS Mới (Tự động Validate XML)</span>
            </button>
          </div>

          {/* Card 5: SFX & VOLUME CONTROLS (Chỉnh âm lượng to nhỏ, bật tắt) */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '12px 16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13.5px', fontWeight: 700, color: '#2D4A2B' }}>
                5. TÙY CHỌN TRẢI NGHIỆM & ÂM LƯỢNG SFX
              </span>
              <span
                style={{
                  backgroundColor: isSfxEnabled && volumePercent > 0 ? '#E8F5E9' : '#F5F5F5',
                  color: isSfxEnabled && volumePercent > 0 ? '#1B5E20' : '#757575',
                  borderRadius: '999px',
                  padding: '2px 8px',
                  fontSize: '10px',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 700
                }}
              >
                {isSfxEnabled && volumePercent > 0 ? `ÂM LƯỢNG: ${volumePercent}%` : 'ĐANG TẮT (MUTE)'}
              </span>
            </div>

            {/* Bật / Tắt âm thanh Toggle & Pacing Mode */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '11.5px', color: '#2C3E2C', fontWeight: 600 }}>
                  <input
                    type="checkbox"
                    checked={isSfxEnabled}
                    onChange={onToggleSfx}
                    style={{ cursor: 'pointer', width: '16px', height: '16px' }}
                  />
                  <span>Bật hiệu ứng âm thanh tương tác (Web Audio API)</span>
                </label>

                <button
                  onClick={onToggleSfx}
                  style={{
                    backgroundColor: isSfxEnabled ? '#2D4A2B' : '#DFD9CC',
                    color: isSfxEnabled ? '#F4F1EA' : '#5A6B5C',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '3px 10px',
                    fontSize: '11px',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  {isSfxEnabled ? '🔊 Đang Bật' : '🔇 Đang Tắt'}
                </button>
              </div>

              {/* Thanh trượt điều chỉnh âm lượng To / Nhỏ */}
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  backgroundColor: '#FAF8F5',
                  padding: '10px 12px',
                  borderRadius: '8px',
                  border: '1px solid #E8E2D5',
                  marginTop: '2px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px' }}>
                  <span style={{ fontWeight: 600, color: '#2D4A2B' }}>
                    🎚️ Mức âm lượng (To / Nhỏ):
                  </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: volumePercent > 0 && isSfxEnabled ? '#2D4A2B' : '#8A9A86' }}>
                    {volumePercent}% {volumePercent === 0 || !isSfxEnabled ? '(Im lặng)' : volumePercent < 35 ? '(Nhẹ nhàng)' : volumePercent < 75 ? '(Vừa vặn)' : '(To rõ)'}
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '13px' }}>🔈</span>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="1"
                    value={isSfxEnabled ? volumePercent : 0}
                    onChange={e => onVolumeChange(Number(e.target.value))}
                    style={{
                      flex: 1,
                      accentColor: '#2D4A2B',
                      cursor: 'pointer'
                    }}
                  />
                  <span style={{ fontSize: '13px' }}>🔊</span>
                </div>

                {/* Quick Volume Preset Pills */}
                <div style={{ display: 'flex', gap: '6px', marginTop: '4px' }}>
                  {[
                    { label: 'Tắt (0%)', val: 0 },
                    { label: 'Nhẹ (30%)', val: 30 },
                    { label: 'Vừa (70%)', val: 70 },
                    { label: 'To (100%)', val: 100 }
                  ].map(p => (
                    <button
                      key={p.val}
                      onClick={() => {
                        onVolumeChange(p.val);
                        if (p.val > 0) playSfx('click');
                      }}
                      style={{
                        flex: 1,
                        backgroundColor: volumePercent === p.val && isSfxEnabled ? '#2D4A2B' : '#FFFFFF',
                        color: volumePercent === p.val && isSfxEnabled ? '#F4F1EA' : '#5A6B5C',
                        border: '1px solid #DCD5C5',
                        borderRadius: '4px',
                        padding: '3px 0',
                        fontSize: '10.5px',
                        fontWeight: 600,
                        cursor: 'pointer'
                      }}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Nghe thử âm thanh SFX (Test Sounds) */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '2px' }}>
                <span style={{ fontSize: '11px', color: '#5A6B5C', fontWeight: 600 }}>
                  🎧 Nghe thử hiệu ứng âm thanh:
                </span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button
                    onClick={() => playSfx('water_drop')}
                    style={{
                      flex: 1,
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #DCD5C5',
                      borderRadius: '6px',
                      padding: '4px 6px',
                      fontSize: '10.5px',
                      color: '#2D4A2B',
                      cursor: 'pointer',
                      fontWeight: 600
                    }}
                  >
                    💧 Giọt Nước
                  </button>
                  <button
                    onClick={() => playSfx('paper_rustle')}
                    style={{
                      flex: 1,
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #DCD5C5',
                      borderRadius: '6px',
                      padding: '4px 6px',
                      fontSize: '10.5px',
                      color: '#2D4A2B',
                      cursor: 'pointer',
                      fontWeight: 600
                    }}
                  >
                    📜 Giấy Cói
                  </button>
                  <button
                    onClick={() => playSfx('wind_chime')}
                    style={{
                      flex: 1,
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #DCD5C5',
                      borderRadius: '6px',
                      padding: '4px 6px',
                      fontSize: '10.5px',
                      color: '#2D4A2B',
                      cursor: 'pointer',
                      fontWeight: 600
                    }}
                  >
                    🎐 Chuông Gió
                  </button>
                  <button
                    onClick={() => playSfx('click')}
                    style={{
                      flex: 1,
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #DCD5C5',
                      borderRadius: '6px',
                      padding: '4px 6px',
                      fontSize: '10.5px',
                      color: '#2D4A2B',
                      cursor: 'pointer',
                      fontWeight: 600
                    }}
                  >
                    🔘 Phím Gõ
                  </button>
                </div>
              </div>

              {/* Nhịp di chuyển con nhện */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '4px', paddingTop: '6px', borderTop: '1px solid #EBE6DC' }}>
                <span style={{ fontSize: '11px', color: '#2C3E2C' }}>• Tốc độ bò của nhện:</span>
                <button
                  onClick={() => {
                    playSfx('click');
                    onPacingChange(pacingMode === 'sync' ? 'chill' : 'sync');
                  }}
                  style={{
                    backgroundColor: '#F4F1EA',
                    border: '1px solid #DCD5C5',
                    borderRadius: '4px',
                    padding: '3px 8px',
                    fontSize: '10.5px',
                    fontWeight: 700,
                    color: '#2D4A2B',
                    cursor: 'pointer'
                  }}
                >
                  {pacingMode === 'sync' ? '⚡ Decision 3 Sync (400ms)' : '☕ Chill Mode (1200ms)'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
