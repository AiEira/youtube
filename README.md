# YouTube Transcript Downloader

下載 YouTube 影片逐字稿，輸出多種格式。**英語影片自動附繁體中文翻譯。**

## 語言次序

```
yue（粵語）→ zh-Hant（繁體）→ zh-Hans（簡體）→ en（英文）
```

抓取 `en` 字幕時，**自動附加 `zh-Hant` 翻譯**（一起放在 transcript 內）。可用 `--no-translate` 停用。

## 安裝

```bash
pip3 install youtube-transcript-api
```

## 使用

```bash
cd vendors/youtube/

# 部落格格式（預設）
python3 src/download-transcript.py https://youtube.com/watch?v=VIDEO_ID

# 指定輸出目錄
python3 src/download-transcript.py https://youtube.com/watch?v=VIDEO_ID -o out/

# 純文字（無時間戳）
python3 src/download-transcript.py VIDEO_ID -f raw

# 附時間戳
python3 src/download-transcript.py VIDEO_ID -f timestamps

# 摘要預覽
python3 src/download-transcript.py VIDEO_ID -f summary

# 自動分段章節
python3 src/download-transcript.py VIDEO_ID -f chapters

# 指定語言偏好
python3 src/download-transcript.py VIDEO_ID -l zh,en

# 自訂標題
python3 src/download-transcript.py VIDEO_ID -t "我的標題"

# 停用自動翻譯
python3 src/download-transcript.py VIDEO_ID --no-translate
```

## 輸出格式

| 格式 | 說明 | 輸出 |
|------|------|------|
| `blog` ⭐ | 部落格格式，全文逐字稿 | `out/{videoId}-{短標題}.md` |
| `raw` | 純文字，無格式 | 同上 |
| `timestamps` | 每行附 `[MM:SS]` | 同上 |
| `summary` | 摘要預覽 | 同上 |
| `chapters` | 每 3 分鐘自動分段 | 同上 |

## 結構

```
vendors/youtube/
├── README.md
├── src/
│   └── download-transcript.py   ← 主程式
└── out/                         ← 預設輸出目錄
```

## 支援的 URL 格式

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- `https://youtube.com/live/VIDEO_ID`
- 或直接傳入 11 位 video ID
