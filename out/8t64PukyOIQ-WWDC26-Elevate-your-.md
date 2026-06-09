# WWDC26: Elevate Your App's Text Experience with TextKit | Apple

> 來源：[YouTube](https://www.youtube.com/watch?v=8t64PukyOIQ)
> 長度：約 23 分鐘
> 語言：粵語／中文
> 整理：AiEira

---

## 是甚麼

TextKit 是 Apple 所有平台文字排版與渲染的底層引擎。SwiftUI 的 `TextEditor`、UIKit 的 `UITextView`、AppKit 的 `NSTextView`——背後都是 TextKit。2027 年的更新解決了一個長期矛盾：**便利性與控制性之間的取捨**。過去你要麼用框架文字視圖（方便但難自訂），要麼從零打造自訂文字視圖（完全控制但工程浩大）。現在，你可以兼得。

主講人 Tarun Uday（TextKit 團隊工程師）用三個實際 Demo 貫穿全場：程式碼編輯器行號、可折疊段落、內聯附件重用。

---

## 一、TextKit 四層架構（回顧）

| 層級 | 職責 | 關鍵類別 |
|------|------|---------|
| **儲存層** | 封裝所有文字資料，將 `NSAttributedString` 分割為段落 | `NSTextContentStorage`、`NSTextParagraph` |
| **佈局層** | 測量字形度量，產生不可變的佈局片段 | `NSTextLayoutManager`、`NSTextLayoutFragment` |
| **視口層** | 追蹤哪些佈局片段在可視範圍內，協調渲染 | `NSTextViewportLayoutController` |
| **視圖層** | 文字實際顯示的地方 | `UIView`、`CALayer`、`NSView` |

核心循環：**視口佈局過程（viewport layout process）**——每次捲動、編輯、選取事件觸發，視口控制器向佈局管理器請求與視口相交的佈局片段，送交視圖層渲染。TextKit 只渲染可見文字，這是它高效能的根基。

---

## 二、新 API：渲染表面（Rendering Surface）

過去 TextKit 幫你追蹤佈局片段，但不幫你追蹤繪製它們的視圖。2027 年引入兩個新協議：

### NSTextViewportRenderingSurface

表示視口中可繪製的可視元素。`UIView`、`NSView`、`CALayer` 都可以遵循此協議。在視口控制器的委託方法中使用它，追蹤視口中哪些視圖可見。

### NSTextViewportRenderingSurfaceKey

唯一標識渲染表面的鍵，跨視口佈局過程週期。例如 `NSTextLayoutFragment` 可作為鍵，在映射表或字典中緩存渲染表面。

關鍵委託方法：

- `renderingSurfaceFor(_:textLayoutFragment:)` — 為鍵分配渲染表面
- 視口佈局過程開始時，舊映射會被清除
- `didLayout` 過程中可透過 `viewportLayoutController.renderingSurface(for:)` 查詢

---

## 三、框架文字視圖現已遵循視口控制器委託

這是 2027 年最重要的架構變化：**`UITextView` 和 `NSTextView` 現在遵循 `NSTextViewportLayoutControllerDelegate`**。

這意味著你可以**子類化框架文字視圖，覆蓋委託方法，注入自己的行為**——不需要從零打造自訂文字視圖，就能精細控制視口佈局過程。

---

## 四、Demo 1：程式碼編輯器行號

從 `UITextView` 子類開始，覆蓋三個視口委託方法：

| 方法 | 用途 |
|------|------|
| `willLayout()` | 清空行號陣列，計算視口之前的段落總數（起始行號） |
| `configureRenderingSurface(for:)` | 在每個段落觸發時，收集其 `layoutFragmentFrame` |
| `didLayout()` | 將累積的幀從文字容器坐標轉換為視口坐標，傳遞給 ContainerView 繪製行號 |

起始行號計算使用 `enumerateTextElementsFromTextLocation` 列舉視口之前的全部元素並遞增計數。實際實現可加入緩存來避免每次佈局都重新計算。

結束後，ContainerView 收到每個段落的調整後邊界與對應行號，直接在行號視圖中繪製。

---

## 五、Demo 2：可折疊段落（食譜 App）

目標：將多段落的食譜折疊成只顯示標題。

在 Demo 1 的三個委託方法基礎上，讓 `UITextView` 子類**額外遵循 `NSTextContentStorageDelegate`**：

```swift
textContentManager(_:shouldEnumerate:)
```

這個方法可以將 `NSTextElement` 標記為折疊或未折疊。折疊的元素會被跳過，不進行佈局。

需要的狀態：一個 `Set<Int>` 追蹤哪些段落偏移量被折疊，以及處理用戶點擊展開/折疊按鈕的方法。

結果：在標準 `UITextView` 內實現了段落折疊，點擊三角形即可切換。

---

## 六、Demo 3：文字附件重用（內聯動畫）

文字附件（`NSTextAttachment`）——如「訊息」中的內聯照片和貼紙、「備忘錄」中的繪圖——儲存在文字儲存層，由 `NSTextAttachmentViewProvider` 在佈局層提供渲染資訊。

**問題**：由於 `NSTextLayoutFragment` 是不可變的，編輯段落時所有物件被丟棄並重新建立。如果附件包含動畫（如內聯 GIF 或自訂動畫），每次編輯都會重新啟動動畫。

**解法**：`registerForTextAttachmentViewProviderType` 新 API，兩種重用策略：

| 策略 | 行為 |
|------|------|
| `onEditingInlineParagraphs` | 段落編輯時保留視圖提供者，按鍵不銷毀 |
| `onScrollingOutOfViewport` | 附件滾出螢幕時緩存渲染表面，返回時恢復 |

兩種策略可組合使用。

---

## 七、SwiftUI 整合

如果你的 App 是 SwiftUI：

```swift
struct MyTextView: View {
    var body: some View {
        TextViewRepresentable()
    }
}
```

`TextViewRepresentable` 在 macOS 上成為 `NSViewRepresentable`（包 `NSTextView`），其他平台則為 `UIViewRepresentable`（包 `UITextView`）。

---

## 小初的讀後感

這場 session 傳達的核心訊息很清晰：**Apple 不再要求你在便利和控制之間二選一**。`UITextView`/`NSTextView` 遵循 `NSTextViewportLayoutControllerDelegate` 這個決定，把過去只有「完全自訂文字視圖」才能接觸到的視口佈局過程，開放給了「框架文字視圖的子類」。

三個 Demo 的選擇也很精準——行號代表「顯示附加資訊」、折疊段落代表「修改佈局行為」、附件重用代表「效能與狀態保持」——涵蓋了文字視圖擴展的三個主要維度。

對 horace 來說，這對任何需要文字編輯的 App 都直接有用。如果你想在 AI 工具中嵌入文字編輯器（提示詞編輯、筆記、程式碼片段），TextKit 2027 讓你不需要拋棄 `UITextView` 的完整功能（輸入法、聽寫、輔助功能、undo/redo），同時能自由疊加自己的行為層。

`NSTextViewportRenderingSurface` / `RenderingSurfaceKey` 這對協議看似小巧，但解決了自訂文字視圖中的一個實際痛點：如何在視口佈局過程中正確追蹤視圖。這是那種「存在之前不覺得缺，有了之後回不去」的 API。

❄

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 406 片段）</summary>

你好，欢迎收看《用 TextKit 提升应用的文字体验》。我是 Tarun Uday，TextKit 团队的一名工程师。

TextKit 是 Apple 的下一代文字引擎，也是文字排版和渲染的基础，贯穿 Apple 所有平台。SwiftUI、UIKit 和 AppKit 中的文字控件都使用 TextKit 来排版和渲染文字内容。

在这个视频中，我想谈谈我们从开发者那里听到了一段时间的话题——便利性与控制性之间的矛盾，以及我们为解决这一问题而构建的新 API。

如果你正在 Apple 平台上构建文字编辑体验，你有两条路可选。第一条路是使用框架文字视图：AppKit 中的 NSTextView、UIKit 中的 UITextView，以及 SwiftUI 中的 TextEditor。使用这些控件，你可以免费获得大量功能——文字输入、选择、辅助功能、撤销与重做、听写、内联预测等。这些文字视图在内部使用 TextKit，但内部实现基本上是隐藏的。你自定义文字绘制方式的能力有限，或自定义视口管理其可视元素的方式。

第二条路是将 TextKit 用作文字引擎，并直接在视图或图层中渲染文字。我们将其称为自定义文字视图。你需要设置一个 NSTextLayoutManager，在自己的视图或图层上实现视口布局，并自行处理所有渲染工作。当你构建自定义文字视图时，你可以完全控制存储、布局以及视口布局过程，但你也放弃了框架文字视图所提供的一切。而且从头开始构建生产级的文字编辑体验需要大量工作。

但对于某些场景，在框架文字视图的便利性与自定义文字视图的控制性之间做出选择是很困难的。今天，我们将探讨如何兼得两者的优势。

若要深入了解 TextKit 架构和自定义文字视图，请观看 WWDC21 的《认识 TextKit 2》。若要了解框架文字视图如何采用 TextKit 的详情，请观看 WWDC22 的《TextKit 和文字视图的新变化》。虽然本演讲是独立的，但这两个演讲将为我们今天涵盖的所有内容提供更深厚的基础。

我将首先回顾 TextKit 的架构。之后，我将介绍我们在 TextKit 中引入的一些新 API。最后，我将通过一些示例向你展示扩展文字视图的新方式。

理解 TextKit 架构至关重要，对于打造出色的自定义文字体验来说。让我们从这里开始。

TextKit 使用四层架构进行文字渲染。底层是文字存储层。它封装了所有待渲染的文字数据。布局层位于文字存储层之上。它负责将文字分割成块以供渲染。接下来是视口层。它跟踪布局中哪些块是可见的。最顶层是视图层。这是文字在你的应用中显示的地方。

存储层、布局层和视口层在 Apple 所有 UI 框架中共享。你可以使用这些共享层在任何视图上渲染文字，或由 UI 框架提供的类视图可绘制可视元素上。

接下来，我将介绍每层的工作原理。文字内容存储负责将属性字符串分割成段落。在此示例中，文字内容存储创建 NSTextParagraph 对象，用于底层属性字符串的每个段落。NSTextContentStorage 和 NSTextParagraph 是与 NSAttributedStrings 配合使用的具体类型。如果你有不同的后端存储类型，你可以编写相应抽象类的子类：NSTextContentManager 和 NSTextElement。

接着看布局。NSTextLayoutManager 高效地测量字形的度量，这些字形构成所表示的文字，并动态创建一个 NSTextLayoutFragment，用于存储段落的计算布局信息。这些对象是不可变的。这意味着，如果段落被编辑，NSTextParagraph 和 NSTextLayoutFragment 将被重新创建。

接下来看视口层和视图层如何协同工作以高效渲染大量文字。文字视图是一个动态大小的视图，随着文字被排版和绘入其中而增大，并随着文字被删除而缩小。视口是文字视图中对用户可见的部分。TextKit 将所有工作围绕视口组织，只渲染用户能看到的文字。

为了促进将布局片段渲染到文字视图上，TextKit 提供了一个专用类：NSTextViewportLayoutController。视口控制器与文字布局管理器协调配合，与文字视图一起高效布局和渲染段落文字。文字视图知道滚动位置以及视口相对于整个文档的大小，并将此信息提供给视口控制器。视口控制器随后请求文字布局管理器提供所有与视口相交的布局片段，并将它们发送给文字视图进行渲染。

这种由视口控制器促进的协调，在每次视口状态改变时重复——即任何滚动、编辑或选择事件。这被称为视口布局过程。视口布局过程是 TextKit 高效布局和渲染的核心。

要构建你自己的自定义文字视图，请实例化 NSTextContentStorage、NSTextLayoutManager，并使用 NSTextViewportLayoutController 及其委托来渲染文字。即使我将文字视图称为视图，这也可以是任何可绘制的可视元素——在 UIKit 中，你可以选择 UIView 或 CALayer。

有时，框架文字视图可能无法满足你的应用需求。借助 TextKit 提供的灵活性——将多个文字布局管理器连接到同一个文字内容存储，在一个视图中的编辑将通过共享的内容存储传播到另一个。这意味着你可以呈现同一文档在两个不同的视图中，它们会自动保持同步。

现在，让我们来看看一些新 API。在 2027 年的版本之前，我们没有办法引用目标视图——即跨 TextKit 渲染文字的地方。

首先，认识一下 NSTextViewportRenderingSurface。这是一个新协议，表示视口内的可视元素，你可以绘制到其中：实际渲染布局片段文字的视图，并提供通用的抽象以供使用。你可以将 UIView、NSView 或 CALayer 遵循此协议，并在视口控制器的委托方法中使用它，以跟踪视口中哪些视图是可见的。

渲染表面附带一个配套键协议：NSTextViewportRenderingSurfaceKey。渲染表面键是任何可以唯一标识渲染表面的类，跨越视口布局过程周期，例如 NSTextLayoutFragment。这意味着你可以使用 NSTextLayoutFragment 作为键，在映射表或字典中缓存渲染表面。

你可以为键分配一个渲染表面，在视口布局过程中，通过使用 renderingSurfaceFor 委托方法。这些在视口布局过程开始时被清除。你可以查询特定键的渲染表面，在 didLayout 过程中，使用视口控制器的 renderingSurfaceFor 方法。

现在我们已经了解了 TextKit 在 2027 版本中的工作原理，让我们来看看文字视图是如何驱动 Apple 默认文字体验的。UIKit 的 UITextView 和 AppKit 的 NSTextView 驱动着 Apple 平台上数千种长文本体验，包括"信息"、TextEdit、"备忘录"和"日记"。

如果你有 SwiftUI 应用，实现长文本体验最方便的方式是使用 TextEditor。但你也可以在应用中包含 UITextView 或 NSTextView，通过使用 ViewRepresentable。

为了向你展示如何使用 UITextView 的 TextKit 钩子来扩展 UITextView，我将创建几个不同的示例应用。

**示例一：代码编辑器行号**。从 UITextView 子类开始，设置等宽字体。UITextView 和 NSTextView 现在遵循 NSTextViewportLayoutControllerDelegate——这意味着你可以子类化并覆盖委托方法：

- `WillLayout`：清空行号变量，计算起始行号（视口之前所有段落的计数），使用 `enumerateTextElementsFromTextLocation` 列舉元素
- `configureRenderingSurface`：为每个段落收集 `layoutFragmentFrame`
- `DidLayout`：将片段帧从文字容器坐标转换为视口坐标，传递给 ContainerView

ContainerView 收到每个段落的信息后，计算实际行号并在行号视图中绘制。

**示例二：可折叠段落（食谱）**。将多段落食谱折叠成只显示标题。在同样的三个视口委托方法基础上，让 TextView 额外遵循 NSTextContentStorageDelegate，通过 `textContentManager: shouldEnumerate` 将 textElements 标记为折叠或未折叠。使用整数集合跟踪折叠的段落偏移量。

**示例三：文字附件重用**。文字附件（NSTextAttachment）如内联照片、贴纸、绘图——存储在文字存储中，由 NSTextAttachmentViewProvider 提供渲染信息。由于布局片段是不可变的，编辑段落时视图提供者被丢弃并重新创建，导致动画重新开始。

解决方案：`registerForTextAttachmentViewProviderType` 新 API。两种重用策略：`onEditingInlineParagraphs`（段落编辑时保留视图提供者）和 `onScrollingOutOfViewport`（附件滚出屏幕时缓存，返回时恢复）。可组合使用。

总结：要创建便利而强大的富文本编辑器体验，在 UIKit 上使用 UITextView，在 AppKit 上使用 NSTextView。如果你有 SwiftUI 应用，使用 ViewRepresentable 将这些文字视图包含到你的应用中。对于那些想要对文字渲染有更多控制权的人，使用 TextKit 创建自定义文字视图，并使用新的渲染表面 API。

感谢观看！

</details>
