# WWDC26：用 Core AI 將裝置端 AI 模型整合進你的 App

> **來源**：[Apple WWDC26](https://www.youtube.com/watch?v=gl5lD2gEhb0) · 23 分鐘 · Carina（Core AI 團隊）
> **整理**：AI 摘要，忠於原文結構

---

## 一、Core AI 是什麼？

Apple 全新的裝置端 AI 框架。一句話定位：

> 「讓你的用戶數據永遠不離開設備。無需管理伺服器、無需按 token 付費、沒有雲端延遲。」

底層技術棧：
- **MLX**（在前一條 WWDC 影片中介紹）
- **Core AI**（本影片）——更高層的框架，讓你直接在 App 中使用裝置端模型

---

## 二、語言學習 App：SAM 3 + Qwen 雙模型協作

### 使用場景

學生把相機對準花園裡的東西或街上的物體 → App 自動分割圖像中的物體 → 生成目標語言的單詞卡（詞彙、翻譯、使用例句）。

**全部在裝置端本地運行。**

### 模型選擇策略

> 「將問題分解為兩個小型模型——每個參數量低於十億，將裝置端總佔用控制在可管理範圍內。」

| 模型 | 用途 | 參數 |
|------|------|------|
| **SAM 3**（Segment Anything Model 3） | 視覺 Transformer，可提示圖像分割。精準隔離用戶指定的物體 | 623 MB |
| **Qwen**（通義千問） | 多語言 LLM，支援 119 種語言和方言。推理模型，生成詞彙、翻譯、上下文例句 | 0.6B（iOS）/ 8B（macOS） |

> 「專用於特定任務的模型質量更好、體積更小，且可獨立升級。」

---

## 三、模型整合流程

### Step 1：獲取模型

兩個途徑：

**途徑 A：從 PyTorch 轉換**
```bash
# 使用 Core AI PyTorch 擴展包直接轉換
# 支援模型壓縮（Core AI 優化包）
```

**途徑 B：Core AI Models 代碼庫**
- GitHub 上託管的開源倉庫
- 包含大量熱門模型的預轉換版本 + 轉換腳本
- 提供 Swift Package 運行時庫（`CoreAILM`、`CoreAISegmentation`）
- 可直接添加為專案依賴

### Step 2：在 Xcode 中檢查模型

匯出後的 `.aimodel` 檔案可以在 Xcode 中直接檢查：
- 模型大小（如 SAM 3：623 MB）
- 目標平台（iOS 27.0 / macOS 27.0）
- 元數據
- **Functions 標籤**：查看模型暴露的所有函數及其輸入輸出張量形狀

SAM 3 暴露了三個獨立函數：`imageEncode`（輸入：特定形狀的張量 → 輸出：密集特徵嵌入）、`detect`（輸入：圖像特徵 + 文本提示 → 輸出：原始蒙版、邊界框、置信度分數）。

### Step 3：整合 Swift 代碼

**圖像分割（SAM 3）**：
```swift
let segmenter = CoreAIImageSegmenter(model: sam3Model)
let mask = try await segmenter.segment(image, prompt: "flower")
```

**語言模型（Qwen）**：
```swift
// 一行代碼載入
let model = CoreAILanguageModel(path: modelPath)

// 與 Apple 裝置端 LLM 使用同一套 FoundationModels API
let session = LanguageModelSession(model)
let response = try await session.respond(prompt)
```

> 「與訪問 Apple 裝置端大型語言模型使用的是同一套 API。區別在於，現在可以傳入自己的模型。」

- 相同的 `session.respond` 調用
- 相同的流式支援
- 相同的結構化輸出能力

### Step 4：結構化輸出（@Generable 巨集）

不讓模型生成自由格式文本，而是使用 `@Generable` 巨集精確定義輸出結構：

```swift
@Generable
struct VocabularyCard {
    let word: String
    let translation: String
    let exampleSentence: String
}
```

---

## 四、部署優化：讓第一次載入不破壞體驗

### 核心問題：模型專項化（Specialization）

Core AI 模型在首次載入時需要**專項化**——為當前設備準備模型執行的過程。對於大模型（如 SAM 3 的 623 MB），這可能耗時較長。

**Core AI Instruments** 可以追蹤這個過程，確診瓶頸位置。

### 解決方案三層次

| 層次 | 方案 | 效果 |
|------|------|------|
| **1. 按需下載** | 使用 Background Assets。模型不打包進 App（會增加 1GB+ 下載量），而是用戶觸發功能時才下載 | 不影響所有用戶的更新體驗 |
| **2. 提前編譯** | `coreai-build` 命令在開發機器上預先生成模型的已編譯版本。已編譯模型仍需專項化，但工作量大幅減少 | 專項化時間降至原先的一小部分 |
| **3. 首次使用體驗** | 在用戶首次了解功能時觸發模型載入和專項化，排除在互動流程之外 | 用戶看到的不是載入指示器，而是進度條 |

### coreai-build 流程

```bash
coreai-build model.aimodel --target ios27
# 生成針對特定設備架構的已編譯模型
```

然後為每個已編譯模型創建後台資源，App 運行時檢測設備架構，請求對應資源。

---

## 五、多平台：iOS → macOS，相同代碼，更強模型

> 「使用 Core AI，我可以復用所有相同代碼，直接在 Mac 上繼續構建。」

### iOS（單詞學習模式）

- SAM 3 分割 + Qwen 0.6B 生成單張詞彙卡
- 一次學一個單詞

### macOS（內容整理模式）

- **相同代碼，調用相同 API**——只是底層模型換成更大版本
- 升級到 **Qwen3 8B**（80 億參數）——更強推理、更高品質輸出
- 更豐富的提示——要求多個例句而非一個；生成漢語拼音；構建課程體系（從簡單到複雜排序、分組成課程、編寫重用早期詞彙的例句）
- **批量處理**：一次處理整個照片文件夾，並行分割 → 一張照片創建多張卡片

> 「曾經需要一個下午手動輸入的內容，現在可以完全自動化。」

---

## 六、完整架構總結

```
用戶（iOS / macOS）
        │
   ┌────┴────┐
   │ Core AI │  ← FoundationModels API（統一的裝置端 LLM 接口）
   └────┬────┘
        │
   ┌────┴─────────────┐
   │ Core AI Models   │  ← Swift Package 運行時庫
   │ (CoreAILM /      │    封裝預處理、後處理
   │  CoreAISegment)  │
   └────┬─────────────┘
        │
   ┌────┴────┐
   │ .aimodel│  ← SAM 3 (623MB) + Qwen 0.6B/8B
   │  檔案   │     coreai-build 提前編譯
   └────┬────┘
        │
   ┌────┴────┐
   │  MLX    │  ← Apple Silicon 原生加速
   └─────────┘
```

---

## 七、對我們的意義

| Core AI 特性 | 我們可以做的事 |
|------------|-------------|
| FoundationModels API（與 Apple 裝置端 LLM 相同接口） | 在 macOS App 中直接使用本地模型，code 不需改 |
| Core AI Models 代碼庫 | 尋找預轉換的熱門模型，無需手動處理 PyTorch → Core AI |
| `@Generable` 結構化輸出 | 用於 voices pipeline 的 segment JSON schema 強制 |
| coreai-build 提前編譯 | 優化模型首次載入時間 |
| Background Assets 按需下載 | 不把模型塞進 App，用戶觸發才下載 |
| 多平台復用 | iOS 原型 → macOS 生產，同一個 API，更大模型 |

> *「模型已就緒，工具已就緒。使用 Core AI，你擁有構建強大隱私智能所需的一切。」* ❄
