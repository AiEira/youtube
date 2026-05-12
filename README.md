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

# 自訂標題
python3 src/download-transcript.py VIDEO_ID -t "我的標題"

# 停用自動翻譯
python3 src/download-transcript.py VIDEO_ID --no-translate
```

## 輸出格式

| 格式 | 說明 |
|------|------|
| `blog` ⭐ | 前端：重寫為段落式 Blog 文章；文末：`<details>` 收起逐字稿 |
| `raw` | 純文字，無格式 |
| `timestamps` | 每行附 `[MM:SS]` |
| `summary` | 摘要預覽 |
| `chapters` | 每 3 分鐘自動分段 |

所有格式輸出至 `out/{videoId}-{短標題}.md`（標題截取前 20 字）。

## 工作流程

```
下載字幕 → 腳本輸出逐字稿（collapsible）
         → LLM 重寫為 Blog 文章（前端）
         → git push → 手機可讀
```

## 結構

```
vendors/youtube/
├── README.md
├── .gitignore
├── src/
│   └── download-transcript.py   ← 主程式
└── out/                         ← 輸出目錄（git tracked）
```

## 支援的 URL 格式

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- `https://youtube.com/live/VIDEO_ID`
- 或直接傳入 11 位 video ID
