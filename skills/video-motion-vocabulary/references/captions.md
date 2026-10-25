# 字幕

跟著講話時間走的字。先分清楚兩件事：**整句一起出現**（讀起來穩，強調靠「目前講到哪」的標示），
還是**一次只出現幾個詞**（節奏強、短影音感，但資訊密度低）。

字幕要「嵌進畫面」（字在講者後面、跟場景融合）時，那是另一套系統：`embedded-captions`
skill 有 36 種視覺身分，逐字稿型口播預設用它的 `anchor`。

## 整句出現，標示講到哪

- **電影字幕 (Subtitle)** `subtitle` — 傳統下方字幕：一整句一起出現、換句才換，可有半透明底框。
  - 感受：可信、安靜、不打擾
  - 適合：知識型口播、訪談、長片
  - 搭配：任何疊畫面
  - 注意：每行 16 字內；這是最穩的預設，不要覺得它無聊就換掉
  - 範例：`remocn/caption-subtitle`
- **卡拉 OK (Karaoke Fill)** `karaoke` — 整句先出現，講到的詞照講話速度從左到右染成強調色。
  - 感受：跟讀、有節奏、短影音
  - 適合：Shorts / Reels、教學重點句
  - 搭配：Outline Caption、Pill
  - 注意：顏色差要大，不然看不出進度
  - 範例：`remocn/caption-karaoke` `snapcn/karaoke-captions` `catalog-components/caption-pill-karaoke`
- **講到才亮 (Dim Progress)** `dimprogress` — 整句先半透明，講到的詞才變全亮。
  - 感受：沉穩、讀得到全句又知道進度
  - 適合：較長的句子、知識型短片
  - 搭配：Subtitle 的位置與字級
  - 注意：沒講到的字也要可讀（透明度 40% 以上）
  - 範例：`remocn/caption-dim-progress`
- **色塊跟讀 (Highlight Box)** `highlightbox` — 一個圓角色塊跟著正在講的詞移動、變寬變窄。
  - 感受：活潑、TikTok 感、很明確
  - 適合：短影音、帶貨、熱情口播
  - 搭配：Outline Caption、Word Pop
  - 注意：色塊移動要平滑，跳格會很廉價
  - 範例：`remocn/caption-highlight-box` `catalog-components/caption-highlight`
- **滑動底線 (Underline Follow)** `underlinefollow` — 整句出現，一條強調色底線跟著正在講的詞滑過去。
  - 感受：克制、編輯感
  - 適合：品牌、知識型、比較安靜的頻道
  - 搭配：Subtitle、Dim Progress
  - 注意：底線太細在手機上看不到
  - 範例：`remocn/caption-underline`
- **講到放大 (Active Pop)** `activepop` — 整句出現，正在講的詞彈簧放大並換色，講完彈回。
  - 感受：熱鬧、有彈性
  - 適合：短影音、興奮的語氣
  - 搭配：Spring、Highlight Box
  - 注意：放大會推擠旁邊的字，留好間距
  - 範例：`remocn/caption-active-pop`
- **粗描邊字幕 (Outline Caption)** `outlinecap` — 粗黑描邊的白字，講到的詞換強調色——短影音最常見的樣子。
  - 感受：直接、大眾、一看就懂
  - 適合：Shorts、Vlog、任何亂背景
  - 搭配：Karaoke、Word Pop、Emoji
  - 注意：跟精緻、極簡的品牌調性不合
  - 範例：`remocn/caption-outline`
- **字重強調 (Weight Caption)** `weightcap` — 整句細字，講到的詞瞬間變超粗、講完慢慢變回。
  - 感受：優雅的強調、設計感
  - 適合：品牌片、Podcast
  - 搭配：Variable Weight、Underline Follow
  - 注意：要可變字型
  - 範例：`remocn/caption-weight` `catalog-components/caption-weight-shift`

## 一次只出現幾個詞

- **一詞一跳 (Word Pop)** `wordpop` — 每次只出現一個（或兩三個）大詞，彈簧彈出來，講完換下一個。
  - 感受：高能量、MrBeast 式、停不下來
  - 適合：短影音前 3 秒、高能口播
  - 搭配：Beat Sync、Keyword Caption、Hard Cut
  - 注意：長片整支用會累；讀不到上下文
  - 範例：`remocn/caption-word-pop` `snapcn/word-captions` `catalog-components/caption-kinetic-slam`
- **逐詞進場 (Word Entrance)** `wordentrance` — 詞照講話時間一個個進場：從下方彈上、從上方掉下、從模糊變清楚、上下切片滑入。
  - 感受：看選哪種進場——彈跳活潑、掉落俏皮、模糊柔和、切片俐落
  - 適合：想要節奏但不想像 Word Pop 那麼吵
  - 搭配：Spring、Blur-in
  - 注意：一支片只選一種進場方式
  - 範例：`remocn/caption-bounce-in` `remocn/caption-drop` `remocn/caption-blur-in` `remocn/caption-slice`
