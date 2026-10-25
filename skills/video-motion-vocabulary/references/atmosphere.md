# 背景、材質與特效

畫面的底層和質地：會動的背景、粒子、底片處理、玻璃、3D 物件。
原則：**背景慢、低對比、不搶戲**。背景一動得比主角還多，主角就消失了。

## 會動的背景

- **流動漸層 (Mesh Gradient)** `meshbg` — 幾團柔和的顏色慢慢漂移、混在一起。
  - 感受：現代、柔和、品牌感
  - 適合：標題卡、金句、產品宣傳的底
  - 搭配：Blur-in、Glass
  - 注意：顏色要跟品牌色系；速度非常慢
  - 範例：`catalog/mesh-gradient` `catalog-components/mesh-gradient-bg` `catalog/flowing-gradient` `catalog/mk-background`
- **極光 (Aurora)** `aurorabg` — 綠紫、藍色的光幕在暗底上緩慢飄動。
  - 感受：科技、夢幻、深夜、高級
  - 適合：深色科技片、Kallaway 風格、AI 主題
  - 搭配：Glass、Glow、Dark
  - 注意：亮色系的頻道不適合
  - 範例：`catalog/aurora` `catalog-components/aurora-drift` `herk-kallaway/t1-section-aurora-bars` `catalog/liquid-glass-notification`
- **雜訊流動 (Noise / Plasma)** `noisebg` — 雲霧般的雜訊、電漿、細胞紋理在整個畫面流動。
  - 感受：抽象、神秘、有機
  - 適合：抽象概念、背景質地、音樂
  - 搭配：Big Type、Blend
  - 注意：細節太多會讓前景難讀
  - 範例：`catalog/fractal-noise` `catalog/plasma` `catalog/worley-noise` `catalog/voronoi`
- **光束 (Light Rays)** `rays` — 光線從角落或中心放射出來，緩慢轉動或飄移；或鏡頭光暈。
  - 感受：希望、神聖、揭曉、舞台
  - 適合：揭曉、開場、結尾
  - 搭配：Logo Sting、Flash
  - 注意：光太強會蓋過字
  - 範例：`catalog/godrays` `catalog/sun-burst` `catalog/lens-flare` `catalog/vfx-anamorphic-flare`
- **幾何圖樣 (Pattern)** `patternbg` — 波浪、條紋、螺旋、磚塊、包浩斯幾何積木等圖樣循環移動。
  - 感受：活潑、設計感、有個性
  - 適合：章節卡、片頭、輕鬆主題
  - 搭配：Flat、Bold Type
  - 注意：對比要壓低才能當背景
  - 範例：`remotion-inspired/pattern-background` `catalog/stripes` `remocn/truchet-flip` `remocn/bauhaus-build`
- **網格背景 (Grid)** `gridbg` — 細線網格或透視地板，可能緩慢平移。
  - 感受：科技、工程、藍圖、秩序
  - 適合：SaaS、程式、數據主題
  - 搭配：Dark、Glow、Connector
  - 注意：線要細且淡
  - 範例：`catalog-components/dynamic-grid` `herk-kallaway/t1-section-gridfloor` `herk-kallaway/t1-section-drift-grid`
- **空間隧道 (Tunnel / Portal)** `tunnel` — 往無限深處延伸的隧道、走廊或傳送門。
  - 感受：深入、速度、穿越
  - 適合：片頭、轉場、「進入」
  - 搭配：Zoom-through、Particles
  - 注意：容易暈；時間短
  - 範例：`catalog/gallery-tunnel` `herk-kallaway/t1-section-tunnel` `herk-kallaway/t1-section-portal`

## 粒子

- **環境粒子 (Ambient Particles)** `particles` — 雪、星空、星系、漂浮的光點，緩慢移動。
  - 感受：氛圍、季節、夢幻、宇宙
  - 適合：節慶、夜晚、太空、片頭
  - 搭配：Calm Pacing、Blur-in
  - 注意：有景深（大小、速度不同）才不會像雜訊
  - 範例：`catalog/snow` `catalog/starfield` `catalog/spiral-galaxy` `herk-kallaway/t1-section-particles`
- **彩帶爆發 (Confetti)** `confetti` — 一陣彩帶、紙片或圖示從一點爆出，受重力落下。
  - 感受：慶祝、成功、驚喜
  - 適合：達成目標、數字揭曉、感謝
  - 搭配：Count-up、Impact
  - 注意：一次就好；顏色跟品牌一致
  - 範例：`catalog-components/confetti` `catalog/apple-money-count`
- **粒子顯影 (Particle Reveal)** `particlereveal` — 粒子聚集、散開，底下的圖片同時顯現。
  - 感受：生成、魔法、AI
  - 適合：AI 生成圖、揭曉作品
  - 搭配：Particle Text
  - 注意：成本高
  - 範例：`catalog-components/particle-image-reveal` `catalog-components/segmentation-flood`

## 畫面處理（Treatment）

- **底片顆粒與暗角 (Film Grain & Vignette)** `film` — 疊一層細小的顆粒雜訊，四角微微變暗。
  - 感受：底片、溫暖、電影、類比
  - 適合：幾乎任何畫面都可以淡淡加；紀錄片、Vlog
  - 搭配：Light Leak、Calm Pacing
  - 注意：要淡到「沒注意到但少了會覺得太乾淨」
  - 範例：`catalog-components/grain-overlay` `catalog-components/vignette` `catalog-components/grain-field` `catalog/yt-lcd-background`
