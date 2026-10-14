import React, { useState, useEffect } from 'react';
import { TopHeaderBar } from './components/chrome/TopHeaderBar';
import { BottomTelemetryBar } from './components/chrome/BottomTelemetryBar';
import { Screen1SpiderArena } from './components/screens/Screen1SpiderArena';
import { Screen2BilingualReader } from './components/screens/Screen2BilingualReader';
import { Screen3ExecutiveDigest } from './components/screens/Screen3ExecutiveDigest';
import { Screen4GitHubRadar } from './components/screens/Screen4GitHubRadar';
import { Screen5TrendVault } from './components/screens/Screen5TrendVault';
import { Screen6Settings } from './components/screens/Screen6Settings';
import { Screen7Analytics } from './components/screens/Screen7Analytics';
import { SpiderCanvas } from './components/SpiderCanvas';
import { FeedDrawer } from './components/FeedDrawer';
import { SkinSelector } from './components/SkinSelector';
import { SearchModalFTS5 } from './components/overlays/SearchModalFTS5';
import { DecisionExplainDrawer } from './components/overlays/DecisionExplainDrawer';
import { AddFeedModal } from './components/overlays/AddFeedModal';
import { ScreenTab, PacingMode, System1Engine, SpiderSkinId, DecisionNode, SpiderEvent } from './types';
import { playSfx, getVolumePercent, setVolumePercent, getIsAudioMuted, setIsAudioMuted } from './utils/audio';
import { apiFetch } from './utils/api';
import { useSpiderStream } from './utils/useSpiderStream';

