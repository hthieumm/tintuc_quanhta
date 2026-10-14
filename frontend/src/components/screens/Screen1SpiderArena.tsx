import React, { useState, useEffect, useRef } from 'react';
import { PacingMode, ScreenTab, DecisionNode, SpiderSkinId } from '../../types';
import { playSfx } from '../../utils/audio';
import { apiFetch } from '../../utils/api';

interface Screen1SpiderArenaProps {
  onNavigate: (tab: ScreenTab) => void;
  pacingMode: PacingMode;
  onPacingChange: (mode: PacingMode) => void;
  onKeywordClick: (index: number, word: string, category: string, el: HTMLElement) => void;
  onOpenExplain: () => void;
  onOpenSkins: () => void;
  decisionNodes: DecisionNode[];
  currentSkin: SpiderSkinId;
}

export const Screen1SpiderArena: React.FC<Screen1SpiderArenaProps> = ({
  onNavigate,
  pacingMode,
  onPacingChange,
  onKeywordClick,
  onOpenExplain,
  onOpenSkins,
  decisionNodes
}) => {
  const [activeFeed, setActiveFeed] = useState<string>('all');
  const [realArticles, setRealArticles] = useState<any[]>([]);
  const [selectedArticle, setSelectedArticle] = useState<any | null>(null);
  const [isCrawling, setIsCrawling] = useState<boolean>(false);
  const [isFetchingFull, setIsFetchingFull] = useState<boolean>(false);

  // Auto-Tour & Continuous Scanner State
  const [isAutoScanning, setIsAutoScanning] = useState<boolean>(true);
  const [currentScanningStep, setCurrentScanningStep] = useState<number>(-1);
  const [totalStepsInArticle, setTotalStepsInArticle] = useState<number>(0);
  const [scanStatusMessage, setScanStatusMessage] = useState<string>('');
  const [scannedArticleIds, setScannedArticleIds] = useState<Set<number>>(new Set());

  const handleNextArticle = () => {
    if (realArticles.length === 0) return;
    const currentIndex = realArticles.findIndex(a => a.id === selectedArticle?.id);
    const nextIndex = (currentIndex + 1) % realArticles.length;
    setSelectedArticle(realArticles[nextIndex]);
    setCurrentScanningStep(-1);
    playSfx('paper_rustle');
  };

  const handlePrevArticle = () => {
    if (realArticles.length === 0) return;
    const currentIndex = realArticles.findIndex(a => a.id === selectedArticle?.id);
    const prevIndex = (currentIndex - 1 + realArticles.length) % realArticles.length;
    setSelectedArticle(realArticles[prevIndex]);
    setCurrentScanningStep(-1);
    playSfx('paper_rustle');
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

  const loadArticles = async (feedCat: string = activeFeed) => {
    try {
      const url = feedCat && feedCat !== 'all' ? `/api/v1/articles?limit=50&category=${feedCat}` : '/api/v1/articles?limit=50';
      const res = await apiFetch(url);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data)) {
          setRealArticles(data);
          setSelectedArticle((prev: any) => {
            if (prev && data.some((a: any) => a.id === prev.id)) return prev;
            return data[0] || null;
          });
        }
      }
    } catch (e) {
      console.error('Lỗi nạp bài viết:', e);
    }
  };

  useEffect(() => {
    loadArticles(activeFeed);
  }, [activeFeed]);

  useEffect(() => {
    loadCategoryStats();

    // Tự động cập nhật liên tục mỗi 15 giây
    const interval = setInterval(() => {
      loadArticles(activeFeed);
      loadCategoryStats();
    }, 15000);

    return () => clearInterval(interval);
  }, [activeFeed]);

  const articleContainerRef = useRef<HTMLElement | null>(null);

  // Auto-Tour & Continuous Walk Effect: Nhện bò qua từ khóa hoặc đi bộ tuần tra liên tục khi không có từ khóa
  useEffect(() => {
    if (!selectedArticle) return;

    let cancelled = false;
    let stepTimer: ReturnType<typeof setTimeout> | null = null;
    const stepDelay = pacingMode === 'sync' ? 850 : 1600;

    const startTourTimer = setTimeout(() => {
      if (cancelled) return;

      const marks = Array.from(
        document.querySelectorAll('#spider-article-content mark.spider-target')
      ) as HTMLElement[];

      setTotalStepsInArticle(marks.length);

      // TRƯỜNG HỢP 1: BÀI BÁO KHÔNG CÓ TỪ KHÓA -> NẾU ĐANG CÀO TOÀN VĂN THÌ CHỜ, NẾU KHÔNG THÌ NHỆN TUẦN TRA
      if (marks.length === 0) {
        if (isFetchingFull) {
          setScanStatusMessage('⚡ Đang tự động tải toàn văn từ tòa soạn gốc để trích xuất từ khóa (chống thất thoát tin)...');
          return;
        }

        setScanStatusMessage('🔍 Không có từ khóa mục tiêu: Con nhện đang đi bộ tuần tra liên tục...');

        if ((window as any).__spiderStartContinuousPatrol) {
          (window as any).__spiderStartContinuousPatrol(
            () => {
              const el = articleContainerRef.current;
              if (el) return el.getBoundingClientRect();
              return { left: 100, top: 100, width: 600, height: 400 };
            },
            (stepCount: number) => {
              if (!cancelled) {
                setScanStatusMessage(`🚶 Nhện đang đi bộ tuần tra tự do trên trang (bước #${stepCount})...`);
              }
            }
          );
        }

        if (isAutoScanning) {
          // Khi bật Tự Động Quét: nhện đi bộ tuần tra liên tục ~5.0s rồi chuyển bài kế tiếp
          stepTimer = setTimeout(() => {
            if (!cancelled && isAutoScanning && !isFetchingFull) {
              if ((window as any).__spiderStopContinuousPatrol) {
                (window as any).__spiderStopContinuousPatrol();
              }
              if (articleContainerRef.current) {
                articleContainerRef.current.scrollTo({ top: 0, behavior: 'smooth' });
              }
              handleNextArticle();
            }
          }, 5000);
        }
        return;
      }

      // TRƯỜNG HỢP 2: BÀI BÁO CÓ TỪ KHÓA -> DỪNG TUẦN TRA TỰ DO VÀ QUÉT TỪNG TỪ
      if ((window as any).__spiderStopContinuousPatrol) {
        (window as any).__spiderStopContinuousPatrol();
      }

      if (!isAutoScanning) {
        setScanStatusMessage(`Đã tìm thấy ${marks.length} từ khóa. Bấm vào từ khóa hoặc bật Tự Động Quét để nhện bò.`);
        return;
      }

      let stepIndex = 0;

      const runStep = () => {
        if (cancelled || !isAutoScanning) return;

        if (stepIndex >= marks.length) {
          setScanStatusMessage(`✓ Đã quét ${marks.length} từ khóa bài #${selectedArticle.id}. Tự động nạp bài tiếp theo trong 2.0s...`);
          setScannedArticleIds(prev => new Set(prev).add(selectedArticle.id));
          stepTimer = setTimeout(() => {
            if (!cancelled && isAutoScanning) {
              // Cuộn mượt về đầu trang trước khi sang bài mới
              if (articleContainerRef.current) {
                articleContainerRef.current.scrollTo({ top: 0, behavior: 'smooth' });
              }
              handleNextArticle();
            }
          }, 2000);
          return;
        }

        const markEl = marks[stepIndex];
        const word = markEl.dataset.word || markEl.textContent || '';
        const cat = markEl.dataset.cat || 'kinh_te';
        const spiderIndex = parseInt(markEl.dataset.spiderIndex || String(stepIndex), 10);

        setCurrentScanningStep(stepIndex);
        setScanStatusMessage(`🕷️ Nhện đang bò tới [${stepIndex + 1}/${marks.length}]: "${word}"...`);

        // TỰ ĐỘNG CUỘN KHUNG BÁO KHI TỪ KHÓA BỊ KHUẤT / TRÀN KHỎI KHUNG NHÌN
        const container = articleContainerRef.current;
        if (container) {
          const cRect = container.getBoundingClientRect();
          const mRect = markEl.getBoundingClientRect();

          // Kiểm tra nếu từ khóa nằm ngoài khung nhìn (trên hoặc dưới)
          const isAbove = mRect.top < cRect.top + 50;
          const isBelow = mRect.bottom > cRect.bottom - 70;

          if (isAbove || isBelow) {
            markEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }

        // Đánh dấu hiệu ứng đang focus trên DOM
        marks.forEach(m => {
          m.style.outline = 'none';
          m.style.boxShadow = 'none';
        });
        markEl.style.outline = '2px solid #C86D51';
        markEl.style.boxShadow = '0 0 10px rgba(200, 109, 81, 0.45)';

        // Điều khiển nhện bò & bắn tơ sang Decision 3 Node
        playSfx('paper_rustle');
        onKeywordClick(spiderIndex, word, cat, markEl);

        stepIndex++;
        stepTimer = setTimeout(runStep, stepDelay);
      };

      runStep();
    }, 450);

    return () => {
      cancelled = true;
      clearTimeout(startTourTimer);
      if (stepTimer) clearTimeout(stepTimer);
      if ((window as any).__spiderStopContinuousPatrol) {
        (window as any).__spiderStopContinuousPatrol();
      }
    };
  }, [selectedArticle?.id, selectedArticle?.content_clean, isAutoScanning, pacingMode, isFetchingFull]);

  const autoEnrichedIdsRef = useRef<Set<number>>(new Set());

  // Tự động kích hoạt cào sâu toàn văn ngay khi mở bài viết dạng tóm tắt (Chống thất thoát tin tức)
  useEffect(() => {
    if (!selectedArticle?.id) return;
    const isSummary = (
      !selectedArticle.content_clean ||
      selectedArticle.content_clean.length <= 320 ||
      selectedArticle.content_clean === selectedArticle.summary_raw
    );

    if (isSummary && !autoEnrichedIdsRef.current.has(selectedArticle.id) && !isFetchingFull) {
      autoEnrichedIdsRef.current.add(selectedArticle.id);
      handleFetchFullArticle();
    }
  }, [selectedArticle?.id, selectedArticle?.content_clean]);

  const handleTriggerCrawl = async () => {
    setIsCrawling(true);
    playSfx('click');
    try {
      await fetch('/api/v1/crawl', { method: 'POST' });
      setTimeout(async () => {
        await loadArticles();
        setIsCrawling(false);
        playSfx('wind_chime');
      }, 3500);
    } catch {
      setIsCrawling(false);
    }
  };

  const handleFetchFullArticle = async () => {
    if (!selectedArticle) return;
    setIsFetchingFull(true);
    playSfx('click');
    try {
      const res = await apiFetch(`/api/v1/articles/${selectedArticle.id}/fetch-full`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        if (data.content_clean && data.content_clean.length > (selectedArticle.content_clean?.length || 0)) {
          setSelectedArticle((prev: any) => ({ ...prev, content_clean: data.content_clean }));
          setRealArticles((prev: any[]) => prev.map(a => a.id === selectedArticle.id ? { ...a, content_clean: data.content_clean } : a));
          playSfx('wind_chime');
        }
      }
    } catch (e) {
      console.error('Lỗi cào sâu bài báo:', e);
    } finally {
      setIsFetchingFull(false);
    }
  };

  const feeds = [
    { id: 'all', icon: '🌐', name: 'Tất Cả Nguồn Tin', count: `${categoryStats['all'] ?? realArticles.length} bài` },
    { id: 'quoc_te', icon: '🌍', name: 'Quốc Tế (BBC, Reuters, AP...)', count: `${categoryStats['quoc_te'] ?? realArticles.filter(a => a.source_category === 'quoc_te').length} bài` },
    { id: 'kinh_te', icon: '🏛️', name: 'Vĩ Mô & Tài Chính (FT, WSJ...)', count: `${categoryStats['kinh_te'] ?? realArticles.filter(a => a.source_category === 'kinh_te').length} bài` },
    { id: 'chung_khoan', icon: '📈', name: 'Chứng Khoán & Cổ Phiếu', count: `${categoryStats['chung_khoan'] ?? realArticles.filter(a => a.source_category === 'chung_khoan').length} bài` },
    { id: 'crypto', icon: '🪙', name: 'Crypto & Web3', count: `${categoryStats['crypto'] ?? realArticles.filter(a => a.source_category === 'crypto').length} bài` },
    { id: 'chinh_tri', icon: '⚖️', name: 'Chính Trị & Ngoại Giao', count: `${categoryStats['chinh_tri'] ?? realArticles.filter(a => a.source_category === 'chinh_tri').length} bài` }
  ];

  const handleMarkClick = (e: React.MouseEvent<HTMLElement>, index: number, word: string, category: string) => {
    e.stopPropagation();
    playSfx('paper_rustle');
    onKeywordClick(index, word, category, e.currentTarget);
  };

  const renderHighlightedContent = (text: string) => {
    if (!text) return null;
    const keywords = [
      // Tiếng Việt
      { word: 'lãi suất', cat: 'kinh_te' },
      { word: 'lạm phát', cat: 'kinh_te' },
      { word: 'tỷ giá', cat: 'vang' },
      { word: 'vàng', cat: 'vang' },
      { word: 'sjc', cat: 'vang' },
      { word: 'cổ phiếu', cat: 'chung_khoan' },
      { word: 'chứng khoán', cat: 'chung_khoan' },
      { word: 'vn-index', cat: 'chung_khoan' },
      { word: 'thanh khoản', cat: 'chung_khoan' },
      { word: 'trái phiếu', cat: 'chung_khoan' },
      { word: 'doanh nghiệp', cat: 'kinh_te' },
      { word: 'ngân hàng', cat: 'kinh_te' },
      { word: 'fed', cat: 'kinh_te' },
      { word: 'vinfast', cat: 'chung_khoan' },
      { word: 'green sm', cat: 'chung_khoan' },
      { word: 'bất động sản', cat: 'kinh_te' },
      { word: 'usd', cat: 'vang' },
      { word: 'ai', cat: 'github' },
      { word: 'chiến sự', cat: 'quoc_te' },
      { word: 'chiến tranh', cat: 'quoc_te' },
      // Tiếng Anh (Báo chí quốc tế: Economist, Reuters, Guardian, Bloomberg, FT, WSJ, Politico...)
      { word: 'dollar', cat: 'vang' },
      { word: 'debased', cat: 'kinh_te' },
      { word: 'inflation', cat: 'kinh_te' },
      { word: 'interest', cat: 'kinh_te' },
      { word: 'interest rate', cat: 'kinh_te' },
      { word: 'federal reserve', cat: 'kinh_te' },
      { word: 'economy', cat: 'kinh_te' },
      { word: 'economic', cat: 'kinh_te' },
      { word: 'markets', cat: 'chung_khoan' },
      { word: 'market', cat: 'chung_khoan' },
      { word: 'stocks', cat: 'chung_khoan' },
      { word: 'stock', cat: 'chung_khoan' },
      { word: 'equities', cat: 'chung_khoan' },
      { word: 'bonds', cat: 'chung_khoan' },
      { word: 'treasury', cat: 'chung_khoan' },
      { word: 'gold', cat: 'vang' },
      { word: 'bitcoin', cat: 'crypto' },
      { word: 'crypto', cat: 'crypto' },
      { word: 'oil', cat: 'quoc_te' },
      { word: 'crude', cat: 'quoc_te' },
      { word: 'brent', cat: 'quoc_te' },
      { word: 'war', cat: 'quoc_te' },
      { word: 'ukraine', cat: 'quoc_te' },
      { word: 'russia', cat: 'quoc_te' },
      { word: 'china', cat: 'quoc_te' },
      { word: 'taiwan', cat: 'quoc_te' },
      { word: 'tariffs', cat: 'kinh_te' },
      { word: 'trade', cat: 'kinh_te' },
      { word: 'gdp', cat: 'kinh_te' },
      { word: 'nvidia', cat: 'github' },
      // Chính trị & Bầu cử (Politico, Washington Post, NYT...)
      { word: 'trump', cat: 'chinh_tri' },
      { word: 'biden', cat: 'chinh_tri' },
      { word: 'democrats', cat: 'chinh_tri' },
      { word: 'republicans', cat: 'chinh_tri' },
      { word: 'gop', cat: 'chinh_tri' },
      { word: 'congress', cat: 'chinh_tri' },
      { word: 'white house', cat: 'chinh_tri' },
      { word: 'senate', cat: 'chinh_tri' },
      { word: 'election', cat: 'chinh_tri' },
      { word: 'elections', cat: 'chinh_tri' },
      { word: 'midterms', cat: 'chinh_tri' },
      { word: 'campaign', cat: 'chinh_tri' },
      { word: 'voters', cat: 'chinh_tri' },
      { word: 'politics', cat: 'chinh_tri' },
      { word: 'political', cat: 'chinh_tri' },
      { word: 'supreme court', cat: 'chinh_tri' },
      { word: 'president', cat: 'chinh_tri' },
      { word: 'chính trị', cat: 'chinh_tri' },
      { word: 'chính phủ', cat: 'chinh_tri' },
      { word: 'quốc hội', cat: 'chinh_tri' },
      { word: 'bầu cử', cat: 'chinh_tri' },
      { word: 'tổng thống', cat: 'chinh_tri' },
      { word: 'chính sách', cat: 'chinh_tri' }
    ];

    // Sắp xếp từ khóa dài trước, ngắn sau; gán word boundary \b cho từ ASCII đơn
    const sortedKeywords = [...keywords].sort((a, b) => b.word.length - a.word.length);
    const pattern = new RegExp(
      `(${sortedKeywords.map(k => {
        const escaped = k.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        return /^[a-zA-Z0-9_]+$/.test(k.word) ? `\\b${escaped}\\b` : escaped;
      }).join('|')})`,
      'gi'
    );
    let markIndex = 0;

    // Tách văn bản và lọc bỏ các dòng rác điều hướng nếu có (vd: Skip to Main Content, * [Link](url))
    const rawParagraphs = text
      .split(/\n+/)
      .map(p => p.trim())
      .filter(p => {
        if (!p) return false;
        if (/^skip to main/i.test(p)) return false;
        if (/^\*?\s*\[.*?\]\(https?:\/\/.*?\)$/.test(p)) return false; // Dòng thuần markdown menu link
        return true;
      });
    const paragraphs = rawParagraphs.length > 0 ? rawParagraphs : [text];

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {paragraphs.map((para, pIdx) => {
          const parts = para.split(pattern);
          return (
            <p
              key={pIdx}
              style={{
                fontFamily: 'var(--font-serif, "Merriweather", "Georgia", serif)',
                fontSize: '15px',
                lineHeight: '1.85',
                color: '#1A2E19',
                margin: 0
              }}
            >
              {parts.map((part, i) => {
                const matchKw = keywords.find(k => k.word.toLowerCase() === part.toLowerCase());
                if (matchKw) {
                  const currentIndex = markIndex++;
                  return (
                    <mark
                      key={i}
                      className="spider-target"
                      data-spider-index={currentIndex}
                      data-word={part}
                      data-cat={matchKw.cat}
                      onClick={e => handleMarkClick(e, currentIndex, part, matchKw.cat)}
                      style={{
                        backgroundColor: '#FFF2C6',
                        color: '#8D5B00',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: 600,
                        transition: 'all 0.2s ease',
                        borderBottom: '2px solid #E5B869'
                      }}
                    >
                      {part}
                    </mark>
                  );
                }
                return <span key={i}>{part}</span>;
              })}
            </p>
          );
        })}
      </div>
    );
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
      {/* 1. LEFT NAVIGATION SIDEBAR (240px) */}
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Feeds Title */}
          <div
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '12.5px',
              fontWeight: 700,
              color: '#2D4A2B',
              letterSpacing: '0.3px'
            }}
          >
            📡 KÊNH TIN NÓNG (FEEDS)
          </div>

          {/* Feeds List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {feeds.map(feed => {
              const isActive = activeFeed === feed.id;
              return (
                <div
                  key={feed.id}
                  onClick={() => setActiveFeed(feed.id)}
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
                    <span>{feed.icon}</span>
                    <span>{feed.name}</span>
                  </div>
                  <span
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '11px',
                      color: isActive ? '#F8AFA6' : '#5F7D58'
                    }}
                  >
                    {feed.count}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Queue Box: Nạp bài báo thật từ Backend */}
          <div
            style={{
              backgroundColor: '#F4F1EA',
              borderRadius: '8px',
              border: '1px solid #DCD5C5',
              padding: '10px',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '10px',
                  fontWeight: 700,
                  color: '#5F7D58',
                  textTransform: 'uppercase'
                }}
              >
                📡 BÀI BÁO THỰC TẾ ({realArticles.length})
              </span>
              <button
                onClick={handleTriggerCrawl}
                disabled={isCrawling}
                style={{
                  background: isCrawling ? '#A8A29E' : '#2D4A2B',
                  color: '#FAF8F5',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '2px 7px',
                  fontSize: '9.5px',
                  fontFamily: 'var(--font-mono)',
                  cursor: isCrawling ? 'not-allowed' : 'pointer',
                  fontWeight: 700
                }}
              >
                {isCrawling ? '⏳ ĐANG CÀO...' : '⚡ CÀO MỚI'}
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '280px', overflowY: 'auto' }}>
              {(() => {
                const filtered = activeFeed === 'all'
                  ? realArticles
                  : realArticles.filter(a => a.source_category === activeFeed);
                if (filtered.length === 0) {
                  return (
                    <div style={{ fontSize: '11px', color: '#78716c', padding: '12px 0', textAlign: 'center' }}>
                      {realArticles.length === 0 ? 'Đang tải tin từ Backend...' : 'Chưa có bài trong danh mục này.'}
                    </div>
                  );
                }
                return filtered.map((art, idx) => {
                  const isSelected = selectedArticle?.id === art.id;
                  return (
                    <div
                      key={art.id || idx}
                      onClick={() => {
                        setIsAutoScanning(false);
                        setSelectedArticle(art);
                        playSfx('paper_rustle');
                      }}
                      style={{
                        backgroundColor: isSelected ? '#FFFFFF' : '#FAF8F5',
                        borderRadius: '6px',
                        padding: '6px 8px',
                        border: isSelected ? '1.5px solid #2D4A2B' : '1px solid #E8E2D5',
                        cursor: 'pointer',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '2px',
                        transition: 'all 0.15s ease',
                        boxShadow: isSelected ? '0 1px 4px rgba(45,74,43,0.1)' : 'none'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{
                          fontSize: '9px',
                          fontFamily: 'var(--font-mono)',
                          color: isSelected ? '#1B5E20' : scannedArticleIds.has(art.id) ? '#4A6B82' : '#8D6E63',
                          fontWeight: isSelected ? 700 : 500
                        }}>
                          {isSelected ? '▶ ĐANG QUÉT' : scannedArticleIds.has(art.id) ? '✓ ĐÃ QUÉT' : `Bài #${art.id}`} • {art.source_name || 'RSS'}
                        </span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <span style={{
                            fontSize: '8px',
                            fontFamily: 'var(--font-mono)',
                            padding: '1px 4px',
                            borderRadius: '3px',
                            backgroundColor: (art.content_clean && art.content_clean.length > 320 && art.content_clean !== art.summary_raw) ? '#E8F5E9' : '#FEF3C7',
                            color: (art.content_clean && art.content_clean.length > 320 && art.content_clean !== art.summary_raw) ? '#1B5E20' : '#B45309',
                            fontWeight: 700
                          }}>
                            {(art.content_clean && art.content_clean.length > 320 && art.content_clean !== art.summary_raw) ? 'TOÀN VĂN' : 'TÓM TẮT'}
                          </span>
                          <span style={{ fontSize: '8.5px', fontFamily: 'var(--font-mono)', color: '#A8A29E' }}>
                            {(art.language || 'vi').toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <span style={{ fontSize: '11px', fontWeight: isSelected ? 700 : 500, color: '#2D4A2B', lineHeight: '1.3', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {art.title}
                      </span>
                    </div>
                  );
                });
              })()}
            </div>
          </div>
        </div>

        {/* Sidebar Bottom Controls */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', paddingTop: '10px' }}>
          <div style={{ fontSize: '10.5px', fontFamily: 'var(--font-mono)', color: '#5F7D58', fontWeight: 600 }}>
            ⚡ TỐC ĐỘ BÒ CỦA NHỆN:
          </div>
          <div style={{ display: 'flex', gap: '6px' }}>
            <button
              onClick={() => onPacingChange('sync')}
              style={{
                flex: 1,
                border: 'none',
                backgroundColor: pacingMode === 'sync' ? '#2D4A2B' : '#FFFFFF',
                color: pacingMode === 'sync' ? '#FAF8F5' : '#5F7D58',
                borderRadius: '6px',
                padding: '6px 0',
                fontSize: '10.5px',
                fontFamily: 'var(--font-mono)',
                fontWeight: 700,
                cursor: 'pointer',
                borderWidth: '1px',
                borderStyle: 'solid',
                borderColor: pacingMode === 'sync' ? '#2D4A2B' : '#DCD5C5'
              }}
            >
              ⚡ SYNC (400ms)
            </button>
            <button
              onClick={() => onPacingChange('chill')}
              style={{
                flex: 1,
                border: 'none',
                backgroundColor: pacingMode === 'chill' ? '#2D4A2B' : '#FFFFFF',
                color: pacingMode === 'chill' ? '#FAF8F5' : '#5F7D58',
                borderRadius: '6px',
                padding: '6px 0',
                fontSize: '10.5px',
                fontFamily: 'var(--font-mono)',
                fontWeight: 700,
                cursor: 'pointer',
                borderWidth: '1px',
                borderStyle: 'solid',
                borderColor: pacingMode === 'chill' ? '#2D4A2B' : '#DCD5C5'
              }}
            >
              ☕ CHILL (1.2s)
            </button>
          </div>

          <button
            onClick={onOpenSkins}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #DCD5C5',
              borderRadius: '6px',
              padding: '6px 0',
              fontSize: '11px',
              fontFamily: 'var(--font-sans)',
              fontWeight: 600,
              color: '#2D4A2B',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              marginTop: '4px'
            }}
          >
            <span>🕷️</span>
            <span>Đổi Skin Con Nhện (2 Mẫu)</span>
          </button>
        </div>
      </aside>

      {/* 2. CENTER: ArXiv RESEARCH PAPER SHEET CANVAS (1160px or flex-1) */}
      <main
        ref={articleContainerRef}
        id="spider-article-main-container"
        style={{
          flex: 1,
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '24px 32px',
          overflowY: 'auto',
          boxShadow: '0 4px 16px rgba(45, 74, 43, 0.04)',
          position: 'relative'
        }}
      >
        {/* Academic Header Top Line */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '10px',
            fontFamily: 'var(--font-mono)',
            color: '#5F7D58',
            fontWeight: 600,
            letterSpacing: '0.8px',
            marginBottom: '8px'
          }}
        >
          <span>2026 SPIDER NEWS RADAR • REAL-TIME INGESTION</span>
          <span>{selectedArticle ? `NGUỒN: ${selectedArticle.source_name || 'RSS'} • ${selectedArticle.published_at || 'Mới nhất'}` : 'SEPTEMBER / OCTOBER 2026'}</span>
        </div>

        <div style={{ height: '1px', backgroundColor: '#E8E2D5', marginBottom: '16px' }} />

        {/* Paper Title Block */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '14px' }}>
          <h1
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '22px',
              fontWeight: 700,
              color: '#1A2E19',
              lineHeight: '1.3'
            }}
          >
            {selectedArticle ? selectedArticle.title : 'GPT-6 and the Geometry of LLM Optimization'}
          </h1>
          <div style={{ fontSize: '13px', fontWeight: 600, color: '#2D4A2B' }}>
            {selectedArticle ? `CHUYÊN MỤC: ${(selectedArticle.source_category || 'Kinh tế vĩ mô').toUpperCase()}` : 'Mapping the Loss Landscape, Training Dynamics and Emergent Capabilities'}
          </div>
          <div style={{ fontSize: '11.5px', color: '#5F7D58', lineHeight: '1.5' }}>
            {selectedArticle ? `Mã băm chống trùng lặp SHA-256: ${selectedArticle.url_hash || 'hash_clean'}` : 'A technical analysis of the structure, dynamics and implications of next-generation foundation models for macro reasoning.'}
          </div>
        </div>

        {/* Paper Metadata Tags Row */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
          {(selectedArticle
            ? ['TIN THỰC TẾ', (selectedArticle.source_name || 'RSS').toUpperCase(), `NGÔN NGỮ: ${(selectedArticle.language || 'vi').toUpperCase()}`, `ID #${selectedArticle.id}`]
            : ['TECHNICAL NOTE', 'INDEPENDENT STUDY', 'DECISION 3 LITE NEURAL RESEARCH LAB', 'NOT AFFILIATED WITH ANY INSTITUTION']
          ).map((tag, idx) => (
            <span
              key={idx}
              style={{
                backgroundColor: '#F4F1EA',
                border: '1px solid #E8E2D5',
                padding: '3px 8px',
                borderRadius: '999px',
                fontSize: '9.5px',
                fontFamily: 'var(--font-mono)',
                color: '#5F7D58',
                fontWeight: 600
              }}
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Khi có selectedArticle: Render Trang Đọc Báo Quốc Tế Đích Thực */}
        {selectedArticle ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
            {/* Action Bar & Auto-Scan Controller */}
            <div
              style={{
                backgroundColor: '#FBF9F5',
                border: '1px solid #E8E2D5',
                borderRadius: '8px',
                padding: '10px 14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '8px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                {/* Auto-Pilot Toggle Button */}
                <button
                  onClick={() => {
                    playSfx('click');
                    setIsAutoScanning(!isAutoScanning);
                  }}
                  style={{
                    backgroundColor: isAutoScanning ? '#1B5E20' : '#D97706',
                    border: 'none',
                    color: '#FAF8F5',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px',
                    boxShadow: isAutoScanning ? '0 0 8px rgba(27,94,32,0.35)' : 'none'
                  }}
                >
                  <span>{isAutoScanning ? '▶️ AUTO-PILOT: ĐANG QUÉT' : '⏸️ AUTO-PILOT: TẠM DỪNG'}</span>
                </button>

                {/* Prev / Next Article Buttons */}
                <button
                  onClick={handlePrevArticle}
                  title="Chuyển về bài báo trước đó"
                  style={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #DCD5C5',
                    color: '#2D4A2B',
                    borderRadius: '6px',
                    padding: '5px 10px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  ⏮️ Bài Trước
                </button>
                <button
                  onClick={handleNextArticle}
                  title="Chuyển sang bài báo tiếp theo"
                  style={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #DCD5C5',
                    color: '#2D4A2B',
                    borderRadius: '6px',
                    padding: '5px 10px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  ⏭️ Bài Kế Tiếp
                </button>

                <button
                  onClick={() => window.open(selectedArticle.url, '_blank')}
                  style={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #2D4A2B',
                    color: '#2D4A2B',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  <span>🌐</span>
                  <span>Mở Trang Gốc ({selectedArticle.source_name || 'Tòa soạn'})</span>
                </button>

                <button
                  onClick={handleFetchFullArticle}
                  disabled={isFetchingFull}
                  style={{
                    backgroundColor: isFetchingFull ? '#A8A29E' : '#2D4A2B',
                    border: 'none',
                    color: '#FAF8F5',
                    borderRadius: '6px',
                    padding: '5px 12px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    cursor: isFetchingFull ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  <span>⚡</span>
                  <span>{isFetchingFull ? 'Đang cào bài viết...' : 'Tải Toàn Văn (Deep Scrape)'}</span>
                </button>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <button
                  onClick={() => onNavigate('feeds')}
                  style={{
                    backgroundColor: '#FAF8F5',
                    border: '1px solid #DCD5C5',
                    color: '#5F7D58',
                    borderRadius: '6px',
                    padding: '5px 10px',
                    fontSize: '11px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  🇻🇳 Đọc Dịch Song Ngữ
                </button>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: '#8D6E63' }}>
                  {selectedArticle.content_clean && selectedArticle.content_clean.length > 250 ? `Toàn văn: ${selectedArticle.content_clean.length} ký tự` : 'Bản tóm tắt RSS'}
                </span>
              </div>
            </div>

            {/* Banner trạng thái Auto-Enrichment chống thất thoát tin tức */}
            {isFetchingFull ? (
              <div
                style={{
                  backgroundColor: '#FEF3C7',
                  border: '1px solid #F59E0B',
                  borderRadius: '8px',
                  padding: '10px 16px',
                  fontSize: '12px',
                  color: '#92400E',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  boxShadow: '0 2px 8px rgba(245, 158, 11, 0.12)'
                }}
              >
                <span style={{ fontSize: '15px' }}>⚡</span>
                <span style={{ lineHeight: '1.4' }}>
                  <strong>Hệ thống phát hiện bản tin dạng tóm tắt ngắn:</strong> Đang tự động cào sâu toàn văn bài viết từ tòa soạn <strong>{selectedArticle.source_name || 'gốc'}</strong> để nhện bắt trọn vẹn từ khóa (chống thất thoát tin tức)...
                </span>
              </div>
            ) : selectedArticle.content_clean && (selectedArticle.content_clean.length <= 320 || selectedArticle.content_clean === selectedArticle.summary_raw) ? (
              <div
                style={{
                  backgroundColor: '#FFFBEB',
                  border: '1px solid #FDE68A',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  fontSize: '12px',
                  color: '#92400E',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '10px'
                }}
              >
                <span>
                  📄 <strong>Bản tóm tắt RSS ({selectedArticle.content_clean.length} ký tự):</strong> Đã kích hoạt cơ chế tự động tải toàn văn. Nếu tòa soạn chặn bot, bạn có thể bấm <strong>[⚡ Tải Toàn Văn (Deep Scrape)]</strong> hoặc mở trang gốc.
                </span>
                <button
                  onClick={handleFetchFullArticle}
                  disabled={isFetchingFull}
                  style={{
                    backgroundColor: '#B45309',
                    color: '#FFF',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '4px 8px',
                    fontSize: '10.5px',
                    fontWeight: 700,
                    cursor: 'pointer',
                    whiteSpace: 'nowrap'
                  }}
                >
                  Thử Lại Ngay
                </button>
              </div>
            ) : (
              <div
                style={{
                  backgroundColor: '#F0FDF4',
                  border: '1px solid #BBF7D0',
                  borderRadius: '8px',
                  padding: '7px 12px',
                  fontSize: '11px',
                  color: '#166534',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}
              >
                <span>
                  ✓ <strong>Toàn văn bài viết ({selectedArticle.content_clean?.length || 0} ký tự):</strong> Đã bóc tách trọn vẹn nội dung chi tiết — không thất thoát từ khóa.
                </span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: '#15803D' }}>
                  CHẾ ĐỘ TRÍCH XUẤT ĐẦY ĐỦ
                </span>
              </div>
            )}

            {/* Khung nội dung bài báo chính */}
            <div
              id="spider-article-content"
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '8px',
                border: '1px solid #E8E2D5',
                padding: '24px 28px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.02)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid #F0ECE1', paddingBottom: '8px' }}>
                <span
                  style={{
                    backgroundColor: isAutoScanning ? '#E8F5E9' : '#FCE8E6',
                    color: isAutoScanning ? '#1B5E20' : '#C86D51',
                    borderRadius: '4px',
                    padding: '3px 8px',
                    fontSize: '10.5px',
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700
                  }}
                >
                  {isAutoScanning ? '📡 RADAR TỰ ĐỘNG QUÉT BÀI VIẾT' : '🎯 CÁC TỪ KHÓA ĐỊNH VỊ CHO CON NHỆN BÒ'}
                </span>
                <span style={{ fontSize: '11px', color: '#5F7D58', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                  {scanStatusMessage || 'Nhấp từ khóa bất kỳ để con nhện bò đến & bắn tơ'}
                </span>
              </div>

              {renderHighlightedContent(selectedArticle.content_clean || selectedArticle.title)}
            </div>

            {/* Filament Emission Bar */}
            <div
              style={{
                backgroundColor: isAutoScanning ? '#F0FDF4' : '#F0F7F2',
                border: isAutoScanning ? '1px solid #86EFAC' : '1px dashed #A8D5BA',
                borderRadius: '8px',
                padding: '8px 14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                fontSize: '11px',
                fontFamily: 'var(--font-mono)',
                color: '#1B5E20',
                fontWeight: 600
              }}
            >
              <span>{scanStatusMessage || '🕸️ TƠ TRANSIENT (0.75px) SẴN SÀNG BẮN SANG VÒNG CUNG ➔➔'}</span>
              <span style={{ color: '#C86D51', fontWeight: 700 }}>[ĐÍCH: SYSTEM 1 DECISION]</span>
            </div>
          </div>
        ) : (
          /* Khi chưa chọn bài nào: Render mockup học thuật */
          <div style={{ display: 'flex', gap: '24px' }}>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ backgroundColor: '#F7F5F0', border: '1px solid #E8E2D5', borderRadius: '8px', padding: '12px' }}>
                <p style={{ fontSize: '13px', color: '#2D4A2B' }}>Vui lòng chọn bài viết từ danh sách bên trái để xem nội dung thực tế.</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* 3. RIGHT: DECISION 3 LITE NEURAL ROUTING ARC COLUMN (470px) */}
      <aside
        id="decision-arc-column"
        style={{
          width: '470px',
          flexShrink: 0,
          backgroundColor: '#EBE6DC',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflowY: 'auto'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span
              style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '13px',
                fontWeight: 700,
                color: '#2D4A2B'
              }}
            >
              DECISION 3 LITE NEURAL ROUTING ARC
            </span>
            <span
              style={{
                backgroundColor: '#E8F5E9',
                border: '1px solid #C8E6C9',
                color: '#1B5E20',
                borderRadius: '999px',
                padding: '2px 8px',
                fontSize: '10.5px',
                fontFamily: 'var(--font-mono)',
                fontWeight: 700
              }}
            >
              ⚡ 8.5ms
            </span>
          </div>

          {/* Decision Arc Nodes List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {decisionNodes.map(node => (
              <div
                key={node.id}
                id={node.id}
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #DCD5C5',
                  borderRadius: '10px',
                  padding: '10px 12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px',
                  transition: 'all 0.25s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
                    {node.label}
                  </span>
                  <span
                    style={{
                      fontSize: '11px',
                      fontFamily: 'var(--font-mono)',
                      color: node.silkCount > 0 ? '#C86D51' : '#5F7D58',
                      fontWeight: 600
                    }}
                  >
                    {node.silkCount > 0 ? `● ${node.silkCount} sợi tơ [ĐANG NHẬN]` : `${node.silkCount} sợi tơ kết nối`}
                  </span>
                </div>
                <div style={{ fontSize: '11px', color: '#5F7D58' }}>
                  {node.subText}
                </div>
              </div>
            ))}
          </div>

          {/* Big Verdict Callout */}
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
              PHÁN QUYẾT TENSOR PHẢN XẠ NHỊ PHÂN
            </div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#2D4A2B' }}>
              QUYẾT ĐỊNH: VĨ MÔ TRỌNG ĐIỂM (PASS THRESHOLD)
            </div>
            <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: '#1B5E20' }}>
              Confidence Score: 0.942 / 1.000 • Tiết kiệm 84.6% LLM Token
            </div>
          </div>
        </div>

        {/* Bottom Actions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', paddingTop: '12px' }}>
          {/* Explain drawer button */}
          <button
            onClick={onOpenExplain}
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #2D4A2B',
              color: '#2D4A2B',
              borderRadius: '8px',
              padding: '9px 12px',
              fontSize: '11.5px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>🧠</span>
            <span>XEM GIẢI TRÌNH QUYẾT ĐỊNH DECISION 3 →</span>
          </button>

          {/* Synthesize button */}
          <button
            onClick={() => {
              playSfx('click');
              onNavigate('feeds');
            }}
            style={{
              backgroundColor: '#2D4A2B',
              border: 'none',
              color: '#FAF8F5',
              borderRadius: '8px',
              padding: '11px 12px',
              fontSize: '12.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 2px 8px rgba(45, 74, 43, 0.2)'
            }}
          >
            <span>⚡</span>
            <span>TỔNG HỢP TIẾNG VIỆT (SYSTEM 2) →</span>
          </button>

          {/* Link to Screen 7 */}
          <button
            onClick={() => onNavigate('analytics')}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              color: '#2D4A2B',
              fontSize: '11px',
              fontFamily: 'var(--font-mono)',
              fontWeight: 600,
              cursor: 'pointer',
              textAlign: 'center',
              padding: '4px 0'
            }}
          >
            📊 XEM BIỂU ĐỒ & CHỈ SỐ VĨ MÔ (SCREEN 7) →
          </button>
        </div>
      </aside>
    </div>
  );
};