- **老電視 (CRT / VHS)** `crt` — 掃描線、色偏、畫面邊緣彎曲、開機閃一下——像老電視或錄影帶。
  - 感受：復古、懷舊、80–90 年代
  - 適合：回顧、懷舊、遊戲
  - 搭配：Glitch、Scramble
  - 注意：讀字會變吃力
  - 範例：`herk-vox-explainer/t1-section-crt` `catalog-components/yt-screen-warp` `catalog/oscilloscope-trace`
- **網點與像素 (Halftone / Dither / ASCII)** `halftone` — 畫面變成網點、抖色像素、或 ASCII 字元。
  - 感受：印刷、復古電腦、駭客、藝術
  - 適合：風格化的片頭、轉場、科技懷舊
  - 搭配：Grid Transition、Glitch
  - 注意：細節會被吃掉，主體要簡單
  - 範例：`catalog/halftone-field` `catalog-components/ordered-dither-pass` `catalog-components/ascii-render-pass` `catalog-components/ascii-trail-reveal`
- **機器視覺 (Machine Vision)** `machinevision` — 掃描框、辨識遮罩、角框、數值讀出——像 AI 在分析畫面。
  - 感受：AI、監控、分析、科幻
  - 適合：AI 辨識、數據分析、科幻
  - 搭配：Telemetry HUD、Scramble
  - 注意：要有明確的「被分析的對象」
  - 範例：`catalog-components/segmentation-flood` `catalog-components/telemetry-hud` `catalog-components/camera-scan-gate`
- **局部動態照 (Cinemagraph)** `cinemagraph` — 整張照片靜止，只有一小塊還在動（熱氣、水、頭髮）。
  - 感受：詩意、安靜、時間凍結
  - 適合：氛圍鏡頭、回憶、品牌
  - 搭配：Calm Pacing、Film Grain
  - 注意：動的部分要循環得很順
  - 範例：`catalog/cinemagraph`

## 材質與物件

- **毛玻璃 (Glass)** `glass` — 半透明、背後模糊的卡片或面板，邊緣一道細光。
  - 感受：現代、科技、Apple / iOS
  - 適合：深色科技風的卡片、通知、名牌
  - 搭配：Aurora、Mesh Gradient
  - 注意：背後要有顏色變化，玻璃才看得出來
  - 範例：`catalog/liquid-glass-widgets` `catalog/ios26-liquid-glass` `herk-kallaway/t2-lt-glasscard` `remocn/glass-code-block`
- **材質球 (Shader Orb)** `orb` — 一顆會動的球：鉻金屬、液態金屬、全息、冰、水、黏液。
  - 感受：高科技、未來、抽象品牌
  - 適合：AI 產品視覺、片頭主視覺
  - 搭配：Dark、Glow
  - 注意：是主視覺，不是背景
  - 範例：`catalog/chrome-orb` `catalog/liquid-metal` `catalog/holographic` `catalog/cosmic-orb`
- **3D 物件 (3D Object)** `object3d` — 真正的 3D 模型：產品轉台、玻璃物件、低多邊形變形。
  - 感受：大製作、產品、立體
  - 適合：產品展示、品牌主視覺
  - 搭配：Orbit、Light Sweep
  - 注意：需要模型檔或 shader；render 久
  - 範例：`catalog/product-turntable` `catalog/glass-hero` `catalog-components/facet-morph`
- **液體 (Liquid / Ink)** `liquid` — 液面波動、墨水在紙上暈開、黏液分裂融合。
  - 感受：有機、流動、藝術
  - 適合：轉場、品牌、抽象概念
  - 搭配：Gooey Text、Morph
  - 注意：速度要像真的液體
  - 範例：`catalog/vfx-liquid-background` `catalog-components/ink-bleed-reveal` `catalog/gooey-split`
- **剪貼簿 (Scrapbook)** `scrapbook` — 撕紙、膠帶、拍立得、貼紙、剪報，啪地貼上。
  - 感受：手作、Vox、回憶、拼貼
  - 適合：Vox 式解說、生活記錄、人物介紹
  - 搭配：Stop-motion、Stamp、Paper Transition
  - 注意：要「亂中有序」——主角還是要清楚
  - 範例：`catalog/freeze-frame-dressing` `herk-vox-explainer/t1-section-collage` `remocn/paper-sticker` `remotion-inspired/polaroid-pictures`
- **白板手繪 (Whiteboard)** `whiteboard` — 白板或紙上一筆一筆畫出插圖，筆尖跟著線走。
  - 感受：教學、思考過程、親切
  - 適合：解釋概念、畫圖說明
  - 搭配：Write-on、Boil、Hand Arrow
  - 注意：圖要簡單
  - 範例：`catalog-components/whiteboard-ink` `catalog/hw-frame` `catalog/hw-text-cloud`
- **角色動畫 (Character)** `character` — 一個簡單的角色走進來、比手勢、指向某個東西。
  - 感受：親切、說故事、兒童向
  - 適合：吉祥物、說明型動畫
  - 搭配：Hand-drawn、Flat
  - 注意：角色動作需要 Lottie 或另外製作
  - 範例：`catalog/lottie-character-walk`
