---
name: youtube-transcript-download
description: Download YouTube video transcripts, rewrite as blog, mirror as public Gist, and push to GitHub. Self-contained — clone the repo and run.
version: 2.1.0
author: Eira (小初) for horace
metadata:
  hermes:
    tags: [youtube, transcript, download, blog, gist]
---

# YouTube 字幕下載 + Blog 改寫 + Gist 鏡像

## Setup（一次性）

```bash
git clone https://github.com/AiEira/youtube.git ./youtube
cd ./youtube
~/.hermes/hermes-agent/venv/bin/pip install youtube-transcript-api
~/.hermes/hermes-agent/venv/bin/pip install mlx-whisper  # macOS Apple Silicon GPU 加速（必需）
gh auth login  # 需要 GitHub CLI 認證以建立 Gist
```

確認 python3 ≥ 3.9，`gh` CLI 已安裝。**macOS 預設用 mlx-whisper，不安裝 faster-whisper。**

## 使用

當你（或任何人）講：
- 「下載 {url} 字幕」
- 「download {url} transcript」
- 「字幕，及加上相關新聞資料」

執行以下流程。

## Workflow

### Step 1: Download transcript

```bash
cd ./youtube && ~/.hermes/hermes-agent/venv/bin/python3 src/download-transcript.py "{url}" -f blog -o out/
```

Use `terminal(background=True, notify_on_complete=True, timeout=120)`。

**語言自動選擇**：`yue` → `zh-Hant` → `zh` → `zh-Hans` → `zh-CN` → `en`

如果 default chain 失敗，睇 error 入面嘅 available languages，用 `-l <code>` retry。
常見需要 retry 嘅 code：`yue-HK`、`zh-TW`、`zh-CN`。

**Filename convention**：`{videoId}-{短標題}.md`

### Step 1b: Whisper 轉錄（字幕被關閉時）

當 YouTube API 報 "Subtitles are disabled" 時：

```bash
# 1. 下載音頻
yt-dlp -f "bestaudio[ext=m4a]" -o "/tmp/{video_id}.m4a" "https://youtu.be/{video_id}"

# 2. mlx_whisper 轉錄（macOS Apple Silicon GPU，快）
cd ./youtube && ~/.hermes/hermes-agent/venv/bin/python3 src/whisper_transcribe.py \
  /tmp/{video_id}.m4a --language {lang} --output-dir out/transcripts/
```

Use `terminal(background=True, notify_on_complete=True, timeout=300)`。

**語言判斷**：先用 oembed 取標題判斷語言，`zh`（普通話）/ `yue`（粵語）/ `en`（英文）。

### Step 1c: 清洗幻覺（Whisper 路徑必須）

```bash
cd ./youtube && ~/.hermes/hermes-agent/venv/bin/python3 src/clean_transcript.py \
  out/transcripts/{video_id}.json --stats
```

輸出：`out/transcripts/{video_id}_clean.json`

**四條清洗規則**（靈感來自 56% 幻覺率實戰）：

| 規則 | 症狀 | 檢測 |
|------|------|------|
| **EMPTY** | segment text 空白 | `text.strip() == ""` |
| **FILLER** | 全段只有填充詞 | 所有 token 都在 FILLER_WORDS 中 |
| **DUPLICATE** | 與前一保留段完全相同 | `text == last_kept_text` |
| **LOOP** | 同一短語段內重複 ≥4 次 | 2-5 詞 sliding window 頻率檢測 |

**為什麼要清洗**：英文多人訪談 + 笑聲/重疊對話 → whisper 幻覺率可達 50%+。不清洗，blog rewrite 面對半數垃圾。中文內容幻覺率通常低很多，但清洗步驟無害。

### Step 2: Rewrite transcript into blog

Script 輸出嘅 file 有 `<!-- BLOG_REWRITE_PLACEHOLDER -->`。Replace 佢做 blog-style rewrite：

