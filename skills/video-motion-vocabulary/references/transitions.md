# 轉場

從一幕到下一幕。先問「這兩幕的關係是什麼」：同一個話題延續（硬切、推移、共享元素）、
換章節（閃白、遮罩覆蓋、明顯的轉場）、還是 A 變成 B（匹配剪接、變形）。
同一支片的轉場種類越少越好——兩三種就夠。

## 基本

- **硬切 (Hard Cut)** `hardcut` — 直接切到下一個畫面，沒有任何過渡。
  - 感受：俐落、節奏快、自信
  - 適合：同一段落內的大部分切換；對拍剪接
  - 搭配：Beat Sync、Punch-in
  - 注意：這是預設，不是偷懶；要「加轉場」先問為什麼
  - 範例：`catalog/beat-freeze-cut` `snapcn/prompt-send` `snapcn/answer-stream`
- **淡化 (Crossfade / Fade-through)** `fade` — 前一幕淡出、下一幕淡入，或中間經過一片底色。
  - 感受：溫和、時間流逝、平靜
  - 適合：段落之間、情緒轉換、時間跳躍
  - 搭配：Calm Pacing、Blur-in
  - 注意：太長（> 0.8s）會拖；資訊型影片用多了顯得業餘
  - 範例：`catalog-components/fade-through` `catalog/transitions-dissolve`
- **推移 (Push / Slide)** `push` — 新畫面從一側推進來，把舊畫面推出去（或蓋上去）。
  - 感受：前進、下一步、App 感
  - 適合：步驟之間、清單的下一項、時間往前
  - 搭配：Motion Blur、Ease-in-out
  - 注意：方向要有意義（往右 = 往前），全片一致
  - 範例：`catalog-components/directional-wipe` `catalog-components/page-slide` `catalog/transitions-push` `catalog/transitions-cover`
- **擦除 (Wipe)** `wipe` — 一道邊（直線、斜線、手繪筆刷）掃過畫面，掃過的地方換成新畫面。
  - 感受：有設計、有方向、比推移輕
  - 適合：章節切換、前後對照
  - 搭配：Clip Wipe 文字、Chromatic Aberration
  - 注意：邊緣的造型就是風格，要跟全片一致
  - 範例：`catalog-components/chromatic-aberration-wipe` `catalog/hw-scribble-transition` `catalog/transitions-radial`
- **圓形開窗 (Iris)** `iris` — 新畫面從一個圓形開口擴大出來，或舊畫面收成一個圓點消失。
  - 感受：復古卡通、聚焦、「看這裡」
  - 適合：揭曉、聚焦到一個點、片尾
  - 搭配：Spotlight、Match Cut
  - 注意：圓心要放在有意義的位置
  - 範例：`catalog-components/iris-reveal` `catalog/sdf-iris` `catalog/transitions-mechanical`

## 有能量的

- **穿越縮放 (Zoom-through)** `zoomthrough` — 鏡頭衝進前一幕的某個點（卡片、螢幕），穿過去就是下一幕。
  - 感受：深入、沉浸、連貫
  - 適合：「我們來看細節」、進入某個工具、App 內頁
  - 搭配：Dive、Motion Blur
  - 注意：要有一個明確的「入口」物件
  - 範例：`catalog-components/zoom-through-transition` `catalog-components/parallax-zoom` `catalog/cinematic-zoom` `catalog/transitions-scale`
- **甩鏡 (Whip Pan)** `whippan` — 鏡頭快速甩向一側，畫面糊成動態模糊，停下時已經是新畫面。
  - 感受：快、有勁、Vlog / 運動感
  - 適合：地點切換、高能段落、同主題的快速串接
  - 搭配：Motion Blur、Beat Sync、Hard Cut
  - 注意：連用三次以上會暈
  - 範例：`catalog-components/whip-pan-cut` `catalog/whip-pan` `catalog-components/cut-the-curve`
- **閃白 (Flash)** `flash` — 畫面亮到一片白（或像相機閃光），亮完已經是新畫面。
  - 感受：衝擊、頓悟、拍照、重新開始
  - 適合：章節切換、揭曉、節拍重音
  - 搭配：Slam、Impact、Beat Sync
  - 注意：太頻繁會刺眼；注意光敏感觀眾
  - 範例：`flash-through-white` `catalog/flash-through-white` `catalog/editorial-flash-overlay` `EP3-stitch/seg_05-transition`
- **漏光 (Light Leak)** `lightleak` — 一團暖色光從畫面邊緣滲進來、掃過，像底片漏光。
  - 感受：溫暖、回憶、底片、浪漫
  - 適合：回憶段落、生活 Vlog、溫暖的結尾
  - 搭配：Film Grain、Fade
  - 注意：和科技、簡報風格不搭
  - 範例：`catalog/light-leak` `catalog/organic-light-leak-overlay` `catalog/transitions-light`
- **故障轉場 (Glitch)** `glitchtrans` — 畫面撕裂、色版錯開、跳格幾下後變成下一幕。
  - 感受：科技、出錯、駭客
  - 適合：科技主題、「系統壞了」、反轉
  - 搭配：Glitch Text、CRT
  - 注意：< 0.4s；用在對的情緒上，不是當裝飾
  - 範例：`catalog/glitch` `catalog/chromatic-radial-split`
