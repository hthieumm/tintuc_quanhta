export type ScreenTab =
  | 'arena'       // Screen 1: Spider Web Arena
  | 'feeds'       // Screen 2: Curated Feeds & Bilingual Reader
  | 'digest'      // Screen 3: Executive Intelligence Digest
  | 'analytics'   // Screen 7: Macro Analytics & Chart Metrics
  | 'github'      // Screen 4: GitHub Tech Radar
  | 'vault'       // Screen 5: Trend Vault & Knowledge Graph
  | 'settings';   // Screen 6: Settings & Data Retention

export type SpiderCategory = 
  | "kinh_te" 
  | "chung_khoan" 
  | "vang" 
  | "crypto" 
  | "chinh_tri" 
  | "github" 
  | "quoc_te";

export type SpiderSentiment = "positive" | "negative" | "neutral";
export type SentimentColor = "#F8AFA6" | "#C86D51" | "#E5B869";

export interface SpiderEvent {
  event_id: string;
  article_id: number;
  target_word: string;
  target_index: number;
  category: SpiderCategory;
  sentiment: SpiderSentiment;
  sentiment_color: SentimentColor;
  sfx_trigger: "water_drop" | "paper_rustle" | "wind_chime";
  pacing_delay_ms: number;
}

export type SpiderSkinId = 'tribal' | 'mecha';

export interface DecisionNode {
  id: string;
  label: string;
  category: SpiderCategory;
  silkCount: number;
  subText: string;
  color: string;
  active?: boolean;
}

export type PacingMode = 'sync' | 'chill';

export type System1Engine = 'auto' | 'laya' | 'd3' | 'mock';

export interface ArticleItem {
  id: number;
  title: string;
  titleEn?: string;
  source: string;
  timeAgo: string;
  category: SpiderCategory;
  categoryName: string;
  summary: string;
  summaryEn?: string;
  contentVi: string[];
  contentEn: string[];
  decisionScore: number;
  routedNode: string;
  sentimentScore: number;
  isBookmarked: boolean;
  sha256Hash: string;
  author: string;
  url?: string;
  language?: string;
  source_category?: string;
}

export interface DigestPanel {
  title: string;
  tag: string;
  tagColor: string;
  highlights: string[];
  narrativeMarkdown: string;
  macroImpact: string;
}

export interface ExecutiveDigestData {
  date: string;
  totalArticles: number;
  sentimentScore: number;
  confidenceScore: number;
  durationSec: number;
  ratio: {
    macro: number;
    geopolitics: number;
    tech: number;
  };
  panels: {
    macro: DigestPanel;
    geopolitics: DigestPanel;
    tech: DigestPanel;
  };
}

export interface GitHubRepoItem {
  name: string;
  owner: string;
  stars: number;
  todayStars: number;
  forks: number;
  language: string;
  license: string;
  description: string;
  score: number;
  latencyMs: number;
  ramUsageMb: number;
  system1Port: number;
  isBookmarked: boolean;
}

export interface KnowledgeNode {
  id: string;
  label: string;
  type: 'central' | 'stable' | 'risk' | 'watch';
  category: SpiderCategory;
  metric: string;
  change: string;
  articlesCount: number;
  isBookmarked?: boolean;
}

export interface RSSSourceItem {
  id: number;
  name: string;
  url: string;
  category: SpiderCategory;
  itemCount: number;
  isActive: boolean;
  lastUpdated: string;
}
