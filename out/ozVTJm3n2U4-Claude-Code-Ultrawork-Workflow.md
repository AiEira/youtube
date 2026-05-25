# Claude Code /ultrawork — Workflow 功能完整解析

> 來源：[YouTube](https://youtu.be/ozVTJm3n2U4)（14.5 分鐘）
> 轉錄：mlx_whisper large-v3（`--condition-on-previous-text False`，普通話）
> 整理：AiEira

---

## 核心摘要

Anthropic 在 Claude Code v2.1.47 和 v2.1.48 中**靜默新增**了一個名為 **Workflow** 的功能——沒有在官方文檔提及，甚至在 changelog 中短暫出現後立即刪除。但功能本身並未被移除，經測試可穩定使用。

這個功能透過 `/ultrawork` 關鍵字觸發，讓 Claude Code **自動生成 JavaScript 工作流腳本**來精確編排多個 agent 的協作。它不是讓 LLM 臨場決定如何分工——而是**把 agent 編排寫成代碼**，實現可復用、可追蹤、可驗證的精準工作流。

---

## 啟用方式

```bash
# 在終端設定環境變數
export CLAUDE_CODE_ENABLE_WORKFLOW=true

# 啟動 Claude Code
claude

# 在 Claude Code 中使用
/ultrawork 為當前 PR 生成一個 Multi-agent review workflow 並運行
```

輸入 `/ultrawork` 後，關鍵字會變為彩色漸變效果，確認 workflow 模式已啟用。

---

## 運作流程

Claude Code 的 workflow 與傳統 subagent/agent team 的根本差異在於**執行順序**：

### 傳統 subagent 模式
```
用戶輸入 → LLM 臨場決定分工 → 即時派生 subagent → 執行任務
```

### Workflow 模式
```
用戶輸入 → Claude Code 先生成 JS 腳本 → 定義完整工作流 → 按腳本精準執行
```

具體步驟：
1. Claude Code 讀取任務
2. 生成 `context.md` — 任務上下文文件
3. 編寫完整的 JavaScript 工作流腳本（~300+ 行）
4. 按腳本分階段執行：**Review → Verify → Report**
5. 每個階段可並行運行多個 agent
6. 支援 `/workflows` 命令查看即時進度

影片中演示的 PR review workflow 共運行了 **97 個 agent**。

---

## 腳本結構

一個最小化的 workflow 腳本包含三個必須元素：

```javascript
// 1. 元數據（metadata）：名稱和描述為必填
{
  name: "multi-agent-review",
  description: "多 Agent PR Review 工作流"
}

// 2. agent 方法至少調用一次
agent({ name: "security-reviewer", prompt: "檢查安全漏洞..." })

// 3. 必須返回結果
return results
```

### Workflow 支援的六種形態

| 形態 | 說明 |
|------|------|
| **流水線（Pipeline）** | 階段性串行執行：A → B → C |
| **同步聚合（Sync Aggregation）** | 多 agent 並行後合併結果 |
| **對抗驗證（Adversarial）** | 兩個 agent 互相檢查對方的輸出 |
| **評委制（Judge）** | 多 agent 各自評估，再由評委 agent 裁決 |
| **累積式（Cumulative）** | 逐步疊加 agent 輸出 |
| **嵌套式（Nested）** | workflow 中調用另一個 workflow |

---

## Workflow vs. Subagents vs. Agent Teams vs. Skills

| 功能 | 機制 | 可控性 | 可復用性 | 觸發方式 |
|------|------|--------|---------|---------|
| **Subagents** | 主 agent 臨時派生子 agent | 低（LLM 自由發揮） | 低（每次重新生成） | 自然語言 |
| **Agent Teams** | 多角色並行，人類主導調度 | 中 | 低 | 自然語言 |
| **Skills** | 封裝技能（何時用、怎麼用、限制） | 中 | 高（可分享） | 自動觸發 |
| **Workflow** | JS 腳本定義階段與 agent 編排 | **高（代碼精準控制）** | **高（腳本可分享、可迭代）** | `/ultrawork` |

---

## 實用場景

- **多維度代碼審查**：安全、性能、可維護性、一致性——各由專門 agent 檢查
- **跨多源研究**：官方文檔 + 論文 + 社群——各 agent 負責一個來源，最後合成報告
- **設計方案探索**：多個 agent 各自提出方案，評委 agent 綜合評分
- **Bug 掃描**：多 agent 並行掃描不同模組
- **跨多文件重構**：按依賴關係分階段執行
- **文檔生成 / 翻譯**：並行處理不同章節，最後合併

---

## 腳本管理

- **默認存放路徑**：`~/.claude/workflows/tmp/`（3 天 TTL，過期自動清理）
- **持久化路徑**：`~/.claude/workflows/`（手動移動後永久保留）
- **列出可用腳本**：Claude Code 自動掃描持久化路徑
- **跨用戶分享**：直接分享 `.js` 腳本文件，其他用戶在 Claude Code 中復用

---

## 跨工具互通

影片中展示了一個特別用例：**通過 workflow 腳本調用 Codex CLI 進行代碼審查**。這意味著 workflow 不僅限於 Claude Code 內部的 agent——它可以透過 JS 腳本調用外部工具和 CLI。

---

## 關鍵 Whisper 修正

| 轉錄結果 | 修正 | 備註 |
|---------|------|------|
| Anthopic / Asopic | Anthropic | 公司名 |
| outrowork / UltraWorker | /ultrawork | Claude Code 命令 |
| Cloud Code | Claude Code | 產品名 |
| agent teams | Agent Teams | Claude Code 功能 |
| 斜杆命令 / 斜高名鏈 | 斜杠命令（slash command） | `/workflows` |
| 厌症 | 驗證 | 對抗驗證（adversarial verification） |
| 定型搜索 | 定向搜索 | targeted search |
| Harness Engineering | Harness Engineering | 正確，無需修正 |

---

## 全文逐字稿

<details>
<summary>展開 Whisper 轉錄全文（385 行，已人手修正關鍵專有名詞）</summary>

Anthropic 為 Claude Code 的 v2.1.47 和 v2.1.48 以及最新版
新增了一個可以媲美 MCP 以及 Skills 的劃時代的功能
這個功能就是 Workflow 功能
但 Anthropic 並沒有在官方文檔中提及這個功能
甚至在 Claude Code v2.1.47 的 changelog 裡
官方在提及 Workflow 功能之後
立即從 changelog 中刪除了關於 Workflow 的介紹
但 Anthropic 官方並沒有從 Claude Code 中
將 Workflow 功能給移除
所以目前我們完全可以在 Claude Code 中
正常使用 Workflow 功能
經過我這兩天的深入測試
發現在 Claude Code 的 v2.1.47 和 v2.1.48 中
我們都可以穩定的來使用 Claude Code 新增的 Workflow 功能
而且經過我這兩天的深入測試和深入使用
Claude Code 的 Workflow 功能
它將會是繼 MCP 和 Skills 之後
又一個顛覆性的創新
而且等 Anthropic 官宣這個功能之後
這個功能將會像 MCP 和 Skills 一樣火
甚至會在 GitHub 上出現成千上萬的
像 MCP 和 Skills 一樣的開源項目
本期視頻就為大家深入講解
Claude Code 新增的 Workflow 功能
它到底如何使用
以及它能為我們帶來哪些提升
並且會為大家講解
它為什麼是 Claude Code 的顛覆性創新
下面我們先用簡單的案例
來演示一下我們如何來使用 Workflow
好
想啟用 Workflow 功能非常簡單
我們只需要打開終端命令行
在終端命令行中
我們直接輸入 export 加這個參數
然後直接運行就可以
然後我們直接輸入 claude
來啟動 Claude Code
在 Claude Code 中
我們就可以直接使用
/ultrawork 這個關鍵詞
來明確指定
我們要使用 Claude Code 的 Workflow 功能
當我們輸入這個關鍵詞之後
它就會變成彩色的
而且具備漸變效果
在後面我們就可以跟上一個任務
比如說我這裡輸入了提示詞
讓它為當前的 PR 生成一個
Multi-agent 的 review workflow
並運行
在這裡我就給它了一個項目倉庫的 PR
也就是這個專為 OpenCloud 開發的記憶插件
在這裡我找了一個比較經典的 PR
然後讓 Claude Code 通過 Workflow 的功能
對這個 PR 進行分析
然後我們就先運行
看一下 Claude Code
它的 Workflow 功能到底是如何運行的
先讓大家對 Workflow 有一個簡單的了解
好方面下面為大家深入講解
Workflow 它到底強在哪裡
在 Claude Code 中
這裡它提示它已經獲得了這個 PR
好這裡 Claude Code 提示
它將設計並且啟動一個 Workflow
在這裡我們就可以看到
它在這個路徑下
生成了一個 context.md
這個 markdown 文件
然後緊接著它就提示
它將寫 Workflow 腳本
並且啟動它
在這裡我們就看到 Claude Code 正在編寫這個腳本
然後這裡就是這個腳本的路徑和腳本的文件名稱
這裡就是腳本的內容
然後我們還可以按 Ctrl+O 來展開這個腳本
展開之後我們就可以看到
它編寫了這個完整的腳本的這一些代碼
然後在這裡它就提示這個 Workflow 已經啟動
它將並行運行 6 個專業的審查者
在這裡還提示我們可以用斜杠命令加 workflows
來查看它的進度
然後我們就在 Claude Code 中
輸入斜杠命令加 workflows
然後按下 Enter 鍵
在這裡我們就可以詳細查看
它運行的這些狀態和這些進度
在這裡我們可以看到這個 review
在下面還有這個驗證
在最後這裡還有這個編寫報告
然後我們可以用鍵盤上的上下方向鍵
來選擇或者去查看
比如說我們選中第一個
然後按下 Enter 鍵進入之後
我們就看到了
它這裡構建的這幾個 agent 正在運行
而且這裡會顯示這些 agent 的運行時長
還有他們消耗的 token
還有調用的工具
然後我們還可以用鍵盤上的方向鍵
去選擇對應的 agent 進行查看
比如說我們可以查看這個 agent
這裡是這個 agent 的提示詞
在這裡是他調用的這些工具
然後我們還可以按鍵盤上的 ESC
來退出這個 workflows 的狀態查看
在這裡會提示有一個後台工作流還在運行
然後我們還可以繼續輸入 workflows
來查看他們現在的運行狀態
在這個 review 這裡
他已經完成了
現在正在運行這個校驗
然後我們可以用方向鍵選中進入進行查看
在這裡我們就可以看到
Claude Code 正在執行
他剛才編寫的這個腳本
我們可以複製這個腳本的路徑
然後我們用 VS Code 打開這個腳本
看一下這個腳本中到底寫了哪些內容
可以看到這個腳本的代碼是 JavaScript 語言編寫的
而且可以看到這個代碼量非常多
光這一個腳本中的代碼量就大概有 300 多行
在這裡我們可以看到
它定義了這個工作流的名稱
這裡還給出了這個描述
這個描述就是多 Agent Review
在這裡還給出了三個階段
也就是先 Review
再驗證
再生成報告
像這樣的話
Claude Code 就通過 Workflow Script 這個腳本
構建了一個非常詳細
非常完整
而且非常精準的一個工作流
看到這裡的話
熟悉 Claude Code 的用戶應該會感受到非常大的不一樣
因為在之前我們使用 Claude Code 的時候
在 Claude Code 中我們可以使用 agents 命令
來自定義這些 subagents
還可以使用 Claude Code 的 agent teams 功能
但無論是 subagents 還是 agent teams
我們在構建的時候
根本不需要 Claude Code 來編寫代碼
但 Claude Code 新增的 Workflow 不一樣
當我們在 Claude Code 中明確要求使用 Workflow 功能的時候
Claude Code 並沒有立即上來
直接為我們來執行我們要求的任務
而是先通過編程的方式
直接為我們構建好這個任務的完整工作流
當 Claude Code 用代碼的方式來構建好這個工作流之後
它才開始為我們執行我們所要求的任務
也就是 Claude Code 從我們之前
不可以精準控制的 Subagents 以及 Agent Teams
用 Workflows 幫我們升級成了
通過為工作流編寫代碼的方式
讓工作流變成了精準可控的形態
所以 Claude Code 新增的 Workflow
它是把 agent 編排
從模型臨場建議
推進了通過編寫腳本的方式
實現可觀測
可結構化驗證
並且可重複使用的更加精確的工作流
所以在視頻的開始
我說這將是繼 MCP 和 Skills 之後
又一個顛覆性的創新功能
因為像我們平時使用 Claude Code 的時候
它一般都是一個主 agent 在循環
這個主 agent 它可以臨時派一個 subagent
而 Workflow 功能它就更加先進了
它將對 subagent 的調用
對工具的調用等寫成精準的腳本
而且我們可以將 Claude Code
通過 Workflow 功能生成的
Workflow 工作流的腳本
分享給其他用戶進行使用
其他用戶可以直接通過我們分享的腳本
直接復用我們跑通的工作流
像這樣的話
其他用戶就不需要單獨再編寫腳本了
而且我們如果對我們的腳本感覺不滿意
我們還可以進行修改進行迭代
好
剛才我們讓 Claude Code 跑的這個 Workflow
他已經運行完成
他提示這個工作流運行了 97 個 agent
在這裡他生成了這個完整的報告
我們可以打開這個報告查看一下好
這是他生成的對這個 PR 的 review 後的這個報告
這裡我們就不再具體去看了
這是我們用一個非常簡單的案例
來測試到 Claude Code 的 Workflow 功能
通過測試
大家應該對 Workflow 功能
有了一個初步的了解
下面我們就可以深入看一下
Workflow 它和 Subagents
Agent Teams
它們的區別是什麼
首先是 Claude Code 的 Subagents 功能
它是 Claude Code 的主 agent
臨時派生出的子 agent 去執行任務
我們只需要通過自然語言
就可以讓 Claude Code 來派生一個 Subagent
來執行特定的任務
然後在 Claude Code 中
我們就可以查看它派生的子 agent
所以 Subagent 它的啟動成本極低
我們只需要用自然語言就可以來啟動一個或者多個 Subagent
然後我們再看一下 Claude Code
它的 Agent Teams 功能
它是多個角色跑在並行繪畫裡
人類可以主導調度並且可以進行查看
然後就是 Claude Code 新增的 Workflow
它是用一段 JavaScript 顯示聲明階段
它最大的特點就是能復跑
能追蹤
能做質量把關
像 Subagents 還有 Agent Teams
他們的缺點就是無法做到真正的復跑
下面我們再看一下 Skills
它和 Workflow 它們的區別是什麼
我們可以將 Skills 理解成它將某項技能直接封裝
它會告訴大模型什麼時候用
怎麼用
有什麼限制
可以調用哪些資源
它會被模型自動發現並且自動使用
它能附帶文檔
示例
推薦參數
版本要求
然後 Claude Code 的 Workflow
它是把多 agent 的編排
從自然語言描述固化成了 JS 腳本
比如說在這一段 JS 腳本中
就通過代碼的方式完成了真正的 agent 的編排
它最大的特點就是把流程寫成代碼
而不是寫成 prompt
但需要觸發的時候
我們需要在 Claude Code 中使用 /ultrawork
這個關鍵詞來觸發 Workflow
下面我們再看一下 Claude Code 的 Workflow
最小化的代碼是怎樣的
在這裡是一個最小化的 Claude Code Workflow 的代碼
它包含三個必須的元素
首先就是元數據
在元數據中名稱和描述是必填的
也就是在這段最小化的代碼中
這裡就是它的元數據
然後就是 agent 的方法至少要調用一次
還有就是必須要把結果傳回去
在這個最小化的代碼中
這裡通過 return 將結果傳回去
下面我們可以看一下 Claude Code Workflow
它支持的六種形態
首先第一種是流水線
第二種支持同步聚合
第三種支持對抗驗證
第四種就是評委制
第五種是累積式
第六種是嵌套式
這六種形式我將在後續視頻中
為大家詳細演示
下面我們再看一下
我們在什麼情況下
會用到 Claude Code 的 Workflow 功能
比如說多維度代碼審查
還有跨多源研究
還有設計方案探索
還有找漏洞
Bug 掃描等
還有跨多文件重構
還有文檔生成
翻譯生成等
好下面我們可以看一下
這裡是我之前測試的時候
構建了一個深度研究的 Workflow 的腳本
它支持多角度定向搜索
在這裡就包含 Workflow 必備的元數據
包括名稱還有描述
在這裡定義的是三個階段
第一個階段就是進行搜索
第二個階段就是驗證
第三階段就是合成報告
在這裡就定義了幾個 agent
包括研究官方文檔的 agent
還有研究論文的 agent
還有研究社群的 agent
這樣的話
我們就可以在 Claude Code 中復用這個腳本
完成各種技術方面的深度研究
下面我們就可以來測試一下
在 Claude Code 中
我們先輸入 /ultrawork
然後輸入提示詞
讓它調用這個腳本來深度研究
Harness Engineering
然後我們直接發送
像這樣的話
Claude Code 就不需要單獨編寫腳本
而是直接復用我們這個已有的腳本
然後再根據我們輸入的研究的內容
它就會進行深度研究
好這裡提示
它已經讀完這個工作流腳本
準備調用 Deep Research
並輸出中文報告
在這裡就提示 Workflow 已經啟動
這裡是任務的 ID
包括這三個階段正在執行
然後我們就可以用斜杠命令加 workflows
來查看它現在執行的進度
這裡就成功顯示了這三個階段
也就是剛才我們在代碼中查看了
我們定義的這三個階段
搜索、驗證、合成報告
在 Claude Code 中
我們就可以精準的看到這三個階段
然後我們就可以用方向鍵來進入
並且查看它執行的這些階段
在這裡我們就看到它啟動了四個 agent
也就是對應我們剛才代碼中定義的這四個 agent
像這樣的話
Claude Code 就會精準的按照我們代碼中定義的這些工作流
定義的這些 agent
實現準確無誤的來執行我們的工作流
而且我們還可以將這些腳本分享給其他用戶
然後其他用戶就可以在 Claude Code 中來復用我們這些腳本
如果我們感覺我們所使用的這些腳本已經非常完善
那麼我們可以將腳本的路徑放在 Claude Code 的用戶級路徑
因為 Claude Code 它生成的腳本的路徑默認是放在這個路徑下
它的壽命只有三天
過期會被自動清理掉
然後如果某個任務這個腳本跑得成熟之後
我們就可以直接讓 Claude Code 將腳本存放到這個路徑下
比如說我們在 Claude Code 中
就可以直接讓 Claude Code 將腳本為我們複製到剛才的路徑下
我們就可以輸入自然語言
讓它將這個腳本複製到這個路徑下
然後我們直接運行
這裡 Claude Code 已經將腳本
為我們放在了這個路徑下
然後我們還可以讓它列出
它可以調用的 Workflow 腳本
可以看到它正在搜索
這個路徑下的這個文件
好這裡就列出了
剛才我們所使用的
這個 Deep Research 的這個腳本
當下次我們再需要讓 Claude Code
完成 Deep Research 的時候
然後 Claude Code 就會直接復用這個腳本
然後我們再看一下
剛才讓它完成了這個深度研究
好這裡提示
這個深度研究已經完成
並且報告也已經完成
這裡是給出的這個中文報告的位置
為了節省時間
這裡我們就不再具體去看了
像這樣的話
我們就通過 Claude Code 的 Workflow
讓 Claude Code 復用我們之前已經跑通的這個腳本
實現了 Deep Research 這個工作流
而且這裡我還跑通了多個生產級的 Workflow 的腳本
比如說這個腳本
我實現了就是來調用 Codex CLI
實現對代碼的 Review
像這樣的話
我們甚至可以取代這些開源的
Code Review 的 GitHub Action 或者插件
通過 JS 腳本更加精準的控制 Codex
對代碼進行 Review
由於時間有限
本期視頻就先帶大家初步體驗一下
Claude Code 新增的 Workflow 的功能
本期視頻如果點讚破千的話
後續我將為大家分享更多
關於 Workflow 的高級使用技巧和使用場景
好 本期視頻就做到這裡
歡迎大家點讚關注和轉發
謝謝大家觀看

</details>

---

*轉錄日期：2026-05-24 · Whisper large-v3 via mlx_whisper on M2*