- **扭曲溶解 (Warp / Dissolve)** `warp` — 畫面像被熱浪、漩渦、水波、重力透鏡扭曲，溶成下一幕。
  - 感受：夢幻、超現實、能量
  - 適合：夢境、想像、概念轉換
  - 搭配：Shader 背景
  - 注意：很搶眼，一支片最多用一種
  - 範例：`catalog/cross-warp-morph` `catalog/domain-warp-dissolve` `catalog/swirl-vortex` `catalog/ridged-burn`

## 造型的

- **格狀轉場 (Grid / Pixelate)** `gridtrans` — 畫面拆成格子或網點，一格一格翻掉或消失。
  - 感受：數位、系統化、復古電腦
  - 適合：科技主題、資料、像素風
  - 搭配：Halftone、Dither
  - 注意：格子大小要配合畫面主體
  - 範例：`catalog-components/grid-pixelate-wipe` `catalog-components/halftone-dissolve` `catalog/transitions-grid`
- **3D 翻轉 (3D Flip)** `flip3d` — 畫面像卡片或磚塊在 3D 空間翻面，背面是下一幕。
  - 感受：俏皮、立體、翻頁
  - 適合：正反面對照、揭曉答案
  - 搭配：Cube Caption
  - 注意：透視要一致
  - 範例：`catalog/transitions-3d` `catalog/code-slice-hero`
- **碎裂 (Shatter / Tear)** `shatter` — 畫面碎成玻璃、撕成兩半、或爆開成碎片。
  - 感受：破壞、決裂、戲劇性
  - 適合：「打破」「結束了」、失敗與重來
  - 搭配：Impact、Shake
  - 注意：情緒很強，用錯地方很突兀
  - 範例：`catalog/transitions-destruction` `catalog/vfx-shatter` `remotion-inspired/tear`
- **紙張轉場 (Paper)** `papertrans` — 翻頁、撕紙、一片片紙片飛走露出下一幕。
  - 感受：手作、書本、剪貼簿
  - 適合：手作風、Vox 風、故事章節
  - 搭配：Scrapbook、Stop-motion
  - 注意：跟平滑的數位動畫混用會不協調
  - 範例：`remocn/page-turn` `catalog-components/torn-paper-rip` `catalog-components/paper-collage-reveal`
- **覆蓋轉場 (Cover)** `cover` — 一層東西（布幕、塗鴉、字牆、色塊格線）先蓋滿畫面，掀開後已經換了。
  - 感受：舞台、章節、儀式感
  - 適合：章節切換、開場、揭幕
  - 搭配：Section Card
  - 注意：蓋滿的那一刻要停 2–4 格，切換才自然
  - 範例：`catalog-components/curtain-reveal` `catalog/mk-clone-wall-transition` `remocn/mondrian-split` `catalog-components/ink-bleed-reveal`

## 連續性

- **匹配剪接 (Match Cut)** `matchcut` — 前一幕的某個形狀（圓、字、物件）在同樣的位置、同樣的速度，直接接成下一幕的另一個東西。
  - 感受：巧妙、連貫、電影
  - 適合：A 變成 B、因果、兩個概念的對應
  - 搭配：Text Match Cut、Morph
  - 注意：要在分鏡階段就設計好兩幕的對應物
  - 範例：`catalog-components/match-cut` `catalog-components/text-match-cut` `catalog-components/type-match-cut`
- **共享元素展開 (Shared Element)** `sharedelement` — 畫面上的一張卡放大成整個面板講細節，講完再縮回原位。
  - 感受：連貫、App 感、一直知道自己在哪
  - 適合：總覽 → 細節 → 總覽、三張卡逐一講
  - 搭配：One Thing at a Time、Stagger
  - 注意：縮回時位置要精準，不然像跳針
  - 範例：`recipes/card-focus` `kit/three-cards` `catalog-components/modal-morph` `web-stack-intro`
- **變形 (Morph)** `morph` — 一個形狀或圖示平滑地變成另一個。
  - 感受：流暢、聰明、狀態改變
  - 適合：狀態切換（未完成 → 完成）、概念轉換、logo
  - 搭配：Match Cut、Spring
  - 注意：兩個形狀差太多時中間態會醜
  - 範例：`catalog-components/morph-swap` `catalog-components/icon-morph-beat` `catalog/gooey-split` `catalog-components/facet-morph`
- **共享軸 (Shared Axis)** `sharedaxis` — 舊內容往上（或往後）退、新內容從下（或從前）進，兩者沿同一條軸交棒。
  - 感受：秩序、Material 感、層級清楚
  - 適合：換句、換頁、深入一層
  - 搭配：Rise、Fade
  - 注意：距離要短（< 30px），長了像推移
  - 範例：`catalog-components/shared-axis-y` `catalog-components/shared-axis-z`
- **子母畫面 / 分割畫面 (PiP / Split Screen)** `pip` — 講者畫面縮到角落（或滑到一半），讓出空間給重點畫面。
  - 感受：講者還在、陪你一起看
  - 適合：講解螢幕錄影、展示圖表時保留講者
  - 搭配：Device Frame、Zoom-follow
  - 注意：講者框要避開重點內容
  - 範例：`remotion-inspired/pip-transition` `remotion-inspired/split-screen`
