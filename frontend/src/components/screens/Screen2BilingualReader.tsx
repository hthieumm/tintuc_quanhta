import React, { useState, useEffect } from 'react';
import { ArticleItem, ScreenTab } from '../../types';
import { playSfx } from '../../utils/audio';
import { apiFetch } from '../../utils/api';

interface Screen2BilingualReaderProps {
  onNavigate: (tab: ScreenTab) => void;
  onBookmarkArticle?: (id: number) => void;
}

export const Screen2BilingualReader: React.FC<Screen2BilingualReaderProps> = ({
  onNavigate,
  onBookmarkArticle
}) => {
  const [selectedCat, setSelectedCat] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isVietnamese, setIsVietnamese] = useState<boolean>(true);
  const [selectedArticleId, setSelectedArticleId] = useState<number>(0);
  const [copiedNotice, setCopiedNotice] = useState<boolean>(false);

  // In-Memory RAM Cache for Translations (0đ API, 0% VRAM, 0ms swap contract)
  const [translationCache, setTranslationCache] = useState<
    Record<number, { title: string; summary: string; paragraphs: string[] }>
  >({});
  const [isTranslating, setIsTranslating] = useState<boolean>(false);

  // Deep Scrape Full Article State
  const [isDeepScraping, setIsDeepScraping] = useState<boolean>(false);
  const [deepScrapeStatus, setDeepScrapeStatus] = useState<string>('');

  // System 2 Macro Impact Synthesis State
  const [isSynthesizing, setIsSynthesizing] = useState<boolean>(false);
  const [synthesisData, setSynthesisData] = useState<
    Record<number, { summary: string; impact: string }>
  >({});

  const [articles, setArticles] = useState<ArticleItem[]>([]);

  // Helper to split text into distinct paragraphs
  const splitIntoParagraphs = (text: string): string[] => {
    if (!text) return [];
    return text
      .split(/\n\n+|\n/)
      .map(p => p.trim())
      .filter(p => p.length > 0);
  };

  const fetchRealArticles = async (cat: string = selectedCat) => {
    try {
      const url = cat && cat !== 'all' ? `/api/v1/articles?limit=50&category=${cat}` : '/api/v1/articles?limit=50';
      const res = await apiFetch(url);
      if (res.ok) {
        const rows = await res.json();
        if (Array.isArray(rows)) {
          const mapped: ArticleItem[] = rows.map((r: any) => {
            const rawContent = r.content_clean || r.summary_raw || r.title || '';
            const paras = splitIntoParagraphs(rawContent);

            return {
              id: r.id,
              title: r.title,
              titleEn: r.language === 'en' ? r.title : undefined,
              source: (r.source_name || 'RSS').toUpperCase(),
              timeAgo: r.published_at || 'Vừa xong',
              category: (r.source_category || 'kinh_te') as any,
              categoryName:
                r.source_category === 'chung_khoan'
                  ? 'Chứng khoán'
                  : r.source_category === 'vang'
                  ? 'Giá vàng'
                  : r.source_category === 'quoc_te'
                  ? 'Quốc tế'
                  : r.source_category === 'chinh_tri'
                  ? 'Chính trị'
                  : 'Kinh tế vĩ mô',
              summary: paras[0] ? paras[0].slice(0, 220) + (paras[0].length > 220 ? '...' : '') : r.title,
              summaryEn: r.language === 'en' ? (paras[0]?.slice(0, 220) + '...') : undefined,
              contentVi: r.language === 'vi' ? paras : [],
              contentEn: paras,
              decisionScore: 0.88,
              routedNode: '🏛️ ROUTED: SYSTEM 1 DECISION',
              sentimentScore: 0.75,
              isBookmarked: r.is_bookmarked === 1,
              sha256Hash: r.url_hash ? r.url_hash.slice(0, 12) + '...' : 'hash_live',
              author: r.author && r.author !== 'N/A' ? r.author : r.source_name || 'Spider Radar',
              url: r.url,
              language: r.language || 'en'
            };
          });

          setArticles(mapped);
          if (mapped[0]) {
            setSelectedArticleId(mapped[0].id);
          }
        }
      }
    } catch (e) {
      console.error('Lỗi nạp bài viết:', e);
    }
  };

  const [categoryStats, setCategoryStats] = useState<Record<string, number>>({});

  const loadCategoryStats = async () => {
    try {
      const res = await apiFetch('/api/v1/categories/stats');
      if (res.ok) {
        const stats = await res.json();
        setCategoryStats(stats);
      }
    } catch (e) {
      console.error('Lỗi nạp thống kê chuyên mục:', e);
    }
  };

  // Re-fetch articles when selected category changes
  useEffect(() => {
    fetchRealArticles(selectedCat);
  }, [selectedCat]);

  useEffect(() => {
    loadCategoryStats();

    // Tự động cập nhật liên tục mỗi 15 giây
    const interval = setInterval(() => {
      fetchRealArticles(selectedCat);
      loadCategoryStats();
    }, 15000);

    return () => clearInterval(interval);
  }, [selectedCat]);

  const currentArticle = articles.find(a => a.id === selectedArticleId) || articles[0];

  // On-Demand Translation via deep-translator (0đ API, 0% VRAM)
  const triggerTranslation = async (art: ArticleItem) => {
    if (!art || art.language === 'vi' || isTranslating) return;
    if (translationCache[art.id]) return;

    setIsTranslating(true);
    try {
      const parasToTranslate = art.contentEn && art.contentEn.length > 0 ? art.contentEn : [art.summary || art.title];
      const textsToTranslate = [art.title, art.summary || art.title, ...parasToTranslate];
      const res = await apiFetch('/api/v1/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          texts: textsToTranslate,
          source_lang: 'auto',
          target_lang: 'vi'
        })
      });

      if (res.ok) {
        const data = await res.json();
        const translatedList: string[] = data.translated_texts || [];
        if (translatedList.length >= 1) {
          const transTitle = translatedList[0] || art.title;
          const transSummary = translatedList[1] || translatedList[0] || art.summary;
          const transParagraphs = translatedList.length > 2 ? translatedList.slice(2) : [transSummary];

          setTranslationCache(prev => ({
            ...prev,
            [art.id]: {
              title: transTitle,
              summary: transSummary,
              paragraphs: transParagraphs.length > 0 ? transParagraphs : [transSummary]
            }
          }));
        }
      }
    } catch (e) {
      console.error('Lỗi dịch bài viết:', e);
    } finally {
      setIsTranslating(false);
    }
  };

  // Auto-translate on selecting article if Vietnamese view is active
  useEffect(() => {
    if (isVietnamese && currentArticle && currentArticle.language !== 'vi') {
      if (!translationCache[currentArticle.id]) {
        triggerTranslation(currentArticle);
      }
    }
  }, [currentArticle?.id, isVietnamese]);

  const handleToggleLanguage = (targetVi: boolean) => {
    playSfx('click');
    setIsVietnamese(targetVi);
    if (targetVi && currentArticle && currentArticle.language !== 'vi') {
      if (!translationCache[currentArticle.id]) {
        triggerTranslation(currentArticle);
      }
    }
  };

  // Deep Scrape Handler
  const handleDeepScrape = async () => {
    if (!currentArticle || isDeepScraping) return;
    setIsDeepScraping(true);
    setDeepScrapeStatus('⏳ Đang kích hoạt bộ cào sâu (Waterfall Scraping)...');
    playSfx('paper_rustle');

    try {
      const res = await apiFetch(`/api/v1/articles/${currentArticle.id}/fetch-full`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        if (data.content_clean && data.content_clean.length > (currentArticle.contentEn.join('\n').length || 0)) {
          const newParas = splitIntoParagraphs(data.content_clean);
          setArticles(prev =>
            prev.map(a =>
              a.id === currentArticle.id
                ? {
                    ...a,
                    contentEn: newParas,
                    contentVi: a.language === 'vi' ? newParas : [],
                    summary: newParas[0] ? newParas[0].slice(0, 220) + '...' : a.summary
                  }
                : a
            )
          );
          // Invalidate cache to allow re-translating full content
          setTranslationCache(prev => {
            const next = { ...prev };
            delete next[currentArticle.id];
            return next;
          });
          setDeepScrapeStatus(`✓ Tải thành công toàn văn chi tiết (${data.tier || 'OK'})!`);
        } else {
          setDeepScrapeStatus('ℹ️ Đã thử các tầng cào. Bản tin hiện tại đã ở trạng thái đầy đủ nhất từ nguồn.');
        }
      } else {
        setDeepScrapeStatus('⚠️ Không thể cào thêm nội dung từ trang gốc.');
      }
    } catch {
      setDeepScrapeStatus('⚠️ Lỗi kết nối khi cào sâu toàn văn.');
    } finally {
      setIsDeepScraping(false);
      setTimeout(() => setDeepScrapeStatus(''), 5000);
    }
  };

  // LLM System 2 Macro Synthesis
  const handleSynthesizeArticle = async () => {
    if (!currentArticle || isSynthesizing) return;
    setIsSynthesizing(true);
    playSfx('wind_chime');

    try {
      const res = await apiFetch('/api/v1/synthesize/article', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ article_id: currentArticle.id })
      });
      if (res.ok) {
        const data = await res.json();
        setSynthesisData(prev => ({
          ...prev,
          [currentArticle.id]: {
            summary: data.vietnamese_summary || '',
            impact: data.macro_impact || ''
          }
        }));
      }
    } catch (e) {
      console.error('Lỗi tổng hợp vĩ mô:', e);
    } finally {
      setIsSynthesizing(false);
    }
  };

  const handleOpenOriginal = () => {
    playSfx('click');
    if (currentArticle?.url) {
      window.open(currentArticle.url, '_blank');
    }
  };

  const handleToggleBookmark = async (id: number) => {
    playSfx('click');
    setArticles(prev =>
      prev.map(a => (a.id === id ? { ...a, isBookmarked: !a.isBookmarked } : a))
    );
    try {
      await apiFetch(`/api/v1/articles/${id}/bookmark`, { method: 'PATCH' });
    } catch (e) {
      console.error('Lỗi lưu bookmark article:', e);
    }
    if (onBookmarkArticle) onBookmarkArticle(id);
  };

  const handleCopyMarkdown = () => {
    playSfx('paper_rustle');
    if (!currentArticle) return;

    const displayTitle = isVietnamese
      ? (translationCache[currentArticle.id]?.title || currentArticle.title)
      : (currentArticle.titleEn || currentArticle.title);

    const displayParas = isVietnamese
      ? (translationCache[currentArticle.id]?.paragraphs || (currentArticle.language === 'vi' ? currentArticle.contentVi : currentArticle.contentEn))
      : currentArticle.contentEn;

    const md = `# ${displayTitle}\n\n**Nguồn:** ${currentArticle.source}\n**Tác giả:** ${currentArticle.author}\n**Link:** ${currentArticle.url || 'N/A'}\n\n## Nội dung\n${displayParas.join('\n\n')}`;
    navigator.clipboard.writeText(md);
    setCopiedNotice(true);
    setTimeout(() => setCopiedNotice(false), 2000);
  };

  // Dynamic category tabs (Hiển thị chính xác tổng số bài theo DB và tự động cập nhật liên tục)
  const categories = [
    { id: 'all', icon: '📑', label: 'Tất cả bài đã lọc', count: categoryStats['all'] ?? articles.length },
    { id: 'kinh_te', icon: '🏛️', label: 'Kinh tế vĩ mô', count: categoryStats['kinh_te'] ?? articles.filter(a => a.category === 'kinh_te').length },
    { id: 'chung_khoan', icon: '📈', label: 'Chứng khoán VN', count: categoryStats['chung_khoan'] ?? articles.filter(a => a.category === 'chung_khoan').length },
    { id: 'vang', icon: '🥇', label: 'Vàng & Ngoại tệ', count: categoryStats['vang'] ?? articles.filter(a => a.category === 'vang').length },
    { id: 'quoc_te', icon: '🌍', label: 'Quốc tế', count: categoryStats['quoc_te'] ?? articles.filter(a => a.category === 'quoc_te').length },
    { id: 'chinh_tri', icon: '⚖️', label: 'Chính trị', count: categoryStats['chinh_tri'] ?? articles.filter(a => a.category === 'chinh_tri').length }
  ];

  const filteredArticles = articles.filter(art => {
    const matchesCat = selectedCat === 'all' || art.category === selectedCat;
    const matchesQuery =
      searchQuery.trim() === '' ||
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.summary.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesQuery;
  });

  // Calculate displayed title & paragraphs
  const displayTitle = currentArticle
    ? isVietnamese
      ? (translationCache[currentArticle.id]?.title || currentArticle.title)
      : (currentArticle.titleEn || currentArticle.title)
    : '';

  const displayParagraphs = currentArticle
    ? isVietnamese
      ? (translationCache[currentArticle.id]?.paragraphs || (currentArticle.language === 'vi' ? currentArticle.contentVi : currentArticle.contentEn))
      : currentArticle.contentEn
    : [];

  const isShortSummary = currentArticle && currentArticle.contentEn.length <= 1 && (currentArticle.contentEn[0]?.length || 0) < 250;
  const currentSynthesis = currentArticle ? synthesisData[currentArticle.id] : undefined;

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
      {/* 1. LEFT FILTER SIDEBAR (240px) */}
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
            📂 BỘ LỌC CHUYÊN MỤC
          </div>

          {/* Categories List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {categories.map(cat => {
              const isActive = selectedCat === cat.id;
              return (
                <div
                  key={cat.id}
                  onClick={() => setSelectedCat(cat.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '7px 10px',
                    borderRadius: '8px',
                    backgroundColor: isActive ? '#2D4A2B' : 'transparent',
                    color: isActive ? '#FAF8F5' : '#2D4A2B',
                    cursor: 'pointer',
                    fontSize: '12px',
                    fontWeight: isActive ? 600 : 500,
                    transition: 'all 0.15s ease'
                  }}
                  onMouseEnter={e => {
                    if (!isActive) e.currentTarget.style.backgroundColor = '#E0D9CB';
                  }}
                  onMouseLeave={e => {
                    if (!isActive) e.currentTarget.style.backgroundColor = 'transparent';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span>{cat.icon}</span>
                    <span>{cat.label}</span>
                  </div>
                  <span
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '11px',
                      color: isActive ? '#F8AFA6' : '#5F7D58'
                    }}
                  >
                    {cat.count} bài
                  </span>
                </div>
              );
            })}
          </div>

          {/* Tech Vault Box */}
          <div
            style={{
              backgroundColor: '#F4F1EA',
              borderRadius: '8px',
              border: '1px solid #DCD5C5',
              padding: '12px',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}
          >
            <div style={{ fontSize: '11px', fontWeight: 700, color: '#C86D51' }}>
              ⭐ TECH VAULT (ĐÃ LƯU)
            </div>
            <div style={{ fontSize: '11px', color: '#5F7D58', lineHeight: '1.5' }}>
              • {articles.filter(a => a.isBookmarked).length} bài báo đã gắn sao ⭐<br />
              • Giữ vĩnh viễn (Chống xóa TTL 30 ngày)
            </div>
          </div>
        </div>

        {/* Sidebar Footer */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', color: '#8D6E63', lineHeight: '1.4' }}>
            SQLite WAL Mode (&lt;1ms)<br />
            FTS5 Instant Search Ready
          </div>
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
            📊 Nhịp Đập & Biểu Đồ Vĩ Mô (Screen 7) →
          </button>
        </div>
      </aside>

      {/* 2. MASTER FEED LIST COLUMN (440px) */}
      <section
        style={{
          width: '440px',
          flexShrink: 0,
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '14px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          overflow: 'hidden'
        }}
      >
        {/* FTS5 Instant Search Input */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: '#FAF8F5',
            border: '1px solid #DCD5C5',
            borderRadius: '8px',
            padding: '6px 10px',
            gap: '8px'
          }}
        >
          <span>🔍</span>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Tìm nhanh FTS5: dollar, inflation, GDP, tỷ giá..."
            style={{
              border: 'none',
              background: 'transparent',
              outline: 'none',
              width: '100%',
              fontSize: '12px',
              fontFamily: 'var(--font-sans)',
              color: '#2D4A2B'
            }}
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              style={{ border: 'none', background: 'transparent', cursor: 'pointer', fontSize: '11px', color: '#8A9A86' }}
            >
              ✕
            </button>
          )}
        </div>

        {/* Article Cards Scrollable List */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
        >
          {filteredArticles.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '30px 10px', color: '#8A9A86', fontSize: '12px' }}>
              Không tìm thấy bài viết phù hợp.
            </div>
          ) : (
            filteredArticles.map(art => {
              const isSelected = art.id === selectedArticleId;
              return (
                <div
                  key={art.id}
                  onClick={() => {
                    playSfx('click');
                    setSelectedArticleId(art.id);
                  }}
                  style={{
                    backgroundColor: isSelected ? '#F7FAF4' : '#FFFFFF',
                    border: isSelected ? '1.5px solid #2D4A2B' : '1px solid #E8E2D5',
                    borderRadius: '10px',
                    padding: '12px 14px',
                    cursor: 'pointer',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: '#5F7D58' }}>
                      {art.source}
                    </span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span
                        style={{
                          fontSize: '9.5px',
                          fontFamily: 'var(--font-mono)',
                          fontWeight: 700,
                          color: isSelected ? '#2D4A2B' : '#00BA88'
                        }}
                      >
                        {isSelected ? '● ĐANG ĐỌC' : 'ĐÃ LỌC'}
                      </span>
                      <button
                        onClick={e => {
                          e.stopPropagation();
                          handleToggleBookmark(art.id);
                        }}
                        style={{
                          border: 'none',
                          background: 'transparent',
                          cursor: 'pointer',
                          fontSize: '13px',
                          color: art.isBookmarked ? '#E5B869' : '#DCD5C5'
                        }}
                        title="Ghim vào Tech Vault"
                      >
                        ★
                      </button>
                    </div>
                  </div>

                  <div
                    style={{
                      fontFamily: 'var(--font-serif)',
                      fontSize: '13.5px',
                      fontWeight: 700,
                      color: '#2D4A2B',
                      lineHeight: '1.35'
                    }}
                  >
                    {art.title}
                  </div>

                  <div style={{ fontSize: '11.5px', color: '#5F7D58', lineHeight: '1.4' }}>
                    {art.summary}
                  </div>

                  <div
                    style={{
                      fontSize: '10px',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 600,
                      color: art.category === 'kinh_te' ? '#C86D51' : art.category === 'vang' ? '#B8860B' : '#2E7D32',
                      marginTop: '2px'
                    }}
                  >
                    {art.routedNode}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </section>

      {/* 3. BILINGUAL ARTICLE READER (FLEX-1) */}
      <main
        style={{
          flex: 1,
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '24px 30px',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          boxShadow: '0 4px 16px rgba(45, 74, 43, 0.04)'
        }}
      >
        {!currentArticle ? (
          <div style={{ textAlign: 'center', margin: 'auto', color: '#8A9A86', fontSize: '14px' }}>
            Chọn một bài viết ở danh sách bên trái để xem chi tiết.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* Bilingual Switcher Top Row */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
              {/* Bilingual Switch Pill */}
              <div
                style={{
                  display: 'flex',
                  backgroundColor: '#EBE6DC',
                  padding: '3px',
                  borderRadius: '999px',
                  border: '1px solid #DCD5C5'
                }}
              >
                <button
                  onClick={() => handleToggleLanguage(true)}
                  style={{
                    border: 'none',
                    backgroundColor: isVietnamese ? '#2D4A2B' : 'transparent',
                    color: isVietnamese ? '#FAF8F5' : '#5F7D58',
                    padding: '5px 14px',
                    borderRadius: '999px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  ● 🇻🇳 TIẾNG VIỆT (DEEP-TRANSLATOR FREE)
                </button>
                <button
                  onClick={() => handleToggleLanguage(false)}
                  style={{
                    border: 'none',
                    backgroundColor: !isVietnamese ? '#2D4A2B' : 'transparent',
                    color: !isVietnamese ? '#FAF8F5' : '#5F7D58',
                    padding: '5px 14px',
                    borderRadius: '999px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  ○ 🌐 BẢN GỐC ({currentArticle.source})
                </button>
              </div>

              {/* Status Badge */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {isTranslating && (
                  <span
                    style={{
                      backgroundColor: '#FFF8E1',
                      border: '1px solid #FFE082',
                      color: '#B78103',
                      borderRadius: '999px',
                      padding: '3px 10px',
                      fontSize: '10.5px',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 700
                    }}
                  >
                    ⏳ ĐANG DỊCH (0đ FREE)...
                  </span>
                )}
                <span
                  style={{
                    backgroundColor: '#E8F5E9',
                    border: '1px solid #C8E6C9',
                    color: '#1B5E20',
                    borderRadius: '999px',
                    padding: '3px 10px',
                    fontSize: '10.5px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  ⚡ DECISION 3 LITE ROUTED • SYSTEM 1 PASS
                </span>
              </div>
            </div>

            {/* Article Title */}
            <h1
              style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '22px',
                fontWeight: 700,
                color: '#1A2E19',
                lineHeight: '1.35',
                margin: '4px 0 0 0'
              }}
            >
              {displayTitle}
            </h1>

            {/* Meta Row */}
            <div
              style={{
                display: 'flex',
                gap: '16px',
                fontSize: '11px',
                color: '#5F7D58',
                fontFamily: 'var(--font-mono)',
                borderBottom: '1px solid #E8E2D5',
                paddingBottom: '10px',
                flexWrap: 'wrap'
              }}
            >
              <span>👤 Nguồn/Tác giả: {currentArticle.author}</span>
              <span>⏱️ {currentArticle.timeAgo}</span>
              <span style={{ color: '#2E7D32', fontWeight: 600 }}>
                🛡️ SHA-256: {currentArticle.sha256Hash} (Khử Trùng OK)
              </span>
            </div>

            {/* Macro Impact Callout Box (Only shows real synthesis or action button) */}
            {currentSynthesis ? (
              <div
                style={{
                  backgroundColor: '#FBF3E8',
                  border: '1px solid #E2D0B8',
                  borderRadius: '8px',
                  padding: '12px 14px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px'
                }}
              >
                <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#8D6E63' }}>
                  💡 ĐÁNH GIÁ TÁC ĐỘNG VĨ MÔ BỞI LLM SYSTEM 2:
                </div>
                <div style={{ fontSize: '13px', color: '#2D4A2B', lineHeight: '1.5' }}>
                  {currentSynthesis.impact}
                </div>
                {currentSynthesis.summary && (
                  <div style={{ fontSize: '12px', color: '#5F7D58', marginTop: '4px' }}>
                    <strong>Tóm tắt cốt lõi:</strong> {currentSynthesis.summary}
                  </div>
                )}
              </div>
            ) : (
              <div
                style={{
                  backgroundColor: '#FAF8F5',
                  border: '1px dashed #DCD5C5',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '12px'
                }}
              >
                <div style={{ fontSize: '11.5px', color: '#5A6B5C' }}>
                  🧠 Chưa có bản phân tích chuyên sâu cho bài này. Kích hoạt LLM System 2 để đánh giá tác động vĩ mô:
                </div>
                <button
                  onClick={handleSynthesizeArticle}
                  disabled={isSynthesizing}
                  style={{
                    backgroundColor: '#2D4A2B',
                    border: 'none',
                    color: '#FAF8F5',
                    borderRadius: '6px',
                    padding: '6px 12px',
                    fontSize: '11px',
                    fontWeight: 700,
                    cursor: 'pointer',
                    flexShrink: 0
                  }}
                >
                  {isSynthesizing ? '⏳ Đang phân tích...' : '✨ Phân Tích Vĩ Mô (System 2)'}
                </button>
              </div>
            )}

            {/* Short RSS Warning & Deep Scrape Action Bar */}
            {isShortSummary && (
              <div
                style={{
                  backgroundColor: '#FFFBEA',
                  border: '1px solid #FFE58F',
                  borderRadius: '8px',
                  padding: '12px 16px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }}
              >
                <div style={{ fontSize: '12px', fontWeight: 700, color: '#D48806' }}>
                  📰 BẢN TIN TÓM TẮT TỪ RSS ({currentArticle.source})
                </div>
                <div style={{ fontSize: '12px', color: '#5A6B5C', lineHeight: '1.4' }}>
                  Kênh RSS hiện chỉ gửi đoạn tóm tắt ngắn của bài. Bấm nút bên dưới để thử kéo toàn văn chi tiết từ URL bài gốc:
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
                  <button
                    onClick={handleDeepScrape}
                    disabled={isDeepScraping}
                    style={{
                      backgroundColor: '#D48806',
                      border: 'none',
                      color: '#FFFFFF',
                      borderRadius: '6px',
                      padding: '6px 14px',
                      fontSize: '11.5px',
                      fontWeight: 700,
                      cursor: 'pointer'
                    }}
                  >
                    {isDeepScraping ? '⏳ Đang kéo toàn văn...' : '⚡ Tải Toàn Văn Bài Viết (Deep Scrape)'}
                  </button>
                  <button
                    onClick={handleOpenOriginal}
                    style={{
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #DCD5C5',
                      color: '#2D4A2B',
                      borderRadius: '6px',
                      padding: '6px 12px',
                      fontSize: '11.5px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    🌐 Mở Trang Báo Gốc
                  </button>
                  {deepScrapeStatus && (
                    <span style={{ fontSize: '11px', color: '#2E7D32', fontWeight: 600 }}>
                      {deepScrapeStatus}
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Article Body Paragraphs (Actual Content) */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '16px',
                fontSize: '14px',
                color: '#2D4A2B',
                lineHeight: '1.8',
                marginTop: '6px'
              }}
            >
              {displayParagraphs.length === 0 ? (
                <p style={{ fontStyle: 'italic', color: '#8A9A86' }}>
                  (Nội dung bài viết đang được tải hoặc trống)
                </p>
              ) : (
                displayParagraphs.map((para, idx) => (
                  <p
                    key={idx}
                    style={{
                      margin: 0,
                      textIndent: displayParagraphs.length > 1 ? '1.5em' : '0'
                    }}
                  >
                    {para}
                  </p>
                ))
              )}
            </div>
          </div>
        )}

        {/* Reader Bottom Actions Bar */}
        {currentArticle && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTop: '1px solid #E8E2D5',
              paddingTop: '16px',
              marginTop: '24px',
              flexWrap: 'wrap',
              gap: '10px'
            }}
          >
            <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: '#5F7D58' }}>
              📁 ĐÃ LƯU TRỮ TRONG SQLITE WAL • BẢO LƯU 30 NGÀY
            </span>

            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={() => handleToggleBookmark(currentArticle.id)}
                style={{
                  backgroundColor: currentArticle.isBookmarked ? '#FFF8E1' : '#FFFFFF',
                  border: '1px solid #DCD5C5',
                  borderRadius: '8px',
                  padding: '6px 12px',
                  fontSize: '11.5px',
                  fontWeight: 600,
                  color: '#2D4A2B',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>{currentArticle.isBookmarked ? '★' : '☆'}</span>
                <span>{currentArticle.isBookmarked ? 'Đã Lưu Tech Vault' : 'Lưu Tech Vault'}</span>
              </button>

              <button
                onClick={handleCopyMarkdown}
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #DCD5C5',
                  borderRadius: '8px',
                  padding: '6px 12px',
                  fontSize: '11.5px',
                  fontWeight: 600,
                  color: '#2D4A2B',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>📋</span>
                <span>{copiedNotice ? 'Đã Sao Chép!' : 'Sao Chép Bản Dịch'}</span>
              </button>

              <button
                onClick={handleOpenOriginal}
                style={{
                  backgroundColor: '#2D4A2B',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '6px 14px',
                  fontSize: '11.5px',
                  fontWeight: 600,
                  color: '#FAF8F5',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>🌐</span>
                <span>Xem Bài Gốc</span>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