- **打字字幕 (Typed Caption)** `typecap` — 字照講話速度打出來：打字機、手寫遮罩、標籤機膠帶。
  - 感受：記錄感、手作、正在寫
  - 適合：日記式 Vlog、教學
  - 搭配：Typewriter、Write-on
  - 注意：打字速度要對上語速，不然會落後
  - 範例：`remocn/caption-typewriter` `remocn/caption-handwrite` `remocn/caption-label-maker`
- **塗黑揭露 (Redact Reveal)** `redact` — 每個詞先被黑條（或白色字卡）蓋住，講到時才露出。
  - 感受：機密、揭秘、懸疑
  - 適合：爆料、「你不知道的」系列
  - 搭配：Stamp、Dossier 風格
  - 注意：整句都蓋住時觀眾讀不到，適合短句
  - 範例：`remocn/caption-redact` `remocn/caption-knockout`

## 特殊用途

- **關鍵詞特效 (Keyword Caption)** `keywordcap` — 一般字幕之外，講到關鍵詞時多一個效果：蓋章、螢光筆劃過、彈出 emoji、粒子爆開。
  - 感受：重點突出、有梗
  - 適合：一句裡最重要的詞
  - 搭配：Subtitle 或 Karaoke 當底
  - 注意：每句最多一個，不然等於沒有重點
  - 範例：`remocn/caption-stamp` `remocn/caption-marker` `remocn/caption-emoji` `catalog-components/caption-particle-burst`
- **語速大小 (Prosody Caption)** `prosody` — 依講話的輕重決定字大小：拖長、強調的詞變大，帶過的詞變小。
  - 感受：有聲音的表情、編輯感
  - 適合：情緒起伏大的口白、詩意的句子
  - 搭配：Editorial 字體
  - 注意：大小差異太大版面會亂
  - 範例：`remocn/caption-prosody` `catalog-components/caption-editorial-emphasis`
- **多人對話字幕 (Speaker Caption)** `speakercap` — 每個說話者一個顏色，換人說話就換色。
  - 感受：清楚、訪談感
  - 適合：Podcast、對談、訪問
  - 搭配：Lower Third
  - 注意：顏色要事先固定給每個人
  - 範例：`remocn/caption-speaker`
- **提詞機 (Teleprompter)** `teleprompter` — 整份逐字稿排成多行往上捲，目前這行最亮；或排在一條水平時間軸上。
  - 感受：完整、透明、像在看稿
  - 適合：朗讀、詩、長引言
  - 搭配：Dim Progress
  - 注意：不適合疊在講者上
  - 範例：`remocn/caption-teleprompter` `remocn/caption-timeline`
- **翻轉換句 (Flip Caption)** `flipcap` — 換句時字幕整塊翻轉：3D 方塊往上翻、拉霸滾動、翻牌。
  - 感受：機械、有趣、有轉場感
  - 適合：一句一句節奏明確的口白
  - 搭配：Split-flap、Slot Roll
  - 注意：每句都翻會太忙，適合短句
  - 範例：`remocn/caption-cube` `remocn/caption-slot` `remocn/caption-split-flap`
- **自動反白 (Blend Difference Caption)** `blendcap` — 字用「差值」混合，背景亮的地方字變黑、暗的地方變白，永遠看得到。
  - 感受：設計感、俐落
  - 適合：背景明暗變化大的畫面
  - 搭配：Big Type、Swiss 風格
  - 注意：顏色只能黑白反轉，不能有品牌色
  - 範例：`catalog-components/caption-blend-difference` `caption-blend-difference`
- **霓虹字幕 (Neon Caption)** `neoncap` — 發光的霓虹色字，關鍵詞換色、微微晃動或故障閃。
  - 感受：夜晚、科技、遊戲
  - 適合：遊戲、科技、音樂
  - 搭配：Dark 背景、Glitch
  - 注意：亮背景完全失效
  - 範例：`catalog-components/caption-neon-glow` `catalog-components/caption-neon-accent` `catalog-components/caption-glitch-rgb`
- **字在講者後面 (Behind-subject Caption)** `behindcap` — 大字放在講者身後，被講者擋住一部分，像在場景裡。
  - 感受：大製作、雜誌封面、電影感
  - 適合：開場標題、一句金句
  - 搭配：Big Type、Push-in
  - 注意：需要去背遮罩；完整做法用 `embedded-captions`
  - 範例：`catalog-components/caption-parallax-layers`
- **鏡頭追字 (Camera-follow Caption)** `cameracap` — 一句話寫在比畫面大很多的空間裡，鏡頭跟著每個詞移動、縮放。
  - 感受：電影、敘事、沉浸
  - 適合：片頭獨白、一段宣言
  - 搭配：Push-in、Calm Pacing
  - 注意：只適合一兩句；製作成本高
  - 範例：`catalog-components/caption-camera-follow`
