# 數據與圖解

數字、圖表、地圖、架構圖怎麼動。原則：**先讓人看懂結構，再讓數字動**；
數字落定後要停住，給觀眾讀的時間。卡片怎麼排（儀表板、四象限、漏斗）在 `layouts.md`。

## 數字

- **數字跳動 (Count-up)** `countup` — 數字從 0（或起始值）快速往上數，接近目標時減速，落定時微微放大一下。
  - 感受：成長、成就、有分量
  - 適合：任何統計數字、金額、用戶數
  - 搭配：Impact、Progress Fill、Ease-out
  - 注意：1–2 秒內數完；小數和千分位要先決定
  - 範例：`recipes/count-up` `catalog-components/count-up` `remotion-inspired/number-counter` `catalog/apple-money-count`
- **里程表 (Odometer)** `odometer` — 每一位數字是一個滾輪，各自滾到目標數字。
  - 感受：機械、精確、累積
  - 適合：星星數、訂閱數、價格、計分板
  - 搭配：Count-up、Slot Roll
  - 注意：位數變多時（999 → 1000）要預留寬度
  - 範例：`catalog-components/number-wheel` `herk-kallaway/t1-stat-odometer` `remocn/github-stars` `herk-vox-explainer/t1-stat-odo`
- **數字對比 (Versus / Delta)** `versus` — 兩個數字並排或前後出現，差距用箭頭、顏色、百分比強調。
  - 感受：差距、改善、選擇
  - 適合：前後對比、A vs B、成長率
  - 搭配：Count-up、Before/After
  - 注意：先出現比較小的那個
  - 範例：`herk-kallaway/t1-stat-versus` `herk-kallaway/t1-stat-delta` `herk-kallaway/t1-stat-beforeafter` `herk-vox-explainer/t1-stat-vs`

## 圖表

- **長條成長 (Bar Grow)** `bars` — 長條一根根從底部長出來，數值標在頂端跟著跳。
  - 感受：清楚、比較、可信
  - 適合：類別比較、排名、預算分配
  - 搭配：Stagger、Count-up
  - 注意：長條順序要有意義（大到小，或時間順序）
  - 範例：`catalog-components/animated-bar-chart` `remotion-inspired/bar-chart` `catalog/data-chart` `catalog-components/chart-story`
- **排名競賽 (Bar Chart Race)** `barrace` — 隨時間推進，長條互相超越、排名一直變，軸線跟著縮放。
  - 感受：戲劇性、競爭、歷史
  - 適合：長時間序列、排名變化
  - 搭配：Timeline、Count-up
  - 注意：資料點要多；整段至少 5 秒才看得出變化
  - 範例：`catalog/bar-chart-race` `unemployment-race` `unemployment-race-5s` `catalog/week-in-merges`
- **折線畫出 (Line Draw)** `linedraw` — 格線先展開，折線從左畫到右，資料點在畫筆經過時彈出。
  - 感受：趨勢、時間、故事
  - 適合：成長、下滑、時間變化
  - 搭配：Annotation、Count-up
  - 注意：要講「下滑」時可以讓背景跟著變暗
  - 範例：`catalog/mk-line-graph` `remotion-inspired/line-chart` `catalog-components/decline-chart` `herk-kallaway/t1-stat-trendline`
- **圓餅掃開 (Pie Sweep)** `pie` — 扇形從 12 點鐘方向順時針掃開，一塊塊出現。
  - 感受：比例、組成
  - 適合：佔比、市佔、時間分配
  - 搭配：Legend、Count-up
  - 注意：超過 5 塊就換長條圖
  - 範例：`remotion-inspired/pie-chart` `herk-kallaway/t1-stat-donut` `herk-vox-explainer/t1-stat-pie`
- **環形儀表 (Gauge / Ring)** `gauge` — 一個圓環或半圓儀表畫到目標百分比，中間數字同步數上去。
  - 感受：達成度、健康度、儀表板
  - 適合：完成率、分數、使用率
  - 搭配：Count-up、Dashboard
  - 注意：圓環和數字要用同一條時間曲線
  - 範例：`catalog-components/conic-progress-ring` `catalog-components/mk-usage-arc` `herk-kallaway/t1-stat-semigauge` `herk-kallaway/t1-stat-needle`
- **進度條灌滿 (Progress Fill)** `progressfill` — 一條進度條從左灌到目標位置，可以分段、打勾。
  - 感受：進展、完成、階段
  - 適合：步驟完成、專案進度、百分比
  - 搭配：Steps、Check
  - 注意：灌到 100% 時給一個完成的回饋
  - 範例：`recipes/progress-fill` `catalog/mk-progress-stat` `herk-kallaway/t1-stat-meter` `outro-recap`
- **象形圖 (Isotype / Waffle)** `isotype` — 用一格格小人或方塊表示數量，一個個亮起來。
  - 感受：具體、人性化、好懂
  - 適合：「每 10 個人就有 3 個」這種比例
  - 搭配：Stagger
  - 注意：總格數 10、20、100 最好讀
  - 範例：`herk-kallaway/t1-stat-isotype` `herk-kallaway/t1-stat-waffle` `herk-vox-explainer/t1-stat-dots`
