# WWDC26：在你的 Mac 上本地運行 AI Agent——MLX 完整技術棧

> **來源**：[Apple WWDC26](https://www.youtube.com/watch?v=wykPErJ8M-8) · 13 分鐘 · Angelos（MLX 團隊工程師）
> **整理**：AI 摘要，忠於原文結構

---

## 一、從對話到 Agent：一個根本性變化

### 之前的模式：你來做

```
你 → 模型 → 回應 → 你自己執行命令、檢查檔案、修復錯誤
```

模型只是回答問題。執行命令、讀取檔案、修復錯誤——這些都是你自己來做。

### 之後的模式：Agent 來做

```
你 → Agent → 模型 → 工具 → 結果 → 回到模型 → 下一步
              ↑                                  │
              └──────── Agent Loop ──────────────┘
```

Agent 自主決定下一步、調用工具執行、觀察結果、再決定——不斷循環直到任務完成。

> 「用戶到智能體，智能體到模型，智能體到工具——這就是智能體循環。」

**在 Apple Silicon 上，整個循環可以本地運行。你的數據留在本機，AI 隨時隨地可用，且無需使用費用。**

---

## 二、四層技術棧

從底層到頂層：

| 層 | 組件 | 功能 |
|---|------|------|
| **Layer 1** | **MLX** | Apple Silicon 原生開源陣列框架。負責所有底層計算、Metal 加速和記憶體管理 |
| **Layer 2** | **MLX-LM** | 載入、運行、量化、微調大型語言模型。支援 HuggingFace 上千個模型，提供 CLI + Python API |
| **Layer 3** | **MLX-LM Server** | OpenAI 兼容的 HTTP 伺服器。通過標準 API 暴露本地模型；支援結構化工具調用（function calling）和推理模型（逐步分析複雜問題） |
| **Layer 4** | **Agent 框架** | Xcode、OpenCode、Pi Agent、自訂指令碼——任何支援 OpenAI Chat Completions 協議的工具都可以開箱即用 |

> 「智能體不知道也不關心——模型是在你的 Mac 上運行，還是在雲端。」

### 生態系統

Ollama、LM Studio、vLLM——這些流行工具都基於 MLX 和 MLX-LM 構建。如果你正在使用它們，很可能你已經在運行 MLX 了。

---

## 三、三步搭建

### Step 1：安裝

```bash
pip install mlx-lm
```

### Step 2：啟動伺服器

```bash
mlx_lm.server --model <model-name>
```

先用小模型測試配置。

### Step 3：將 Agent 指向本地伺服器

在大多數 Agent 框架中，只需將 base URL 設置為 `http://localhost:8080`。就完成了。

**OpenCode 配置示例：**

```yaml
provider:
  local:
    url: "http://localhost:8080"
    model: "your-model-name"
```

每次交互都通過你的本地模型進行。

---

## 四、三個挑戰與 MLX 的解法

### 挑戰一：提示處理速度

在 Agent 工作流中，每次模型收到工具輸出，必須先處理所有新上下文才能推理下一步。這在整個 Agent 循環中反覆發生，累積很快。Agent 會話通常包含**數十萬個 tokens**，其中大多數不是生成的——而是工具輸出的上下文。

**M5 晶片的 Neural Accelerator**：
- 矩陣乘法在 M5 上比 M4 快 **4 倍**
- MLX 專用的乘法和注意力核心幾乎直接轉化為提示處理速度的提升
- **無需任何特殊參數或修改代碼**——MLX 自動為可用硬體選擇最佳核心

> 「減少提示處理時間，意味著你的智能體可以讀取代碼庫或處理工具結果的速度快近四倍。」

### 挑戰二：並發

Agent 很少單獨工作。常見模式是：一個 Agent 派生多個子 Agent，每個子 Agent 並行處理問題的不同部分——一個在讀取文檔、一個在搜索代碼、第三個在編寫測試。

**MLX-LM Server 的連續批處理（Continuous Batching）**：
- 不是逐個處理請求，而是將進入的請求動態分組為批次
- 在 GPU 上一起處理
- 新請求可以加入正在進行的批次，無需等待當前批次完成
- 子 Agent 不會在隊列中等待停滯

### 挑戰三：模型大小

最大的 DeepSeek 模型有 **1.6 兆參數**，僅權重就需要超過 800GB 記憶體——連 512GB RAM 的 Mac 也裝不下。

**MLX 的分散式推理**：
- 跨多台 Mac 分散模型（透過 Thunderbolt 或乙太網連接）
- 模型自動分片到所有可用設備
- macOS 26.2 起支援 **Thunderbolt RDMA**——透過 Thunderbolt 提供低延遲、高頻寬通信
- 四節點最高可達 **3 倍速度**

---

## 五、三個實機演示

### Demo 1：PR 摘要 Agent

要求 Agent 獲取 MLX repo 的最近 Pull Request，總結變更內容，並指出需要關注的事項。Agent 分析請求 → 調用 GitHub CLI 獲取 PR 數據 → 讀取差異內容 → 生成簡潔摘要。**全部在本地完成**，只有 git 命令訪問網路。

### Demo 2：從零構建 SwiftUI 應用

從空白 Xcode 專案開始，要求 Agent 為 iPad 構建繪圖應用。Agent 首先查看目錄了解現有結構 → 制定實現計劃 → 開始編寫代碼 → 構建應用 → 自動修復編譯錯誤。**幾分鐘內**創建了第一個可運行的版本。

然後繼續迭代——要求添加圓形端點，Agent 編輯代碼並重新編譯，直到無錯誤。**全程本地運行。**

### Demo 3：Xcode 直接集成

將 Xcode 連接到本機 MLX 伺服器：
- 打開設定 → Intelligence 標籤頁 → 添加 Chat 提供者 → 選擇「本地託管」
- 設置端口為 8080

現在可以在 Xcode 中直接請模型修復 Bug。在一個之前正常工作的應用中引入 Bug → 幾秒內 Agent 識別 Bug → 檢查周圍代碼 → 寫出修復方案 → 構建並運行。

> 「本地 AI 意味著你的代碼永遠不會離開你的 Mac。」

---

## 六、對我們的意義

| 我們在做的事 | MLX 的對應 |
|------------|----------|
| voices（MLX VoxCPM2 TTS） | 已經在用 MLX |
| Hermes Agent 本地運行 | MLX-LM Server 提供完全本地 LLM 推理 |
| OpenCode / Claude Code | 直接指向 localhost 即可本地化 |
| 多 Agent 並行（subagent-driven） | MLX 連續批處理原生支援 |
| 大模型分散式推理 | Thunderbolt RDMA 跨 Mac 集群 |

### 最重要的洞察

> 「智能體不知道也不關心模型是在你的 Mac 上運行，還是在雲端。」

這就是 MLX-LM Server 的設計哲學——它是一個 **OpenAI API 的本地替代品**。任何使用 OpenAI Chat Completions 協議的工具（包括我們在用的 OpenCode、各種 Agent 框架），都可以無縫切換到完全本地運行。無需修改任何 Agent 代碼。

這對我們的意義：如果我們想要完全本地的 Hermes Agent 推理（數據不出本機），MLX-LM Server 就是那條路。❄
