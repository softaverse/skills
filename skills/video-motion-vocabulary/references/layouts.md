# 資訊卡版式

一張切畫面卡片怎麼排它的資訊。版式決定「觀眾一眼看到什麼結構」，動態則決定「這個結構
怎麼一步步長出來」——每個版式都寫了它通常怎麼動。Herk 的卡片大量屬於這一類，同一個版式在
Kallaway（深色玻璃）和 Vox（紙質）各有一版，可以並排比。

## 清單

- **編號清單 (Numbered List)** `numlist` — 編號＋短標題一列列往下排，跟著口白一項項出現。
  - 感受：清楚、有順序、可記憶
  - 適合：「三個原因」「五個步驟」
  - 搭配：Stagger、One Thing at a Time
  - 注意：超過 6 項要拆兩張
  - 範例：`herk-kallaway/t1-overview-numlist` `herk-kallaway/t1-overview-bigleft` `herk-vox-explainer/t1-overview-numlist`
- **勾選清單 (Checklist)** `checklist` — 每一項前面有方框，出現時打勾。
  - 感受：完成感、可執行
  - 適合：準備清單、功能檢查、需求
  - 搭配：Stagger、Hand-drawn
  - 注意：勾的動作要明確，可以加小彈跳
  - 範例：`herk-kallaway/t1-overview-checklist` `remocn/check-list` `catalog-components/marker-checklist-card` `catalog/mk-specs-list`
- **格狀清單 (Grid List)** `gridlist` — 2–6 張卡片排成格子，每張是編號／圖示＋標題＋一兩行說明。
  - 感受：完整、一覽、系統
  - 適合：功能一覽、技巧清單、分類
  - 搭配：Stagger、Grid Card Assemble
  - 注意：每張卡的字要短到一眼讀完
  - 範例：`kit/grid-list` `herk-kallaway/t1-overview-grid6` `herk-kallaway/t1-overview-featuregrid` `EP3-stitch/seg_15`
- **三卡並排 (Three Cards)** `threecards` — 三張大卡片並排，可以依序展開成面板講細節。
  - 感受：平衡、選擇、三個面向
  - 適合：三個工具、三種方案、三個概念
  - 搭配：Shared Element、One Thing at a Time
  - 注意：三張要等重，除非刻意突出一張
  - 範例：`kit/three-cards` `herk-kallaway/t1-overview-deck3` `herk-kallaway/t1-overview-tricards` `recipes/card-focus-column`
- **便當格 (Bento Grid)** `bento` — 大小不一的格子拼在一起，一格大的主打、幾格小的配角。
  - 感受：現代、產品頁、有主次
  - 適合：產品功能、一個主角帶幾個細節
  - 搭配：Stagger、Spring、Pan
  - 注意：主角格要明顯大
  - 範例：`herk-kallaway/t1-overview-bento` `remocn/infinite-bento-pan`
- **議程 / 目錄 (Agenda / TOC)** `agenda` — 影片的章節列表：時間碼或編號＋章節名，目前這章亮起來。
  - 感受：有架構、知道接下來講什麼
  - 適合：長片開頭、章節之間回到目錄
  - 搭配：Stagger、Chapter Bar
  - 注意：回目錄時只亮下一章
  - 範例：`herk-kallaway/t1-overview-agenda` `herk-kallaway/t1-overview-toc` `herk-vox-explainer/t1-overview-agenda` `herk-vox-explainer/t1-overview-toc`

## 比較

- **前後對比 (Before / After)** `beforeafter` — 左右兩欄（或上下）：之前 vs 之後、做 vs 不做、優點 vs 缺點。
  - 感受：差異、改善、取捨
  - 適合：改善前後、正確 vs 錯誤做法
  - 搭配：Strike、Desaturate 舊的那邊、Versus
  - 注意：先出現「之前」，讓它停一下，再出「之後」
  - 範例：`herk-kallaway/t1-overview-beforeafter` `herk-kallaway/t1-overview-duallist` `herk-kallaway/t1-overview-proscons` `herk-vox-explainer/t1-overview-compare`
- **表格 (Table)** `table` — 髮絲線分隔的 2–3 欄表格，一列列出現，重點格加強調。
  - 感受：嚴謹、清楚、可比較
  - 適合：功能比較、規格、方案比較
  - 搭配：Stagger、Outline Draw 圈重點
  - 注意：最多 7 列；字要大
  - 範例：`kit/table-card` `herk-kallaway/t1-overview-vstable` `herk-kallaway/t1-overview-featurecompare` `herk-kallaway/t1-overview-tiercompare`
