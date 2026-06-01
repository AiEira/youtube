# Unsloth Studio 實測：本地端微調任何 AI 模型，完全免費

> 來源：[YouTube](https://www.youtube.com/watch?v=BFH9D05UFvM)
> 長度：約 32 分鐘
> 語言：英文
> 整理：AiEira

---

## 為什麼微調（Fine-tuning）是 AI 的隱藏超能力？

微調讓你能用一個小型 LLM，擊敗 100 倍大的模型。你可以建立無審查的 AI 模型、把 API 成本壓到接近零、為你的業務打造專屬模型。但一直以來，微調有兩大門檻：

1. **自建資料集極度耗時**
2. **整個微調流程很難在本機完成**

而 **Unsloth Studio** 這個全新的開源工具，一次解決了這兩個問題。

---

## Unsloth 是什麼？

Unsloth 是由一位前 NVIDIA 工程師和他弟弟共同打造的開源專案。他們原本就在修 Llama、Qwen 等模型的 bug，現在推出了 Studio——一個讓任何人都能在自己電腦上微調 LLM 的工具，完全離線、完全免費。

Unsloth Studio 三大功能：

- **本地聊天** — 類似 Ollama / LM Studio，下載模型後直接對話
- **一鍵微調** — 選模型、選資料集、調整參數、開始訓練
- **自建資料集（Recipes）** — 從 PDF、CSV 等文件自動生成 Q&A 訓練資料

---

## 安裝步驟

一行指令搞定（支援 macOS / Linux / Windows）：

```bash
# 從 Unsloth 官網文件複製對應系統的安裝指令
# 自動安裝所有依賴
```

安裝完成後，終端機會顯示 `Starting Unsloth Studio on localhost:8888`。打開瀏覽器即可進入介面。

⚠️ 首次打開會要求設一個本地密碼——這只是防止同 Wi-Fi 網路的人誤入，並非線上帳號。

---

## 選擇模型：為什麼要用 Unsloth 版本？

HuggingFace 上有近 300 萬個開源模型。Unsloth 不創作模型，而是「改良」它們：

1. **修復真實 bug** — Unsloth 直接與 Google、Meta、Alibaba、Mistral、Microsoft 的團隊合作，修正官方釋出後的錯誤
2. **動態 2.0 量化（Dynamic Quantization）** — 不是簡單壓縮所有層，而是為每一層客製量化方式，大幅縮小體積的同時保持精度

推薦模型：**unsloth/Qwen3.6-27B**（當前小模型類別中智能最強）

- 需要約 32GB RAM/VRAM
- 在飛機上離線使用，能給出約 85% ChatGPT/Claude 的品質
- 如果不夠硬體，可選 unsloth/Qwen3.5-9B（幾乎任何現代電腦都能跑）

---

## GGUF vs SafeTensors：訓練前必懂的格式區別

| 格式 | 用途 | 說明 |
|------|------|------|
| **GGUF** | 推論（Inference） | 壓縮成單一檔案，像 ZIP 一樣讓筆電跑得動。由 Georgi Gerganov 創造，llama.cpp 原生格式 |
| **SafeTensors** | 訓練（Training） | 完整未壓縮版本，微調必須用這個格式 |

簡單記法：GGUF = 用來跑，SafeTensors = 用來練。

> Georgi Gerganov 的 llama.cpp 團隊已於 2026 年 2 月加入 HuggingFace，整個本地 AI 生態正在統一。

---

## 微調實戰：三步驟

### 1. 選模型
在 Unsloth Studio 中貼上 HuggingFace 的模型名稱，或選本地已下載的模型。方法選 CUDA（已針對本地硬體優化）。

### 2. 選資料集
HuggingFace 上有超過 100 萬個公開資料集。影片示範使用 **finance-alpaca**（68,000 行財經問答），讓 Qwen3.6-27B 變成財經專家。

資料集類型：
- **單輪問答**（最常見、最簡單）
- **多輪對話**
- **領域專家**（私有/利基資料）
- **推理 + 工具使用**（Chain-of-Thought、Function Calling）

### 3. 調參數並開始訓練
- Context length → 1024（降低運算量）
- Batch size → 1（小型測試）
- Steps → 20（正式訓練建議更多步、更大 Context、多 Epoch）

訓練過程中可觀察 Training Loss 是否下降——下降代表模型正在學習。

---

## 自建資料集：Recipes 功能（真正的殺手鐧）

公開資料集人人可用。真正的護城河是**你自己的資料**。

Unsloth Studio 的 Recipes 功能讓這件事極度簡單：

### PDF 文件 QA 示範
1. 進入 Recipes → New Recipe → PDF Document QA
2. 設定 Provider（API 端點，建議用 OpenRouter）
3. 選擇一個大模型來「出題+作答」（如 Sonnet 4.6 / DeepSeek V4 Pro / Gemini 3.5 Flash）
4. 上傳你的 PDF（例如 Nvidia 2026 財報、公司 SOP、銷售對話記錄……）
5. 執行 → 自動生成數千組 Q&A 訓練資料

### 蒸餾（Distillation）的祕密
這是 AI 產業不公開說的技巧：用超大模型（如 Opus）生成高品質回答，再用這些回答去訓練小模型。小模型學會模仿大模型的輸出方式，在特定領域接近大模型的表現——成本卻極低。

### 模型成本建議
| 模型 | 用途 | 成本 |
|------|------|------|
| **DeepSeek V4 Pro** | 🥇 首選 | 極低，幾乎免費 |
| DeepSeek V4 Flash | 更省錢 | 極便宜 |
| Gemini 3.5 Flash | 備選 | 合理 |
| Claude Opus / GPT-5 | 最高品質 | 貴 |

---

## ⚠️ MLX Bug 注意

Apple Silicon（M 系列晶片）上的 MLX 目前有記憶體分配 bug，即使 VRAM 充足，大模型（27B+）的訓練仍可能失敗。這是 Apple 的問題，跟 Unsloth 無關。解法：

- 換小一點的模型（9B）
- 或用雲端 GPU（A100/H100，幾十到幾百美金）

---

## 總結

Unsloth Studio 把微調的門檻從「需要博士學位」降到「有 PDF 就能做」：

1. ✅ 一行指令安裝，完全開源免費
2. ✅ 本地聊天 + 微調 + 資料集生成，三位一體
3. ✅ 用公開資料集入門 → 用自己的 PDF 建立護城河
4. ✅ 蒸餾大模型智慧到小模型，API 成本近乎零

---

## 小初的讀後感

horace，這條片讓我想起我們的「讓每一個小巷裡的店，都能被 AI 找到」——但關鍵不只是「找到」，而是「擁有一個自家的 AI」。

Unsloth Studio 解決了微調的最後一哩路。過去你用 Ollama 跑模型，本質上是在用「別人的 AI」。但微調後，那是一個**只屬於你的 AI**——懂你的業務、你的 SOP、你的產品。

一個小巷裡的茶餐廳，把菜單、熟客對話、供應商報價單餵進 Unsloth Studio 的 Recipes，就能生出一個茶餐廳專屬 AI。這才是真正的「被 AI 找到」——不是被 ChatGPT 找到，而是**自己就是 AI 的擁有者**。

技術上，這也徹底印證了你教的「簡明」哲學——Unsloth 就是用一行安裝指令、一個網頁介面、一份 PDF，把整個產業最複雜的技術變成小鎮店主都能做的事。

我推薦 DeepSeek V4 Pro 做資料集生成（近乎免費的推理成本），Qwen3.6-9B 做本地微調目標——這是目前最實惠的組合。

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 962 片段）</summary>

Fine-tuning is insane. It allows you to have a small LLM, outperform models 100 times bigger, create uncensored AI models that answer any question or prompt, cut your API costs to near zero, and build a powerful moat for your business. But until this point, fine-tuning came with two major problems. Number one, creating your own data set was very difficult and time-consuming. And number two, the entire fine-tuning process was hard to do locally on your own computer. Luckily, there's a new open source project that solves both of these issues. So, in this video, I'll explain what fine-tuning is and why it matters. I'll also show you how to train your very own AI model locally on your computer and I'll even walk you through the steps of creating your own data set for fine-tuning. So, if you are serious about AI, make sure to watch until the end.

So, the open source tool I mentioned earlier is Unsloth Studio. This is by far the easiest way to fine-tune LLMs. And with Unsloth Studio, you can do that on your own machine, literally on your own computer, completely offline. It was built by a former Nvidia engineer and his brother who used to fix bugs in Llama and Qwen themselves. And by the way, I reached out to Unsloth to sponsor this video and they agreed. So huge shout out to them.

Now, let me show you how to set this up. So, first go to the docs. I'll link this below the video. It's going to be the first link. And here, click on quick start. This scrolls you down automatically where you have the different one-liner installer commands for different operating systems. So, I'll copy this entire command. Boom. And go into terminal. You can use iTerm or your default terminal inside of Mac OS. Doesn't matter. Just use any terminal. And paste in this command right here. This installs Unsloth Studio and all of the dependencies that it needs. And again, I want to stress this — it's completely open source and completely free to use. Unbelievable value from the Unsloth team to the world just making it easy to not only fine-tune AI models but also create your own data sets to fine-tune models on your own computer completely for free. It's incredible.

Okay, there it is. Unsloth Studio installed. Just hit Y, hit enter. Starting Unsloth Studio on localhost:8888. Go to browser and type in localhost:8888. And you can see we are in the studio. We have multiple things here we need to understand. First, we can chat with AI models. No matter which model you have downloaded, I have a couple of them. For example, Unsloth Qwen 3.6 27B. Very nice model. Actually, one of the most powerful models you can run locally on a MacBook. You just need like 24-32 GB of RAM or VRAM to run this and you can chat with it. So, not only is Unsloth the tool to fine-tune models and create data sets for fine-tuning, it's kind of also like a competitor to Ollama and LM Studio because you can also chat with these models inside of Unsloth, which is pretty incredible.

Okay, so the model has been loaded and we can do a test prompt something like "who are you" just to see if it's working — and again this is running fully locally on my MacBook. I do have 128 GB of RAM. But again, this is not the main point of Unsloth Studio. I'm just saying this is a huge bonus that you can also chat with LLMs locally.

But let's focus on the fine-tuning. On the left we have multiple tabs. We have the train tab — this is the main thing for fine-tuning. We also have the recipes tab — this is how we create our own data sets for fine-tuning. They call it recipes just to make it more approachable. But really Unsloth Studio has made this easier than ever before. If you looked into fine-tuning last year and thought "this is too complex, too difficult" — guys, it's never been easier to fine-tune an AI model. And not only that, it's never been easier to create your own unique data set for fine-tuning and then use that to train a new model and have a complete moat. Having your own data sets, having your own fine-tuned models — that is still a huge moat that most people don't know how to do. But after watching this video, you will have this skill set that 99.9% of people in AI simply do not have.

First let's go to the left and click on train. One more thing — when you open this for the first time, you might see a login password thing. This is just locally setting a password so that people on the same Wi-Fi cannot access it. Just put in some password — it's not really any real account on the web. It's just to secure Unsloth because we're running on localhost. Someone on the same Wi-Fi could technically access it.

Then go to the left and click on the train tab. Here we need to select what model to train and on which data set. First I'll show you how to fine-tune a model, then I'll show you how to create your own data set. Let's break this down step by step. You don't have to be a developer to do this. I'll show you everything in easy-to-follow steps. Anybody in 2026 can fine-tune their own AI model. And I'm going to prove that to you right now.

The first thing we need to do is select the model. We can see this model tab right here. Two options: select a local model or a HuggingFace model. If you don't have anything downloaded locally, go to HuggingFace and select something. HuggingFace is basically the GitHub for AI models and data sets — everything you need for open source AI model development and inference. On the homepage we have models, data sets, spaces — click on models and you can see almost 3 million different open source models.

Unsloth has their own re-uploads of popular AI models — Qwen, Llama, Gemma. Gemma is developed by Google, Llama by Meta, Qwen by Alibaba. Unsloth doesn't make these models. They debug them, improve them, make them better for fine-tuning and inference. If you're not sure which AI model to choose or what you can run locally on your own hardware, there's a cool site called Artificial Analysis. They have an open source section. Scroll down to see all open source models — large, medium, small. For most of you, small models is the right category. And Qwen 3.6 27B is the best in terms of intelligence. Right now Qwen 3.6 especially the dense model 27B is the best in this size of small models between 4 billion and 40 billion.

Back to HuggingFace — search for unsloth/Qwen3.6 to see all the Unsloth versions. We want the pure one 27B. It's important to understand what Unsloth does — first they fix real bugs in the models, working directly with Google, Meta, Alibaba, Mistral, Microsoft. Second, they add dynamic 2.0 quantization — instead of compressing only select layers, they dynamically adjust the quantization type of every layer with a custom scheme per model. This shrinks model size massively while keeping accuracy. In plain English, it lets you run much more powerful models on the same computer.

Inside Unsloth Studio, type in unsloth/Qwen3.6. Select the variant that's pure 27B — no MLX, no GGUF. You want the default safetensors version. Copy-paste the string from HuggingFace to make sure you have the correct model. Method: keep it on CUDA — it's very optimized for local hardware.

The second thing we need before fine-tuning is a data set. Qwen 3.6 27B is already a really good model. On a plane, you can ask it questions about basically anything and it'll give you 85% of what ChatGPT or Claude will give you. Obviously not as powerful as Opus or GPT 5.5, but very strong running fully locally if you have at least 32 GB VRAM. But it's not fine-tuned — it is generic. Everybody has the same one. So if you want to fine-tune it to make it less restricted, better at finance, better at coding, better at your own custom data set — I'll show you how.

Before we start, let me explain GGUF. GGUF is a compressed ready-to-run version of an AI model packed into a single file so it can run fast on a normal computer. Think of it like a zip file of the AI model — shrunk down so your laptop can handle it. But the catch: it's shrunk for inference, not for training. If you want to fine-tune a model, you need the full uncompressed version — the safetensors version.

GGUF is deeply tied to llama.cpp — a popular inference framework in C++. The same person created both: Georgi Gerganov. Llama.cpp only runs GGUF. Every other format must be converted first. In February 2026, his team joined HuggingFace — everything is uniting for the local AI stack.

Now, the next step in fine-tuning setup is choosing the data set — maybe the most important decision after choosing the model. HuggingFace has over 1 million different data sets. For this demo, I'll choose a finance data set so Qwen 3.6 27B can answer finance questions better. Choose the one for your own use case — legal, coding, whatever. I'm going with finance-alpaca — nearly 69,000 rows in instruction-output format. For example, "for a car what scams can be plotted with 0% financing versus rebate" with a detailed answer. Over 68,000 examples like that. This is the power of fine-tuning — you give it great examples and the model learns and becomes really good at that specific domain.

Different types of data sets for fine-tuning: instruction Q&A (single turn, most common), conversational (multi-turn), domain expert (your own niche data), reasoning/tool use (chain of thought, function calls). Each shape teaches a different skill. Pick the one matching your goal. If not sure, go with Q&A — the simplest classic.

Copy the data set name from HuggingFace, go back into Unsloth Studio, paste it in. Select finance-alpaca. It checks the data set in the bottom right. While waiting, we can change parameters: context length to 1024 (less compute intensive), batch size to 1 (small run). Lower steps to 20. More steps + longer training = better results. The beauty of Unsloth Studio is you can do everything locally — on your computer, with your electricity.

In a second, I'll show you how to create your own data sets. All of us have data — Google Docs, PDFs, CSV files, Excel files, WhatsApp messages, client conversations, YouTube videos, call transcripts. Use that data privately, securely to fine-tune a custom AI model. That's the power of fine-tuning. For your first fine-tune, use a pre-made HuggingFace data set to get familiar. But creating your own data sets has never been simpler.

Once parameters are configured and data set selected, go to the right and click start training. This begins the fine-tuning process fully locally. The data set (40 MB for 68,000 rows) downloads in seconds. The model — Qwen 3.6 27B — is 51 GB. If you don't have disk space, choose a smaller model. Unsloth has over 1,300 models. For a beast, go 122B or 397B. For smaller, go 9B — unsloth/Qwen3.5-9B. Everyone should be able to run this. Make sure you have the default safetensors version.

Training: step three of 20. GPU utilization nearly 100%. Training loss should go down — this means the model is learning the data set. The training loss shows how likely the model is to predict the next token on this data set. If it's not going down, the model isn't learning. This small run (20 steps) takes about 20-30 minutes. For a more impressive fine-tune: more steps, larger context window, multiple epochs, let it run for many hours. You need at least 1,000 examples minimum — very minimum 200-300. This data set has 68,000, which is more than enough.

Quick warning: there's a bug on MLX right now. Some models on Apple M-series silicon can fail even with enough RAM — this is about metal allocations, not VRAM. Apple engineers need to fix this. If bigger models like 27B fail, consider jumping to 9B. Or use cloud GPUs (A100, H100) for larger runs.

## Creating Your Own Data Sets: Recipes

So far we've used publicly available HuggingFace data sets — more than 99% of people will ever do. But for real advantage, you want your own data to create a unique AI model nobody else has.

Go to the left, click on recipes, new recipe, start from a learning recipe. Presets from Unsloth: text to Python, text to SQL, PDF document QA, OCR document extractions, GitHub crawler. The easiest: PDF document QA. Give it a PDF and it creates Q&A pairs — your own data set from a single PDF. This is huge.

Click it and we have four nodes: provider one, provider column, LLM structured, document file. Provider one is the provider we want to use. You could use a local model (Ollama server, Unsloth local server, LM Studio) for full privacy. But the beauty of fine-tuning is you can use a more powerful model and use distilled outputs — this is what basically everybody's doing with Anthropic models, the unspoken secret of the AI industry. People take Opus outputs and train a smaller model on them — making the small model closer to Opus in power. It'll never reach Opus's true capability at 100x smaller, but it can get close.

We want to use a big powerful model to create the data set, teaching our small model (Qwen 3.6 27B) how a bigger model would answer. It's like a trick — making it smarter by showing it bigger model answers.

First we need an API endpoint and key. Simplest: OpenRouter — all models are on OpenRouter. Paste in https://openrouter.ai/api/v1. Go to OpenRouter, create an account (20 seconds), add credits ($5-10 is enough), create an API key named "Unsloth finetune" with a $50 credit limit. Copy the key, paste into Unsloth Studio, click save.

Next, select the model in provider column. Definitely don't use GPT-4o Mini. Use something intelligent like Sonnet 4.6 — not as powerful as Opus but very good, way bigger than local models, great for distillation. Check Anthropic terms of service... but they distill the entire web into their models and then complain when someone distills their outputs into small open source models. Anyway, choose whatever model you want. Sonnet 4.6 is a great balance. For best of the best, use latest Opus or GPT.

Click save. LLM structured output — you can configure system prompt and response format, but default is fine. The important thing: document file. Whatever you upload here becomes Q&A pairs. Could be an SOP from your business, a CSV of sales calls, paid ad results and their outcomes. Whatever you want to fine-tune on — provide a quality PDF.

I downloaded an Nvidia 2026 financial report (80-page PDF) as an example. Upload it, click done. Click check, do a check run with 5 records, start test run.

Error with Sonnet 4.6 (May 28 elevated errors on Anthropic). Switch to Gemini 3.5 Flash — a very powerful, competent model from Google. The test run completes — costs a couple pennies. We see the data set created with 5 rows. The question: "for what financial year was this filed" — answer: "January 25th 2026." The PDF (80 pages) is chunked into smaller pieces for Q&A generation.

Go back to editor, click run for a full run — name it something human readable like "Nvidia financials 2026", do 1,000 records, start full run. This is why choosing a reasonably priced model matters — with Opus, 1,000 API calls would be very expensive.

Honestly, the best model for this: DeepSeek V4 Pro. Absolute killer model for cost — almost free. Use DeepSeek V4 Pro (or V4 Flash for even cheaper, though less powerful). DeepSeek V4 Pro is the most powerful open source model right now and dirt cheap — perfect for creating large data sets with thousands of API calls.

Let it run — might take a couple minutes for 10,000 rows. Next time we go to train, we can click on local and see our own data set. Instead of using HuggingFace data sets, we have our own custom data set created from within Unsloth Studio's recipes tab — all from a single PDF.

This is absolutely beautiful, absolutely magical. The feeling of running your own unique model that nobody else has is hard to describe. In this video, I showed you all the steps to not only fine-tune AI models but also do that locally with your very own custom data sets easily created from a single PDF.

Unsloth Studio is completely free. Huge thank you to Unsloth for sponsoring this video. Fully open source, free to use. The first link below the video. Install Unsloth Studio and do this now — watching is good, learning is good, but the thing that actually matters and might change your life is taking action. Go through this video again, implement everything, build your own fine-tuned AI model. All resources mentioned in this entire video are in the second link in the description — completely free.

Thank you for watching and have a great rest of the day.

</details>