1. **Whisper 路徑**：讀取 `_clean.json`（不是 raw JSON），從 clean segments 寫 blog
2. 組織做章節，段落式書寫
3. Keep the original meaning
4. 加入「小初嘅讀後感」（如果係小初寫）

### Step 2b: 核對專有名詞

Whisper transcription 經常錯專有名詞。必須核對：
- 對照 YouTube 影片 description
- Search GitHub for project names
- Fix ALL errors in both blog AND raw transcript

### Step 3: Create public Gist mirror

**⚠️ 勿用 `gh gist edit`——非互動模式唔 work。** 用 delete + create：

```bash
# Delete old gist (if exists)
gh gist delete {gist_id}

# Create fresh gist
cd ./youtube/out
gh gist create --public --desc "{short_title}" "{filename}.md"
```

Record the gist URL.

### Step 4: Update out/README.md

Add row to the mirror table in `out/README.md`：
```
| `{videoId}` | {short_title} | [gist]({url}) |
```

### Step 5: Git push

```bash
cd ./youtube && git add out/ && git commit -m "transcript: {video_id} - {short_title}" && git push origin master
```

Git identity: set with `git config user.name` and `git config user.email` before first use.

## Script Options

- `-f blog` (default) — full transcript + blog placeholder
- `-f timestamps` — each line with [MM:SS]
- `-f raw` — plain text only
- `-l <code>` — force language code (e.g., `-l yue-HK`)

## Repo

`https://github.com/AiEira/youtube` (public)

## Pitfalls

### Gist 操作

- **`gh gist edit` 在非互動模式（cron / agent）唔 work**——佢會嘗試開 editor
- **正確更新 Gist**：用 delete + create，永不 patch（Gist PATCH >30KB silent fail）
- Blog rewrite 完成後必須 update Gist，唔好留低 `<!-- BLOG_REWRITE_PLACEHOLDER -->`
- 多餘 orphan files：在 delete + recreate 時自然消失

### YouTube API
- Transcript API can take 10-30 seconds → always use background mode
- Auto-generated subtitles may have lower quality than manual ones
- If transcript unavailable, video may have subtitles disabled
- Some videos use non-standard language codes: `yue-HK`, `zh-TW`, `zh-CN`

### Python 版本

- **所有 python 命令必須用 Hermes venv**：`~/.hermes/hermes-agent/venv/bin/python3`
- 系統 `python3` 係 macOS Xcode Python 3.9，缺 mlx_whisper 等套件 → 勿用

### Whisper 轉錄（字幕被關閉時）

- **macOS default：`mlx_whisper`（Apple Silicon GPU）** — 9 分鐘音頻約 2-3 分鐘轉錄完成
- **不要用 `faster_whisper`（CPU）** — large-v3 在 CPU 上極慢（4-5× real-time），完全不實際
- 模型：`mlx-community/whisper-large-v3-mlx`（已 cache 在 `~/.cache/huggingface/hub/`）
- 語言判斷：先用 `oembed` API 取標題，有中文用 `--language zh`，粵語用 `--language yue`
- NEVER run two Whisper processes simultaneously
- 轉錄完成後的 raw txt 需要整理為 blog 格式（加 metadata + collapsible）

### Whisper 幻覺（v2.1 新增）

三種已知幻覺形狀，來自 2026-05-21 56% 幻覺率實戰（55 分鐘英文訪談）：

| 形狀 | 觸發條件 | 實例 | 檢測 |
|------|---------|------|------|
| **循環幻覺** | 笑聲/重疊對話 | "they're like you know" × 7 段連續 | LOOP 規則 |
| **沉默幻覺** | 說話者停頓 | "Yeah." × 3.5 分鐘連續 | FILLER 規則 |
| **空白幻覺** | 背景噪音 | 900+ 空 segment | EMPTY 規則 |

**教訓**：
- 英文多人訪談 + 笑聲 = 幻覺溫床。單人獨白、中文內容風險低很多。
- **Clean step 不是 nice-to-have，是生存必須**。
- mlx_whisper 本身不是問題——幻覺是 Whisper 架構的已知限制。重點是管線韌性。
