import { useEffect } from 'react';
import { SpiderEvent } from '../types';
import { apiBase, BACKEND_ORIGIN } from './api';

const enqueue = (ev: SpiderEvent) => {
  (window as any).__spiderEnqueueEvent?.(ev);
};

/**
 * Mở luồng SSE /api/stream/spider-events và đẩy từng SpiderEvent
 * nhận được vào FIFO animationQueue của SpiderCanvas.
 * Tự reconnect sau khi mất kết nối (5s). Không ném lỗi ra ngoài.
 */
export function useSpiderStream(enabled: boolean = true) {
  useEffect(() => {
    if (!enabled) return;
    let es: EventSource | null = null;
    let closed = false;
    let retryTimer: ReturnType<typeof setTimeout> | null = null;

    const connect = () => {
      if (closed) return;
      try {
        const url = `${apiBase()}/api/stream/spider-events`;
        es = new EventSource(url);
      } catch {
        retryTimer = setTimeout(connect, 5000);
        return;
      }

      es.addEventListener('spider_event', (e: Event) => {
        try {
          const data = JSON.parse((e as MessageEvent).data);
          enqueue(data as SpiderEvent);
        } catch {
          // bỏ qua event lỗi, giữ luồng sống
        }
      });

      // Trường hợp backend trả JSON thuần (fallback khi proxy không phải SSE)
      es.onmessage = (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data);
          if (data && data.target_word) enqueue(data as SpiderEvent);
        } catch {
          // comment ping / heartbeat — bỏ qua
        }
      };

      es.onerror = () => {
        try { es?.close(); } catch { /* noop */ }
        es = null;
        if (!closed) retryTimer = setTimeout(connect, 5000);
      };
    };

    // Tauri production (tauri://) không có Vite proxy -> thử ping backend trực tiếp
    if (typeof window !== 'undefined' && window.location.protocol === 'tauri:') {
      fetch(`${BACKEND_ORIGIN}/api/health`).catch(() => undefined).finally(connect);
    } else {
      connect();
    }

    return () => {
      closed = true;
      if (retryTimer) clearTimeout(retryTimer);
      try { es?.close(); } catch { /* noop */ }
    };
  }, [enabled]);
}
