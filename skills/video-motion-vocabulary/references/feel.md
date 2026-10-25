# 手感與節奏

同樣是「卡片進場」，0.3 秒急停和 0.9 秒慢慢靠過來是兩種個性。這一類不是效果，是**怎麼動**：
速度曲線、時間長短、先後順序。討論「俐落」「有彈性」「太死板」「太亂」時看這裡。

## 速度曲線

- **緩出 (Ease-out)** `easeout` — 一開始快、接近終點時減速停下，像東西滑進來後煞車。
  - 感受：俐落、自然、專業
  - 適合：幾乎所有進場；頻道預設手感
  - 搭配：Rise、Stagger、Push
  - 注意：進場 0.4–0.6s、退場更短；線性（等速）移動看起來像機器
  - 範例：`recipes/headline-rise` `recipes/card-stagger` `catalog-components/titlecard-calm`
- **彈性過衝 (Spring / Overshoot)** `spring` — 衝過頭一點再彈回定位，像有彈簧。
  - 感受：活潑、友善、有生命、App 感
  - 適合：徽章、按鈕、圖示、通知、小卡片
  - 搭配：Stagger、Badge Pop、Micro UI
  - 注意：過衝 5–10% 就夠；大面積的卡片彈起來會廉價；嚴肅主題少用
  - 範例：`catalog-components/spring-pop` `catalog-components/badge-pop` `catalog-components/sheet-spring-up` `remocn/caption-bounce-in`
- **慢慢靠近 (Extended Keyframe)** `creep` — 前 20% 的時間就走完大部分距離，剩下的時間極慢地「蹭」到終點，好像永遠不完全停下。
  - 感受：高級、電影、細膩
  - 適合：標題卡、品牌字、要停留很久的畫面
  - 搭配：Blur-in、Ken Burns
  - 注意：要整幕都這樣才有效
  - 範例：`catalog-components/extended-keyframe`

## 順序與節奏

- **依序錯開 (Stagger)** `stagger` — 一組元素不同時出現，一個接一個，間隔固定。
  - 感受：有節奏、有秩序、好讀
  - 適合：清單、格子卡片、逐詞文字
  - 搭配：Rise、Spring、Grid List
  - 注意：間隔 40–120ms；超過 8 個項目要加快或分組；跟口白對拍時改成「跟著口白出現」
  - 範例：`recipes/card-stagger` `catalog-components/stagger-cascade` `catalog-components/stagger-lattice` `catalog-components/grid-card-assemble`
- **一次一件事 (One Thing at a Time)** `onething` — 畫面上同時只有一個東西在動、只有一個是亮的，其他暗下或停住。
  - 感受：清楚、被引導、簡報感
  - 適合：講解型影片、多張卡片逐一說明、架構圖
  - 搭配：Shared Element、Spotlight、Dim
  - 注意：這是頻道預設原則（「一次只強調一件事」）
  - 範例：`recipes/card-focus` `catalog-components/focus-swap` `catalog-components/constellation-hub` `kit/three-cards`
- **加速堆疊 (Escalation)** `escalate` — 東西一個個出現，而且越來越快、越來越多，最後塞滿畫面。
  - 感受：壓力、爆量、混亂、「太多了」
  - 適合：痛點、通知轟炸、待辦爆炸
  - 搭配：Notification Stack、Shake、然後一個安靜的反轉
  - 注意：結尾要有釋放（清空、凍住、一句話）
  - 範例：`catalog-components/notification-pileup` `catalog-components/overwhelm-surround` `catalog/slack-notification-ad` `catalog/notification-cascade`
- **對拍 (Beat Sync)** `beat` — 動作落在音樂節拍上：切換、閃光、彈跳都對準鼓點。
  - 感受：爽快、音樂感、精準
  - 適合：片頭、蒙太奇、短影音
  - 搭配：Hard Cut、Flash、Impact
  - 注意：需要先標出節拍時間；口白為主的段落不要硬對拍
  - 範例：`catalog-components/beat-accent` `catalog-components/beat-pulse-background` `catalog-components/beat-timeline` `catalog/beat-freeze-cut`
- **節奏：從容 (Calm Pacing)** `calm` — 進場慢（0.8s 以上）、停留長、元素少、幾乎不同時動。
  - 感受：沉穩、高級、可信、留白
  - 適合：品牌片、金句、結尾、嚴肅主題
  - 搭配：Blur-in、Fade、Push-in
  - 注意：從容 ≠ 拖；口白快的地方會對不上
  - 範例：`catalog-components/titlecard-calm` `catalog-components/per-word-crossfade` `intro-title`
