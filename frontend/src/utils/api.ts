export const BACKEND_ORIGIN = 'http://127.0.0.1:8001';

/**
 * Trả về base URL của backend:
 * - Khi chạy Vite dev trên localhost:5173: dùng đường dẫn tương đối để đi qua Vite proxy.
 * - Khi chạy trong Tauri (tauri:// hoặc https://tauri.localhost) hoặc production: dùng trực tiếp BACKEND_ORIGIN.
 */
export const apiBase = (): string => {
  if (typeof window === 'undefined') return BACKEND_ORIGIN;
  const isLocalDevVite = window.location.hostname === 'localhost' && window.location.port === '5173';
  if (isLocalDevVite) return '';
  return BACKEND_ORIGIN;
};

export const apiUrl = (path: string): string => {
  const cleanPath = path.startsWith('/') ? path : '/' + path;
  const base = apiBase();
  return base ? `${base}${cleanPath}` : cleanPath;
};

export async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const url = apiUrl(path);
  try {
    const res = await fetch(url, init);
    if (!res.ok && !url.startsWith(BACKEND_ORIGIN)) {
      // Nếu proxy thất bại, thử gọi thẳng sang backend port 8001
      const cleanPath = path.startsWith('/') ? path : '/' + path;
      return await fetch(`${BACKEND_ORIGIN}${cleanPath}`, init);
    }
    return res;
  } catch {
    const cleanPath = path.startsWith('/') ? path : '/' + path;
    return await fetch(`${BACKEND_ORIGIN}${cleanPath}`, init);
  }
}