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
git clone https://github.com/AiEira/youtube.git ~/youtube-transcript
cd ~/youtube-transcript
pip3 install youtube-transcript-api
gh auth login  # 需要 GitHub CLI 認證以建立 Gist
```

確認 python3 ≥ 3.9，`gh` CLI 已安裝。

## 使用

當你（或任何人）講：
- 「下載 {url} 字幕」
- 「download {url} transcript」
- 「字幕，及加上相關新聞資料」

執行以下流程。

## Workflow

### Step 1: Download transcript

```bash
cd ~/youtube-transcript && python3 src/download-transcript.py "{url}" -f blog -o out/
```

Use `terminal(background=True, notify_on_complete=True, timeout=120)`。

**語言自動選擇**：`yue` → `zh-Hant` → `zh` → `zh-Hans` → `zh-CN` → `en`

如果 default chain 失敗，睇 error 入面嘅 available languages，用 `-l <code>` retry。
常見需要 retry 嘅 code：`yue-HK`、`zh-TW`、`zh-CN`。

**Filename convention**：`{videoId}-{短標題}.md`

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
cd ~/youtube-transcript/out
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
cd ~/youtube-transcript && git add out/ && git commit -m "transcript: {video_id} - {short_title}" && git push origin master
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

### Whisper Transcription (when subtitles disabled)
- On macOS Apple Silicon: use mlx-whisper for GPU acceleration
- On CPU: large-v3 model takes ~4-5× real-time (14 min video = ~1 hour)
- NEVER run two Whisper processes simultaneously