- **節奏：衝擊 (Punchy Pacing)** `punchy` — 進場快（0.2–0.3s）、硬切多、常有重擊和閃光。
  - 感受：高能、刺激、短影音
  - 適合：短影音、開場前 5 秒、運動、遊戲
  - 搭配：Slam、Word Pop、Hard Cut、Beat Sync
  - 注意：整支片都衝會讓觀眾疲乏；要有喘口氣的地方
  - 範例：`catalog-components/caption-kinetic-slam` `catalog-components/shutter-slam` `catalog/beat-freeze-cut`

## 重量與物理

- **重擊落地 (Impact)** `impact` — 東西重重落下的那一刻：瞬間定住、閃一下、微微晃，然後完全靜止。
  - 感受：肯定、有分量、完成
  - 適合：數字揭曉、Logo 定版、關鍵詞
  - 搭配：Slam、Flash、Shake
  - 注意：落地後要「完全不動」，衝擊才會被感覺到
  - 範例：`catalog-components/logo-sting` `catalog-components/headline-slam` `catalog-components/gloss-sweep`
- **物理拋擲 (Physics)** `physics` — 東西被丟出去、甩、拉扯、擺盪，有加速度和慣性。
  - 感受：真實、好玩、有手感
  - 適合：丟掉舊東西、拖曳卡片、吊牌晃動
  - 搭配：Spring、Motion Blur
  - 注意：方向和速度要合理，不然像飄
  - 範例：`catalog-components/physical-exit` `catalog-components/pendulum-swing` `catalog-components/rubber-band-bumper` `catalog-components/velocity-throw-snap`
- **動態模糊 (Motion Blur)** `mblur` — 移動很快的東西沿著方向拖出模糊，像真的攝影機拍到。
  - 感受：速度、真實、電影
  - 適合：快速飛入、甩鏡、重擊
  - 搭配：Whip Pan、Slam
  - 注意：慢動作加模糊會看起來像對焦失敗
  - 範例：`catalog-components/motion-blur` `catalog-components/shutter-slam` `catalog-components/dart-cursor`
- **殘影 (Echo Trail)** `echo` — 移動的東西後面跟著幾個越來越淡的分身。
  - 感受：速度、復古、迷幻
  - 適合：游標、logo、快速移動的小物件
  - 搭配：Neon、Retro
  - 注意：分身 3–5 個就夠
  - 範例：`catalog-components/echo-trail`

## 質地

- **定格動畫 (Stop-motion Cadence)** `stopmotion` — 故意降低格數（每 2–3 格才動一次），像黏土或紙偶動畫。
  - 感受：手作、可愛、復古、有溫度
  - 適合：手作風、紙張風、幽默段落
  - 搭配：Boil、Paper、Scrapbook
  - 注意：跟流暢的 60fps 動畫放在同一畫面會很怪
  - 範例：`catalog-components/stop-motion-cadence` `remocn/paper-wobble` `remocn/hand-count` `remocn/crumple-toss`
- **手繪抖動 (Boil)** `boil` — 手繪的線條每幾格就換一個微微不同的姿勢，像手繪動畫的線一直在「沸騰」。
  - 感受：手繪、活的、溫暖
  - 適合：手繪標註、塗鴉、白板風
  - 搭配：Write-on、Hand Underline、Stop-motion
  - 注意：抖動幅度要小
  - 範例：`catalog-components/hw-boil` `catalog/hw-title` `catalog/hw-frame`
- **呼吸停留 (Breathing Hold)** `breathe` — 東西落定後不是完全靜止，而是極輕微地縮放、漂移、閃一道光。
  - 感受：活著、不死板、精緻
  - 適合：停留較久的卡片、標題、主視覺
  - 搭配：Ken Burns、Shimmer
  - 注意：和 Impact 相反——要衝擊感的地方就不要呼吸
  - 範例：`catalog-components/drift-hold` `catalog-components/titlecard-lockup`
- **無縫循環 (Seamless Loop)** `loop` — 動畫的最後一格接回第一格，可以一直重播。
  - 感受：持續、環境、不會結束
  - 適合：背景、圖示、等待畫面、GIF
  - 搭配：Background、Glyph Loop
  - 注意：循環點要看不出接縫
  - 範例：`recipes/glyph-loop` `catalog-components/aurora-drift` `catalog/product-turntable`