- **四象限 (Quadrant / Matrix)** `quad` — 十字線切出四格，或兩軸矩陣，東西放進對應的格子。
  - 感受：分析、策略、分類
  - 適合：兩個維度的分類（重要 × 緊急）
  - 搭配：Stagger、Spotlight
  - 注意：先畫軸、標軸名，再放內容
  - 範例：`herk-kallaway/t1-overview-quad` `herk-kallaway/t1-overview-matrix` `EP3-stitch/seg_16` `herk-vox-explainer/t1-overview-quad`
- **價格方案 (Pricing Tiers)** `pricing` — 幾個方案卡並排，推薦的那張放大、加標籤。
  - 感受：選擇、商業
  - 適合：方案比較、付費 vs 免費
  - 搭配：Circle、Spring
  - 注意：推薦方案最後出現或最後被強調
  - 範例：`herk-kallaway/t1-overview-pricing` `remocn/scribble-circle`
- **光譜 (Spectrum)** `spectrum` — 一條從一端到另一端的軸，東西放在軸上的不同位置。
  - 感受：程度、光譜、不是非黑即白
  - 適合：「從簡單到複雜」「從便宜到貴」
  - 搭配：Connector、Label Chip
  - 注意：兩端的名稱要先出現
  - 範例：`herk-kallaway/t1-overview-spectrum` `herk-kallaway/t1-stat-spectrum`

## 流程與結構

- **步驟流程 (Steps / Pipeline)** `steps` — 幾個節點由左到右（或上到下）排列，用箭頭或線連起來，依序亮起。
  - 感受：流程、方向、因果
  - 適合：工作流程、做法步驟、資料流
  - 搭配：Connector、Progress Fill、Pan
  - 注意：節點 3–6 個；線跟著口白長
  - 範例：`herk-kallaway/t1-overview-steps` `herk-kallaway/t1-overview-pipeline` `herk-vox-explainer/t1-overview-stepper` `EP3-stitch/ep3-stitch-intro`
- **循環 (Cycle)** `cycle` — 幾個階段排成一圈，箭頭繞圈，光點一直轉。
  - 感受：反覆、迭代、生態
  - 適合：「做 → 測 → 改」、回饋循環
  - 搭配：Connector、Loop
  - 注意：要講「跳出循環」時讓箭頭斷掉
  - 範例：`herk-kallaway/t1-overview-cycle` `build-test-fix-loop`
- **漏斗 (Funnel)** `funnel` — 由寬到窄的幾層，數字一層層變少。
  - 感受：篩選、轉換、聚焦
  - 適合：轉換率、篩選過程
  - 搭配：Count-up、Stagger
  - 注意：從上往下出現
  - 範例：`herk-kallaway/t1-overview-funnel` `herk-kallaway/t1-stat-funnel`
- **金字塔 / 層級 (Pyramid / Levels)** `pyramid` — 由下到上（或上到下）堆疊的層級。
  - 感受：基礎、層級、進階
  - 適合：需求層次、技能等級、優先順序
  - 搭配：Stagger、Exploded Stack
  - 注意：從底層開始長
  - 範例：`herk-kallaway/t1-overview-pyramid` `herk-kallaway/t1-overview-levels` `herk-kallaway/t1-overview-layers`
- **路線圖 (Roadmap / Milestones)** `roadmap` — 一條路或時間軸上的里程碑，可以標出「現在在這」。
  - 感受：計畫、未來、進度
  - 適合：專案規劃、系列預告、學習路徑
  - 搭配：Timeline Grow、Pan
  - 注意：已完成和未完成要有明顯差別
  - 範例：`herk-kallaway/t1-overview-roadmap` `herk-kallaway/t1-overview-milestones` `herk-kallaway/t1-overview-journey` `herk-vox-explainer/t1-overview-roadmap`
- **心智圖 / 樹狀 (Mind Map / Tree)** `mindmap` — 中心或頂端一個主題，往外長出分支。
  - 感受：發散、組織、全貌
  - 適合：概念整理、組織圖、分類
  - 搭配：Connector、Hub
  - 注意：先長第一層，講到再長第二層
  - 範例：`herk-kallaway/t1-overview-mindmap` `herk-kallaway/t1-overview-tree` `herk-kallaway/t1-overview-orgchart` `herk-kallaway/t1-overview-network`
