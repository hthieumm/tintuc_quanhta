# 19 — DECK SPEC SCHEMA (JSON cho adapter (b) python-pptx)

> **Nạp khi** adapter = **(b) python-pptx**. Đây là cầu nối giữa DECK SPEC markdown (`00-output-spec.md` §2) và `build_deck.py` (`16-tool-adapters.md` §B).
> **Quy tắc:** file `deck_spec.json` = chuyển **máy-móc** DECK SPEC sang JSON. Không thêm thứ gì không có trong spec; không bỏ element nào.

## 1. Cấu trúc

```json
{
  "meta": {
    "title": "Đặc điểm dân tộc Việt Nam",
    "medium": "b-pptx",
    "style": "wavy-asymmetric",
    "canvas": { "w": 1920, "h": 1080 },
    "grid": { "cols": 12, "margin_pct": 5, "gutter_pct": 1.25, "pitch_pct": 7.60 },
    "palette": {
      "bg": "A61E22", "surface": "FEF9E3", "accent": "FACC15",
      "text": "1A1A1A", "text_inverse": "FEF9E3"
    },
    "fonts": { "heading": "Playfair Display", "body": "Be Vietnam Pro" }
  },
  "slides": [ { "...": "..." } ]
}
```

- `hex` luôn **không có `#`** — `RGBColor.from_string()` cần đúng 6 ký tự.
- `meta.palette` chỉ chứa màu thật dùng ≤5; không để màu placeholder.
- Adapter (a) và (c) **không dùng file này** — (a) đọc Markdown, (c) người dựng tay đọc `00 §2` + `16 §C`.

## 2. Một slide

```json
{
  "index": 1,
  "type": "cover",
  "archetype": "full-bleed-hero",
  "title": "Đặc điểm dân tộc Việt Nam — 54 dân tộc, 1 văn hoá giao thoa",
  "notes": "4 phút — đây là trang mở. Không nói gì hết, chờ 2s rồi bấm.",
  "elements": [ { "...": "..." } ]
}
```

| Field | Bắt buộc | Giá trị |
|---|---|---|
| `index` | có | số thứ tự, bắt đầu từ 1 |
| `type` | có | `cover` \| `agenda` \| `divider` \| `content` \| `quote` \| `data` \| `closing` |
| `archetype` | có | tên archetype trong `01-layout.md` §4 (bỏ dấu gạch ngang để làm key) |
| `title` | có | chuỗi rỗng nếu slide không có tiêu đề |
| `notes` | có | speaker notes — luôn điền, kể cả 1 câu |
| `elements` | có | mảng, **thứ tự = z-order tăng dần** |

## 3. Một element

```json
{
  "id": "E3",
  "role": "title",
  "x": 8, "y": 62, "w": 70, "h": 16,
  "z": 3,
  "text": "Đặc điểm dân tộc Việt Nam",
  "font": { "role": "H1", "size_px": 72, "weight": 800, "family": "Playfair Display", "line_height": 1.1, "align": "left" },
  "fill": null,
  "opacity": null,
  "frame": null,
  "alt": null,
  "src": null,
  "crop": null,
  "href": null
}
```

| Field | Bắt buộc | Quy tắc |
|---|---|---|
| `id` | có | khớp `[E<n>]` trong Markdown spec |
| `role` | có | `img` \| `title` \| `body` \| `caption` \| `number` \| `rule` \| `scrim` \| `card` \| `icon` \| `container` |
| `x,y,w,h` | có | **đơn vị %** (0–100, 1 chữ số thập phân). Không dùng px trong file này |
| `z` | có | số thứ tự đặt, cũng là thứ tự phần tử trong `elements` |
| `text` | khi role = chữ | không để `null` |
| `font` | khi role = chữ | `size_px` là **px** (adapter tự đổi sang pt) |
| `fill` | khi role = khối màu | hex 6 ký tự, không `#` |
| `opacity` | tuỳ chọn | 0–100 (scrim: 55 = 55%) |
| `frame` | tuỳ chọn | `{"shape":"rounded","radius_px":16}` hoặc `{"shape":"blob","path":"..."}` |
| `alt` | **bắt buộc** khi role = `img`/`icon` | mô tả cảnh, không phải tên file |
| `src` | bắt buộc khi role = `img` | đường dẫn tương đối trong `assets/` |
| `crop` | tuỳ chọn | `{"l":0,"t":0,"r":0,"b":0}` trong 0–1 |
| `href` | tuỳ chọn | URL hoặc `#slide-3` |

## 4. Quy tắc chuyển đổi Markdown → JSON

| Trong `00 §2` | Thành JSON |
|---|---|
| `Palette: bg #A61E22 \| surface #FEF9E3 ...` | `meta.palette` (bỏ `#`) |
| `[E1] img x:0% y:0% ... \| alt: "..."` | `{"id":"E1","role":"img","x":0,...,"alt":"..."}` |
| `\| z:3` | `z` + vị trí trong `elements` |
| `font:H1 72px/800 Playfair Display` | `font.size_px=72, weight=800, family="Playfair Display"` |
| `fill:#3A0A0A opacity:55%` | `fill:"3A0A0A", opacity:55` |
| `frame:rounded 24px` | `frame:{"shape":"rounded","radius_px":24}` |
| `Click order: E3 → E4` | **bỏ qua** — python-pptx không có on-click (16 §B "Giới hạn") |
| `Transition: pan-left 0.7s` | **bỏ qua** — không có API transition |
| `Contrast: ... PASS` | không đưa vào JSON (kiểm ở `00 §5`, không phải lúc build) |

## 5. Sai lầm thường gặp

- Nhân 4 lần `duration_sec × 60/11` cho pacing → sai. Đúng là `duration_sec / 11` (xem `00 §5` #4).
- Để `#` trong hex → `RGBColor.from_string()` ném lỗi.
- Dùng `px` cho `x/y/w/h` → tràn khung. File này **chỉ %**.
- Truyền `animation` vào JSON → bị bỏ qua âm thầm, dễ tưởng đã có on-click.
- Thiếu `alt` cho `img` → fail check #2 của `00 §5`.
- Element có `x` + `w` vượt 100 → tràn slide, không có cảnh báo.
