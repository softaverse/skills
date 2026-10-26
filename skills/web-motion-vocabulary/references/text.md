# C｜文字特效

最常用在 Hero 主標題。文字是內容本身，所以特效必須在一秒內結束，而且不能讓文字在動畫前「不存在」。

- **文字逐行浮現 (Split Text Reveal)** `splitreveal` — 標題拆成一行一行（或一個字一個字），從看不見的遮罩下方依序升上來。
  - 感受：沉穩、高級、雜誌感
  - 適合：Hero 主標題、章節標題、品牌標語
  - 搭配：reveal、pinned
  - 注意：只給大標題；中文逐字拆會太碎，建議逐行；總時長 ≤ 0.8 秒
  - 工具：GSAP SplitText；React 有 React Bits Split Text
  - 成本：複雜度 低｜效能 低｜持續動畫 否
  - 手機：同桌機；換行位置不同，要用逐行模式自動重算
  - 減少動態：直接顯示
  - 來源：GSAP SplitText https://gsap.com/docs/v3/Plugins/SplitText/ ；React Bits Split Text（MIT + Commons Clause）https://reactbits.dev/text-animations/split-text
  - Demo：`demos/splitreveal.js`（按 ↻ 重播）
- **亂碼解碼 (Scramble Text)** `scramble` — 文字先是一串亂跳的符號，再從左到右一個個定成正確的字。
  - 感受：科技、駭客、AI、解密
  - 適合：科技 / AI 品牌的短標語、數字、按鈕 hover
  - 搭配：spot、borderbeam
  - 注意：只用在短字串（10 字內）；長段落會很難讀；中文字可用英數符號當亂碼
  - 工具：GSAP ScrambleText；React 有 React Bits Scrambled Text
  - 成本：複雜度 低｜效能 低｜持續動畫 否
  - 手機：同桌機
  - 減少動態：直接顯示正確文字
  - 來源：GSAP ScrambleTextPlugin https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin/ ；React Bits Scrambled Text（MIT + Commons Clause）https://reactbits.dev/text-animations/scrambled-text
  - Demo：`demos/scramble.js`（按 ↻ 重播）
- **流光文字 (Shimmer Text)** `shimmer` — 一道細細的光反覆從左到右掃過文字，像金屬或玻璃反光。
  - 感受：新穎、吸睛、AI 產品感
  - 適合：「NEW」標籤、公告列、Hero 上方的小標
  - 搭配：borderbeam
  - 注意：**持續播放**，佔掉同畫面唯一的持續動畫額度；不要用在主標題或大段文字
  - 工具：CSS `background-clip: text` + 漸層動畫；React 有 Magic UI Animated Shiny Text
  - 成本：複雜度 低｜效能 低｜持續動畫 是
  - 手機：同桌機
  - 減少動態：停住光，只留靜態漸層
  - 來源：Magic UI Animated Shiny Text（MIT）https://magicui.design/docs/components/animated-shiny-text ；React Bits Shiny Text（MIT + Commons Clause）https://reactbits.dev/text-animations/shiny-text
  - Demo：`demos/shimmer.js`（直接看）
