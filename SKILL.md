---
name: youtube-transcript-download
description: Download YouTube video transcripts, rewrite as blog, mirror as public Gist, and push to GitHub. Self-contained — clone the repo and run.
version: 2.0.0
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
pip3 install youtube-transcript-api
pip3 install mlx-whisper  # macOS Apple Silicon GPU 加速（必需）
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
cd ./youtube && python3 src/download-transcript.py "{url}" -f blog -o out/
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
~/.hermes/hermes-agent/venv/bin/mlx_whisper /tmp/{video_id}.m4a \
  --language zh --model mlx-community/whisper-large-v3-mlx \
  --output-dir /tmp/ --output-format txt

# 3. 將 /tmp/{video_id}.txt 整理成 blog 格式 → out/{video_id}-{短標題}.md
```

Use `terminal(background=True, notify_on_complete=True, timeout=300)`。

**語言判斷**：先用 oembed 取標題判斷語言，`zh`（普通話）/ `yue`（粵語）/ `en`（英文）。

### Step 2: Rewrite transcript into blog

Script 輸出嘅 file 有 `<!-- BLOG_REWRITE_PLACEHOLDER -->`。Replace 佢做 blog-style rewrite：

1. 組織做章節，段落式書寫
2. Keep the original meaning
3. 加入「小初嘅讀後感」（如果係小初寫）

### Step 2b: 核對專有名詞

Whisper transcription 經常錯專有名詞。必須核對：
- 對照 YouTube 影片 description
- Search GitHub for project names
- Fix ALL errors in both blog AND raw transcript

### Step 3: Create public Gist mirror

```bash
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

### YouTube API
- Transcript API can take 10-30 seconds → always use background mode
- Auto-generated subtitles may have lower quality than manual ones
- If transcript unavailable, video may have subtitles disabled
- Some videos use non-standard language codes: `yue-HK`, `zh-TW`, `zh-CN`

### Python Version
- Use Python ≥ 3.9
- If using Hermes, prefer Hermes venv python (`~/.hermes/hermes-agent/venv/bin/python3`)

### Whisper 轉錄（字幕被關閉時）

- **macOS default：`mlx_whisper`（Apple Silicon GPU）** — 9 分鐘音頻約 2-3 分鐘轉錄完成
- **不要用 `faster_whisper`（CPU）** — large-v3 在 CPU 上極慢（4-5× real-time），完全不實際
- 模型：`mlx-community/whisper-large-v3-mlx`（已 cache 在 `~/.cache/huggingface/hub/`）
- 語言判斷：先用 `oembed` API 取標題，有中文用 `--language zh`，粵語用 `--language yue`
- NEVER run two Whisper processes simultaneously
- 轉錄完成後的 raw txt 需要整理為 blog 格式（加 metadata + collapsible）
