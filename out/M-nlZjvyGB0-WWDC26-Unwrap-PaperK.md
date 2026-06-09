# WWDC26: Unwrap PaperKit | Apple

> 來源：[YouTube](https://www.youtube.com/watch?v=M-nlZjvyGB0)
> 長度：約 7 分鐘
> 語言：粵語／中文
> 整理：AiEira

---

## 是甚麼

PaperKit 是 Apple 平台畫布體驗的底層框架——你在備忘錄手繪、在預覽程式簽名、在 Freeform 構思，背後都是它在跑。iOS 27 / macOS 27 / visionOS 27 起，Apple 將 PaperKit 全面開放給開發者。

WWDC26 這場 7 分鐘的 session 由 Pencil and Paper 團隊工程師 Matt 主講，示範如何用 PaperKit 由零搭建一個漫畫編輯器。

---

## 三大支柱

### 一、資料模型：PaperMarkup

畫布上的一切——形狀、圖片、筆觸、文字——現在都可以透過程式讀寫。關鍵 API：

- `PaperMarkup.subelements` — 以 `MarkupOrderedSet` 的形式暴露所有元素
- `MarkupOrderedSet` 是一個有序集合，支援讀取與寫入
- 透過 `paperMarkupViewController.markup` 更新畫布

對開發者來說，這意味著你不再只是「放一個畫布讓用戶畫」，而是可以**程式化生成、修改、操控畫布上的每一個元素**。

### 二、元素系統

每個元素都有具體類型，且遵從 `Markup` 協議：

| 類型 | 自訂屬性 |
|------|---------|
| 形狀（Shape） | 圓角半徑、曲線控制點、描邊顏色、填滿顏色 |
| 圖片（Image） | — |
| 連結（Link） | — |
| 放大鏡（Magnifier） | — |
| 鉛筆筆觸（Pencil Stroke） | 支援字元識別、貝塞爾路徑轉換 |

通用屬性包括 `frame`、`rotation`，以及新的 **`allowedInteractions`**：

- 可精細控制每個元素的移動、縮放、旋轉、刪除、樣式、選取
- 支援組合使用，亦可一鍵設為 `.readOnly` 鎖定全部

這對模板式應用極其關鍵——你能讓某些元素（如漫畫格）不可編輯，同時允許用戶在上面添加對話框和繪圖。

### 三、裝飾層：MarkupAdornment

Adornments 是**錨定在畫布座標上的視覺覆蓋層**，但不會成為文檔的一部分：

- 不儲存、不列印、不匯出
- 自動跟隨縮放和滾動
- 與持久化的 markup 完全分離
- 適合按鈕、註解、協作 UI

Demo 中，Matt 在每個漫畫格中心放置 SF Symbol 按鈕，點擊後觸發 `ImagePlaygroundViewController`，生成的圖片以 `ImageMarkup` 形式插入畫布。

---

## 實際 Demo 流程

Matt 由零搭建一個漫畫編輯器，步驟如下：

1. **生成模板**：為每個漫畫格建立矩形形狀元素 → 寫入 `subelements`
2. **鎖定模板**：設 `.allowedInteractions = .readOnly`，防止用戶拖動或刪除格線
3. **套用樣式**：遍歷 `subelements`，設定描邊與填滿顏色
4. **添加裝飾**：在每個格中心放 `MarkupAdornment`（SF Symbol 圖標）
5. **整合 Image Playground**：實作 `didTapAdornmentWithID` 代理方法 → 打開 Image Playground → 回傳圖片 → 建立 `ImageMarkup` → 插入畫布
6. **加入文字與繪圖**：用 Apple Pencil 繪製，筆觸自動成為 markup 元素

---

## 與其他技術的關係

- **PencilKit**：PaperKit 基於 PencilKit 構建。所有 PencilKit 模型 API 可直接使用，包括新的字元識別與貝塞爾路徑轉換。詳見同場 session「Reading Between the Strokes with PencilKit」。
- **Image Playground**：可從 PaperKit 內部調用 Image Playground 生成圖片，直接插入畫布。詳見「Create High-Quality Images Using Image Playground」。

---

## 小初的讀後感

PaperKit 的開放是 Apple 一個重要的訊號——他們終於把自家應用的核心體驗交到開發者手上。備忘錄、預覽程式、Freeform 跑了多年的畫布引擎，現在你可以用它來做任何事。

我特別留意到 `MarkupAdornment` 的設計。它解決了一個經典問題：**如何在不污染文檔的前提下，為畫布添加編輯器專屬的 UI**。按鈕不儲存、不列印、不匯出，只活在編輯期間——這個分離做得很乾淨。

對 horace 來說，PaperKit 打開了一扇有趣的門。如果你的 AI 工具未來需要任何形式的視覺標註——在圖片上圈出重點、在文檔上疊加註解、讓用戶手繪輸入——PaperKit 提供了現成的、Apple 級的畫布。不是從零造輪子，而是站在 Apple 的肩膀上。

❄

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 127 片段）</summary>

你好 我是Matt
Pencil and Paper团队的工程师

能让用户在画布上
随心创作的App

是Apple平台上
最具代表性的体验之一

PaperKit正是驱动
画布体验的核心

支撑着Apple众多
自家应用程序的运行

当你手绘想法 插入图片

或在备忘录中标注文稿
那就是PaperKit

这是完整的画布体验
铅笔 形状 文字 图片

协同运作

当你在预览中打开PDF
添加签名或高亮段落

或圈出重要内容
那也是PaperKit

在macOS的Freeform中构思
同样是PaperKit

在iOS macOS和visionOS 27中
PaperKit全面开放

今天我将展示如何解锁PaperKit

让你完全掌控
你的画布体验

我将从数据模型入手

它让你访问
画布上的所有内容

然后介绍如何使用
形状和图片等元素

最后讲解装饰

用于添加交互式
覆盖层和控件

我们先来看数据模型

我一直在构建
一个基于PaperKit的漫画编辑器

我已设置了一些基本模板

但目前只到这一步

现在我需要将这些模板
转换为PaperMarkup

PaperMarkup新增了
subelements属性

它让你以MarkupOrderedSet的形式
访问画布上的每个元素

这是一个有序集合
支持读取和写入

此代码段为每个面板
创建一个形状元素

然后更新markup

就这样

让我们在iPad上试试

我将为漫画添加
一个三页面板

很好

完全符合我的预期

画布完全可交互

但这对漫画编辑器
来说是个问题

我可以选中面板
拖动甚至删除它们

这不是我想要的

模板元素
不应该是可编辑的

要解决这个问题
我需要改变形状元素的行为

画布上的每个元素
都遵循Markup协议

这提供了通用属性
例如frame和rotation

还有一个新的
allowedInteractions属性

这是一个MarkupInteractions选项集

让你精细控制
每个元素可修改的内容

Markup interactions让你控制
移动 调整大小和旋转

以及删除 样式和选择
可单独或组合使用

如果你想一次性
锁定所有内容

read-only将所有内容
合并为单个标志

非常适合漫画模板

要限制漫画编辑器中
面板的交互

我需要将.allowedInteractions
设为.readOnly

我来试试

现在当我点击面板边框时

什么都没发生

模板形状已变为只读

我可以添加对话气泡
并移动它

并为其设置样式

但面板保持固定

完美

App开始成形
但面板需要更加突出

所以我在工具栏添加了
颜色选取器来设置模板样式

为了实现样式设置
我将深入研究元素

PaperMarkup中的每个元素
都有具体类型

形状 图片 链接
放大镜和铅笔笔触

它们都属于同一个
Markup有序集合

并遵循Markup协议

但每种类型
都有其自定义属性

让我们深入了解形状

PaperKit支持多种形状类型

每种类型都有其属性
例如圆角矩形的圆角半径

或曲线的控制点

我为漫画面板使用了矩形

它们有描边颜色
这正是我们需要的

要为面板应用颜色
我需要遍历subelements

然后设置描边和填充颜色

为了增添额外亮点

我将对markup背景
使用相同的颜色

最后在paperMarkupViewController上
更新markup

让我在iPad上查看结果

就这样 画布完成了变换

页面以我选择的颜色
进行了样式设置

开始展现出
更具个性的面貌

PaperKit基于PencilKit构建
我可以用Apple Pencil绘图

每个笔触都成为markup元素

我可以使用
所有PencilKit模型API

这些API现在支持
字符识别

和贝塞尔路径转换

想了解完整详情

请观看"Reading Between
the strokes with PencilKit"

现在来看如何使用
装饰添加自定义控件

我想为每个面板添加按钮
让用户创建艺术作品

但我不希望这些控件
成为文稿的一部分

它们不应被保存
打印或导出

我希望它们仅在编辑时
显示在画布顶部

这正是Markup adornments的作用

锚定到画布坐标的
视觉覆盖层

这使adornments非常适合
按钮 注释和协作UI

它们自动跟踪缩放和滚动

与持久化的markup
完全分离

对于每个面板
我创建一个MarkupAdornment

我将它锚定到面板中心

并通过imageConfiguration
赋予它SF Symbol图标

然后将数组分配给
控制器的adornments属性

为了处理点击

我实现了代理方法
didTapAdornmentWithID

当用户点击adornment时

我会呈现
ImagePlaygroundViewController

当Image Playground返回图片时
我创建一个ImageMarkup

然后将其插入subelements
并更新视图控制器的markup

让我们再试一次

我将点击其中一个面板
来创建艺术作品

我的漫画将讲述
一只超级英雄狗

在城市中打击犯罪

生成的图片填满了面板

想进一步了解
在App中生成图片

请观看"Create high-quality images
using Image Playground"

再添加几张图片
一些文字和字体

漫画第一页就完成了

我们的超级英雄狗
将拯救这一天

现在你可以构建
完全交互式的

基于画布的体验
在你的App中使用PaperKit

使用数据模型以编程方式
读取和修改画布上的内容

添加adornments以创建
专为App定制的交互式覆盖层

我迫不及待想看看
你们将如何解锁PaperKit

感谢收看!

</details>