- **文氏圖 (Venn)** `venn` — 兩三個圓重疊，交集是重點。
  - 感受：交集、剛好、平衡
  - 適合：「同時具備 A 和 B」
  - 搭配：Spotlight 交集
  - 注意：圓一個個滑進來，最後亮交集
  - 範例：`herk-kallaway/t1-overview-venn`
- **儀表板 (Dashboard / KPI Row)** `dashboard` — 幾個數字小卡、迷你圖排在一起，同時或依序跳動。
  - 感受：全面、數據驅動、專業
  - 適合：成果總覽、多個指標
  - 搭配：Count-up、Gauge、Pull-back
  - 注意：數字太多看不完——挑 3–4 個
  - 範例：`herk-kallaway/t1-overview-dashboard` `herk-kallaway/t1-overview-kpirow` `herk-kallaway/t1-overview-statgrid` `EP3-stitch/awwwards-score`

## 單一焦點

- **金句卡 (Statement Card)** `statementcard` — 一句話置中，上面可以有一行灰色引言，關鍵詞強調。
  - 感受：重要、記住這句
  - 適合：金句、結論、問句
  - 搭配：Rise、Hand Underline、Marker、Push-in
  - 注意：一句就好；字越少越有力
  - 範例：`kit/statement-card` `kit/question-card` `EP3-stitch/seg_38` `simpler-question`
- **章節字卡 (Section Card)** `sectioncard` — 「第 N 步」「Chapter 2」：大編號或大標＋副標，背景可以有浮水印。
  - 感受：段落分明、重新開始
  - 適合：章節開頭
  - 搭配：Rise、Ghost Word、Flash、Eyebrow Rule
  - 注意：全片的章節卡要長得一樣
  - 範例：`kit/step-card` `herk-kallaway/t1-section-chaptercard` `herk-kallaway/t1-section-numeral` `herk-vox-explainer/t1-section-numeral`
- **聚焦單卡 (Spotlight Card)** `spotcard` — 一張大卡置中當主角，其他退到旁邊或不出現。
  - 感受：專注、深入一件事
  - 適合：一個痛點、一個功能、一個案例
  - 搭配：One Thing at a Time、Shared Element
  - 注意：卡片內容也要有層次（編號 → 標題 → 條列）
  - 範例：`kit/problem-card` `herk-kallaway/t1-overview-spotlightcard` `recipes/card-focus-pick` `EP3-stitch/seg_11`
- **引言牆 (Quote Grid)** `quotegrid` — 幾則引言或評論排在一起，或一則大引言。
  - 感受：聲音、證據、口碑
  - 適合：使用者回饋、名人引言
  - 搭配：Testimonial、Stagger
  - 注意：每則都要讀得完
  - 範例：`herk-kallaway/t1-overview-quotegrid` `herk-kallaway/t1-stat-quotestat` `herk-vox-explainer/t2-lb-pullquote`

## 展示

- **輪播 (Carousel)** `carousel` — 一組圖片卡沿著圓圈、球面、曲線或一排移動，主角轉到前面。
  - 感受：豐富、作品集、展示
  - 適合：作品集、產品圖、截圖集
  - 搭配：Depth Stack、Orbit
  - 注意：轉速要讓人看清每一張；圖片品質要一致
  - 範例：`catalog/carousel-circle-1` `catalog/carousel-orbit-1` `catalog/carousel-path-1` `catalog/carousel-vision-1`
- **卡片堆 (Card Stack)** `cardstack` — 一疊卡片，最上面一張被抽走或扇形攤開。
  - 感受：一張張看、收藏、商品
  - 適合：產品系列、多個選項
  - 搭配：Spring、Physics
  - 注意：卡片數 3–5 張
  - 範例：`catalog-components/spring-stack-shuffle` `remotion-inspired/product-cards` `catalog-components/keyframe-scrub-stack`
- **畫面格 (Media Grid)** `mediagrid` — 2–6 格圖片或影片排在一起，或直式影片填滿橫式畫面。
  - 感受：對照、多視角、豐富
  - 適合：多個範例並排、直式素材放進橫式影片
  - 搭配：Stagger、Ken Burns
  - 注意：每格都在動時會亂
  - 範例：`catalog/mk-placeholder-grid` `catalog/yt-vertical-fill` `herk-vox-explainer/t1-overview-filmstrip` `catalog-components/screen-flow-carousel`
