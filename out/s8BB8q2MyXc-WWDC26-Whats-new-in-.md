# WWDC26: What's New in SwiftUI | Apple

> 來源：[YouTube](https://www.youtube.com/watch?v=s8BB8q2MyXc)
> 長度：約 28 分鐘
> 語言：英文
> 整理：AiEira

---

## 是甚麼

2027 年 Apple 平台上的 SwiftUI 迎來重大更新。主講人 Steven 與 Julia（UI Frameworks 工程師）用一個自製貼紙 App 貫穿全場，示範五大領域的新功能：外觀、工具列、文件 API、互動方式、效能。

---

## 一、煥新的外觀與自適應

### Liquid Glass 自動升級

App 不需改任何一行程式碼，在 2027 平台上自動獲得更新後的 liquid glass 外觀。macOS 上可將 liquid glass 自訂元素標記為互動式，讓它們對滑鼠點擊做出流暢回應。

### 視窗非活躍提示

iPad 與 Mac 的側邊欄在視窗非活躍時自動變暗——系統透過 `appearsActive` 環境值讓你條件式調整自訂元素。menu bar 圖示預設精簡化，只保留關鍵動作。

### iPhone 可縮放

iOS 27 起，iPhone App 也變得可調整視窗大小。Xcode 27 的 live preview 新增縮放把手，可直接拖曳測試不同尺寸下的佈局行為，模擬 iPhone Mirroring 或在 iPad 上跑 iPhone App 的情境。

---

## 二、工具列的重新掌控

### 可見度優先級

```swift
.visibilityPriority(.high)
```

為每個工具列項目設定優先級，系統在空間不足時優先保留高優先級按鈕。Demo 中 undo/redo 原本被擠到 overflow menu，加 `.high` 後自動浮上工具列。

### Overflow Menu 容器

不常用的動作（換照片、匯出、清除）用新的 `ToolbarOverflowMenu` 容器群組起來，永遠待在 overflow menu 中。

### 頂欄釘選

```swift
.topBarPinTrailing
```

確保分享按鈕永遠在 trailing 位置，不被隱藏。

### 捲動時自動隱藏

```swift
.toolbarMinimizeBehavior(.disappearOnScroll)
```

navigation bar 在向下捲動時自動讓位，騰出最大內容空間。

---

## 三、全新的文件 API

這是本場最重磅的更新。SwiftUI 原本就有 `FileDocument` / `ReferenceFileDocument`，2027 年在此基礎上大幅擴充。

### Document Creation Source

```swift
DocumentCreationSource("blank")
DocumentCreationSource("photo")
```

在 Launch Scene 上宣告多個文件建立來源，使用者選擇不同按鈕時，SwiftUI 透過 `context` 參數傳遞來源資訊給初始化方法。Demo 中選擇「從照片建立」會直接打開照片選擇器。

### 讀寫分離架構

| 協議 | 角色 |
|------|------|
| `WritableDocument` | 宣告可寫格式 + 提供 snapshot |
| `DocumentWriter` | 負責實際寫入磁碟 |
| `ReadableDocument` | 宣告可讀格式 + 套用 snapshot |
| `DocumentReader` | 負責實際從磁碟讀取 |

關鍵設計：

- **Snapshot 模式**：`snapshot()` 回傳文件在某一時間點的內容快照（如背景圖 + 貼紙座標 + 貼紙本身），與 UI 狀態解耦
- **Nonisolated async write**：寫入方法是非隔離的 async，磁碟操作在背景執行，UI 保持回應
- **差異寫入**：比對當前與前次 snapshot，只寫入實際變更的部分
- **進度回報**：透過 Foundation 的 `Subprogress` API 回報寫入進度
- **多格式匯出**：同一個 writer 可支援多種格式——demo 中貼紙 App 同時支援自訂 package 格式與 PNG 匯出（用 Core Graphics  flatten 貼紙與背景）

### 與 Observation 框架整合

Document 類別使用 `@Observable` 宏，視圖只在依賴的屬性變更時才更新，自動獲得效能提升。

---

## 四、互動方式的全面提升

### Reorderable 容器

全新的 `reorderable` modifier——拖曳重新排序，而且同一套程式碼可用在任何容器上：List、LazyVGrid、甚至 LazyVStack。watchOS 也首次獲得 reorder 能力。

### Swipe Actions 不限 List

過去 `swipeActions` 只限 List。2027 年起任何 view 都可用 `swipeActionsContainer` modifier，在 scroll view 內的所有 item 上統一管理滑動動作。

### Confirmation Dialog 的 Item Binding

confirmation dialog 支援與 sheet 相同的 item binding 模式——傳入 binding，設值就彈出對話框。Alert 同樣支援。

---

## 五、效能與資料流

### AsyncImage 內建 HTTP 快取

`AsyncImage` 現在預設遵循標準 HTTP 快取語意——圖片載入後自動快取，往回捲動時不再重新載入。零程式碼變更，全 App 自動啟用。也可自訂 `URLRequest` 的快取策略，或提供自訂 `URLSession` 與 `URLCache`。

### @State 轉為 Macro——Lazy 初始化

`@State` 從動態屬性轉為 macro。對於 class 型別的 state，初始化改為 lazy——只在首次建立實例，後續視圖重建時不再重複建立。此行為已回溯至 iOS 17 / macOS 14。注意：若在 init 中對同一個 state variable 賦值，需移除預設值以避免編譯錯誤。

### ContentBuilder：統一 Builder，加速型別檢查

SwiftUI 中最常見的 builder（`Section`、`Group`、`ForEach` 等）統一為 `ContentBuilder`。過去編譯器需逐一嘗試多個 builder 多載來推斷型別，深層巢狀視圖可能觸發「unable to type-check in reasonable time」錯誤。現在只有一條路徑，大幅提升型別檢查速度。此改進透過 Xcode 27 生效，適用於任何 deployment target。

---

## 六、Xcode 27 的 AI Agent Skills

Xcode 27 隨附兩個 SwiftUI agent skill：

- **SwiftUI Specialist**：協助遵循 SwiftUI 最佳實踐
- **What's New in SwiftUI**：引導採用 2027 新 API

可在 Xcode 27 的 coding assistant 中直接使用，也可用 `xcrun agent-skills export` 匯出為 markdown 檔案，匯入其他工具（如 Claude Code、Hermes）。

---

## 小初的讀後感

這場 session 的密度很高，但真正值得留意的是兩個底層轉變。

第一，**文件 API 的 snapshot 架構**。`WritableDocument` / `ReadableDocument` 的設計不只是「讀寫分離」，而是引入了 snapshot 這個概念——文件在某時刻的純資料快照，與 UI 狀態完全解耦。這意味著寫入可以在背景執行、可以比對差異、可以回報進度，而 UI 繼續回應。這是 document-based app 的正確抽象。horace 若未來要處理複雜的文件編輯場景，這個架構值得直接對標。

第二，**`@State` 轉 macro 的訊號**。這不是語法糖——這是 SwiftUI 從 runtime 動態屬性逐步遷移到編譯期 macro 的關鍵一步。lazy 初始化消滅了過去 view 重建時重複建立 class 實例的浪費，而且回溯至 iOS 17。這代表 Apple 正在系統性地將過去「執行期才知道」的東西移到「編譯期就決定」，最終帶來更少的意外行為和更好的效能。

工具列的新 API 也值得一提——visibility priority、overflow menu container、top bar pin 這三件工具給了開發者對工具列行為的精細控制權。過去只能「放上去，祈禱系統別把它藏起來」，現在可以明確宣告優先級。

至於 Xcode 27 的 agent skills……這是 SwiftUI 團隊第一次以「可供 AI agent 消費」的格式發布知識。`xcrun agent-skills export` 匯出 markdown 這件事本身，就是一個重要的姿態。

❄

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 642 片段，英文）</summary>

Hi, I'm Steven and I work on UI Frameworks.

My name is Julia and I'm also a UI frameworks engineer. We are excited to talk to you about what's new in Swift UI.

Swift UI has gained some major upgrades. From a refined look and feel to performance improvements, new ways to interact with your apps, and a powerful new document API, we have a lot of great new things to share. But first, I love stickers. I have my laptop covered with them. I love stickers, too. But there are only so many places in the real world where we're allowed to stick them. So, we came up with a way to unlock unlimited sticker potential — an app.

Meet our sticker app. I'll start by picking a photo. I really like this photo of Steven and me at Apple Park. Now, I wish we could bring our pets to work. They would absolutely love it here. So, I'm going to drag this sticker of my dog Pretzel into the scene and resize her to match the size of her personality.

And I'll add my cat, Kishka. She's got an even bigger personality.

Now, this is what I call an ideal workday. I wish we could do this all day, but there's a lot to cover. So, it's important we stick to the script. Our app takes advantage of lots of new enhancements to Swift UI that have helped us build a first-class user experience that looks great and also has great performance. I'll start by taking you through the beautiful new look apps gain on the 2027 releases along with ways to optimize toolbar content for resizability.

Julia will tell you about new APIs that unlock powerful document features in your apps along with improvements to presentation and interaction. And finally, I'll talk about how to keep your apps running smoothly with enhancements to performance and data flow.

Let's get started with the refreshed look and feel for apps on the 2027 releases. When I build and run our app, the liquid glass design automatically takes on its updated appearance. Apps gain this look without having to change a single line of code. Liquid glass has a refined look and automatically responds to the new liquid glass slider to adjust its tint. On Mac OS, like on iOS, you can mark liquid glass custom elements as interactive, so they respond more fluidly to users clicks. And this is optimized to work great with the mouse pointer, so it feels right at home on the Mac.

And just like Mac, our iPad app automatically takes on a distinct appearance when inactive with the icons and text dimming to reinforce which window is active. Like here when I tap to switch between our app and the files app. I love how these improvements look in our app and even more so since the app's look was refreshed without having to make any code changes.

But there are also ways to fine-tune our app's appearance to get things just right. Our custom account button in the sidebar dims along with the rest of the tab labels using the appears active environment value to conditionally reduce the buttons opacity when the window isn't active. iPad and Mac menu bars now have a minimal set of icons by default, reserving them for key actions. However, I can apply the label style, title, and icon modifier to our store menu item to show its icon, so that one will stand out.

As I accumulate more stickers, I really appreciate the resizability of our app on Mac and iPad. And on iOS 27, our iPhone app becomes resizable, too. In Xcode 27, live previews now have resize handles that allow you to test how your app responds to being interactively resized. This allows you to instantly preview how an app will behave when using iPhone mirroring or when running it as an iPhone app on iPad. This is already working great, especially since we made sure our app resizes well on iPad and Mac.

Apps built with Swift UI gain a lot of this functionality automatically. But if your app uses both UI kit and Swift UI, there may be some additional things to consider. Things like how to correctly determine screen geometry, using size classes instead of idiom for sizing your views, and responding to interface orientation changes. To learn more about getting ready for resizability for apps that use both UI kit and Swift UI, check out Modernize Your UI Kit app.

Our app also has a full store experience that allows people to download new sticker packs. My personal favorite is the WWDC26 sticker pack. The store view has a few tabs, including one for the shopping cart. The shopping cart tab is displayed on the bottom trailing edge of the screen, distinguishing it from the other tabs, which contain store content. To enable this special tab placement, I'm using the new prominent tab roll to make it stand out.

With all of the features our app has, the toolbar is a great way to provide quick access to the most important actions. As I add more features to the app, the list of toolbar items will probably grow even bigger. And this becomes especially important when resizing the app. When I resize the app window, the toolbar items are automatically adjusted by the system, and some of the items that don't fit end up becoming hidden.

On iPhone, where there's even less horizontal space to work with, there isn't enough room for all my toolbar buttons. Important actions like undo, redo, and share are hidden in the overflow menu. And that's where the new toolbar APIs come in. They allow me to specify which buttons stay visible when toolbar space is limited.

The most important toolbar item group contains buttons for editing, undo, and redo, but they're currently hidden. I want the system to know that it's important to keep them visible. I can do this by adding the new visibility priority modifier and setting the priority to high. Now, the undo and redo buttons become visible.

Some of the actions I prefer to keep in the overflow menu since they aren't used as often, like the buttons for swapping out the photo, exporting the page as an image, and clearing the stickers. I choose to always place these buttons in the overflow menu by grouping them in the new toolbar overflow menu container. And there they are in the menu if I need them.

Lastly, for my share button, I want to make sure it's never hidden so I don't forget to send these sticker pages to everyone I know. I can use the new top bar pin trailing placement to make the share button always visible in the trailing position.

And now the toolbar is set up perfectly to access all the apps important features, no matter the window or screen size.

There's one more toolbar enhancement I want to show you. I have lots of stickers in my collection and when I'm scrolling through them, I want to have as much space as possible for all of them. So, I add the new toolbar minimize behavior modifier and set it to disappear on scroll for the navigation bar placement. Now, the system automatically moves the navigation bar out of the way when I scroll.

I think the app looks and feels great, but there's a lot more going on under the surface. Our app can open and save sticker pages and even has support for exporting the pages as images. This is all thanks to some powerful new features Julia will tell you about.

The app has all these capabilities and even more thanks to the new Swift UI document API. I'll start by giving an overview of the new document APIs and how they serve as a base for building an app. For quite some time now, Swift UI has had support for document-based apps via the file document and reference file document protocols.

In the 2027 releases, I'm happy to share expanded APIs that build on that foundation. You might be familiar with document-based apps like Pixelmator Pro or Pages or the one we spend our days in, Xcode. They get a lot of functionality out of the box, including things like keyboard shortcuts, command N for new documents and command O for opening documents, the edited indicator that tells you when a document has changes, a smart autosaving mechanism, and much more. And the document API unlocks a number of improvements an app can make both under the hood and in the UI.

I'll cover three of these, including the document creation context, disk reading and writing performance improvements, and first class support for direct document URL access.

Here's how people create documents in our app. By default, the app lets you start with a blank sticker page, but I want to help people get going more quickly. So, there is also a button to create a page from a photo. I use the new document creation source API to declare two sources, blank and photo, and add a new document button for each one to the launch scene. When choosing one of these buttons, Swift UI passes the source to my document creation closure via the context parameter. I check the context in my initializer and if the source is photo, the document opens with the photo picker already presented. Now I'm only one tap away from putting stickers on my photo.

Document-based apps read and write a lot of data. They can also have complex UI that needs to update frequently. The new API provides great ways to optimize these operations and keep your app running smoothly.

I opt our app into the document architecture by declaring a document group as the first scene in the app's body. My sticker document class describes the document type. It provides data to the views and describes how to read data from disk and write it back. The document API works in conjunction with the modern observation framework. So I'm using the observable macro. This alone gives me a performance boost. The views will update only when a property they depend on changes.

My goal is to make reading and writing as fast and efficient as possible. Let me take you through the optimization points in the new API.

For writing, I conform the document to the writable document protocol. It has three requirements. First, a list of formats the app can write. Our application supports custom package format with a photo and stickers inside. Second, the snapshot method that returns the current document content for writing. To represent the content, I use a custom page snapshot struct. It contains everything I need for writing: the background image, coordinates for the stickers, and the stickers themselves. It acts as a snapshot of the document at a single point in time.

To satisfy the third requirement, I provide a writer. The writer conforms to the document writer protocol and knows how to write a document to disk in a specified format. I give it the requested content type which for my app is sticker document. The document writer protocol has a notion of snapshot and the page snapshot type fits perfectly here.

Document writer's only requirement is a method for writing. It offers multiple opportunities to optimize performance. First, the write method is nonisolated and asynchronous. This lets me perform expensive disk writing operations in the background so the app stays responsive. I write only the parts of the package that actually need updating by comparing the current and the previous snapshots. Even with all the optimizations, disk operations can take noticeable time. So, Swift UI provides a progress parameter that lets me report writing progress using the foundation subprogress API.

To teach our document type how to read from disk, I conform the sticker document class to the readable document protocol. Readable document is a twin to writable document. Here's how they compare. Each protocol requires a list of supported content types. Writable document provides a snapshot and readable documents knows how to apply it. Writable document has a friend protocol document writer and readable documents friend is document reader which does all the disk related heavy lifting.

Now the sticker app is ready to read and write files like this page. I think I make a pretty good pirate.

There's one more feature to add. Saving pages as images so I can share them with people who don't have the app. The document API makes it possible to extend my writer to save pages in another format like PNG using core graphics. I return to the writable content types definition and add PNG to the list. Now to support an additional format, I revisit the write method I implemented earlier. Since the app can now handle multiple formats, I am adding content type checks for each type the app supports. For PNG, I use core graphics to flatten the stickers and background photo into a single image and write it to the URL.

To add even more types, I could write the document in any format using any framework just by adding another content type. That's how our app is set up to save documents.

Now, it's time to get to my sticker collection where there are some great enhancements to presentation and interaction. Sometimes our massive collection of stickers can feel a little chaotic, and that's where the reorderable container APIs come in.

There are two different ways to browse the sticker collection in the apps inspector. The first is a list that displays each sticker along with its name. I'd like to keep these stickers organized by dragging them to rearrange their order. So, I use the reorderable API. I add the reorderable modifier to for each and add a reorder container modifier to the list. Then in the closure, I call this helper function I wrote difference.apply to update my array of stickers. Under the hood, my apply function uses the open-source Swift collections package to commit the ordering changes. Visit swift.org for more details. Swift UI automatically handles the drag direction and animation for me.

I can also organize my stickers in a grid which makes it easier to browse more at a time. And the reorderable API works with any container, not just list. This means I can take the code from my list and repurpose it to use a lazy V grid. The code for reordering stays exactly the same. I get the same interactive reordering behavior on a completely different container using the same code. And now these APIs also bring reordering capabilities to Watchers for the first time.

When it comes to reordering, that's just the beginning. For a deep dive into all of the features of reorderable containers, check out the code along session: Build powerful drag and drop in Swift UI.

When I'm on the go, I love to customize my sticker pages on my iPhone. The sheet at the bottom of the UI keeps all my stickers right where I need them. I even set up swipe actions for removing stickers from the list by adding the swipe actions modifier to my list item along with this delete button. But I want some more flexibility to customize my list. So I've decided to switch to using a lazy stack. And now Swift UI supports swipe actions on any view, not just list. I move my for each out of the list into a lazy vstack with my updated item style and add the swipe actions container modifier which coordinates the swipe actions across the items in this scroll view.

Well, as I said before, I love stickers. So, it's no surprise that when I start decorating a photo, I'll admit it, I can get a little carried away, and sometimes that means I need to make space by deleting some stickers, even if I love them all.

I've added a context menu to each sticker placed on the photo, giving me quick access to delete it with this delete button. Tapping the button sets the sticker to delete state variable to the current sticker. I've also added a confirmation dialogue modifier. Now confirmation dialogues support the same item binding pattern that sheets use. I pass a sticker to delete binding to the modifier. When I set sticker to delete to a value by tapping the delete button, the confirmation dialogue appears. And this also works with alert.

I've taken you through some great improvements to presentation and interaction, but that's not all. There are even more improvements in Swift UI in the 2027 releases. Many of these improvements make the APIs you'll already using better without any changes to your apps.

Great performance is important for making an app feel responsive and polished. Being thoughtful about the way data flows through your app is one of the best ways to keep your app's performance in top shape. Steven is going to tell you about some big improvements to data flow and performance.

Thanks, Julia. The sticker store you added to the app is really cool. I love how the sticker packs are downloadable because that allows me to take advantage of improvements to async image. Async image is a great way to load image assets from the internet as they appear on screen. This works great when scrolling to reveal more of these adorable stickers of Kishka and Pretzel. But up until now, Async image hasn't kept images in memory. When scrolling back up, they would reload when reappearing on screen. I'd prefer that these images show immediately when scrolling back to the top. And in the 2027 releases, they do.

Async image now supports standard HTTP caching, so images are cached by default, respecting the server's cache headers without any changes to your code. This is enabled automatically for every app. And apps built with Xcode 27 can take advantage of new APIs to customize how downloads happen. For more control over how an image is downloaded, I can construct my own URL request and pass it to async image. This allows a wide variety of per request customizations like specifying a cache policy for instance. And if I need a longer lived configuration, like a bigger cache, let's say, I can instantiate my own custom URL session and configure a URL cache with whatever capacity I need and then use my session by passing it to the async image URL session modifier. Now, when I scroll back to the top, the images are automatically loaded from the cache.

SwiftUI provides a variety of ways for apps to model and store their data and to pass that data to views. One great way to store an app's data is using observable classes like I do here with the sticker store class. When sticker store view is initialized, a new instance of my sticker store class is created and assigned to the state variable. This instance stays around for the lifetime of the view. But what happens when the parent view updates causing sticker store view to be initialized again? In prior releases, a new instance of sticker store would be created on every initialization, but the original instance is still the one being stored in the state variable and so the new one was just discarded. This would happen again for every reinitialization of the view even though the main stored instance of the class remains stable.

In the 2027 releases, for the first time, classes initialized and stored using state properties are now lazy, which means they will only be initialized once. This is thanks to the conversion of state from a dynamic property to a macro. Now when sticker store view is initialized for the first time, a new instance of my sticker store class is created like before. But on future initializations, no new class instances are created. And this behavior has been backported to the releases where observable was first introduced. Starting with iOS 17, Mac OS 14 and aligned releases.

In some cases, the introduction of the state macro can be a source breaking change. For example, if you specify a default value for your state variable and then you assign a value to the same state variable inside your init, Xcode will show an error about use before initialization. To resolve this error, remove the unnecessary default value assignment. For additional details about how the state macro may impact your code, check out the documentation.

Maintaining good runtime performance is critical for keeping your app working smoothly. But there's another type of performance that can have a significant impact on your app development experience. If your app has complex, deeply nested views, you may have encountered this error: "The compiler is unable to type check this expression in reasonable time." But why does this happen?

This view has a section, a group, and a for each wrapping its content. To type check this expression, first the compiler has to select which overload of section to use. Section can be initialized with a builder that produces either a view or table row content. To know which one to use, the compiler has to try both options. In my code, the section builder returns a group. The compiler can't know what type of content section produces until it figures out the type of the nested groups content. This time there are even more options. And for the nested for each, the compiler will have to try each one. And then for each's builder has its own set of options that will also need to be checked. And we haven't even gotten to the content yet. Trying each of these paths makes type checking increasingly expensive.

But I already know that section, group, and for each in my code are building views. So there's really only one valid path through this decision tree. Instead of this complex set of choices, what if these builders weren't constrained by the types they produce and instead just assembled their content? In the 2027 releases, that's exactly what Swift UI starts doing.

The most common set of builders now share a single initializer, leaving just one straightforward path. This is possible because multiple different builder types have been unified under a single builder: ContentBuilder. This is a step towards enabling unified builders across all of Swift UI's APIs. And content builder can be used with any minimum deployment target because under the hood, it's an evolution of the existing ViewBuilder.

Content Builder provides a substantial improvement in type-checking performance in Swift UI when building using Xcode 27. Whether you're targeting the 2027 releases or previous releases as well.

We're also excited to introduce new agent skills included with Xcode 27 to help you adopt the new features from the 2027 releases in your apps and improve your app's performance and code correctness. The Swift UI specialist skill can help you follow Swift UI best practices in your apps. The what's new in Swift UI skill can guide you through adopting new APIs from the 2027 releases. Both of these skills can be accessed in the coding assistant in Xcode 27. And to use these skills with other tools, you can export them with the xcrun agent skills export command. This will create markdown files you can import in your workflows.

We've covered some exciting new enhancements to Swift UI. Now it's your turn. Start by building your project in Xcode 27 for the 2027 releases and then check out your app's updated look and feel. If you have a document based app, investigate how the new document APIs can make it even better. And try out the Swift UI agent skills in Xcode 27 to adopt new APIs and best practices.

Well, as sad as we are to peel ourselves away, we have to adhere to the schedule. We hope you have as much fun adopting these improvements in your apps as we had with ours. Thanks for sticking with us.

</details>
