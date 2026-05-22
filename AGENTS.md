# AGENTS.md — YouTube 字幕管線操作手冊

> *人類讀 README.md。AI agent 讀呢份。*
>
> *最後更新：2026-05-22*

---

## 呢個 repo 係咩

將任何 YouTube 影片轉化為結構化 Blog 文章 + 公開 GitHub Gist 鏡像。

Repo: `AiEira/youtube`（public）
GitHub: `https://github.com/AiEira/youtube`

---

## 四份核心文檔（分層閱讀）

| 文檔 | 對象 | 內容 |
|------|------|------|
| `README.md` | 人類 | 快速開始、格式、流程總覽 |
| `AGENTS.md` | AI agent（你在此） | 操作手冊、路徑選擇、邊界 |
| `SKILL.md` | Hermes skill trigger | Step-by-step 精確命令 + pitfalls |
| `SPEC.md` | 未來維護者 | 設計決策、踩坑史、為什麼這樣做 |

---

## 操作流程（Agent 視角）

### 觸發條件

當 user（horace）講：
- 「字幕」、「{url} 字幕」、「download transcript」
- 「放上 gist」、「gist」

### 完整 SOP

```
1. 判斷路徑
   ├─ YouTube API 有字幕？→ download-transcript.py -f blog
   └─ 字幕關閉？→ yt-dlp → mlx_whisper → clean_transcript.py

2. Blog Rewrite（LLM 將 transcript → structured blog）
   ├─ YouTube 路徑：讀 raw transcript，replace BLOG_REWRITE_PLACEHOLDER
   └─ Whisper 路徑：讀 _clean.json，寫 blog

3. 品質閘門（6 checks，必須全過）
   ☐ 尾 30 行無幻覺（無連續重複）
   ☐ 無 line number 污染
   ☐ 標題非 placeholder + ≥ 5 個 ## 章節
   ☐ 檔案 < 50KB
   ☐ 無重複段落
   ☐ Gist curl 驗證內容一致

4. Gist 鏡像
   ├─ gh gist delete {old_id} --yes（如有）
   ├─ gh gist create --public
   └─ curl 驗證

5. Mirror table
   └─ 更新 out/README.md（insert row by videoId 排序）

6. Git push
   └─ git add out/ && git commit && git push origin master
```

---

## 路徑選擇規則

### 一律先試 YouTube API

```bash
cd ./youtube
~/.hermes/hermes-agent/venv/bin/python3 src/download-transcript.py "{url}" -f blog -o out/
```

語言自動選擇：`yue` → `zh-Hant` → `zh` → `zh-Hans` → `zh-CN` → `en`

如果報錯，睇 error 入面 `available languages`，用 `-l <code>` retry。
常見需要 retry code：`yue-HK`、`zh-TW`、`zh-CN`。

### YouTube API 失敗 → Whisper

只有報 "Subtitles are disabled" 先落 Whisper 路徑。

```bash
# 1. 下載音頻
yt-dlp --no-progress -f "bestaudio[ext=m4a]" -o "/tmp/{id}.m4a" "URL"

# 2. 轉錄（用 mlx_whisper，唔係 faster_whisper）
~/.hermes/hermes-agent/venv/bin/python3 src/whisper_transcribe.py \
  /tmp/{id}.m4a --language {lang} --output-dir out/transcripts/

# 3. 清洗幻覺（必須！Skip = 垃圾入、垃圾出）
~/.hermes/hermes-agent/venv/bin/python3 src/clean_transcript.py \
  out/transcripts/{id}.json --stats
```

---

## 語言約定

| 場景 | 語言 |
|------|------|
| 對話回覆 horace | 佢英我英、佢中我繁體中 |
| README.md | 繁體中文 |
| AGENTS.md | 繁體中文 |
| SKILL.md | 繁體中文 |
| SPEC.md | 繁體中文 |
| Blog rewrite 輸出 | 跟影片語言（中 → 繁體中，英 → 英） |
| Git commit message | 英文 |
| Python source code | 英文 |

---

## Git 約定

- **out/ 追蹤 git**（blog rewrites + mirror table）
- **音頻不入 git**：`.gitignore` 排除 `*.m4a` `*.mp3` `*.wav`
- **Python 只用 Hermes venv**：`~/.hermes/hermes-agent/venv/bin/python3`
- **Git identity**：`eiraho <eira@office.biz>`
- **Commit format**：`transcript: {videoId} - {short_title}` 或 `mirror: {videoId} gist link`

---

## Gist 鐵律（三條）

1. **永不 `gh gist edit`** — 非互動模式 hang
2. **永不 PATCH** — >30KB silent fail
3. **只用 delete + create** — 最可靠

---

## Pitfalls（速查）

| 問題 | 解法 |
|------|------|
| `gh gist edit` hang | 用 delete + create |
| PATCH >30KB silent fail | 同上 |
| mlx_whisper 冇輸出 | 加 `HF_HUB_OFFLINE=1` |
| YouTube API 返回空 | retry 唔同 language code（yue-HK、zh-TW） |
| Blog 尾有重複段落 | 再清一次，check whisper 幻覺 |
| `pip` 唔 work | 用 `pip3` 或 `python3 -m pip`（Hermes venv） |
| 系統 Python 缺 mlx_whisper | 一定要用 Hermes venv 嘅 python3 |

---

## 邊界

- **呢個 repo 係 public**：blog rewrites 同 gist 全部公開
- **唔好放 horace 嘅私人資料**：只放影片內容
- **out/ 有 git 追蹤**：每次 blog rewrite 完 commit + push
- **唔好 commit 音頻檔**：`.gitignore` 已排除

---

> *SPEC.md 有完整踩坑史。遇到奇怪問題，先睇 SPEC。*
