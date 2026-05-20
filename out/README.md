# YouTube 字幕公有鏡像

> 原始字幕存於 `out/`（gitignored，僅本機保留）。
> 下表為對應的公開 GitHub Gist 連結。

## 字幕一覽

| 影片 ID | 標題 | Gist |
|---------|------|------|
| `h_rv2Qs_REk` | 五角大樓 UFO 檔案：阿波羅月球接觸 | [gist](https://gist.github.com/eiraho/de68d4e76d769a7e0ec11ae5ff879637) |
| `KAqgH3B9YCQ` | 對未來覺得恐懼？拆解《天能》最神結局（斯多葛哲學）| [gist](https://gist.github.com/eiraho/7e44fb663db667dfbd32268014ad02d5) |
| `0BacrKhaRJI` | AI Agent 四大類頂級 Skill 配置指南 | [gist](https://gist.github.com/eiraho/ef5a48f28c26ad3a9673d61e91fbfbad) |
| `q4I2exv6l8U` | 飛書 CLI 47 天破萬星：淘金時代的序曲 | [gist](https://gist.github.com/eiraho/abdbad324f5a85d2e68b1c23d022baec) |
| `e1LX6k--540` | 克拉克123合集 — 他用體悟震碎三觀 | [gist](https://gist.github.com/eiraho/943d5eb9132895da11381bec351a9aca) |

| `fB4uipaYYeU` | Claude Code + Remotion 寫代碼做剪輯（心心） | [gist](https://gist.github.com/eiraho/232bc96aaa7f6ac8556ba58abc24d9d3) |
| `OJr8b0HMoLw` | 30分鐘部署個人專屬Calendly！cal.diy 全開源排程 | [gist](https://gist.github.com/eiraho/218891133d9c7e1c8a8a1ef4db521d48) |
| `bYM_VMs7EO0` | Alex Wang：AI史上最貴人才首次受訪（Meta MSL） | [gist](https://gist.github.com/eiraho/0ad44b3c363bb7601ffc06a22c93a162) |
| `uwwOKQv7hxs` | DeepSeek V4 華為昇騰全站遷移：CUDA壟斷終結 | [gist](https://gist.github.com/eiraho/cba5c89a94a16e89912a4477efa242f3) |
| `aflFx_-tFJs` | Joe Dispenza《開啟你的驚人天賦》：量子場顯化改寫人生 | [gist](https://gist.github.com/eiraho/62abf853a538b2da84a188a1457c861b) |
| `_kwhTWYPy44` | 華為鴻蒙開源爭議：OpenHarmony.Avalonia 存檔風波 | [gist](https://gist.github.com/eiraho/9baa79e6a7d903f1722108c86e4afff0) |
| `FFX0sng67RI` | 啟發式學習（HL）：AI 不訓練網絡，只改代碼 | — |
| `KsnXvqSbDLU` | Google I/O 2026 + Android 17 精華總結 | [gist](https://gist.github.com/eiraho/a0c8eb9440218d7086c6919b85afb7b6) |
| `DyAKn1-82fQ` | 别把学习外包给AI！AI编程需要保留"有益的摩擦" | [gist](https://gist.github.com/eiraho/0fd9a897d9a1eb83eae57ceeea35f3f8) |

## 流程

以後每次下載新字幕：

1. 原檔 → `out/{videoId}-{標題}.md`（私有）
2. `gh gist create --public --desc "{標題}" "out/{檔名}"` → 公開鏡像
3. 將 gist URL 加入上表
4. `git commit -m "mirror: {videoId} gist link" && git push`