export const App: React.FC = () => {
  useSpiderStream(true);
  const [activeTab, setActiveTab] = useState<ScreenTab>('arena');
  const [currentSkin, setCurrentSkin] = useState<SpiderSkinId>('tribal');
  const [pacingMode, setPacingMode] = useState<PacingMode>('sync');
  const [system1Engine, setSystem1Engine] = useState<System1Engine>('d3');
  const [volumePercent, setVolumeState] = useState<number>(() => getVolumePercent());
  const [isSfxEnabled, setIsSfxEnabled] = useState<boolean>(() => !getIsAudioMuted());

  const handleToggleSfx = () => {
    const next = !isSfxEnabled;
    setIsSfxEnabled(next);
    setIsAudioMuted(!next);
    if (next) playSfx('click');
  };

  const handleVolumeChange = (newVol: number) => {
    setVolumeState(newVol);
    setVolumePercent(newVol);
    if (newVol > 0 && !isSfxEnabled) {
      setIsSfxEnabled(true);
      setIsAudioMuted(false);
    }
  };

  // Modals & Drawers state
  const [isFeedsOpen, setIsFeedsOpen] = useState<boolean>(false);
  const [isSkinsOpen, setIsSkinsOpen] = useState<boolean>(false);
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);
  const [isExplainOpen, setIsExplainOpen] = useState<boolean>(false);
  const [isAddFeedOpen, setIsAddFeedOpen] = useState<boolean>(false);

  // Telemetry state
  const [totalFilaments, setTotalFilaments] = useState<number>(6);
  const [avgLatencyMs, setAvgLatencyMs] = useState<number | null>(8.5);
  const [feedCount, setFeedCount] = useState<number>(25);

  const refreshSourcesCount = async () => {
    try {
      const res = await apiFetch('/api/v1/sources');
      if (res.ok) {
        const list = await res.json();
        if (Array.isArray(list)) setFeedCount(list.length);
      }
    } catch {}
  };

  useEffect(() => {
    refreshSourcesCount();
  }, [isFeedsOpen]);

  const [decisionNodes, setDecisionNodes] = useState<DecisionNode[]>([
    {
      id: 'node-macro',
      label: '🏛️ NODE KINH TẾ & DÒNG TIỀN',
      category: 'kinh_te',
      silkCount: 4,
      subText: 'Lãi suất 4.5% • Tín dụng 12% • OMO',
      color: '#1B5E20'
    },
    {
      id: 'node-stocks',
      label: '📈 NODE CHỨNG KHOÁN (VN-INDEX)',
      category: 'chung_khoan',
      silkCount: 2,
      subText: 'VN-Index 1.298 • Thanh khoản 28.5k tỷ',
      color: '#2563EB'
    },
    {
      id: 'node-gold',
      label: '🥇 NODE GIÁ VÀNG & TỶ GIÁ',
      category: 'vang',
      silkCount: 1,
      subText: 'SJC 88.5 tr • Tỷ giá trung tâm 24.280',
      color: '#D97706'
    },
    {
      id: 'node-policy',
      label: '🌐 NODE CHÍNH SÁCH VĨ MÔ',
      category: 'chinh_tri',
      silkCount: 3,
      subText: 'Quyết sách tài khóa & phối hợp tiền tệ',
      color: '#7C3AED'
    },
    {
      id: 'node-breaking',
      label: '⚡ NODE BREAKING NEWS',
      category: 'quoc_te',
      silkCount: 2,
      subText: 'Tâm lý: TÍCH CỰC (+0.82) • Rủi ro thấp',
      color: '#C86D51'
    }
  ]);

  // Keyboard shortcut Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Poll latency from backend if available
  useEffect(() => {
    let alive = true;
    const poll = async () => {
      try {
        const res = await apiFetch('/api/v1/system1/status');
        if (!res.ok) return;
        const j = await res.json();
        if (alive) {
          setAvgLatencyMs(j.avg_latency_ms ?? j.latency_ms ?? 8.5);
          if (j.engine) setSystem1Engine(j.engine);
        }
      } catch {
        // Fallback to local default
      }
    };
    poll();
    const id = setInterval(poll, 15000);
    return () => {
      alive = false;
      clearInterval(id);
    };
  }, []);

  const handleKeywordClick = (
    index: number,
    word: string,
    category: string,
    targetEl: HTMLElement
  ) => {
    if (isSfxEnabled) playSfx('water_drop');

    let targetNodeId = 'node-macro';
    if (category === 'vang') targetNodeId = 'node-gold';
    else if (category === 'chung_khoan') targetNodeId = 'node-stocks';
    else if (category === 'chinh_tri') targetNodeId = 'node-policy';

    const nodeEl = document.getElementById(targetNodeId) || undefined;

    const eventData: Partial<SpiderEvent> = {
      event_id: Math.random().toString(36).substring(7),
      article_id: 1,
      target_word: word,
      target_index: index,
      category: category as any,
      sentiment: 'positive',
      sentiment_color: category === 'vang' ? '#E5B869' : category === 'chung_khoan' ? '#F8AFA6' : '#C86D51',
      sfx_trigger: 'paper_rustle',
      pacing_delay_ms: pacingMode === 'sync' ? 400 : 1200
    };

    if ((window as any).__spiderCrawlToKeyword) {
      (window as any).__spiderCrawlToKeyword(targetEl, index, nodeEl, eventData);
    }

    setDecisionNodes(prev =>
      prev.map(n => (n.id === targetNodeId ? { ...n, silkCount: n.silkCount + 1 } : n))
    );
    setTotalFilaments(prev => prev + 1);
  };

  const getSkinDisplayName = (id: SpiderSkinId) => {
    switch (id) {
      case 'tribal':
        return 'Gothic Tribal Neon';
      case 'mecha':
        return 'Mecha CAD Vector (Phong Cách A)';
      default:
        return 'Gothic Tribal Neon';
    }
  };

  const getEngineDisplayName = (eng: System1Engine) => {
    switch (eng) {
      case 'laya':
        return 'Laya GPU (CUDA)';
      case 'd3':
        return 'Decision 3 Lite';
      case 'mock':
        return 'Mock Engine';
      default:
        return 'Decision 3 Lite';
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        backgroundColor: '#F4F1EA',
        overflow: 'hidden',
        position: 'relative'
      }}
    >
      {/* Global Top Header Bar (48px) */}
      <TopHeaderBar
        activeTab={activeTab}
        onTabChange={tab => {
          if (isSfxEnabled) playSfx('click');
          setActiveTab(tab);
        }}
        avgLatencyMs={avgLatencyMs}
        engineName={getEngineDisplayName(system1Engine)}
        isSfxEnabled={isSfxEnabled}
        volumePercent={volumePercent}
        onToggleSfx={handleToggleSfx}
        onOpenSearch={() => setIsSearchOpen(true)}
      />

      {/* Main Viewport Container */}
      <div style={{ flex: 1, position: 'relative', overflow: 'hidden', display: 'flex' }}>
        {/* Render Active Screen */}
        {activeTab === 'arena' && (
          <div style={{ width: '100%', height: '100%', position: 'relative' }}>
            <Screen1SpiderArena
              onNavigate={setActiveTab}
              pacingMode={pacingMode}
              onPacingChange={setPacingMode}
              onKeywordClick={handleKeywordClick}
              onOpenExplain={() => setIsExplainOpen(true)}
              onOpenSkins={() => setIsSkinsOpen(true)}
              decisionNodes={decisionNodes}
              currentSkin={currentSkin}
            />
            {/* Global Spider Canvas Overlay with GSAP */}
            <SpiderCanvas currentSkin={currentSkin} />
          </div>
        )}

        {activeTab === 'feeds' && (
          <Screen2BilingualReader
            onNavigate={setActiveTab}
            onBookmarkArticle={id => {
              if (isSfxEnabled) playSfx('click');
            }}
          />
        )}

        {activeTab === 'digest' && (
          <Screen3ExecutiveDigest onNavigate={setActiveTab} />
        )}

        {activeTab === 'github' && (
          <Screen4GitHubRadar onNavigate={setActiveTab} />
        )}

        {activeTab === 'vault' && (
          <Screen5TrendVault onNavigate={setActiveTab} />
        )}

        {activeTab === 'settings' && (
          <Screen6Settings
            onNavigate={setActiveTab}
            pacingMode={pacingMode}
            onPacingChange={setPacingMode}
            system1Engine={system1Engine}
            onEngineChange={setSystem1Engine}
            isSfxEnabled={isSfxEnabled}
            onToggleSfx={handleToggleSfx}
            volumePercent={volumePercent}
            onVolumeChange={handleVolumeChange}
            onOpenAddFeed={() => setIsAddFeedOpen(true)}
          />
        )}

        {activeTab === 'analytics' && (
          <Screen7Analytics onNavigate={setActiveTab} />
        )}
      </div>

      {/* Global Bottom Telemetry Status Bar (44px) */}
      <BottomTelemetryBar
        activeTab={activeTab}
        latencyMs={avgLatencyMs ?? 8.5}
        avgLatencyMs={avgLatencyMs}
        totalFilaments={totalFilaments}
        pacingMode={pacingMode}
        onPacingChange={setPacingMode}
        onOpenFeeds={() => setIsFeedsOpen(true)}
        onOpenSkins={() => setIsSkinsOpen(true)}
        currentSkinName={getSkinDisplayName(currentSkin)}
        feedCount={feedCount}
      />

      {/* Overlays */}
      <SearchModalFTS5
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onNavigate={setActiveTab}
      />

      <DecisionExplainDrawer
        isOpen={isExplainOpen}
        onClose={() => setIsExplainOpen(false)}
      />

      <AddFeedModal
        isOpen={isAddFeedOpen}
        onClose={() => setIsAddFeedOpen(false)}
        onAddFeed={() => {
          refreshSourcesCount();
        }}
      />

      <FeedDrawer
        isOpen={isFeedsOpen}
        onClose={() => setIsFeedsOpen(false)}
        onOpenAddFeed={() => setIsAddFeedOpen(true)}
      />

      <SkinSelector
        isOpen={isSkinsOpen}
        currentSkin={currentSkin}
        onSelectSkin={skin => {
          if (isSfxEnabled) playSfx('click');
          setCurrentSkin(skin);
          setIsSkinsOpen(false);
        }}
        onClose={() => setIsSkinsOpen(false)}
      />
    </div>
  );
};
