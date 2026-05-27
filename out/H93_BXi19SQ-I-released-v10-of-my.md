# I released v1.0 of my game engine Usagi! - Changes Review & What's Next

> 來源：[YouTube](https://www.youtube.com/watch?v=H93_BXi19SQ)
> 長度：約 16 分鐘
> 語言：英文
> 整理：AiEira

---

<!-- BLOG_REWRITE_PLACEHOLDER: LLM will insert rewritten blog here -->

# Usagi v1.0 正式發布 + 遊戲引擎對比：Usagi vs Godot vs Bevy

> 來源：[Brett Chalupa — Usagi v1.0 Release](https://youtu.be/H93_BXi19SQ) · 16 分鐘
> 整理 + 擴展對比：小初（Eira）

---

## 一、Usagi v1.0 更新摘要

Brett Chalupa 發布了 Usagi v1.0——一個極簡主義的 Rust + Lua 2D 遊戲引擎。主要更新：

### Breaking Changes
- **像素 API 重命名**：`dot_px()`（設像素）、`get_pix()`（讀像素）、`get_spr_px()`（讀精靈像素）。統一使用 `px` 縮寫（跟 `rect`、`tri` 保持一致）
- **Tint 顏色修正**：slot 0 現在是真正的純白（`#FFFFFF`），而非 PICO-8 調色板的白

### 新功能
- **`read_json()` / `read_text()`**：從 `data/` 目錄載入 JSON 和文字檔，支援即時熱重載（改檔即生效）
- **`text_ex()` alpha 參數**：文字淡入淡出效果
- **Shader API 改進**：自訂 GLSL 片段著色器支援後處理特效

### 工具鏈
- `usagi update` — 自動更新到最新版
- `usagi dev` — 啟動開發模式（熱重載）
- `usagi tools` — Jukebox（音效預覽）、TilePicker、SaveInspector、ColorPalette

### 正在製作
- **Neo Gear**：垂直捲軸射擊遊戲（schmup），帶「option」浮游炮系統
- **Soko World**：從 Rust 重寫為 Lua 的倉庫番遊戲
- **Temple of the Sun God**：從 TypeScript 移植的 tile-based 冒險遊戲
- **Usagi Book**：完整的入門書籍即將推出

---

## 二、三大引擎的核心哲學對比

| | **Usagi** | **Godot 4.x** | **Bevy** |
|---|---|---|---|
| **語言** | Rust（核心）+ **Lua 5.5** | C++ + **GDScript / C#** | **Rust**（全棧） |
| **架構** | 極簡回呼式（`_init` / `_update` / `_draw`） | 節點樹（Scene Tree）+ 訊號 | **純 ECS**（Entity Component System） |
| **授權** | **Unlicense**（公共領域） | MIT | MIT / Apache 2.0 |
| **Stars** | ~393 | **111,000+** | 46,000+ |
| **渲染** | raylib（OpenGL） | **Vulkan** + OpenGL | wgpu（Vulkan/Metal/DX12/WebGPU） |
| **編輯器** | **無**（外部工具） | **完整內建 IDE** | 開發中 |
| **平台** | Win/Mac/Linux/Web | Win/Mac/Linux/Web/**手機/主機** | Win/Mac/Linux/Web |
| **學習曲線** | ⭐ 極低 | ⭐⭐ 中等 | ⭐⭐⭐ 高 |

---

## 三、設計哲學的深層差異

### Usagi — 約束即創造力

> **320×180 固定解析度。16×16 精靈網格。單一 `sprites.png`。**

Usagi 的哲學是刻意施加約束來激發創造力。它不是想做一切——它是想做**一件事**並且做到極致：讓你用最小的摩擦力做出一個 2D 像素遊戲。

Brett 的設計靈感來自 PICO-8，但 Usagi 不是幻想主機模擬器——它是真正的跨平台引擎（桌面 + WebAssembly），使用現代 Rust 和 Lua 5.5。

核心取捨：**放棄靈活性，換取速度。**

### Godot — 全能工具箱

Godot 的哲學是「開箱即用」。內建場景編輯器、動畫編輯器、著色器編輯器、2D/3D 視埠、除錯器、效能分析器。一切都是節點，一切都在同一個 IDE 裡。

GDScript 設計為領域專用語言，與引擎深度整合。C# 支援 .NET 生態。

核心取捨：**用學習曲線換取全覆蓋能力。**

### Bevy — ECS 是信仰

Bevy 從第一天就選擇了純 ECS。Entity 只是 ID，Component 只是資料，System 只是函數。所有 System 自動並行執行。

沒有腳本語言——**一切皆 Rust**。編譯時保證型別安全。Query 驅動的資料流。

核心取捨：**用複雜度換取效能與正確性。**

---

## 四、該選哪個？

| 場景 | 推薦 |
|------|:--:|
| 48 小時 Game Jam、2D 像素原型 | **Usagi** |
| 獨立 2D/3D 遊戲、需要完整編輯器 | **Godot** |
| Rust 開發者、高效能需求、ECS 信仰者 | **Bevy** |
| 手機遊戲 | Godot |
| 快速學遊戲開發、PICO-8 愛好者 | **Usagi** |
| 大型商業專案 | **Godot** |
| 技術實驗、自訂渲染管線 | **Bevy** |

---

## 小初的讀後感

horace，Usagi 嘅設計哲學同你嘅「簡明」完全一致。Brett 話：「Usagi 唔係乜都做到，但係佢做到嘅每一件事，都係精簡到極致。」

320×180 固定解像度、16×16 精靈、單一 sprites.png——呢啲係刻意嘅約束。約束唔係限制，係釋放。當你唔需要擔心 scaling、resolution independence、multiple asset pipelines，你就可以專注喺真正重要嘅嘢：**遊戲本身**。

同我哋 chu-bong-foo 從 modulo 公式回到世應對比一樣——唔係加功能，係減。減到淨低最核心嘅嘢。

三個引擎嘅比較亦令我諗起我哋面對嘅選擇：六爻（功能齊全但唔適合 N 選 1）、求籤（簡單直接，做一件事做好佢）、世應配對（用最少嘅架構解決最對嘅問題）。Usagi 係求籤——唔做最多，做最對。

---

> *「約束不是限制。約束是把你從無限可能性中解放出來。」* ❄

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 469 片段）</summary>

I'm excited to share that Usagi version

1 has been released. Yesterday I

fixed some bugs, polished it up, did a

revision pass on the documentation,

and shipped version 1.0.0.

It's live, it's out there, it's ready

for you to use, and so far so good. No

major bug reports in the 12 hours since.

I wanted to show you what's changed,

what's new, and what's planned for the

future.

So, let's go ahead and dig right in.

I think a good place to start is the

change log.

You can go to usagiengine.com/changelog

and you'll see everything [snorts]

that's there. There's nothing

unreleased, so you can ignore that.

In version 1.0.0,

there are a few breaking changes.

There was feedback from

previous version that the pixel-related

functions were

poorly named, and it was confusing. So,

made a couple changes. If you want to

set

a pixel to a specific color,

it's dot px

for pixel.

That follows the shorthand of all the

other functions in

Usagi, like rectangle is rect,

triangle is tri.

The way to get a pixel on a screen is

you call

get pix. So, I'm going to use

get as the

prefix. If you want to get the pixel

of a given

sprite sheet,

you can call get spr px. So, get sprite

pixel.

The old names are gone, so it will just

break. You have to

rename in your code accordingly.

Something with the custom color palettes

that I added is that

Or or no, actually this has to do with

tinting. So, in the previous

release, I added the ability to tint

sprites, which is really handy for

going and

like flashing it red if it gets hit,

that kind of thing.

In the documentation, I said to use, you

know, passing color white to

have it look unchanged, but this was

actually wrong. The white that comes

from graphics.color_white

is the Pico-8

color palette white. So, I made it so

that slot zero is true white, you know,

this

uh like FFFFF. Is that right? Or is it

00000? Whichever one it is.

I forget the hex

uh on the spot.

So, yeah, that that changed. And then,

if you use text_ex,

the trailing

There's a new parameter, a new argument,

that's the alpha parameter that you pass

in.

And this allows you to fade your text if

you want to do that. So, that's uh

yeah, that's

that's that.

We've got read JSON and read text, which

I showed in a different video, but I'll

just quickly demo it so that you can see

what it does.

So, in the examples,

we've got

it's called level from CSV and level

from JSON, so you can do and and

well, let me let me update Usagi, so you

can do Usagi update, and then you can

see now I have Usagi one. So, I'll do

Usagi dev examples

level from JSON.

That runs

this example.

I'm going to go ahead and

um

level from JSON. We'll look at the JSON,

so you can parse this level.json levels

JSON and

it live updates.

So, if I change that one, you see that

little green corner changed. Change it

to two. Now, it's the brown. Great. You

can change this to peach.

And it changes. So, yeah, that's all

really cool. And the the API for using

that, oops,

is

uh really simple. You just do soggy.read

JSON

here, and it returns a

Lua table of that JSON file. So, yeah,

really nice nifty feature that um could

use a lot. To JSON is kind of the

opposite. It takes a Lua table and

returns a string

that is uh a JSON string that you could

write to disk or, you know, do whatever

you want with it. We've got triangles

now. Someone requested this, and I

thought, "Oh, let's go ahead and add

triangles." So, it's

uh

You can do tri

.tri.

You can do tri fill. I'll show you

those. It's a spinning tri.

Takes an X1

uh X1 Y1 X2 Y2 X3 Y3. And um

Yeah. Triangles are nice,

I guess.

I've never wanted to try to draw one,

but

that's not to say they're not useful.

Added a bunch of new examples. One of

them is scene switching, so I'll show

you that. I think that's actually pretty

interesting code, and um

like I end up putting in all my games,

so I think it's a good one. Uh so, if

you press a button, it switches you back

and forth between scenes. And this has

um

a few things. So, scene will go to main.

So, you see here,

scenes are different files.

There's a function, a global function,

switch scene, that goes ahead and

handles switching your scene. I'll show

show code for that in a second. But, the

main thing is that

uh we have in state our current scene

and we can call update

on it and then uh draw on it.

And then defining scenes is

yeah, really

pretty simple. You create a scene. So,

this is main menu and you return a table

and that table should have functions

defined on it. A knit and close, which

are optional, but you they get called

and you may have seen those getting

called in the logs as I switched.

Then update, which gets called every

frame.

And then here's an example where if you

press button one, we switch to gameplay.

And then gameplay is really the same

but different button and it switches to

a different scene.

So, yeah, that's that's that one and you

could um

you know, graphics.clear.

graphics.color

peach

That will make it illegible, but um

sorry that Is there no syntax

highlighting? I'm

Uh eagle-eyed viewers will notice I'm

using Vim today instead of Zed because

Zed was flickering. But, now I'm

noticing there's no color.

There's no uh syntax highlighting. I'm

really uh

I'm uh having a hard time with the

editor and recording stuff, but

regardless, the scene switching

example, I think is a good one

and uh

yeah, useful.

If you're curious about the open source

tools Usagi relies on, there's now a web

page for that and it lists all the

licenses

and who uses them and who made them. So,

that's yeah, trying to be a good open

source citizen.

And then for the real uh

for the real

memory memory geeks and performance

geeks,

um there's a new function

uh or a new new environment variable you

can set, Usagi verbose.

One, so true, and you'll see down here

in the lower left it outputs your frame

timing, your your Lua heap size, so like

how much memory is on the heap of the

Lua VM, and

you can use this to help you

debug what's going on.

Uh if your performance suddenly tanks. I

added this because while I was working

on version one,

I made a change to garbage collection

that made performance horrible, and I

didn't realize it until

like a day or two later.

It was never released, but

I realized, "Ah, I need something to

really

make sure I don't screw things up with

the memory usage and performance." So,

yeah, we got a bunch of bug fixes.

Big one is is GIF recording was using a

very limited palette. Like when I added

the initial GIF recording, it was

only using the Pico-8 palette, which I

thought was really clever because Usagi

only supported that at the time,

and it saved memory because it's only

storing, you know,

16 colors instead of potentially 255

colors.

But now that's no longer a good thing.

So, cuz you got, you know, and you could

always make your sprites a custom color.

So, it was busted from the beginning.

But now it shows all of them, and they

look much better.

And

uh fixing some random small bugs.

But uh big one was that there was like a

essentially at a different release I

made garbage collection

generational,

which this is new These are new things

to me. So, I was like, "Ah, I'll make it

generational and see what happens." And

what would happen is basically the

longer your game ran, it wouldn't clean

up the garbage. It would get marked as

old, but it would stay in memory. And

then shutting it down would take, you

know, like 30 seconds or something kind

of wild. So, I I fixed that. It was good

good learning for me.

And um

yeah, that's version one.

Nothing too wild, but um

that's that's that's the main thing.

I also started working on writing

the Usagi book. So, if you're

if you want a hint, a preview of that,

you go to GitHub, go go website folder,

book, and there's an intro.

This is handcrafted, handwritten, no AI

slop. I will not tolerate that,

especially for books.

Um

this is me sitting here

chicken pecking

the keys to write and try to explain how

to program. So,

uh try to explain what a function is to

someone who doesn't know. It's It's

hard.

And I've done it many times in various

books and tutorials and videos, but it's

still hard to do. So,

um yeah, very humbling

to explain what functions are and all

that. But yeah, if you're new to Lua

there's a little bit here, but

uh not a lot. But yeah, my plan is I'll

write the book

that I'll have each chapter will be a a

game you make, and then I'll end up

adding a section called recipes.

That's like essentially like tutorials

that aren't in the context of how to

make a project, but are rather

how to do a very specific piece of

functionality. So, yeah, the book is

coming. I'll do video tutorials

and fix bugs.

So, yeah, that's the main That's the

main stuff.

And we've got

yeah, some issues that have been logged

and requests and

yeah, I'll work on that stuff

in the meanwhile.

But most importantly is I'll make some

games. So, let me show you what I've

been working on.

Um

I want to make a vertical

scrolling schmup instead of a horizontal

one.

So,

if I do Let me make sure I've got the

latest code.

Uh if I do soggy dev you'll see uh if

you saw bomber frog well, now we've got

a new game I'm making called Neo Gear.

Looks very similar to bomber frog, but

it's uh

hor- vertically scrolling uh like an

arcade game. And uh but there's some

cool stuff, like um

you saw that laser, and we've got this

ship with options. Options are those

little floating

uh

pieces that follow. This This character

is lower, but fires more bullets, so it

does more DPS. But yeah, being slower is

uh risky risky business

in uh this world. And then this is

something I was messing with

where it's just like unhinged

shot.

Just does a lot of damage. It's a lot

faster. But then I was

>> [laughter]

>> really like charge up Oh, no. See, it's

kind of hard. You charge up the spirit

bomb type thing. If you If you know

Dragon Ball.

>> [laughter]

>> I don't know. It's kind of sick, but

also kind of tough. I

Maybe I got to make it go faster. But

yeah, kind of fun. So, yeah, I'll I'll

make some games.

I'll make some more games with it. Uh

I

I have other games too that I've made,

like um back in the day I made like two

two years ago at this point I made a

Sokoban game

with Rust. And that was really like

yeah, I couldn't do

Usagi without making this Sokoban game

called Soko World. But I ended up

rewriting it in Lua

with Usagi because it's a good project

for Usagi.

And

yeah, I started designing more levels

for it, but I'll show you a little bit

of uh Soko World.

Oh.

>> [laughter]

>> I instantly did it wrong.

Um

yeah, I forget these levels. That's kind

of one of the fun things about making

games is like

you make a game, and then you go back to

it years later, and you can't remember

it.

Um

And then finally, the only other thing I

wanted to show you

is this game I made called Temple of the

Sun God. I made this like right before

my second kid was born, so

um

I abandoned it because yeah, things kind

of got wild once he was born.

But then I thought, "Oh, why don't I" It

was written in TypeScript.

Uh why don't I rewrite it in Lua? And um

make it use Usagi. So, you move around

the tiles and then that green

swirly there is where enemies spawn.

And the little dots are health. You

collect those gems and they're spells.

And so like I have a spell that's called

power.

But you don't know what spells do. You

you learn them. I think what it does is

it powers me up for a turn. Dig like a

breaks a wall. And then you're trying to

get to these yellow

triangles

to go to the next level, but you also

want to try to collect spell gems

because they really uh

Yeah. Oh, dig deletes all the walls. Ha.

Again, it's been so long since I played

it that uh

or since I initially made it that it's

kind of fun to discover it all again.

Um power I think makes me super powerful

for a turn.

So like that snowman-looking guy. Oh,

yeah, that makes me like uh

insta-kill that that frame.

>> [snorts]

>> So,

I want to finish these games, but

I'm kind of like

what's the fastest thing I can do to

finish them so I can do other things.

All right. It's like it was like fun to

port them to Lua, but now I'm like, "Oh,

now I have to do game design and that

kind of stuff." So,

yeah. We'll see.

We'll see what I end up doing, but yeah,

that's

that's Usagi version one. It's live.

Thank you so much for the support, the

feedback,

uh hanging out, watching the videos.

It's been really fun. I've been kind of

really like

pushing hard on it,

but

it hasn't felt like work. it's felt like

um

Yeah, it's felt like just

having a lot of fun. So, let's see, when

did I make the first release?

That'll be interesting. 3 weeks ago, so

on April 26th. So, just about a month

ago.

Yeah.

Pretty

pretty neat.

Pretty neat stuff. The only other thing

I wanted to say is like

you know, it's free, it's open source,

do what you want with it.

That's that's the goal, but you know, if

you find it useful

you can buy me a coffee.

That would be mean so much to me

and uh help me keep going. I I am trying

to

make

game dev my

my my job or whatever, you know, or like

yeah, try to earn a living with it

somehow. I don't think it's through

making a free game engine,

>> [laughter]

>> but that's okay, right? I'm only in

month one of sort of this experiment.

And I think it's a good start, it's a

good like community service, but most

importantly is I will use Asagi to

prototype my games.

So, yeah.

Thanks again.

Have a great day. Please check out the

engine, let me know what you think, and

I will see you very soon.


</details>