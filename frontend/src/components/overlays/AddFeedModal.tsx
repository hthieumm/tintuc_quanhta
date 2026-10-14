import React, { useState } from 'react';
import { SpiderCategory } from '../../types';
import { playSfx } from '../../utils/audio';

import { apiFetch } from '../../utils/api';

interface AddFeedModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddFeed: (name: string, url: string, category: SpiderCategory) => void;
}

export const AddFeedModal: React.FC<AddFeedModalProps> = ({ isOpen, onClose, onAddFeed }) => {
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');
  const [category, setCategory] = useState<SpiderCategory>('kinh_te');
  const [isValidating, setIsValidating] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setErrorMsg('Vui lòng nhập tên nguồn tin.');
      return;
    }
    if (!url.trim().startsWith('http')) {
      setErrorMsg('URL phải bắt đầu bằng http:// hoặc https://');
      return;
    }

    setIsValidating(true);
    setErrorMsg(null);
    playSfx('click');

    try {
      const res = await apiFetch('/api/v1/sources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          url: url.trim(),
          category,
          source_type: 'rss',
          fetch_interval_min: 15
        })
      });
      if (!res.ok) {
        const data = await res.json();
        setErrorMsg(data.detail || 'Không thể thêm nguồn tin này (URL không hợp lệ hoặc đã tồn tại)');
        setIsValidating(false);
        return;
      }
      playSfx('wind_chime');
      onAddFeed(name.trim(), url.trim(), category);
      setName('');
      setUrl('');
      onClose();
    } catch (err: any) {
      setErrorMsg(err.message || 'Lỗi kết nối máy chủ');
    } finally {
      setIsValidating(false);
    }
  };

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.4)',
        backdropFilter: 'blur(3px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 100
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          width: '480px',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #DCD5C5',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: '16px', fontWeight: 700, color: '#2D4A2B' }}>
            + Thêm Nguồn Tin RSS Mới
          </h2>
          <button
            onClick={onClose}
            style={{
              border: 'none',
              backgroundColor: '#F4F1EA',
              borderRadius: '50%',
              width: '26px',
              height: '26px',
              cursor: 'pointer',
              fontSize: '11px'
            }}
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '11px', fontWeight: 600, color: '#2D4A2B' }}>Tên Nguồn Tin:</label>
            <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Ví dụ: Báo Đầu Tư Vĩ Mô"
              style={{
                padding: '8px 10px',
                borderRadius: '6px',
                border: '1px solid #DCD5C5',
                fontSize: '12px',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '11px', fontWeight: 600, color: '#2D4A2B' }}>URL RSS Feed:</label>
            <input
              type="text"
              value={url}
              onChange={e => setUrl(e.target.value)}
              placeholder="https://example.com/rss/macro.xml"
              style={{
                padding: '8px 10px',
                borderRadius: '6px',
                border: '1px solid #DCD5C5',
                fontSize: '12px',
                fontFamily: 'var(--font-mono)',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '11px', fontWeight: 600, color: '#2D4A2B' }}>Chuyên Mục Phân Loại:</label>
            <select
              value={category}
              onChange={e => setCategory(e.target.value as SpiderCategory)}
              style={{
                padding: '8px 10px',
                borderRadius: '6px',
                border: '1px solid #DCD5C5',
                fontSize: '12px',
                outline: 'none'
              }}
            >
              <option value="kinh_te">Kinh Tế Vĩ Mô & Tiền Tệ</option>
              <option value="chung_khoan">Chứng Khoán VN</option>
              <option value="vang">Vàng & Ngoại Tệ</option>
              <option value="crypto">Crypto & Web3</option>
              <option value="chinh_tri">Địa Chính Trị Quốc Tế</option>
              <option value="github">GitHub Tech & AI</option>
            </select>
          </div>

          {errorMsg && (
            <div style={{ color: '#C86D51', fontSize: '11px', fontWeight: 600 }}>
              ⚠️ {errorMsg}
            </div>
          )}

          <div style={{ fontSize: '10.5px', color: '#5A6B5C', lineHeight: '1.4' }}>
            Hệ thống sẽ tự động xác thực chuẩn XML RSS và kiểm tra trạng thái HTTP 200 trước khi lưu vào SQLite.
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '6px' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '7px 14px',
                borderRadius: '6px',
                border: '1px solid #DCD5C5',
                backgroundColor: '#FFFFFF',
                fontSize: '11.5px',
                cursor: 'pointer'
              }}
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={isValidating}
              style={{
                padding: '7px 16px',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: '#2D4A2B',
                color: '#FAF8F5',
                fontSize: '11.5px',
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              {isValidating ? 'Đang Kiểm Tra XML...' : 'Xác Thực & Thêm Nguồn'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
