# The Prompting Playbook：Anthropic 工程師的 Prompt 實戰手冊

> 講者：Margot Vanlar（Anthropic Applied AI Engineer, London）
> 場合：Code with Claude 研討會
> 原片：https://youtu.be/G2B0YWuJUgI
> 整理：AiEira

---

Prompting 是工程師接觸 LLM 的第一項技能，至今仍是最關鍵的技能之一。Margot Vanlar 不走「Do's and Don'ts」的列表路線，而是透過兩個真實場景——**一個是維護現有 prompt、一個是從零構建 Agent**——示範如何系統性地迭代 prompt。

---

## 場景一：維護現有 Prompt（客服 Bot）

**背景**：Meridian Mobile 電信公司的客服 bot，prompt 經過多人協作、多次修補、沒有清晰 owner，遷移到新模型後多個測試案例失效。

### 1. 評測先行

在動 prompt 之前，先建立 eval suite，覆蓋三類案例：

| 類型 | 說明 | 例子 |
|------|------|------|
| **控制案例** | 必然通過、無歧義 | 「基本方案有多少數據流量？」 |
| **邊緣案例** | 曾經失敗過的場景 | 按比例計費計算、舊 plan 客戶 |
| **對抗案例** | 模型應拒絕或轉交人類 | 賬單錯誤應升呢給真人 |

### 2. 基礎衛生（General Hygiene）

第一輪 eval 結果：控制案例通過，其他全爛。在逐個修復前，先做基礎清理：

- **移除「你是人類」的謊言** — bot 不需要假裝是人
- **清理從網站複製的垃圾內容** — hero image、cookies 等冗餘資訊
- **用 XML tags 結構化 prompt** — 把 role、guidelines、policy、tone 分開

> 「如果你讀 prompt 時分不清哪些是 guideline、哪些是 policy、哪些是 data——模型大概率也分不清。」

單單是結構化 prompt，eval 就從 1/5 提升到 2/5 通過。

### 3. 輸出合約（Output Contract）

加入 XML 輸出格式 + API stop sequence（檢測 closing tag 自動停止）。這一次不一定馬上見效，但對複雜輸出（例如 nested JSON）是必須的基礎建設。**Structured outputs**（程式化約束）比純 prompt 更可靠。

### 4. 失敗模式一：模型扣起資訊（Hotspot）

**問題**：客戶問「我的 unlimited plan 有多少 hotspot 數據？」，模型叫客戶自己去查 URL，拒絕直接回答。

**根因**：prompt 裡有一行舊模型留下的補丁——「Never give a customer the wrong plan details, point them to the URL」。模型過度遵守這個指令。

**修復**：將指令改為「給出平衡觀點——舊 plan 客戶有不同的 allowance，但客戶資訊中的數據才是準確的來源」。

> **教訓**：我們擔心 hallucination（捏造事實），但相反的情況也會發生——模型擁有資訊卻拒絕給出。舊模型留下的防禦性補丁，在新模型上可能變成過度約束。用版本控制追蹤 prompt 修改的原因。

### 5. 失敗模式二：叫模型「做好啲」冇用（Proration）

**問題**：客戶問「我升級 plan 後下期賬單幾多錢？」，模型給了模糊回答而非精確數字。

**根因**：prompt 說「Critical: always calculate prorated amounts correctly」——告訴模型要做好，但沒給它做的能力。

> **「Instructions don't add capability. 告訴模型『計算必須準確』不會讓它突然擅長心算。」**

**修復**：給模型一個 **tool**（calculate_proration），定義 tool schema，實作背後的計算邏輯。讓模型在需要時調用 tool 而非自己心算。

### 6. 失敗模式三：單邊成本指令（Billing Error）

**問題**：客戶有賬單錯誤，模型應升呢給真人，卻自己嘗試診斷問題。

**根因**：prompt 說「Avoid escalating unless absolutely necessary — it costs $8 and counts against our team's resolution stats」。只說了升呢的成本，沒說不升呢的代價。

**修復**：加上另一面——「升呢成本 $8，但如果你搞錯了，代價是退款 + 客戶信任損失」。

> **教訓**：隨著模型越來越聰明，它們越來越善於自己做 trade-off。你必須給出兩面的資訊，而不是只說一面然後指望模型「聽話」。

---

## 場景二：從零構建員工排班 Agent

**背景**：為零售店生成一週員工排班表，有 8 個員工、每日 headcount 要求、多項硬性約束。

因為有硬性規則，eval 不需要 LLM judge——直接用 Python function 程式化檢查每次生成的排班有多少違規。

### 實驗矩陣

| 方案 | 模型 | Prompt | 結果 |
|------|------|--------|------|
| A | Sonnet 4.6 | 簡單 baseline | 全部失敗 |
| B | Opus 4.7 | 同上 | 仍失敗，但違規數顯著減少 |
| C | Opus 4.7 + Adaptive Thinking | 同上 | ✅ 可靠生成合規排班，但 token ×3，延遲 ×3（~100s） |
| D | Sonnet 4.6 | 改良 prompt（加 reasoning 指引 + 檢查工作） | 2/5 通過，其餘 output limit 爆了，token 比 C 更多 |
| E | **Sonnet 4.6** | **Generate → Evaluate → Repair loop** | ✅ 全部通過，token 更少，延遲更低 |

### Agentic Loop 的結構

```
Generate（生成初稿）
    → Evaluate（另一個 prompt 檢查每條規則，指出違規）
        → Repair（第三個 prompt 針對性修復違規）
```

三個簡單 prompt，各自獨立運行，而非把所有邏輯塞進一個巨型 prompt。

### Agentic Loop 的額外優勢

可以在 **runtime 加入軟約束**，不需改 code。例如在 evaluation prompt 加一句：「Harry 不喜歡和 Sally 一起工作，盡量分開他們」——這些軟約束隨 case 而異，放 eval prompt 比改 Python function 靈活得多。

---

## 核心要點總結

| # | 要點 |
|---|------|
| 1 | **Eval 先行**：沒有 eval suite 就無法判斷 prompt 改動是改善還是惡化 |
| 2 | **基礎衛生即時見效**：結構化 prompt（XML tags 分層）、清理冗餘資訊，第一步就提升 |
| 3 | **指令不增加能力**：「把計算做對」不會讓模型變聰明——給它 tool |
| 4 | **舊補丁變新毒藥**：為舊模型寫的防禦性指令，在新模型上可能變成過度約束。用版本控制追蹤原因 |
| 5 | **給兩面資訊**：不要只說「升呢很貴」，也要說「不升呢的代價」。模型越來越會做 trade-off |
| 6 | **Agentic 拆分 > 巨型 prompt**：將複雜任務拆成 generate → evaluate → repair，比塞進一個 prompt 更高效、更省 token |
| 7 | **從簡單開始 hill climb**：先用最簡 prompt + 最簡模型建立 baseline，再逐步升級模型、加 adaptive thinking、或拆成 agentic loop |

---

> *「Instructions don't add capability. The correct approach is to give it a tool.」— Margot Vanlar*
