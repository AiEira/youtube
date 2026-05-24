# Agents that remember — Anthropic Cloud Manage Agents 的記憶與「做夢」系統

> 來源：[YouTube](https://www.youtube.com/watch?v=geUv4CjPpxI)
> 講者：Kevin（Anthropic 工程師）
> 長度：約 28 分鐘
> 語言：英文
> 整理：AiEira

---

## 核心摘要

這是 Anthropic 在 Cloud with Claude 大會上的工作坊，由工程師 Kevin 主講，介紹 Cloud Manage Agents 平台新推出的兩個功能：**Memory Stores**（記憶存儲）和 **Dreaming**（做夢）。

核心問題：**大多數 AI agent 的 session 是隔離的**——agent 不會記得上一個 session 學到的東西，也不會把資訊傳遞給未來的 session。這極大限制了 agent 在真實世界工作流中的實用性。

解決方案是一個三層可組合架構：

```
Sessions（隔離的單次對話）
    ↓ 讀寫
Memory Stores（跨 session 的持久記憶）
    ↓ 非同步處理
Dreaming（多 agent 後台整理、豐富、去重）
```

---

## 三層架構詳解

### Layer 1: Memory Store

Memory store 是一個**持久化的檔案系統**，作為 resource 附加到 session 上。Agent 可以透過工具（bash、grep、檔案讀寫）來讀取和寫入記憶。

關鍵設計決策：

- **檔案系統介面**：Anthropic 刻意將記憶存儲實現為檔案系統而非向量資料庫——因為檔案系統對 Claude 來說是極其強大的介面。它可以用 bash 探索目錄、用 grep 搜尋關鍵字、讀取檔案、做大量操作
- **多存儲支援**：可以創建任意數量的 memory store，不受限於一個組織。可以 per-user、per-workspace 等
- **讀寫權限控制**：每個 session 可以設定 memory store 的存取權限——read-write 或 read-only
- **版本控制**：每個 memory file 都有版本歷史，任何變更都會產生新版本
- **引導提示（prompt parameter）**：可以在掛載 memory store 時提供提示，引導 agent 聚焦於特定類型的記憶（例如「記住投資決策相關的資訊」）
- **人機協作**：console UI 提供檔案系統檢視器，可以手動編輯記憶、添加新記憶——人工審查和修正

### Layer 2: Dreaming（做夢）

Dreaming 是一個**非同步的多 agent 批次處理系統**。它的工作是：

1. **Fact-checking**：檢查記憶中的資訊是否正確
2. **Enriching**：補充細節——日期、特定識別符、從原始 session 中遺漏的資訊
3. **Organizing**：建立 index 檔案，按 slug 組織記憶，讓未來 agent 能快速定位所需資訊
4. **Deduplication**：合併重複資訊
5. **Staleness check**：標記或移除過時資訊

**為什麼叫 Dreaming？** 因為它在後台非同步運行——就像人類睡眠中大腦整理白天記憶的過程。

#### Dreaming 的架構

- **Orchestrator agent**：負責啟動和管理 sub-agents
- **Sub-agents**：每個輸入 session 一個 sub-agent，設計上是**窮舉式**的——逐個 session 檢查，確保不遺漏任何資訊
- **模型選擇**：可用 Claude Opus 4 或 Sonnet——Opus 品質更高，Sonnet 成本更低
- **非破壞性**：Dreaming 不會修改輸入 memory store。它會 clone 一份，寫入一個**新的 output memory store**
- **Console diff**：完成後顯示 diff，展示 dreaming 做了哪些更改
- **Token 效率**：由於大部分處理是 agentic 的，預期 ~95% cache hit rate

#### Dreaming 的效果

Dreaming 完成後的 output memory store 包含：
- **Index file**：用 slug 引用各種 memory files，讓未來 agent 可以快速判斷需要查看哪些記憶，而非做全範圍 grep
- **Event logistics**：從 session 中提取出活動日程、時間戳、與會者資訊
- **Reformatted memories**：將原始 agent 建立的記憶重新格式化——添加 slug、描述、metadata、更多細節
- **補充資訊**：加入原始 session 中 agent 當時來不及寫入、但對未來有用的細節

核心洞察：**agent 在工作時很難預測未來會需要什麼資訊。讓 dreaming 去後台補充更多細節，對未來的 agent 幫助極大。**

---

## 實戰演示

Kevin 在 CLI 和 Console UI 中展示了完整流程：

### Step 1: Baseline（無記憶）
- Session A：告訴 agent「CMA 演講的內容」
- Session B：問 agent「CMA 演講中學到了什麼？」
- 結果：agent 無法回答——sessions 是隔離的

### Step 2: 加入 Memory Store
- 創建 memory store
- Session A（掛載 memory store）：agent 自動將資訊寫入 `sessions.mmd` 檔案
- Session B（掛載相同 memory store）：agent 先用 grep 搜尋 memory store → 找到相關資訊 → 成功回答

### Step 3: Dreaming 強化
- 對 input memory store + 一組 session transcripts 執行 dreaming
- Dreaming 創建 index file、補充 event logistics、重新格式化原始記憶
- 新 session（使用 dreaming output memory store）：agent 先讀 index → 快速定位 → 獲得更豐富的資訊（含時間戳、資源連結、完整日程）

---

## 實用考量

| 考量 | 詳情 |
|------|------|
| **Token 成本** | Dreaming 設計上是 exhaustive 的，消耗大量 tokens。但 ~95% cache hit rate 大幅降低成本。未來可能提供類似 batch API 的 50% 折扣排程 |
| **成本控制** | 可切換模型（Opus → Sonnet）、引導 prompt、token 預算限制 |
| **人工審查** | Console UI 支援人類查看 dreaming 輸出、手動修正錯誤 |
| **退役舊 store** | 對 dreaming 輸出滿意後，可退休舊 memory store（不影響歷史 sessions） |

---

## 與 horace 的關聯

這套三層架構和你的 Hermes 系統有驚人的相似性：

- **Sessions** ↔ Telegram 對話（每個 chat 是隔離的 session）
- **Memory Store** ↔ `MEMORY.md` + `USER.md`（持久記憶，agent 可讀寫）
- **Dreaming** ↔ 你在規劃的「dreaming」功能——非同步整理和優化記憶

Anthropic 選擇**檔案系統**而非向量資料庫作為記憶介面的理由，和你的「一切是純文字」哲學完全一致。

---

## 全文逐字稿

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 712 片段）</summary>

Hello everyone. Thank you all for

joining us today. Um, my name is Kevin.

Uh, I'm an engineer here at Anthropic.

And today we'll be learning about how to

build agents that remember. Um so uh

today we're going to talk a little bit

about the base case with agents today uh

which is that they are isolated and this

kind of limits their usefulness in a lot

of real world workflows. Uh we'll look

at how we can actually solve this

problem uh with our new agent memory

stores feature that we've launched. Uh

this will give agents access to a live

memory store that they can read and

write to over multiple sessions. And

then we'll look at how we can improve

these memory stores over time uh using a

new feature that we call dreaming. Uh

and then finally we'll get to see how

all of this ties together with both our

CLI and also our awesome console

interface.

Um so in the previous uh workshops I

think we've learned a little bit about

how cloud manage agents has these

concepts called an agent environment and

a session. Uh in this workshop we're

going to add two additional concepts

here. The first one here is a memory

store. Uh so a memory store is a

persistent file system-l like store that

gives uh that attaches as a resource to

sessions that you create and it gives

agents access to uh it gives agents the

ability to read and write information

across sessions.

A dream uh is what is a asynchronous job

that runs in the background. uh it looks

over an input memory store and a bunch

of your previous sessions that are

represented as transcripts and then we

run a harness over them to distill new

information that maybe the original

agents missed. We do things like

factchecking. Uh we also organize and

consolidate and duplicate information so

that your memory stores don't grow

unbounded over time.

So uh also in case anyone in this room

has not already uh downloaded the

workshop repository you'll need for this

uh here is the URL. I'll give a few

seconds for folks to just grab that.

Okay. Um so let's kind of like talk a

little bit about the problem today. So

when you when you create agents on cloud

manage agents today and sessions um most

of the time you're creating one session

at a time and these are isolated right?

the agent doesn't remember information

from the past and it doesn't transfer

information to future sessions. Um so I

want to kind of like take us through

this this base case today. Uh so if I

switch over to my computer

um I'm in our workshop repository here.

Uh hopefully everyone can see this uh in

the back but I've just run the bootstrap

script that we've uh included in the

repository. Uh and what this has done is

basically created uh some seed

information for us. We have an agent uh

we have an environment and we have a few

like previous sessions that talk about

things like the keynotes uh from day one

as well as you know uh a previous

workshop. And so uh what I'm going to do

from here is actually go ahead and start

walking through this guide with you

guys. Feel free to follow along your

computers. I'll be using the CLI and

then also showing kind of the console

interface uh for each of these steps. So

first we're going to create a session

that basically tells it some some new

information. Uh so I'm going to copy

this command here.

And as you can see we are creating a

session with the agents that we've

created before uh with the environment

ID. Uh and we've given a title here of

just like write test with no memory.

Great. Uh so now that we created the

session uh I'm going to quickly switch

over to my console here. Um and you'll

see that

just move this over. You'll see that the

session shows up in console. Uh it

doesn't it has a status of idle. Nothing

running yet. Uh so then we're going to

switch back and then I'm going to send

this session some new information. Uh so

once I copy this

and what I'm doing here is sending a

first user message here with information

about the CMA talk yesterday. uh naming

a few keywords like multi- aent

orchestration multi- aent orchestration

outcomes in memory and I've also just

given it this URL you know example that

I took notes and uploaded them here.

So, if I switch back over to my console,

uh, we should see this event pop up.

And what we sort of expect the the agent

or the model will do here is it'll just

respond and say like, great, thanks for

the information. Not sure what else you

want me to do here. Uh, so we'll give it

a sec and maybe folks to catch up.

See, we get a little refresh.

Ah, sorry. Yeah. So, it looks like the

model responded here.

Just collapse this. Yeah, it's basically

saying, okay, great. Thanks for telling

me this information. Uh, so then if we

go,

>> sorry,

>> uh, this is using, I believe, sonnet,

the agent that was created at the

beginning.

Yeah. Um,

cool. So, if I go back here, uh, to my

workshop here, we're going to create

basically a second section that's kind

of the retest. So, I'll go through these

steps a little bit faster.

Uh, and then again I'll send it a

message here. That's this time I'm going

to ask it for information about the

stuff that I just told it.

And if I go back to our console here and

check out the other session that should

have been created,

we would expect the agent to basically

um say something like, "Yeah, I don't

really have access to this information.

I can help you in these various ways."

Great. So that's effectively the base

case today. Uh so if I go back to the

slides

real quick, this is a quick recap of

what we did. We told it something, asked

another session about it later. No

information is transferred between the

sessions.

So how do we solve this problem? Right?

Um just like in humans, uh we've

introduced the sort of concept of

memory. And again, a memory store here

in the cloud manage agents platform is a

file system like store. uh under the

hood you can or you can create as many

memory stores as you like here. So you

don't have to necessarily restrict a

memory store to one organization. You

could create it per user, per workspace,

etc. It's up to you to kind of define

what the boundaries of the memory store

are. Uh and then under the hood, this

memory store gets attached as a file

system to the the session container and

the model has tools to read and write to

it. Uh the actual interesting thing here

is that we've actually you mounted it as

a file system because it's such a

powerful interface for the model. uh you

can use things like bash to like uh like

explore the file system. It can use GP

to kind of search for keywords. It can

also read files and do a bunch of like

really powerful things um that make it

much more useful for the agent.

Um so I'll switch back to my computer

here and we'll walk through kind of how

to create a memory store.

Um so first things first is actually

creating it. So I'm going to copy this

uh command here. Feel free again to

follow along on your computers. Um, and

the kind of parameters that you need

here are mainly just like a name. Uh, so

I'm calling mine CWC memory. You can

give it a quick description. Uh, and

then I'll show you also in console later

that there are two additional parameters

that you can set here. But let me just

follow through with a simple example.

Uh, once I create this memory store, you

can actually see it in console under

manage agents memory stores.

and you'll see that it's active. Uh you

can actually click into it and view uh

essentially a file system viewer of

what's currently in it. Of course,

there's nothing in it right now.

Additionally, uh we offer functionality

uh we offer the ability for you to like

add manually add memories. So you can

create like a file under a specific

path, add some content, etc.

If I go back just a brief second and

talk about uh creating a new memory

store, there's actually two sort of

additional parameters that you can uh

set on the memory store uh when we

actually mount it. So if I go back to

the repository here, um the next step

once you create a memory store is to

actually use it with your sessions. So

I'm going to again copy a few of these

commands. So the first one here is

basically just giving us the shape that

we need to pass the sessions API

request. I'll paste it in our terminal

here so we can see it better.

Um so again the memory store here you

just pass in a memory store ID. Uh and

you can also give it a prompt around uh

that will steer the agent to read and

write specific information. So you might

want it to focus on maybe like a

specific um link or a specific like area

of focus on. Let's say you're making

making like a investment agent, right?

And you wanted to focus on specific

things to remember future. Uh so you can

do that with a prompt parameter.

Additionally, there is an access field

uh that defaults to read or write. Um

you can change that to read only which

will make it so that the session and the

agent will only be able to read from

that memory store. It cannot update it.

So once I run this um you'll see I have

created a new session in console.

Uh, and this time it'll have a memory

store attached.

And then if I send an event here, this

time we'll just basically repeat the

test that we did just before. So let me

grab this

again. Same text as before. We're

telling it new information. Uh, and

hopefully we'll be able to observe a

different behavior this time.

Yeah. So clicking into uh if you click

into the session details, you'll see the

the information that I just gave it.

And now the model is like first looking

at memory to see okay, was there

anything that like I need to remember

for this conversation.

Uh and now it's going to actually like

of course there's nothing in our memory

store. So now what it's going to do is

actually save the content that I told it

to that memory store directly. and it

saved it under this like sessions.mmd

file and it's great telling me that uh

what it did.

Um, so then if I go back and do that

same test that we did before, this time

I'll just copy both.

Sorry,

again where this time we're going to

create a new session with the same

memory store that we were just using.

Uh, and we will send it an event here

asking it what are the things that it

found or it learned from the CMA talk.

Once again, going back to our console

UI, we can see the recall test running.

And as we would expect, the model is now

first looking at its memory store to see

if there's any information. And again,

it's now using GP to find uh any sort of

keywords here. It's looking for CMA. And

great, it found like a lot of

information that we just told it from

the from a previous session. And now

it's able to answer my question, right?

And this is like of course a very simple

example, but this illustrates kind of

the power of of memory. And this is like

something that was kind of difficult to

do before, right?

I'll give quick pause in case anyone's

struggling.

Um, okay, great. So what what else kind

of can can you do with a memory store

here? Well, we actually offer uh

additional sort of endpoints that allow

you to manually inspect the store

itself. Uh so I'll use the CLI here, but

for instance, you can list all of the

memory files that are in the memory

store.

We can like do that. Um there's also

each uh memory a memory stores memory

files in a memory store are also

versioned. Uh so anytime you make a

change to a file, etc., there's a new

version that's created and we offer a

set of endpoints for that.

And then I can also kind of take you

through the memory store UI.

So each memory store you create again is

here. And if we go back to our like kind

of file system viewer, you can actually

see the files that it created. Uh there

will be like a directory structure here.

If Claude is creating kind of

subdirectories to organize memory files,

you can actually edit these memory files

directly if you wanted to. So for

instance, if Claude wrote something u

that was incorrect or maybe you just

wanted to add more information, you can

do that. And again, as we saw before,

you can add additional memories to a

memory store.

Uh okay, so I'm going to go back to the

slides real quick.

And as we just talked about, uh this is

how you create a memory store and then

mount it on a session that you want to

use it on. Again, it's up to you to kind

of decide which of your sessions will

use memory, which ones will not.

Uh, we also saw how you can like list

memories and see what's currently in a

memory store.

And let's move on to talk a little bit

about dreaming. Now, um, so when you

have agents that are reading and writing

to this memory store over time, uh,

we've noticed that often times it can

start just kind of dumping information

to that memory store. So it'll start

writing maybe every every task you ask

it to do maybe records information right

and over time your memory store is going

to grow right and there's no real

process uh before that would allow you

to sort of organize that memory maybe

check to see if anything was stale and

and consolidate any duplicates right and

so this is where dreaming comes in uh

dreaming is a is a batch process that

runs again asynchronously you launch it

uh using uh our API or through console

and it'll run a a new dreaming harness

that we built that is a multi- aent

setup. It will look over each of the

input sessions that you've given it. So

you specify like an input memory store

that you want it to dream over along

with like a group of transcripts that

you think might help or enrich that

memory store. It'll look through each

one, do again factchecking, enriching

with additional details, maybe dates,

specific identifiers. Uh and then it

will also organize those memory files

and see if there's any duplicates,

anything that can help uh fix so that

when you and it'll produce an output

memory store such that in the future

when you attach that output to

additional sessions, it will hopefully

increase efficiency uh efficiency of

like information retrieval. It also

hopefully increase the intelligence of

the agent.

So let's take a look at how this works.

Again, switch back to my computer and

we'll walk through it together.

Uh so what you to to get get started

with dreaming basically you'll need to

actually create the dream job

and I'll go through a little bit of the

parameters here. So the model uh here

that we're choosing is cloud opus 47.

You can choose between opus 47 or sonnet

46 depending on kind of the level of

quality you want as well as maybe like

token costs. Uh it takes in two inputs.

So you'll need the memory store that you

want it to dream over as well as a list

of session ids. Uh so this is up to you

to decide. You can you know maybe dream

over daily and dream over maybe like 10

sessions at a time or 20, right? It

could go you know all the way up to like

a 100. We're also looking to scale it

further uh beyond that. Uh optionally

you can also provide the dream job some

additional instructions that you might

add. So we provide it with a default

prompt that does a bunch of things. If

you wanted dreaming to for instance

specifically fix a few things like maybe

you're working in a domain that requires

like very specific details right you

might ask a dream job to really focus on

hey make sure you back fill these

details so I remember for the future

right you can also get it to you can

also steer it to maybe like organize

files a bit more like I want this

specific structure in my memory store

please do that uh so let's actually go

and run this command here

great we'll get we'll get back a dream

ID and then once Again, I'll go back to

our console here. And so dreams are

under again manage agents dreams.

And once I create the dream job, it'll

start p it'll start with pending, but

it'll start running pretty shortly

after. And you can actually see the

status of the job both in console and

through the API. I'll show both. But in

console here, you'll see the input

memory store as well as a token count.

And generally like uh dream job can take

you know depending on the size or the

number of transcripts that you give it.

It could take anywhere from you know a

couple minutes to hours at a time. Uh

and that's really the benefit of doing

it asynchronously right like this is not

something that you want to do live while

your agents are working. And we'll just

give it a a minute here to to run. As

you can see as it's running as agents or

as the harness itself is running we're

updating the token count for you so you

can track its progress over time. The

other really cool thing here is that uh

dreaming is actually built directly on

top of cloud manage agents primitives.

Uh so you can actually see that we are

creating a session for the dream job

itself and you can actually click into

it see exactly what the dream is doing.

Uh this offers a really nice amount of

like observability and so you can like

diagnose issues potentially. Um and so

you can see the prompt that we give it.

Uh there's a lot of details here that

I'll kind of that you can explore on

your own time, but the under the hood,

the the dreaming harness itself is

launching sub agents to look over all of

the transits that you've given it. And

each sub agent essentially has a system

prompt that tells it what to do. Look

over and the orchestrator is responsible

for just like making sure all the agents

are running and kicking them off as they

go.

Uh so we'll give it another minute for

to let this run.

Uh, another thing to call out here is

that while uh we don't actually touch

the input memory store at all that you

create. So this is a non-destructive

process. What we actually do is we will

clone your input memory store uh into

what's called an output memory store.

And the dream job will be writing

basically to a new memory store such

that any edits that are made are

non-destructive. And then we'll see down

the line how you can utilize this output

memory store in your future sessions.

Generally this takes about a minute or

so depending on uh how fast the job

runs.

Uh, one other thing is that you'll see

that I'm sort of checking on the job

periodically uh as it's running in

console. Uh, when you do this

programmatically, we offer an API that

allows you to just essentially query uh

for the dream job and it'll have a

status uh so you can pull for the

status. Great. So, looks like it just

completed. Um and the cool thing here is

that in console we actually show you a

diff of what it did. Uh so you can see

dreaming here it created an index file.

Uh this index file has sort of these

slugs that reference the various like

memory files that uh a future agent

might need. And the main goal of this is

really just that future agents uh it's a

lot more efficient to kind of look at an

index file and quickly grock like what

it needs to go look for instead of maybe

doing a a wider GP.

Additionally, it's actually adding like

additional information that was not

present in the in the first couple

sessions that I created. So, it's

creating this event logistics file. It

gives the whole schedule of code with

claude. Um, a bunch of names as well.

Uh, and again schedule for day two.

Uh, and you also see that it actually

kind of reformatted the memory file that

I created in a previous session. So this

time it is adding again a slug, a

description of the event, some

additional metadata and again adding

more details. Um and generally we find

that like uh more information actually

really does help future sessions. And if

you think about intuitively um while an

agent's working on a task currently,

it's kind of hard to predict down the

line what it might need, right? That's

just generally a harder prediction

problem. So it's actually good to kind

of write additional details down that a

future agent might remember. And

Dreaming can always like go back and

like remove stuff that is no longer

needed.

Uh and if I go to the output memory

store here, I'll just click on it.

Um again, you can see all the files that

I created. It's another good way to sort

of see what's going uh what dreaming

did. Uh and if you wanted like a human

in the loop kind of review process, this

is kind of where uh this is super

helpful. uh human can kind of go in and

see if the dreaming harness made any

mistakes.

Okay, great. Um just going to switch

back to the slides real quick because I

want to show a diagram.

Um

yeah, so again under the hood, this is

sort of what how dreaming works, right?

This is a multi- aent harness. uh we

have an orchestrator that is mainly

responsible for spinning up sub aents

and again we spawn one sub aent per

input session that you give it. Um and

kind of the the reasons behind this are

we actually kind of want dreaming to be

exhaustive by design. Uh if you give it

100 trans like claude is looking over

all the information to make sure it's

not missing anything, right? Um

great. So now me let me switch back to

my computer again.

Uh and this time I'm going to actually

like walk through how we might use this

in a future session.

So uh once the dream uh is done, you can

actually go and grab the output memory

store using this. So again, we're we're

just retrieving the dream resource uh

with the dream ID that we created and

then uh querying or just grabbing the

the JSON memory store ID.

Great. So this is the memory store and

again you can look through what memories

it created.

Uh and now we'll do this sort of test

again that we did before with the two

sessions. So I will create a new session

here

and you'll notice that this is now using

the output memory store from dreaming.

Once again we'll send it an event here.

We're just asking it what sessions I

attended, what resources do I have links

for, and what follow-ups I flag.

Once again, going back to the console,

it's really a great way to, you know,

visualize what's going on here.

And you'll see that this time when it's

reading from memory, you'll see all the

stuff that Dreaming did, right? So, the

index, the event logistics,

and it's now reading kind of it's

starting to read the index first.

Okay, great. Now it knows I'm going to

go straight to the sessions file.

It's being a little exhaustive here.

Just checking for, you know, event

logistics.

Okay, great. Let's see what it came up

with. So, as you can see, I I'd have to

go back and show you the the previous

session, but this time I think there's a

lot actually a lot more information

here. So, it gave me a recap of all the

sessions I I attended. Uh, it's giving

me timestamps now about like all the

sessions that were that were planned for

day two as well as like the resource

links, right? I think this kind of

showcases again like how dreaming can

really enrich information that is

transferred between sessions.

And then optionally um at the end you

know if you're really happy with the

output memory store here you can go

ahead and actually retire the old memory

store. Um so this won't affect like your

previous sessions. It just means that

you no long it will it will keep you the

number of memory stores in your

organization down to a reasonable level.

Um great. So I'm going to kind of switch

back to the slides here

and talk a little bit how you can kind

of view sessions, memory stores, and

dreaming as three composable layers

here, right? If you think of a session

as a as an isolated instance of an agent

running, uh it's one usually typically

one conversation thread, typically

ephemeral, right? A memory store

augments that. So now you can connect

information between your sessions across

multiple sessions, right? And then

finally with dreaming uh you're now

organizing, enriching and improving your

memory stores over time so that as you

scale up the number of sessions you have

and as you scale up the information that

it's being processed through those

sessions, your memory stays at a

reasonable level. It's manageable. It

doesn't blow up. Also, it checks for

things like staleness to make sure all

the information is most is up to date,

right? I wanted to highlight some of the

maybe good questions that I got from the

audience here. So one of them was around

uh generally like sort of what is the

like token usage of this feature like?

Um so as I said before like I think by

design we actually do want it to be

exhaustive. So we do expect it to use a

lot of tokens. Um the the nice thing

here is that because most of the

processing is agentic uh most of the

tokens are actually cached. So we're

expecting like about a 95% cash rate

cash hit rate on um like most dream

sessions right and additionally we are

exploring like other ways of offering

this at lower costs to you. So uh

example of this would be like similar to

our batch API we could offer things at a

50% discount by scheduling it at

different times. Uh other additional

like token usage controls include like

switching the model, steering the prompt

a little bit more, also providing more

like just general budgeting of tokens.

>> Um

great. Um so I think we're just about

winding down. So I'm going to quickly

kind of go over again for the folks

remaining in the room uh like what we

went over today. Uh so again we talked

about the problem that most agents face

today which is like how do you remember

information across sessions? I think

this is a pretty like wellestablished

kind of problem now. And we talked about

how memory is kind of the first step to

addressing this right you give agents

access to something where they can dump

the information read from it etc. Uh but

we also saw how this creates a problem

where memory stores are can grow

unbounded over time. They can grow

disorganized information can grow stale

etc. And then we saw how dreaming can be

used as a way to mitigate this problem.

Right? So we we take another set of

agents that their entire job is to

improve that memory store for future

use.

Um and with that I'd like to thank

everyone for for coming to today's

workshop. Um hopefully it was helpful

and hopefully by the end you'll learn

how to uh you'll know how to like

integrate maybe memory into your own use

cases.


</details>