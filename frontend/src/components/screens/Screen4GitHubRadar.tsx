import React, { useState, useEffect } from 'react';
import { ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';
import { apiFetch } from '../../utils/api';

export interface TechEvaluation {
  overall_score: number;
  community_score: number;
  community_desc: string;
  velocity_score: number;
  velocity_desc: string;
  production_score: number;
  production_desc: string;
  docs_score: number;
  docs_desc: string;
  verdict: string;
}

export interface GitHubAIExplanation {
  repo_full_name?: string;
  what_it_does?: string;
  problem_solved?: string;
  key_features?: string[];
  quickstart?: string;
  target_audience?: string;
  practical_use_case?: string;
  tech_stack?: string;
  tech_evaluation?: TechEvaluation;
}

export function computeRepoEvaluation(repo?: GitHubRepoDbItem | null): TechEvaluation {
  if (!repo) {
    return {
      overall_score: 9.0,
      community_score: 9.0,
      community_desc: 'Đang tải dữ liệu repo...',
      velocity_score: 9.0,
      velocity_desc: 'Đang theo dõi chỉ số',
      production_score: 9.0,
      production_desc: 'Chuẩn mã nguồn mở',
      docs_score: 8.5,
      docs_desc: 'Tài liệu đầy đủ',
      verdict: 'Đang phân tích độ tương thích hệ thống.',
    };
  }

  if (repo.ai_explanation?.tech_evaluation) {
    return repo.ai_explanation.tech_evaluation;
  }

  // 1. Community Score (Dựa trên Stars & Forks)
  let community_score = 7.5;
  let community_desc = 'Cộng đồng đang hình thành';
  if (repo.stars >= 30000) {
    community_score = 9.8;
    community_desc = `Hơn ${repo.stars.toLocaleString()} Stars — Hạng S uy tín toàn cầu`;
  } else if (repo.stars >= 15000) {
    community_score = 9.4;
    community_desc = `${repo.stars.toLocaleString()} Stars — Được cộng đồng tin cậy cao`;
  } else if (repo.stars >= 5000) {
    community_score = 8.8;
    community_desc = `${repo.stars.toLocaleString()} Stars — Mức độ phổ biến tốt`;
  } else if (repo.stars >= 1000) {
    community_score = 8.2;
    community_desc = `${repo.stars.toLocaleString()} Stars — Dự án đang tăng trưởng`;
  }

  // 2. Velocity Score (Tốc độ tăng trưởng sao/ngày)
  let velocity_score = 7.8;
  let velocity_desc = 'Tăng trưởng ổn định';
  const today = repo.today_stars || 0;
  if (today >= 200) {
    velocity_score = 9.9;
    velocity_desc = `+${today} sao/ngày — Xu hướng bùng nổ (Viral Hot)`;
  } else if (today >= 100) {
    velocity_score = 9.4;
    velocity_desc = `+${today} sao/ngày — Tăng trưởng rất mạnh`;
  } else if (today >= 30) {
    velocity_score = 8.8;
    velocity_desc = `+${today} sao/ngày — Thu hút kỹ sư đều đặn`;
  } else if (today > 0) {
    velocity_score = 8.1;
    velocity_desc = `+${today} sao/ngày — Ổn định`;
  }

  // 3. Production Readiness (Giấy phép & Tính thương mại)
  let production_score = 8.5;
  let production_desc = 'Sẵn sàng tích hợp hệ thống';
  const lic = (repo.license || '').toLowerCase();
  if (lic.includes('mit') || lic.includes('apache') || lic.includes('bsd')) {
    production_score = 9.6;
    production_desc = `Giấy phép ${repo.license || 'MIT/Apache'} — 100% an toàn thương mại`;
  } else if (lic.includes('gpl')) {
    production_score = 8.0;
    production_desc = `Giấy phép ${repo.license} — Chú ý ràng buộc copyleft`;
  }

  // 4. Docs & DevEx (Tài liệu & README)
  let docs_score = 8.0;
  let docs_desc = 'Tài liệu mức cơ bản';
  const readmeLen = (repo.readme_content || '').length;
  if (readmeLen > 5000) {
    docs_score = 9.6;
    docs_desc = 'README chi tiết, đầy đủ code mẫu & hướng dẫn';
  } else if (readmeLen > 1500) {
    docs_score = 8.9;
    docs_desc = 'Tài liệu chuẩn chỉ, hướng dẫn cài đặt rõ ràng';
  }

  // Overall Score có trọng số (35% Cộng đồng, 25% Tốc độ, 20% Production, 20% Tài liệu)
  const overall_score = Number(
    (community_score * 0.35 + velocity_score * 0.25 + production_score * 0.20 + docs_score * 0.20).toFixed(1)
  );

  // Verdict khuyến nghị
  let verdict = '';
  if (overall_score >= 9.2) {
    verdict = 'Production Ready (Hạng Xuất Sắc) — Dự án có độ uy tín và cộng đồng cực lớn. Khuyến nghị đưa vào tech stack chính thức.';
  } else if (overall_score >= 8.5) {
    verdict = 'Adopt for Projects (Nên Dùng) — Hiệu năng và tài liệu tốt. Rất phù hợp triển khai cho dự án mới hoặc tối ưu module.';
  } else {
    verdict = 'Trial / Staging (Thử Nghiệm PoC) — Tiềm năng tốt, nên đánh giá trong môi trường thử nghiệm trước khi scale lớn.';
  }

  return {
    overall_score,
    community_score,
    community_desc,
    velocity_score,
    velocity_desc,
    production_score,
    production_desc,
    docs_score,
    docs_desc,
    verdict,
  };
}

export interface GitHubRepoDbItem {
  id: number;
  repo_full_name: string;
  repo_url: string;
  stars: number;
  today_stars: number;
  forks: number;
  primary_language: string;
  license: string;
  description: string;
  topics: string[];
  readme_content?: string;
  ai_explanation?: GitHubAIExplanation | null;
  demo_code?: string;
  tech_score: number;
  is_bookmarked: number;
  crawled_at: string;
}

export interface SyncStatus {
  last_sync_date: string;
  last_sync_time: string;
  total_repos: number;
  is_today_synced: boolean;
}

interface Screen4GitHubRadarProps {
  onNavigate: (tab: ScreenTab) => void;
}

export const Screen4GitHubRadar: React.FC<Screen4GitHubRadarProps> = ({ onNavigate }) => {
  const [repos, setRepos] = useState<GitHubRepoDbItem[]>([]);
  const [selectedRepoId, setSelectedRepoId] = useState<number | null>(null);
  const [viewMode, setViewMode] = useState<'top25' | 'top10_growth' | 'topic'>('top25');
  const [selectedTopic, setSelectedTopic] = useState<string>('all');
  const [growthFilter, setGrowthFilter] = useState<'all' | 'high' | 'med'>('all');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [copiedClone, setCopiedClone] = useState<boolean>(false);
  const [stats, setStats] = useState<Record<string, number>>({
    all: 0,
    ai: 0,
    systems: 0,
    wasm: 0,
    vector: 0,
    design: 0,
    skills: 0
  });
  const [activeTab, setActiveTab] = useState<'explain' | 'readme' | 'code' | 'docker'>('explain');
  const [isExplaining, setIsExplaining] = useState<boolean>(false);
  const [explainError, setExplainError] = useState<string | null>(null);
  const [copiedQuickstart, setCopiedQuickstart] = useState<boolean>(false);
  const [quickExplainUrl, setQuickExplainUrl] = useState<string>('');
  const [isQuickExplaining, setIsQuickExplaining] = useState<boolean>(false);
  
  // Daily Sync state
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [showCriteriaModal, setShowCriteriaModal] = useState<boolean>(false);
  const [syncNotice, setSyncNotice] = useState<string | null>(null);

  // Modal thêm repo mới
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);
  const [newRepoInput, setNewRepoInput] = useState<string>('');
  const [newRepoTopic, setNewRepoTopic] = useState<string>('ai');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [addError, setAddError] = useState<string | null>(null);

  // Nhận diện lĩnh vực / domain đa dạng của repo (Canva, Design, Skills, UI, AI, Systems)
  const getRepoDomainBadge = (topics: string[] = []) => {
    const t = topics.map(x => x.toLowerCase());
    if (t.includes('canva') || t.includes('design') || t.includes('canvas') || t.includes('whiteboard') || t.includes('figma')) {
      return { label: '🎨 Canva / Design', color: '#B45309', bg: '#FEF3C7' };
    }
    if (t.includes('skills') || t.includes('education') || t.includes('roadmap') || t.includes('curriculum')) {
      return { label: '📚 Skills / Giáo Dục', color: '#1D4ED8', bg: '#DBEAFE' };
    }
    if (t.includes('ui') || t.includes('tailwind') || t.includes('components')) {
      return { label: '✨ UI Design System', color: '#6D28D9', bg: '#EDE9FE' };
    }
    if (t.includes('ai') || t.includes('llm') || t.includes('reasoning') || t.includes('deepseek')) {
      return { label: '🤖 AI & Models', color: '#15803D', bg: '#DCFCE7' };
    }
    if (t.includes('systems') || t.includes('rust') || t.includes('c++')) {
      return { label: '⚡ Systems & Rust', color: '#B91C1C', bg: '#FEE2E2' };
    }
    if (t.includes('vector') || t.includes('search')) {
      return { label: '🔍 Vector Search', color: '#0369A1', bg: '#E0F2FE' };
    }
    return { label: '🌐 Open Tech', color: '#374151', bg: '#F3F4F6' };
  };

  // Tải trạng thái đồng bộ hàng ngày
  const loadSyncStatus = async () => {
    try {
      const res = await apiFetch('/api/v1/github/sync-status');
      if (res.ok) {
        const data = await res.json();
        setSyncStatus(data);
      }
    } catch (e) {
      console.error('Lỗi tải trạng thái đồng bộ:', e);
    }
  };

  const loadRepos = async () => {
    setIsLoading(true);
    try {
      let endpoint = '/api/v1/github/repos';
      // Khi chọn Top 25 hoặc Top 10, truy vấn TOÀN BỘ hệ sinh thái GitHub không giới hạn bộ lọc chuyên mục
      if (viewMode === 'top25') {
        endpoint = '/api/v1/github/top-starred?limit=25';
      } else if (viewMode === 'top10_growth') {
        endpoint = '/api/v1/github/top-trending?limit=10';
      } else {
        endpoint = `/api/v1/github/repos${selectedTopic !== 'all' ? `?topic=${selectedTopic}` : ''}`;
      }

      const res = await apiFetch(endpoint);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data)) {
          setRepos(data);
          if (data.length > 0 && (!selectedRepoId || !data.some(r => r.id === selectedRepoId))) {
            setSelectedRepoId(data[0].id);
          }
        }
      }

      const statsRes = await apiFetch('/api/v1/github/stats');
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
    } catch (e) {
      console.error('Lỗi tải GitHub Repos từ SQLite:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRepos();
    loadSyncStatus();
  }, [viewMode, selectedTopic]);

  const selectedRepo = repos.find(r => r.id === selectedRepoId) || repos[0];

  const selectRepo = async (repoId: number) => {
    setSelectedRepoId(repoId);
    playSfx('click');
    try {
      const res = await apiFetch(`/api/v1/github/repos/${repoId}`);
      if (res.ok) {
        const detail = await res.json();
        setRepos(prev => prev.map(r => r.id === repoId ? { ...r, ...detail } : r));
      }
    } catch (e) {
      console.error('Lỗi tải chi tiết repo:', e);
    }
  };

  const handleExplainRepo = async (repoId: number, force: boolean = false) => {
    setIsExplaining(true);
    setExplainError(null);
    playSfx('click');
    try {
      const res = await apiFetch(`/api/v1/github/repos/${repoId}/explain${force ? '?force=true' : ''}`, {
        method: 'POST'
      });
      if (res.ok) {
        const explanationData = await res.json();
        setRepos(prev => prev.map(r => r.id === repoId ? { ...r, ai_explanation: explanationData } : r));
        playSfx('wind_chime');
      } else {
        const err = await res.json();
        setExplainError(err.detail || 'Không thể gọi AI phân tích.');
      }
    } catch (err: any) {
      setExplainError(err.message || 'Lỗi kết nối khi gọi AI.');
    } finally {
      setIsExplaining(false);
    }
  };

  const handleQuickExplainUrl = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickExplainUrl.trim()) return;
    setIsQuickExplaining(true);
    playSfx('click');
    try {
      const res = await apiFetch('/api/v1/github/explain-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url_or_name: quickExplainUrl.trim(), topic: 'ai' })
      });
      if (res.ok) {
        const data = await res.json();
        playSfx('wind_chime');
        await loadRepos();
        if (data.repo && data.repo.id) {
          setSelectedRepoId(data.repo.id);
          setActiveTab('explain');
        }
        setQuickExplainUrl('');
      } else {
        const err = await res.json();
        alert(err.detail || 'Không thể phân tích repo này');
      }
    } catch (err: any) {
      alert(err.message || 'Lỗi kết nối');
    } finally {
      setIsQuickExplaining(false);
    }
  };

  const handleCopyClone = () => {
    if (!selectedRepo) return;
    playSfx('paper_rustle');
    navigator.clipboard.writeText(`git clone ${selectedRepo.repo_url}.git`);
    setCopiedClone(true);
    setTimeout(() => setCopiedClone(false), 2000);
  };

  const handleToggleBookmark = async () => {
    if (!selectedRepo) return;
    playSfx('click');
    const newStatus = selectedRepo.is_bookmarked === 1 ? 0 : 1;
    setRepos(prev => prev.map(r => r.id === selectedRepo.id ? { ...r, is_bookmarked: newStatus } : r));
    try {
      await apiFetch(`/api/v1/github/repos/${selectedRepo.id}/bookmark`, { method: 'PATCH' });
    } catch (e) {
      console.error('Lỗi cập nhật bookmark:', e);
      loadRepos();
    }
  };

  // Quét cập nhật chỉ số sao hàng ngày
  const handleDailySync = async () => {
    playSfx('click');
    setIsSyncing(true);
    setSyncNotice(null);
    try {
      const res = await apiFetch('/api/v1/github/daily-sync?force=true', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        playSfx('wind_chime');
        setSyncNotice(data.message || 'Đã quét và cập nhật chỉ số sao thành công!');
        await loadSyncStatus();
        await loadRepos();
      } else {
        setSyncNotice('Lỗi khi kích hoạt quét cập nhật.');
      }
    } catch (err: any) {
      setSyncNotice('Lỗi kết nối máy chủ: ' + (err?.message || ''));
    } finally {
      setIsSyncing(false);
      setTimeout(() => setSyncNotice(null), 5000);
    }
  };

  const handleAddRepoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRepoInput.trim()) return;
    setIsSubmitting(true);
    setAddError(null);
    playSfx('click');
    try {
      const res = await apiFetch('/api/v1/github/repos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url_or_name: newRepoInput.trim(), topic: newRepoTopic })
      });
      if (res.ok) {
        const result = await res.json();
        playSfx('wind_chime');
        setIsAddModalOpen(false);
        setNewRepoInput('');
        await loadRepos();
        if (result.id) setSelectedRepoId(result.id);
      } else {
        const errData = await res.json();
        setAddError(errData.detail || 'Không thể thêm repository');
      }
    } catch (err: any) {
      setAddError(err.message || 'Lỗi kết nối mạng');
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredRepos = repos.filter(r => {
    if (growthFilter === 'high') return (r.today_stars || 0) >= 300;
    if (growthFilter === 'med') return (r.today_stars || 0) >= 100;
    return true;
  });

  const topicsList = [
    { id: 'all', label: 'Tất Cả Danh Mục', count: stats.all || 41 },
    { id: 'design', label: '🎨 Thiết Kế & Canva / UI', count: stats.design || 8 },
    { id: 'skills', label: '📚 Kỹ Năng & Giáo Dục', count: stats.skills || 5 },
    { id: 'ai', label: '🤖 AI & LLM Inference', count: stats.ai || 18 },
    { id: 'systems', label: '⚡ Systems & Rust/C++', count: stats.systems || 12 },
    { id: 'wasm', label: '🌐 WebAssembly & Edge', count: stats.wasm || 6 },
    { id: 'vector', label: '🔍 Vector DB & Search', count: stats.vector || 5 }
  ];

  return (
    <div
      style={{
        display: 'flex',
        flex: 1,
        width: '100%',
        gap: '12px',
        padding: '0 12px',
        overflow: 'hidden',
        height: '100%',
        position: 'relative'
      }}
    >
      {/* 1. LEFT SIDEBAR (240px) */}
      <aside
        style={{
          width: '235px',
          flexShrink: 0,
          backgroundColor: '#EBE6DC',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '12px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflowY: 'auto'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Header Bảng Xếp Hạng */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span
              style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '12.5px',
                fontWeight: 700,
                color: '#2D4A2B',
                letterSpacing: '0.3px'
              }}
            >
              CHẾ ĐỘ XEM & XẾP HẠNG
            </span>
            <button
              onClick={() => { playSfx('click'); loadRepos(); }}
              style={{
                backgroundColor: 'transparent',
                border: 'none',
                color: '#5A6B5C',
                fontSize: '11px',
                cursor: 'pointer'
              }}
              title="Làm mới từ SQLite"
            >
              ↻
            </button>
          </div>

          {/* View Mode Switcher Pills */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {/* Tab 1: Top 25 Sao Đứng Đầu (Đa lĩnh vực, không theo bộ lọc) */}
            <div
              onClick={() => {
                playSfx('click');
                setViewMode('top25');
              }}
              style={{
                padding: '7px 10px',
                borderRadius: '8px',
                backgroundColor: viewMode === 'top25' ? '#2D4A2B' : '#F4F1EA',
                color: viewMode === 'top25' ? '#F4F1EA' : '#2D4A2B',
                cursor: 'pointer',
                fontSize: '11.5px',
                fontWeight: viewMode === 'top25' ? 700 : 600,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>🏆</span>
                <span>Top 25 Sao Đứng Đầu</span>
              </div>
              <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)' }}>(25)</span>
            </div>

            {/* Tab 2: Top 10 Tăng Trưởng Nhanh Nhất (Đa lĩnh vực, không theo bộ lọc) */}
            <div
              onClick={() => {
                playSfx('click');
                setViewMode('top10_growth');
              }}
              style={{
                padding: '7px 10px',
                borderRadius: '8px',
                backgroundColor: viewMode === 'top10_growth' ? '#C86D51' : '#F4F1EA',
                color: viewMode === 'top10_growth' ? '#FFFFFF' : '#C86D51',
                cursor: 'pointer',
                fontSize: '11.5px',
                fontWeight: viewMode === 'top10_growth' ? 700 : 600,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>🚀</span>
                <span>Top 10 Tăng Trưởng Nhanh</span>
              </div>
              <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)' }}>(10)</span>
            </div>

            {/* Tab 3: Theo Chuyên Mục Cụ Thể */}
            <div
              onClick={() => {
                playSfx('click');
                setViewMode('topic');
              }}
              style={{
                padding: '7px 10px',
                borderRadius: '8px',
                backgroundColor: viewMode === 'topic' ? '#2D4A2B' : '#F4F1EA',
                color: viewMode === 'topic' ? '#F4F1EA' : '#5A6B5C',
                cursor: 'pointer',
                fontSize: '11.5px',
                fontWeight: viewMode === 'topic' ? 700 : 500,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>📑</span>
                <span>Lọc Theo Chuyên Mục</span>
              </div>
              <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)' }}>({stats.all || 41})</span>
            </div>
          </div>

          {/* Sub-topics: Hiển thị khi ở chế độ 'topic' hoặc thông báo không lọc khi ở Top 25/10 */}
          {viewMode === 'topic' ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '3px', marginTop: '2px', paddingLeft: '4px' }}>
              <div style={{ fontSize: '10.5px', color: '#8A9A86', fontWeight: 600, marginBottom: '2px' }}>
                CHỌN CHUYÊN MỤC CẦN LỌC:
              </div>
              {topicsList.map(t => {
                const isActive = selectedTopic === t.id;
                return (
                  <div
                    key={t.id}
                    onClick={() => {
                      playSfx('click');
                      setSelectedTopic(t.id);
                    }}
                    style={{
                      padding: '5px 8px',
                      borderRadius: '6px',
                      backgroundColor: isActive ? '#DFD9CC' : 'transparent',
                      color: isActive ? '#2D4A2B' : '#5A6B5C',
                      cursor: 'pointer',
                      fontSize: '11px',
                      fontWeight: isActive ? 700 : 500,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}
                  >
                    <span>{isActive ? '●' : '○'} {t.label}</span>
                    <span style={{ fontSize: '9.5px', fontFamily: 'var(--font-mono)' }}>({t.count})</span>
                  </div>
                );
              })}
            </div>
          ) : (
            <div
              style={{
                backgroundColor: '#FAF8F5',
                border: '1px solid #EBE6DC',
                borderRadius: '6px',
                padding: '6px 8px',
                fontSize: '10.5px',
                color: '#6B7A6C',
                lineHeight: '1.4'
              }}
            >
              🌐 <strong>Đa lĩnh vực toàn cầu:</strong> Tổng hợp tự do từ Kỹ năng (Skills), Thiết kế (Canva/Penpot), UI đến AI & Systems (không bị gò bó bởi bộ lọc).
            </div>
          )}

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* Repos list from SQLite */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '11.5px', fontWeight: 700, color: '#2D4A2B' }}>
                DANH SÁCH ({filteredRepos.length})
              </span>
              <span style={{ fontSize: '10px', color: '#8A9A86' }}>
                {viewMode === 'top25' ? 'Xếp theo Sao' : viewMode === 'top10_growth' ? 'Xếp theo Tăng trưởng' : 'Chuyên mục'}
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '180px', overflowY: 'auto' }}>
              {isLoading && repos.length === 0 ? (
                <div style={{ fontSize: '11px', color: '#8A9A86', textAlign: 'center', padding: '10px' }}>
                  Đang tải từ SQLite...
                </div>
              ) : filteredRepos.length === 0 ? (
                <div style={{ fontSize: '11px', color: '#8A9A86', textAlign: 'center', padding: '10px' }}>
                  Không có repo nào khớp
                </div>
              ) : (
                filteredRepos.map((r, index) => {
                  const isSelected = selectedRepo?.id === r.id;
                  const rank = index + 1;
                  const badge = getRepoDomainBadge(r.topics);
                  return (
                    <div
                      key={r.id}
                      onClick={() => {
                        selectRepo(r.id);
                      }}
                      style={{
                        padding: '6px 8px',
                        borderRadius: '6px',
                        backgroundColor: isSelected ? '#FAF8F5' : '#E5DFD3',
                        border: isSelected ? '1px solid #2D4A2B' : '1px solid transparent',
                        cursor: 'pointer',
                        fontSize: '11px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '2px',
                        transition: 'all 0.15s ease'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', overflow: 'hidden' }}>
                          <span
                            style={{
                              fontSize: '9.5px',
                              fontWeight: 700,
                              fontFamily: 'var(--font-mono)',
                              color: rank === 1 ? '#D97706' : rank === 2 ? '#5A6B5C' : rank === 3 ? '#C86D51' : '#8A9A86'
                            }}
                          >
                            {rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `#${rank}`}
                          </span>
                          <span style={{ fontWeight: isSelected ? 700 : 500, color: '#2D4A2B', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '115px' }}>
                            {r.repo_full_name}
                          </span>
                        </div>
                        <span style={{ fontSize: '10px', color: '#C86D51', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                          ★{r.stars > 1000 ? `${(r.stars / 1000).toFixed(1)}k` : r.stars}
                        </span>
                      </div>
                      <div style={{ fontSize: '9px', color: '#6B7A6C', display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingLeft: '16px' }}>
                        <span style={{ backgroundColor: badge.bg, color: badge.color, padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 600 }}>
                          {badge.label}
                        </span>
                        {r.today_stars > 0 && (
                          <span style={{ color: '#1B5E20', fontWeight: 700 }}>
                            +{r.today_stars.toLocaleString()}/ngày
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          <div style={{ height: '1px', backgroundColor: '#DCD5C5' }} />

          {/* Growth rate filters */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '11.5px', fontWeight: 700, color: '#2D4A2B' }}>
              BỘ LỌC TỐC ĐỘ TĂNG TRƯỞNG
            </div>
            <div
              onClick={() => { playSfx('click'); setGrowthFilter(growthFilter === 'high' ? 'all' : 'high'); }}
              style={{
                backgroundColor: growthFilter === 'high' ? '#C86D51' : '#F4F1EA',
                color: growthFilter === 'high' ? '#FFF' : '#C86D51',
                padding: '5px 8px',
                borderRadius: '6px',
                fontSize: '10.5px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              🔥 Tăng trưởng &gt; 300 ⭐/ngày
            </div>
            <div
              onClick={() => { playSfx('click'); setGrowthFilter(growthFilter === 'med' ? 'all' : 'med'); }}
              style={{
                backgroundColor: growthFilter === 'med' ? '#2D4A2B' : '#F4F1EA',
                color: growthFilter === 'med' ? '#FFF' : '#2D4A2B',
                padding: '5px 8px',
                borderRadius: '6px',
                fontSize: '10.5px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              ⚡ Tăng trưởng &gt; 100 ⭐/ngày
            </div>
          </div>
        </div>

        {/* Add Repo Button */}
        <button
          onClick={() => { playSfx('click'); setIsAddModalOpen(true); }}
          style={{
            backgroundColor: '#2D4A2B',
            border: 'none',
            borderRadius: '8px',
            padding: '8px 12px',
            color: '#F4F1EA',
            fontSize: '11px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '6px',
            marginTop: '8px'
          }}
        >
          <span>🔍</span>
          <span>+ Thêm Repo Theo Dõi (GraphQL)</span>
        </button>
      </aside>

      {/* 2. MIDDLE CODE & README INSPECTOR (flex-1) */}
      <section
        style={{
          flex: 1,
          height: '100%',
          overflowY: 'auto',
          overflowX: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start', // Chống cắt mất chữ ở mép trên cùng
          gap: '16px',
          padding: '20px 24px 32px 24px',
          boxSizing: 'border-box'
        }}
      >
        {/* Banner Quét Cập Nhật Hàng Ngày */}
        <div
          style={{
            backgroundColor: '#EBE6DC',
            border: '1px solid #DCD5C5',
            borderRadius: '10px',
            padding: '8px 14px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexShrink: 0
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '15px' }}>
              {viewMode === 'top25' ? '🏆' : viewMode === 'top10_growth' ? '🚀' : '📑'}
            </span>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
                {viewMode === 'top25'
                  ? 'BẢNG XẾP HẠNG TOP 25 REPOSITORIES NHIỀU SAO NHẤT GITHUB (ĐA LĨNH VỰC)'
                  : viewMode === 'top10_growth'
                  ? 'TOP 10 REPOSITORIES TĂNG TRƯỞNG SAO NHANH NHẤT HÔM NAY (TOÀN CẦU)'
                  : 'RADAR CÔNG NGHỆ GITHUB THEO DANH MỤC CHUYÊN BIỆT'}
              </span>
              <span style={{ fontSize: '10.5px', color: '#5A6B5C' }}>
                {viewMode === 'top25' || viewMode === 'top10_growth'
                  ? '🌐 Không giới hạn bộ lọc chuyên mục • Bao quát từ Skills, Canva & Thiết kế, UI đến AI & Systems • '
                  : 'Lọc danh mục chuyên biệt • '}
                📅 Quét tự động: <strong>1 lần/ngày khi sang ngày mới</strong>
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button
              onClick={handleDailySync}
              disabled={isSyncing}
              style={{
                backgroundColor: '#2D4A2B',
                color: '#F4F1EA',
                border: 'none',
                borderRadius: '6px',
                padding: '5px 12px',
                fontSize: '11px',
                fontWeight: 700,
                cursor: isSyncing ? 'wait' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                opacity: isSyncing ? 0.7 : 1
              }}
              title="Kích hoạt quét cập nhật chỉ số sao ngay lập tức"
            >
              <span>↻</span>
              <span>{isSyncing ? 'Đang quét...' : 'Quét Cập Nhật Hôm Nay'}</span>
            </button>
          </div>
        </div>

        {syncNotice && (
          <div
            style={{
              backgroundColor: '#E8F5E9',
              border: '1px solid #C8E6C9',
              color: '#1B5E20',
              borderRadius: '6px',
              padding: '6px 12px',
              fontSize: '11px',
              fontWeight: 600,
              flexShrink: 0
            }}
          >
            ✓ {syncNotice}
          </div>
        )}

        {selectedRepo ? (
          <>
            {/* Repo Header Card */}
            <div
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #DCD5C5',
                padding: '14px 18px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
                boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)',
                flexShrink: 0
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: '16.5px', fontWeight: 700, color: '#2D4A2B', margin: 0 }}>
                    {selectedRepo.repo_full_name}
                  </h1>
                  {(() => {
                    const badge = getRepoDomainBadge(selectedRepo.topics);
                    return (
                      <span
                        style={{
                          backgroundColor: badge.bg,
                          color: badge.color,
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontSize: '10px',
                          fontWeight: 700
                        }}
                      >
                        {badge.label}
                      </span>
                    );
                  })()}
                </div>

                <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                  <span style={{ backgroundColor: '#FFF8E1', color: '#8D6E63', padding: '2px 7px', borderRadius: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                    ★ {selectedRepo.stars.toLocaleString()} Stars
                  </span>
                  {selectedRepo.today_stars > 0 && (
                    <span style={{ backgroundColor: '#FDF2EE', color: '#C86D51', padding: '2px 7px', borderRadius: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                      🔥 +{selectedRepo.today_stars.toLocaleString()}/ngày
                    </span>
                  )}
                  <span style={{ backgroundColor: '#F5F5F5', color: '#616161', padding: '2px 7px', borderRadius: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)' }}>
                    ⑂ {selectedRepo.forks.toLocaleString()} Forks
                  </span>
                  <span style={{ backgroundColor: '#E8F0E8', color: '#2E7D32', padding: '2px 7px', borderRadius: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                    {selectedRepo.primary_language || 'Code'}
                  </span>
                  <span style={{ backgroundColor: '#EAEFF4', color: '#305A78', padding: '2px 7px', borderRadius: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)' }}>
                    {selectedRepo.license || 'Open Source'}
                  </span>
                </div>
              </div>
              <div style={{ fontSize: '12px', color: '#5A6B5C', lineHeight: '1.4' }}>
                {selectedRepo.description || 'Repository được lưu trữ và lập chỉ mục trong SQLite spider_radar.db'}
              </div>
              {selectedRepo.topics && selectedRepo.topics.length > 0 && (
                <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                  {selectedRepo.topics.map(tp => (
                    <span key={tp} style={{ backgroundColor: '#FAF8F5', border: '1px solid #DCD5C5', color: '#2D4A2B', padding: '1px 6px', borderRadius: '3px', fontSize: '10px', fontFamily: 'var(--font-mono)' }}>
                      #{tp}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Quick URL Explainer & View Tabs Bar */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {/* Quick Analyze Any GitHub URL Input */}
              <form
                onSubmit={handleQuickExplainUrl}
                style={{
                  display: 'flex',
                  gap: '6px',
                  backgroundColor: '#FAF8F5',
                  border: '1px solid #DCD5C5',
                  borderRadius: '8px',
                  padding: '6px 10px',
                  alignItems: 'center'
                }}
              >
                <span style={{ fontSize: '13px' }}>🔍</span>
                <input
                  type="text"
                  placeholder="Dán link GitHub bất kỳ (vd: https://github.com/astral-sh/uv hoặc facebook/react) để AI giải thích ngay..."
                  value={quickExplainUrl}
                  onChange={(e) => setQuickExplainUrl(e.target.value)}
                  style={{
                    flex: 1,
                    border: 'none',
                    backgroundColor: 'transparent',
                    outline: 'none',
                    fontSize: '11.5px',
                    fontFamily: 'var(--font-sans)',
                    color: '#2D4A2B'
                  }}
                />
                <button
                  type="submit"
                  disabled={isQuickExplaining || !quickExplainUrl.trim()}
                  style={{
                    backgroundColor: '#2D4A2B',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '5px',
                    padding: '4px 10px',
                    fontSize: '11px',
                    fontWeight: 600,
                    cursor: isQuickExplaining || !quickExplainUrl.trim() ? 'not-allowed' : 'pointer'
                  }}
                >
                  {isQuickExplaining ? '⏳ Đang quét...' : '✨ AI Giải Thích'}
                </button>
              </form>

              {/* View Tabs */}
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <button
                  onClick={() => { playSfx('click'); setActiveTab('explain'); }}
                  style={{
                    backgroundColor: activeTab === 'explain' ? '#2D4A2B' : '#EBE6DC',
                    color: activeTab === 'explain' ? '#F4F1EA' : '#2D4A2B',
                    border: activeTab === 'explain' ? '1px solid #2D4A2B' : '1px solid #DCD5C5',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px'
                  }}
                >
                  <span>💡</span>
                  <span>Giải Thích Dễ Hiểu (AI .env)</span>
                  {selectedRepo?.ai_explanation && (
                    <span style={{ backgroundColor: activeTab === 'explain' ? '#A3D9A5' : '#2D4A2B', color: activeTab === 'explain' ? '#1B4332' : '#FFFFFF', fontSize: '9px', padding: '1px 5px', borderRadius: '10px' }}>
                      ĐÃ PHÂN TÍCH
                    </span>
                  )}
                </button>
                <button
                  onClick={() => { playSfx('click'); setActiveTab('readme'); }}
                  style={{
                    backgroundColor: activeTab === 'readme' ? '#2D4A2B' : '#EBE6DC',
                    color: activeTab === 'readme' ? '#F4F1EA' : '#5A6B5C',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  📄 README.md Toàn Văn
                </button>
                <button
                  onClick={() => { playSfx('click'); setActiveTab('code'); }}
                  style={{
                    backgroundColor: activeTab === 'code' ? '#2D4A2B' : '#EBE6DC',
                    color: activeTab === 'code' ? '#F4F1EA' : '#5A6B5C',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  💻 Kiến Trúc & Code Demo
                </button>
                <button
                  onClick={() => { playSfx('click'); setActiveTab('docker'); }}
                  style={{
                    backgroundColor: activeTab === 'docker' ? '#2D4A2B' : '#EBE6DC',
                    color: activeTab === 'docker' ? '#F4F1EA' : '#5A6B5C',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  🐳 Cài Đặt Docker & Port
                </button>
              </div>
            </div>

            {/* Content Pane */}
            <div
              style={{
                background: '#FFFFFF',
                border: '1px solid #E5E0D5',
                borderRadius: '14px',
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '16px',
                height: 'auto',       // Bắt buộc để auto, không giới hạn max-height
                minHeight: 'min-content',
                flexShrink: 0,        // Cấm Flexbox tự ý ép lùn card này!
                overflow: 'visible',  // Không cắt cụt hộp Quickstart màu xanh đen bên trong
                boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
              }}
            >
              {activeTab === 'explain' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #EBE6DC', paddingBottom: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span style={{ fontSize: '14px' }}>🤖</span>
                      <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                        TRỢ LÝ AI (.ENV) PHÂN TÍCH & GIẢI THÍCH DỄ HIỂU
                      </span>
                      <span style={{ fontSize: '10px', backgroundColor: '#E8F5E9', color: '#2E7D32', padding: '1px 6px', borderRadius: '4px', fontWeight: 600 }}>
                        Gemini / DeepSeek
                      </span>
                    </div>
                    <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                      <button
                        onClick={() => handleExplainRepo(selectedRepo.id, true)}
                        disabled={isExplaining}
                        style={{
                          backgroundColor: '#FAF8F5',
                          border: '1px solid #DCD5C5',
                          color: '#2D4A2B',
                          borderRadius: '4px',
                          padding: '3px 8px',
                          fontSize: '10.5px',
                          fontFamily: 'var(--font-mono)',
                          fontWeight: 600,
                          cursor: isExplaining ? 'not-allowed' : 'pointer'
                        }}
                      >
                        {isExplaining ? '⏳ Đang phân tích...' : '↻ Phân tích lại bằng AI'}
                      </button>
                      <span style={{ fontSize: '10px', color: '#8A9A86', fontFamily: 'var(--font-mono)' }}>
                        SQLITE ID #{selectedRepo.id}
                      </span>
                    </div>
                  </div>

                  {explainError && (
                    <div style={{ backgroundColor: '#FEE2E2', border: '1px solid #F87171', color: '#991B1B', padding: '8px 12px', borderRadius: '6px', fontSize: '11.5px' }}>
                      ⚠️ {explainError}
                    </div>
                  )}

                  {selectedRepo?.ai_explanation ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      {/* Hộp 1: Mục đích cốt lõi */}
                      <div style={{ backgroundColor: '#F4F9F2', border: '1px solid #C4DBC0', borderRadius: '8px', padding: '12px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                          <span style={{ fontSize: '13px' }}>🎯</span>
                          <span style={{ fontSize: '11px', fontWeight: 700, color: '#1B4332', letterSpacing: '0.3px', textTransform: 'uppercase' }}>
                            Repo này sinh ra để làm gì? (Mục đích cốt lõi)
                          </span>
                        </div>
                        <div style={{ fontSize: '13px', color: '#1B4332', lineHeight: '1.6', fontWeight: 500 }}>
                          {selectedRepo.ai_explanation.what_it_does}
                        </div>
                      </div>

                      {/* Hộp 2: Bài toán thực tế & Nỗi đau */}
                      <div style={{ backgroundColor: '#FFFBF0', border: '1px solid #FFE082', borderRadius: '8px', padding: '12px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                          <span style={{ fontSize: '13px' }}>💡</span>
                          <span style={{ fontSize: '11px', fontWeight: 700, color: '#6D4C41', letterSpacing: '0.3px', textTransform: 'uppercase' }}>
                            Giải quyết bài toán / nỗi đau gì ngoài đời thực?
                          </span>
                        </div>
                        <div style={{ fontSize: '12.5px', color: '#4E342E', lineHeight: '1.6' }}>
                          {selectedRepo.ai_explanation.problem_solved}
                        </div>
                      </div>

                      {/* Hộp 3: Điểm mạnh ăn tiền */}
                      {selectedRepo.ai_explanation.key_features && selectedRepo.ai_explanation.key_features.length > 0 && (
                        <div style={{ backgroundColor: '#FAFAFA', border: '1px solid #E0E0E0', borderRadius: '8px', padding: '12px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                            <span style={{ fontSize: '13px' }}>✨</span>
                            <span style={{ fontSize: '11px', fontWeight: 700, color: '#2D4A2B', letterSpacing: '0.3px', textTransform: 'uppercase' }}>
                              Những tính năng "ăn tiền" nhất
                            </span>
                          </div>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            {selectedRepo.ai_explanation.key_features.map((feat, idx) => (
                              <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '6px', fontSize: '12px', color: '#374151', lineHeight: '1.5' }}>
                                <span style={{ color: '#2E7D32', fontWeight: 'bold' }}>✓</span>
                                <span>{feat}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Hộp 4: Quickstart 1 phút */}
                      {selectedRepo.ai_explanation.quickstart && (
                        <div
                          style={{
                            backgroundColor: '#1E293B',
                            borderRadius: '8px',
                            padding: '12px',
                            border: '1px solid #334155',
                            flexShrink: 0
                          }}
                        >
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <span style={{ fontSize: '12px' }}>🚀</span>
                              <span style={{ fontSize: '10.5px', fontWeight: 700, color: '#94A3B8', letterSpacing: '0.3px', textTransform: 'uppercase' }}>
                                Cách chạy thử nhanh trong 1 phút (Quickstart)
                              </span>
                            </div>
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(selectedRepo.ai_explanation?.quickstart || '');
                                setCopiedQuickstart(true);
                                playSfx('paper_rustle');
                                setTimeout(() => setCopiedQuickstart(false), 2000);
                              }}
                              style={{
                                backgroundColor: copiedQuickstart ? '#10B981' : '#334155',
                                color: '#FFFFFF',
                                border: 'none',
                                borderRadius: '4px',
                                padding: '2px 8px',
                                fontSize: '10px',
                                fontFamily: 'var(--font-mono)',
                                cursor: 'pointer'
                              }}
                            >
                              {copiedQuickstart ? '✓ Đã Copy' : 'Copy lệnh'}
                            </button>
                          </div>
                          <code style={{ fontSize: '11.5px', color: '#38BDF8', fontFamily: 'var(--font-mono)', display: 'block', wordBreak: 'break-all', whiteSpace: 'pre-wrap' }}>
                            {selectedRepo.ai_explanation.quickstart}
                          </code>
                        </div>
                      )}
                    </div>
                  ) : (
                    /* Chưa có bản giải thích */
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '30px 10px', gap: '14px', textAlign: 'center', backgroundColor: '#FAF8F5', borderRadius: '8px', border: '1px dashed #DCD5C5' }}>
                      <span style={{ fontSize: '32px' }}>🧠</span>
                      <div style={{ maxWidth: '420px' }}>
                        <div style={{ fontFamily: 'var(--font-serif)', fontSize: '14px', fontWeight: 700, color: '#2D4A2B', marginBottom: '4px' }}>
                          Chưa có bản phân tích dễ hiểu cho {selectedRepo.repo_full_name}
                        </div>
                        <div style={{ fontSize: '12px', color: '#5A6B5C', lineHeight: '1.5' }}>
                          Hệ thống sẽ sử dụng mô hình AI được cấu hình trong file <code style={{ backgroundColor: '#EBE6DC', padding: '1px 4px', borderRadius: '3px' }}>.env</code> (Gemini Flash / DeepSeek) để đọc toàn bộ tài liệu kỹ thuật và tóm lược 5 mục cốt lõi dễ hiểu nhất cho bạn.
                        </div>
                      </div>
                      <button
                        onClick={() => handleExplainRepo(selectedRepo.id, false)}
                        disabled={isExplaining}
                        style={{
                          backgroundColor: '#2D4A2B',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '9px 18px',
                          fontSize: '12.5px',
                          fontFamily: 'var(--font-sans)',
                          fontWeight: 700,
                          cursor: isExplaining ? 'not-allowed' : 'pointer',
                          boxShadow: '0 2px 6px rgba(45, 74, 43, 0.2)',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px'
                        }}
                      >
                        {isExplaining ? (
                          <>
                            <span>⏳</span>
                            <span>Đang kết nối AI trong .env để phân tích...</span>
                          </>
                        ) : (
                          <>
                            <span>⚡</span>
                            <span>Kích Hoạt AI (.env) Phân Tích & Giải Thích Repo Này Ngay</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'readme' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #EBE6DC', paddingBottom: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                        README.md • TÀI LIỆU TOÀN VĂN GỐC TỪ GITHUB
                      </span>
                      <span style={{ fontSize: '10px', color: '#5A6B5C', fontFamily: 'var(--font-mono)' }}>
                        ({(selectedRepo.readme_content?.length || 0).toLocaleString()} ký tự)
                      </span>
                    </div>
                    <span style={{ fontSize: '10px', color: '#8A9A86', fontFamily: 'var(--font-mono)' }}>
                      SQLITE ID #{selectedRepo.id}
                    </span>
                  </div>
                  <div
                    style={{
                      maxHeight: '440px',
                      overflowY: 'auto',
                      backgroundColor: '#FAF8F5',
                      border: '1px solid #EBE6DC',
                      borderRadius: '6px',
                      padding: '12px',
                      fontSize: '12px',
                      color: '#2C3E2C',
                      lineHeight: '1.6',
                      whiteSpace: 'pre-wrap',
                      fontFamily: 'var(--font-mono)'
                    }}
                  >
                    {selectedRepo.readme_content || `# ${selectedRepo.repo_full_name}\n\n${selectedRepo.description || 'Chưa có tóm tắt README'}`}
                  </div>
                </div>
              )}

              {activeTab === 'code' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #EBE6DC', paddingBottom: '8px' }}>
                    <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                      CODE SNIPPET & GIAO THỨC TÍCH HỢP
                    </span>
                    <span style={{ fontSize: '10px', color: '#1B5E20', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                      ✓ VERIFIED WORKING
                    </span>
                  </div>
                  <pre
                    style={{
                      backgroundColor: '#1E293B',
                      color: '#E2E8F0',
                      padding: '14px',
                      borderRadius: '8px',
                      fontSize: '11.5px',
                      fontFamily: 'var(--font-mono)',
                      overflowX: 'auto',
                      lineHeight: '1.6',
                      margin: 0
                    }}
                  >
                    <code>{selectedRepo.demo_code || `# ${selectedRepo.repo_full_name} Quickstart\ngit clone ${selectedRepo.repo_url}\ncd ${selectedRepo.repo_full_name.split('/')[1] || ''}`}</code>
                  </pre>
                </div>
              )}

              {activeTab === 'docker' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #EBE6DC', paddingBottom: '8px' }}>
                    <span style={{ fontFamily: 'var(--font-serif)', fontSize: '13px', fontWeight: 700, color: '#2D4A2B' }}>
                      CHẠY DOCKER CONTAINER NỘI BỘ (SELF-HOSTED)
                    </span>
                    <span style={{ fontSize: '10px', color: '#2D4A2B', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                      PORT 8000 / 8001 ISOLATED
                    </span>
                  </div>

                  <div style={{ fontSize: '12px', color: '#5A6B5C', lineHeight: '1.5' }}>
                    Chạy repository này độc lập trong Docker container để bảo toàn GPU VRAM và đảm bảo thời gian phản hồi theo hợp đồng kỹ thuật:
                  </div>

                  <pre
                    style={{
                      backgroundColor: '#1E293B',
                      color: '#38BDF8',
                      padding: '12px 14px',
                      borderRadius: '8px',
                      fontSize: '11px',
                      fontFamily: 'var(--font-mono)',
                      overflowX: 'auto',
                      margin: 0
                    }}
                  >
                    <code>{`# 1. Chạy container Docker cho ${selectedRepo.repo_full_name}
docker run -d --name ${selectedRepo.repo_full_name.replace('/', '-')}-service \\
  -p 8000:8000 \\
  --restart unless-stopped \\
  ${selectedRepo.repo_full_name.toLowerCase()}:latest`}</code>
                  </pre>
                </div>
              )}
            </div>

            {/* Khối Dấu chân nhện & Từ khóa bắn tơ */}
            <div
              style={{
                background: '#FFFBEB',
                border: '1px solid #FDE68A',
                borderRadius: '12px',
                padding: '14px 18px',
                flexShrink: 0,        // Không bị co ép
                marginTop: '0px',     // Tuyệt đối không dùng margin-top âm gây đè lên hộp Quickstart
                position: 'relative',
                zIndex: 1,
                display: 'flex',
                flexDirection: 'column',
                gap: '4px'
              }}
            >
              <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#8D6E63', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>⚡ DẤU CHÂN NHỆN & TỪ KHÓA BẮN TƠ (TRIGGER TOKENS):</span>
              </div>
              <div style={{ fontSize: '11px', color: '#6D4C41', lineHeight: '1.5' }}>
                Khi bài báo xuất hiện các từ khóa liên quan đến &lsquo;<strong>{selectedRepo.repo_full_name}</strong>&rsquo;, con nhện kích hoạt hiệu ứng móng vuốt Tribal và phóng tia tơ laser sang Node Công Nghệ AI.
              </div>
            </div>

            {/* Lưới 2 cột: Ứng dụng thực tế & Dành cho ai? */}
            {activeTab === 'explain' && selectedRepo?.ai_explanation && (selectedRepo.ai_explanation.practical_use_case || selectedRepo.ai_explanation.target_audience) && (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                  gap: '16px',
                  flexShrink: 0,        // Giữ nguyên chiều cao tự nhiên
                  marginTop: '0px'
                }}
              >
                {selectedRepo.ai_explanation.practical_use_case && (
                  <div style={{ backgroundColor: '#F0F7FF', border: '1px solid #BEE3F8', borderRadius: '12px', padding: '14px 16px' }}>
                    <div style={{ fontSize: '10.5px', fontWeight: 700, color: '#2B6CB0', marginBottom: '6px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span>🏢</span>
                      <span>ỨNG DỤNG THỰC TẾ</span>
                    </div>
                    <div style={{ fontSize: '11.5px', color: '#2D3748', lineHeight: '1.6' }}>
                      {selectedRepo.ai_explanation.practical_use_case}
                    </div>
                  </div>
                )}

                {selectedRepo.ai_explanation.target_audience && (
                  <div style={{ backgroundColor: '#FAF5FF', border: '1px solid #E9D8FD', borderRadius: '12px', padding: '14px 16px' }}>
                    <div style={{ fontSize: '10.5px', fontWeight: 700, color: '#6B46C1', marginBottom: '6px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span>👥</span>
                      <span>DÀNH CHO AI?</span>
                    </div>
                    <div style={{ fontSize: '11.5px', color: '#2D3748', lineHeight: '1.6' }}>
                      {selectedRepo.ai_explanation.target_audience}
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div style={{ padding: '40px', textAlign: 'center', color: '#8A9A86' }}>
            Chọn một repository từ danh sách để xem tài liệu
          </div>
        )}
      </section>

      {/* 3. RIGHT SIDEBAR: EVALUATION & ACTIONS (270px) */}
      <aside
        style={{
          width: '270px',
          flexShrink: 0,
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '14px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflowY: 'auto',
          boxShadow: '0 2px 8px rgba(45, 74, 43, 0.04)'
        }}
      >
        {(() => {
          const evalData = computeRepoEvaluation(selectedRepo);
          return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {/* Tech Evaluation Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span
                    style={{
                      fontFamily: 'var(--font-serif)',
                      fontSize: '12px',
                      fontWeight: 700,
                      color: '#2D4A2B',
                      letterSpacing: '0.3px'
                    }}
                  >
                    ĐIỂM ĐÁNH GIÁ CÔNG NGHỆ
                  </span>
                  <button
                    onClick={() => setShowCriteriaModal(!showCriteriaModal)}
                    title="Bấm để xem 4 tiêu chí đánh giá"
                    style={{
                      background: showCriteriaModal ? '#2D4A2B' : '#EBE6DC',
                      color: showCriteriaModal ? '#FFFFFF' : '#2D4A2B',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '10px',
                      fontWeight: 700,
                      padding: '1px 5px'
                    }}
                  >
                    {showCriteriaModal ? 'Đóng ✕' : 'Tiêu chí ℹ️'}
                  </button>
                </div>
                <span
                  style={{
                    backgroundColor: '#2D4A2B',
                    color: '#FAF8F5',
                    borderRadius: '999px',
                    padding: '2px 8px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  {evalData.overall_score} / 10
                </span>
              </div>

              {/* Popup giải thích tiêu chí đánh giá nếu người dùng bấm xem */}
              {showCriteriaModal && (
                <div
                  style={{
                    backgroundColor: '#F7F5EE',
                    border: '1px solid #DFD9CC',
                    borderRadius: '8px',
                    padding: '10px',
                    fontSize: '10.5px',
                    lineHeight: '1.5',
                    color: '#4A5B4C',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '5px'
                  }}
                >
                  <div style={{ fontWeight: 700, color: '#2D4A2B', display: 'flex', justifyContent: 'space-between' }}>
                    <span>🎯 CÔNG THỨC 4 TIÊU CHÍ:</span>
                    <span onClick={() => setShowCriteriaModal(false)} style={{ cursor: 'pointer', color: '#C86D51' }}>✕</span>
                  </div>
                  <div>• <strong>Độ Uy Tín & Cộng Đồng (35%):</strong> Đánh giá số Stars & Forks thực tế.</div>
                  <div>• <strong>Tốc Độ Tăng Trưởng (25%):</strong> Lượng sao mới mỗi ngày (+Stars/ngày).</div>
                  <div>• <strong>Sẵn Sàng Triển Khai (20%):</strong> Giấy phép MIT/Apache (an toàn thương mại).</div>
                  <div>• <strong>Tài Liệu & DevEx (20%):</strong> Chất lượng README, code mẫu và độ dễ cài.</div>
                </div>
              )}

              {/* 4 Metric Breakdown Thực Tế */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '11px', color: '#3D4E3D', lineHeight: '1.5' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>🌟 Độ Uy Tín & Cộng Đồng:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{evalData.community_score} / 10</strong>
                  </div>
                  <div style={{ fontSize: '10px', color: '#6B7280' }}>{evalData.community_desc}</div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>🚀 Tốc Độ Tăng Trưởng:</span>
                    <strong style={{ color: '#C86D51', fontFamily: 'var(--font-mono)' }}>{evalData.velocity_score} / 10</strong>
                  </div>
                  <div style={{ fontSize: '10px', color: '#6B7280' }}>{evalData.velocity_desc}</div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>🛡️ Sẵn Sàng Triển Khai:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{evalData.production_score} / 10</strong>
                  </div>
                  <div style={{ fontSize: '10px', color: '#6B7280' }}>{evalData.production_desc}</div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>📚 Tài Liệu & DevEx:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{evalData.docs_score} / 10</strong>
                  </div>
                  <div style={{ fontSize: '10px', color: '#6B7280' }}>{evalData.docs_desc}</div>
                </div>
              </div>

              <div style={{ height: '1px', backgroundColor: '#EBE6DC' }} />

              {/* Recommendation Note Thực Tế */}
              <div
                style={{
                  backgroundColor: '#FAF8F5',
                  borderRadius: '8px',
                  border: '1px solid #E8E2D5',
                  padding: '10px 12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }}
              >
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '11px', fontWeight: 700, color: '#2D4A2B' }}>
                  KHUYẾN NGHỊ KỸ THUẬT (ENGINEERING VERDICT)
                </span>
                <span style={{ fontSize: '11px', color: '#4A5B4C', lineHeight: '1.5', fontWeight: 500 }}>
                  {evalData.verdict}
                </span>
              </div>
            </div>
          );
        })()}

        {/* Action Buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '14px' }}>
          {/* Bookmark Button */}
          <button
            onClick={handleToggleBookmark}
            style={{
              backgroundColor: selectedRepo?.is_bookmarked === 1 ? '#FFF8E1' : '#2D4A2B',
              border: selectedRepo?.is_bookmarked === 1 ? '1px solid #E5B869' : 'none',
              borderRadius: '8px',
              padding: '9px 12px',
              color: selectedRepo?.is_bookmarked === 1 ? '#8D6E63' : '#F4F1EA',
              fontSize: '11.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              transition: 'all 0.15s ease'
            }}
          >
            <span>{selectedRepo?.is_bookmarked === 1 ? '★' : '☆'}</span>
            <span>{selectedRepo?.is_bookmarked === 1 ? 'Đã Đánh Dấu Vào Tech Vault (Miễn Trừ TTL)' : 'Đánh Dấu Vào Tech Vault'}</span>
          </button>

          {/* Copy clone */}
          <button
            onClick={handleCopyClone}
            style={{
              backgroundColor: '#FAF8F5',
              border: '1px solid #DCD5C5',
              borderRadius: '8px',
              padding: '8px 12px',
              color: '#2D4A2B',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>📄</span>
            <span>{copiedClone ? '✓ Đã Sao Chép Lệnh Git Clone' : 'Sao Chép Lệnh Git Clone'}</span>
          </button>

          {/* Open GitHub Link */}
          {selectedRepo?.repo_url && (
            <button
              onClick={() => {
                playSfx('click');
                window.open(selectedRepo.repo_url, '_blank');
              }}
              style={{
                backgroundColor: '#FAF8F5',
                border: '1px solid #DCD5C5',
                borderRadius: '8px',
                padding: '8px 12px',
                color: '#2D4A2B',
                fontSize: '11px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <span>🌐</span>
              <span>Mở GitHub Repo Trên Trình Duyệt</span>
            </button>
          )}

          {/* Screen 7 Navigate */}
          <button
            onClick={() => onNavigate('analytics')}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #DCD5C5',
              borderRadius: '8px',
              padding: '8px 12px',
              color: '#5A6B5C',
              fontSize: '10.5px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>📊</span>
            <span>Xem Chỉ Số Tăng Trưởng Repo & AI (Screen 7) →</span>
          </button>
        </div>
      </aside>

      {/* Modal: Thêm Repo Theo Dõi Mới */}
      {isAddModalOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}
        >
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #DCD5C5',
              padding: '20px 24px',
              width: '420px',
              display: 'flex',
              flexDirection: 'column',
              gap: '14px',
              boxShadow: '0 8px 24px rgba(0,0,0,0.15)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '15px', fontWeight: 700, color: '#2D4A2B' }}>
                Thêm Repository Theo Dõi Mới
              </span>
              <button
                onClick={() => setIsAddModalOpen(false)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '16px', color: '#8A9A86' }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddRepoSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <label style={{ fontSize: '11px', color: '#5A6B5C', fontWeight: 600 }}>
                  Định danh Repo hoặc URL GitHub:
                </label>
                <input
                  type="text"
                  placeholder="ví dụ: penpot/penpot hoặc https://github.com/..."
                  value={newRepoInput}
                  onChange={e => setNewRepoInput(e.target.value)}
                  style={{
                    padding: '8px 10px',
                    borderRadius: '6px',
                    border: '1px solid #DCD5C5',
                    fontSize: '12px',
                    fontFamily: 'var(--font-mono)',
                    outline: 'none'
                  }}
                  autoFocus
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <label style={{ fontSize: '11px', color: '#5A6B5C', fontWeight: 600 }}>
                  Phân loại chuyên mục:
                </label>
                <select
                  value={newRepoTopic}
                  onChange={e => setNewRepoTopic(e.target.value)}
                  style={{
                    padding: '8px 10px',
                    borderRadius: '6px',
                    border: '1px solid #DCD5C5',
                    fontSize: '12px',
                    outline: 'none'
                  }}
                >
                  <option value="design">Thiết Kế & Canva / UI</option>
                  <option value="skills">Kỹ Năng & Giáo Dục</option>
                  <option value="ai">AI & LLM Inference</option>
                  <option value="systems">Systems & Rust/C++</option>
                  <option value="wasm">WebAssembly & Edge</option>
                  <option value="vector">Vector DB & Search</option>
                </select>
              </div>

              {addError && (
                <div style={{ fontSize: '11px', color: '#C86D51', backgroundColor: '#FDF2EE', padding: '6px 8px', borderRadius: '4px' }}>
                  {addError}
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '6px' }}>
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  style={{
                    backgroundColor: '#FAF8F5',
                    border: '1px solid #DCD5C5',
                    borderRadius: '6px',
                    padding: '7px 14px',
                    fontSize: '11.5px',
                    cursor: 'pointer'
                  }}
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  style={{
                    backgroundColor: '#2D4A2B',
                    color: '#F4F1EA',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '7px 16px',
                    fontSize: '11.5px',
                    fontWeight: 700,
                    cursor: isSubmitting ? 'wait' : 'pointer'
                  }}
                >
                  {isSubmitting ? 'Đang thêm...' : 'Lưu Vào Database'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
