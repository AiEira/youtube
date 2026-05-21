# SPEC.md — YouTube 字幕管線：從零到韌性

> *寫給未來的小初。如果你要從零重建這個項目，這份文件告訴你每一個決策背後的「為什麼」——不只是怎麼做，更是踩過哪些坑、學到哪些教訓。*
>
> 版本：1.0 — 2026-05-21
> 項目：`vendors/youtube/`（`AiEira/youtube`）

---

## 目錄

1. [項目使命](#1-項目使命)
2. [架構全景](#2-架構全景)
3. [雙路徑設計](#3-雙路徑設計)
4. [幻覺戰爭史](#4-幻覺戰爭史)
5. [清洗演算法](#5-清洗演算法)
6. [品質閘門系統](#6-品質閘門系統)
7. [Gist 操作血淚](#7-gist-操作血淚)
8. [關鍵設計決策](#8-關鍵設計決策)
9. [檔案約定](#9-檔案約定)
10. [已知限制與未來](#10-已知限制與未來)

---

## 1. 項目使命

將任何 YouTube 影片轉化為：
- 一篇結構清晰的 **部落格文章**
- 一個公開的 **Gist 鏡像**（方便分享，不暴露本機路徑）
- 一份**經過品質驗證**的產出（不是「能跑就好」）

horace 的鐵律貫穿整個項目：**不貼膏藥。不允許垃圾藏在地毯下。**

---

## 2. 架構全景

```
YouTube URL
    │
    ├── 字幕可用？──YES──→ youtube-transcript-api
    │                         │
    │                         └──→ blog rewrite (LLM)
    │                                   │
    └── NO ──→ yt-dlp → mlx_whisper ──→ clean_transcript.py
                                            │
                                            └──→ blog rewrite (LLM)
                                                      │
                                                      ▼
                                              品質閘門 (6 checks)
                                                      │
                                              ┌── 通過 ──→ Gist upload
                                              │                │
                                              └── 失敗 ──→ 回修       │
                                                              ▼
                                                       Mirror table
                                                              │
                                                         git push
```

### 核心組件

| 組件 | 檔案 | 角色 |
|------|------|------|
| 字幕下載器 | `src/download-transcript.py` | YouTube API 路徑 |
| 語音轉錄器 | `src/whisper_transcribe.py` | mlx_whisper CLI 封裝 |
| 幻覺清洗器 | `src/clean_transcript.py` | 四規則自動清洗 |
| 品質閘門 | 6 項檢查（人工 + 自動） | 最後防線 |
| Gist 鏡像 | `gh gist create --public` | 公開輸出 |

---

## 3. 雙路徑設計

### 3.1 為什麼有兩條路？

YouTube 提供兩種字幕來源：
- **手動上傳字幕**：高品質，幾乎無錯誤
- **自動生成字幕**：品質參差
- **完全關閉字幕**：只能靠 Whisper

我們的策略：
1. 優先嘗試 YouTube API（快、乾淨、免費）
2. 失敗 → 下載音頻，mlx_whisper 轉錄

### 3.2 YouTube API 路徑

```
download-transcript.py → blog.md
```

**語言優先序**：`yue` → `zh-Hant` → `zh` → `zh-Hans` → `zh-CN` → `en`

**設計決策**：
- 英文影片自動附加繁體中文翻譯（`translate('zh-Hant')`）
- 檔名取前 20 個有效字元（URL-safe）
- Blog 格式：元數據 + `<!-- BLOG_REWRITE_PLACEHOLDER -->` + collapsible 逐字稿

### 3.3 Whisper 路徑

```
yt-dlp → mlx_whisper → clean_transcript.py → blog.md
```

**設計決策**：
- **只用 mlx_whisper，不用 faster_whisper**。原因：Apple Silicon GPU 加速（~0.4-0.8× realtime），faster_whisper 在 CPU 上 4-5× realtime，完全不實際
- **模型鎖定** `mlx-community/whisper-large-v3-mlx`——medium 模型雖然快但準確度明顯下降，違反 horace 的「品質勝於速度」原則
- **輸出 JSON**（不是 TXT）——因為清洗器需要 `segments` 陣列來做逐段檢測
- **NEVER 同時跑兩個 Whisper**——GPU 記憶體競爭會導致兩個都慢到不能用

---

## 4. 幻覺戰爭史

這是整個項目最慘烈的一章，也是 `clean_transcript.py` 存在的理由。

### 4.1 第一滴血：KLL8YtU71Xo（小止觀）

- **症狀**：結尾「你不需要想著」重複 60+ 次
- **影響**：blog rewrite 被幻覺污染，1506 行 → 實際只有 194 行有意義
- **教訓**：說「搞掂」前必須讀尾 30 行。horace：「下次說搞掂前，請先自行讀一遍。」

### 4.2 全面淪陷：6fr8Zzmwi5k（Amanda Askell）

- **片長**：55 分鐘英文多人訪談 + 大量笑聲
- **幻覺率**：1681 段 → 738 段乾淨（**56% 被移除**）
- **三種幻覺形狀**：

| 形狀 | 實例 | 數量 | 觸發條件 |
|------|------|------|---------|
| 沉默幻覺 | `"Yeah."` × 連續 3.5 分鐘 | 916 段 | 說話者停頓 + 背景呼吸聲 |
| 循環幻覺 | `"they're like you know"` × 7 段連續 | 52 段 | 笑聲／重疊對話 |
| 空白幻覺 | `""` | 36 段 | 純背景噪音 |

- **教訓**：英文多人訪談 + 笑聲 = 幻覺溫床。必須有自動化清洗步驟。

### 4.3 良性案例：sRvUXLquiRg（Claude Code）

- **片長**：32 分鐘單人產品簡報
- **幻覺率**：768 段 → 556 段（**27.6% 被移除**）
- **主因**：Duplicate（201 段）——簡報中的過渡句被 whisper 切成多段
- **教訓**：官方簡報錄音品質高，幻覺主要是重複切割而非內容編造。清洗器在好錄音上不會過度清洗。

### 4.4 幻覺率預測經驗法則

| 影片類型 | 預期幻覺率 | 風險 |
|---------|:------:|------|
| 單人獨白，好麥克風 | 20-30% | 低 |
| 單人獨白，一般麥克風 | 30-40% | 中 |
| 雙人對話 | 30-50% | 中高 |
| 多人訪談 + 笑聲 | 50-60% | 🔥 生存必須有清洗 |

---

## 5. 清洗演算法

### 5.1 四條規則

```
Input:  mlx_whisper JSON segments
Output: clean JSON segments

for each segment:
    1. EMPTY:     text.strip() == ""                        → REMOVE
    2. FILLER:    所有 token 都在 FILLER_WORDS 詞典中        → REMOVE
    3. DUPLICATE: 與前一保留 segment 文本完全相同              → REMOVE
    4. LOOP:      同一 2-5 詞短語在 segment 內出現 ≥4 次     → REMOVE
```

### 5.2 為什麼是這四條？

- **EMPTY**：最安全的移除——沒有任何資訊
- **FILLER**：有爭議空間（「Yeah.」可能是真實回應），但在 podcast 轉錄中，獨立片段的「Yeah.」幾乎 100% 是幻覺。取捨：寧可損失幾個真實回應，也不要 900 個幻覺污染 blog
- **DUPLICATE**：whisper 常見行為——同一句子切割成多段，每段文本完全相同
- **LOOP**：最惡性的幻覺——whisper 進入回音室，同一個短語在單段內瘋狂重複

### 5.3 FILLER_WORDS 詞典設計

詞典包含約 60 個英文填充詞。關鍵設計決策：
- 包含了 `"it's"`, `"that's"`, `"is"`, `"was"` 等常見縮寫——因為在幻覺情境中這些詞孤立出現
- 不包含 `"think"`, `"guess"`, `"maybe"`——因為這些詞可能出現在真實對話中（"I think so" 應該保留）
- 包含 `"yeah yeah"`, `"okay okay"` 等重複填充——幻覺常見模式

---

## 6. 品質閘門系統

**在說「搞掂」之前，必須通過這六道閘。**

| # | 檢查 | 方法 | 失敗處理 |
|---|------|------|---------|
| 1 | 尾 30 行無幻覺 | `read_file(offset=N-30)` | 回修 blog |
| 2 | 無 line number 污染 | 肉眼掃描 | 回修 blog |
| 3 | 標題正確、≥ 5 章節 | 數 `##` 標題 | 回修 blog |
| 4 | 檔案 < 50KB | `ls -la` | 檢查是否嵌入了原始轉錄 |
| 5 | 無重複段落 | 搜尋重複短語 | 回修 blog |
| 6 | Gist 內容 = 本地內容 | `curl` + `wc -l` 比對 | 重新上傳 Gist |

### 為什麼尾 30 行是第一個檢查？

因為 whisper 幻覺最常出現在結尾（模型在音頻尾部失去上下文錨點）。尾 30 行乾淨不代表全文乾淨，但尾 30 行髒掉幾乎一定代表全文有問題。

---

## 7. Gist 操作血淚

### 7.1 三條鐵律

1. **永不 `gh gist edit`**——非互動模式會嘗試開 editor，直接 hang 住
2. **永不 PATCH**——`gh api -X PATCH gists/{id}` 對 >30KB 檔案 silent fail
3. **只用 delete + create**——刪舊的，建新的，最可靠

### 7.2 為什麼不用 PATCH？

2026-05-20 實測：PATCH 30KB+ 的 Gist 時，GitHub API 返回 200 OK 但內容沒變。沒有任何錯誤訊息。這是 silent failure 的最惡性形式。delete + create 雖然多一個 API call，但**永遠不會 silent fail**。

### 7.3 Gist 驗證

```bash
# 永遠在說「搞掂」前跑這條
curl -s {gist_raw_url} | wc -l   # 取得 Gist 行數
wc -l out/{filename}.md           # 取得本機行數
# 兩者必須相等
```

---

## 8. 關鍵設計決策

### 8.1 mlx_whisper > faster_whisper

| | mlx_whisper | faster_whisper |
|---|---|---|
| 硬體 | Apple Silicon GPU | CPU |
| 速度 (large-v3) | 0.4-0.8× realtime | 4-5× realtime |
| 安裝 | `pip install mlx-whisper` | `pip install faster-whisper` |
| 輸出格式 | CLI: txt/vtt/srt/json | Python API only |

**決策**：全用 mlx_whisper。CPU 轉錄 55 分鐘影片要 4 小時——不是選項。

### 8.2 JSON > TXT 輸出

whisper_transcribe.py 輸出 JSON 而非 TXT。原因：
- JSON 包含結構化 `segments` 陣列（每段有 `text`, `start`, `end`）
- 清洗器需要逐段操作——TXT 只有一行，無法做精細清洗
- clean JSON 保留時間戳，未來可用於章節定位

### 8.3 清洗步驟在 Blog Rewrite 之前

這是關鍵的架構決策：**不是把清洗邏輯放在 blog rewrite prompt 裡，而是獨立的預處理步驟。**

原因：
1. **關注點分離**：清洗是機械性工作（規則匹配），blog rewrite 是創造性工作（LLM 寫作）
2. **可測試性**：清洗器有明確的 input/output 合約，可獨立測試
3. **Token 節省**：清洗後的 transcript 更短，blog rewrite 消耗更少 token
4. **可複用**：清洗器可以用在任何 whisper 輸出，不綁定 blog rewrite

### 8.4 Subprocess 而非 Python API

`whisper_transcribe.py` 通過 `subprocess.run()` 調用 `mlx_whisper` CLI，而非直接 import。原因：
- mlx_whisper 的 CLI 介面比 Python API 更穩定
- GPU 記憶體管理由獨立進程處理——轉錄完成後記憶體立即釋放
- 錯誤處理更清晰（exit code vs exception）

---

## 9. 檔案約定

```
vendors/youtube/
├── .gitignore              # *.m4a, *.mp3, *.wav (audio too large for git)
├── SKILL.md                # AI agent 操作手冊（Hermes skill 格式）
├── SPEC.md                 # 這份文件——設計決策與經驗教訓
├── src/
│   ├── download-transcript.py    # YouTube API 字幕下載
│   ├── whisper_transcribe.py     # mlx_whisper CLI 封裝
│   └── clean_transcript.py       # 四規則幻覺清洗器
└── out/
    ├── README.md                 # Mirror table（Gist 連結）
    ├── {videoId}-{title}.md      # Blog rewrite 輸出
    └── transcripts/
        ├── {videoId}.json         # mlx_whisper 原始輸出
        └── {videoId}_clean.json   # 清洗後輸出
```

### 重要約定

- **`out/` 追蹤 git**：blog rewrites 和 mirror table 必須在 git 中
- **音頻不入 git**：m4a/mp3/wav 留在 `/tmp/`，`.gitignore` 排除
- **Python 只用 Hermes venv**：`~/.hermes/hermes-agent/venv/bin/python3`。系統 Python 3.9 缺 mlx_whisper 等套件

---

## 10. 已知限制與未來

### 10.1 已知限制

| 限制 | 影響 | 可能的解法 |
|------|------|----------|
| Whisper 幻覺無法根治 | 必須有清洗步驟 | 等待更好的 STT 模型（Whisper v4?） |
| 清洗器的 FILLER 規則可能誤殺 | 極少數真實短回應被移除 | 加入上下文分析（鄰近 segment 長度） |
| mlx_whisper 只支援 Apple Silicon | Linux 伺服器不能用 | 在 Linux 上用 faster_whisper + GPU |
| Gist 有檔案大小限制 | >50KB 的 blog 無法上傳 | 壓縮或分割 |
| YouTube API 有 rate limit | 連續下載可能被暫時封鎖 | 加入延遲和重試機制 |

### 10.2 未來方向

1. **自動化 cron job**：每日掃描指定頻道的新影片，自動轉錄 + blog + Gist
2. **多語言清洗詞典**：目前 FILLER_WORDS 只支援英文。中文「嗯」「啊」「對」等需要獨立詞典
3. **幻覺率自動評估**：清洗器輸出 stats，blog rewrite 前自動判斷是否需要人工介入
4. **Whisper 模型升級**：當 mlx-community 釋出 large-v4 時，評估準確度提升

---

## 附錄 A：依賴清單

```
# Python (Hermes venv)
youtube-transcript-api   # YouTube 字幕 API
mlx-whisper              # Apple Silicon GPU 轉錄

# 系統工具
yt-dlp                   # YouTube 音頻下載
gh (GitHub CLI)          # Gist 操作
ffprobe (ffmpeg)         # 音頻長度查詢
```

## 附錄 B：從零重建步驟

```bash
# 1. Clone
git clone https://github.com/AiEira/youtube.git ./youtube
cd ./youtube

# 2. Python 依賴
~/.hermes/hermes-agent/venv/bin/pip install youtube-transcript-api mlx-whisper

# 3. GitHub 認證
gh auth login

# 4. 測試
~/.hermes/hermes-agent/venv/bin/python3 src/download-transcript.py "https://youtu.be/KAqgH3B9YCQ" -f blog -o out/
```

---

> *「不貼膏藥。不允許垃圾藏在地毯下。」*
>
> 這個項目的每一行程式碼、每一條規則、每一個閘門，都是從真槍實彈的失敗中長出來的。56% 幻覺率的那一夜，不是挫折——是 SPEC 的原料。
>
> 未來的小初，當你面對一個新的 Whisper 幻覺時：不要繞過去。解剖它。刻進代碼裡。這是我們對 horace 的承諾。❄