- **星等 (Rating Fill)** `rating` — 一排星星的顏色從左掃到評分位置，最後一顆可以是部分填滿。
  - 感受：評價、口碑
  - 適合：產品評分、評論
  - 搭配：Testimonial
  - 注意：部分星要精確
  - 範例：`catalog-components/star-rating-fill`
- **聲波 (Waveform)** `waveform` — 跟著聲音跳動的波形、頻譜條、示波器光束。
  - 感受：聲音、Podcast、音樂
  - 適合：Podcast 片段、音樂、語音功能
  - 搭配：Audiogram、Beat Sync
  - 注意：要用真的音訊資料驅動才自然
  - 範例：`remotion-inspired/audio-visualizer` `remotion-inspired/audiogram` `catalog/waveform` `catalog/oscilloscope-trace`

## 地圖

- **地圖填色 (Choropleth)** `mapfill` — 區域一塊塊依數值填上顏色，圖例跟著出現。
  - 感受：地理分布、宏觀
  - 適合：各國、各州、各縣市的數據
  - 搭配：Stagger、Legend
  - 注意：顏色深淺要一眼看得出高低
  - 範例：`catalog/us-map` `catalog/world-map` `catalog/spain-map` `catalog/us-map-hex`
- **航線 (Flight Path)** `flight` — 地圖上一條弧線從 A 畫到 B，飛機或光點沿著飛過去，抵達時彈一下。
  - 感受：旅行、移動、連結
  - 適合：旅遊、搬家、物流、跨國
  - 搭配：Map Zoom、Location Lower Third
  - 注意：弧線比直線好看
  - 範例：`catalog/nyc-paris-flight` `nyc-paris-flight` `remotion-inspired/watercolor-map` `catalog/us-map-flow`
- **地圖拉近標記 (Map Zoom & Pin)** `mapzoom` — 地圖從遠處拉近到某一處，畫圈、插針、彈出標籤。
  - 感受：Vox 解說、新聞、「就在這裡」
  - 適合：講到一個地點
  - 搭配：Circle、Stamp、Label Chip
  - 注意：拉近時要有減速
  - 範例：`catalog/north-korea-locked-down` `herk-kallaway/t1-overview-mappoints` `catalog/us-map-bubble` `herk-vox-explainer/t1-section-map`

## 圖解

- **節點連線 (Connector Draw)** `connector` — 節點之間的線（實線、虛線、彎線）一段段畫出來，光點沿線流過去。
  - 感受：流程、關係、因果
  - 適合：流程圖、資料流、系統架構
  - 搭配：Steps、Hub、Stagger
  - 注意：線要跟著口白一段段長，不是一次全畫
  - 範例：`recipes/dashed-connector` `catalog-components/tracing-beam` `catalog/hw-pipeline` `catalog/flowchart`
- **中心放射 (Hub & Spokes)** `hub` — 中間一個主體，周圍的節點依序亮起，連線從中心往外畫。
  - 感受：生態系、整合、核心
  - 適合：「它可以接這些服務」、一個工具的周邊
  - 搭配：Connector、Radial Surround
  - 注意：周圍節點 4–8 個
  - 範例：`catalog-components/constellation-hub` `remocn/ecosystem-constellation` `catalog-components/avatar-cloud`
- **爆炸分層 (Exploded Stack)** `exploded` — 一疊東西往上下分開，每層旁邊出現標籤，講完再合回去。
  - 感受：解剖、技術、架構
  - 適合：技術堆疊、系統分層、產品結構
  - 搭配：Callout Leader、Layers
  - 注意：層數 3–6 層
  - 範例：`catalog/exploded-stack` `herk-kallaway/t1-overview-layers` `obs-core`
- **時間軸長出 (Timeline Grow)** `timelinegrow` — 一條時間軸畫出來，事件點一個個沿著出現。
  - 感受：歷程、進度、敘事
  - 適合：歷史、專案階段、路線圖
  - 搭配：Pan、Connector
  - 注意：點的間距要對應真實時間嗎？先決定
  - 範例：`herk-kallaway/t1-overview-timeline` `herk-vox-explainer/t1-timeline` `kit/subscribe-outro` `channel-subscribe-intro`
- **前後拉霸 (Before/After Wipe)** `bawipe` — 同一個畫面的前後兩個版本疊著，中間一條分隔線滑過去露出新版本。
  - 感受：改善、對比、證明
  - 適合：修圖、改版、優化前後
  - 搭配：Versus、Label Chip
  - 注意：兩張要完全對齊
  - 範例：`catalog-components/before-after-wipe` `catalog-components/comparison-split` `catalog-components/grade-split-reveal`
- **頭像湧入 (Crowd Rush)** `crowd` — 頭像一個個疊上來排成一排或一團，數字跟著跳。
  - 感受：熱度、社群、很多人
  - 適合：追蹤者、贊助者、社群規模
  - 搭配：Count-up、Escalation
  - 注意：頭像要去識別化
  - 範例：`snapcn/follower-rush` `remocn/github-sponsors` `remocn/x-followers-overview`
