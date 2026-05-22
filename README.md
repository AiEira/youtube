# YouTube 字幕管線

> 將任何 YouTube 影片轉化為結構化 Blog 文章 + 公開 Gist 鏡像。
>
> 完整設計哲學與踩坑記錄：[SPEC.md](SPEC.md)

## 語言優先序

```
yue（粵語）→ yue-HK → zh-Hant（繁體）→ zh-TW → zh（普通話）→ zh-Hans（簡體）→ zh-CN → en
```

英文影片自動附加 `zh-Hant` 翻譯。可用 `--no-translate` 停用。

## 快速開始

```bash
# 安裝（僅 Hermes venv）
~/.hermes/hermes-agent/venv/bin/pip install youtube-transcript-api mlx-whisper

# 下載字幕 + Blog 模板
~/.hermes/hermes-agent/venv/bin/python3 src/download-transcript.py "https://youtu.be/VIDEO_ID" -f blog -o out/

# 然後由 LLM 完成 Blog Rewrite → 品質閘門 → Gist 鏡像
```

## 五種輸出格式

| 格式 | 說明 |
|------|------|
| `blog` ⭐ | 元數據 + `<!-- BLOG_REWRITE_PLACEHOLDER -->` + collapsible 逐字稿 |
| `raw` | 純文字，無格式 |
| `timestamps` | 每行附 `[MM:SS]` |
| `summary` | 摘要預覽 |
| `chapters` | 每 3 分鐘自動分段 |

所有格式輸出至 `out/{videoId}-{短標題}.md`。

## 雙路徑架構

```
YouTube URL
    │
    ├── 字幕可用？──YES──→ youtube-transcript-api → download-transcript.py
    │
    └── NO ──→ yt-dlp → mlx_whisper → clean_transcript.py → 清洗
                     │
                     ▼
               Blog Rewrite（LLM）
                     │
                     ▼
              品質閘門（6 checks）
                     │
              通過 → Gist 鏡像 → Mirror table → git push
              失敗 → 回修
```

### 路徑 A：YouTube API（優先）

```bash
~/.hermes/hermes-agent/venv/bin/python3 src/download-transcript.py "URL" -f blog -o out/
```

字幕直接拉取，乾淨、免費、秒回。

### 路徑 B：Whisper 語音轉錄（字幕被關閉時）

```bash
# 1. 下載音頻
yt-dlp --no-progress -f "bestaudio[ext=m4a]" -o "/tmp/{id}.m4a" "https://youtu.be/{id}"

# 2. mlx_whisper 轉錄（Apple Silicon GPU 加速）
~/.hermes/hermes-agent/venv/bin/python3 src/whisper_transcribe.py \
  /tmp/{id}.m4a --language {lang} --output-dir out/transcripts/

# 3. 清洗幻覺（必須）
~/.hermes/hermes-agent/venv/bin/python3 src/clean_transcript.py \
  out/transcripts/{id}.json --stats

# 4. 由 LLM 從 _clean.json 做 Blog Rewrite
```

**⚠️ 只用 mlx_whisper（Apple Silicon GPU）。不要用 faster_whisper（CPU，比 realtime 慢 4-5×）。**

## 品質閘門（6 checks）

在說「搞掂」之前：

| # | 檢查 | 方法 |
|---|------|------|
| 1 | 尾 30 行無幻覺 | `read_file` 尾 30 行 |
| 2 | 無 line number 污染 | 肉眼掃描 |
| 3 | 標題正確 + ≥ 5 章節 | 數 `##` |
| 4 | 檔案 < 50KB | `ls -la` |
| 5 | 無重複段落 | 搜尋重複短語 |
| 6 | Gist 內容 = 本地 | `curl` + `wc -l` 比對 |

## 完整流程

詳細步驟見 [SKILL.md](SKILL.md)。簡化版：

```
下載字幕 → (Whisper 路徑: 清洗) → Blog Rewrite → 品質閘門
    → delete old gist + create new → 更新 out/README.md mirror table
    → git commit + push
```

## 目錄結構

```
vendors/youtube/
├── README.md          ← 你正在讀（人類入門）
├── AGENTS.md          ← AI agent 操作手冊
├── SKILL.md           ← Hermes skill 觸發格式
├── SPEC.md            ← 設計決策與踩坑全紀錄
├── .gitignore         # 只排除音頻（*.m4a *.mp3 *.wav）
├── src/
│   ├── download-transcript.py    ← YouTube API 字幕下載
│   ├── whisper_transcribe.py     ← mlx_whisper CLI 封裝
│   └── clean_transcript.py       ← 四規則幻覺清洗器
└── out/                ← 輸出目錄（追蹤 git）
    ├── README.md                 ← Mirror table（Gist 連結）
    ├── {videoId}-{title}.md      ← Blog rewrite 成品
    └── transcripts/              ← Whisper 原始 + 清洗輸出
```

**out/ 追蹤 git**——只有音頻檔（m4a/mp3/wav）被 `.gitignore` 排除。

## 支援的 URL 格式

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- `https://youtube.com/live/VIDEO_ID`
- 或直接傳入 11 位 video ID

---

> *不貼膏藥。不允許垃圾藏在地毯下。— SPEC.md*
