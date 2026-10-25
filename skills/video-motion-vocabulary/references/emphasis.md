# 強調與標註

指著畫面上的某個東西說「看這裡」。原則：**一次一個**。同時圈三個地方等於沒有重點。
疊在講者畫面上時，標註要小、快、指向明確。

## 手繪類

- **螢光筆 (Marker Highlight)** `marker` — 一道略微傾斜的螢光筆從左到右劃過關鍵詞，字留在筆跡上面。
  - 感受：重點、讀書筆記、親切
  - 適合：金句裡的關鍵詞、新聞頭條、文件重點
  - 搭配：Statement Card、Rise
  - 注意：筆跡在字後面；顏色飽和度不要太高
  - 範例：`catalog-components/marker-highlight` `catalog-components/inline-highlight` `remotion-inspired/text-annotation` `remocn/caption-marker`
- **手繪底線 (Hand Underline)** `handunderline` — 一條手繪感的線從左到右畫在關鍵詞下面（起筆粗、收筆細）。
  - 感受：強調但不吵、有溫度
  - 適合：問句、金句的關鍵詞——頻道問句字卡的固定手法
  - 搭配：Question Card、Write-on
  - 注意：只畫一個詞
  - 範例：`recipes/hand-underline` `kit/question-card` `catalog-components/hw-underline` `remocn/ink-underline`
- **手繪圈選 (Hand Circle)** `circle` — 一個不太圓的手繪圈繞住目標，繞一圈多一點、收尾超出一點。
  - 感受：「就是這個」、手作、教學
  - 適合：價目表選項、地圖位置、截圖裡的按鈕
  - 搭配：Arrow、Label Chip
  - 注意：圈的線條要比目標粗一點才看得到
  - 範例：`catalog-components/hw-callout-circle` `remocn/scribble-circle` `catalog-components/yt-circle-pointer` `catalog/north-korea-locked-down`
- **手繪箭頭 (Hand Arrow)** `arrow` — 一支彎彎的手繪箭頭從標籤畫向目標，最後畫箭頭頭。
  - 感受：指引、筆記、溫暖
  - 適合：連接標籤和目標、指出畫面裡的東西
  - 搭配：Circle、Label Chip
  - 注意：箭頭彎的方向要自然（從上方繞下來最順）
  - 範例：`catalog-components/hw-arrow` `remocn/ink-arrow` `catalog-components/cursor-annotate`
- **劃掉 (Strike)** `strike` — 一條線（或兩條）劃過字或卡片，常伴隨變灰。
  - 感受：否定、修正、「不是這個」
  - 適合：痛點、舊方法、迷思
  - 搭配：Strikethrough Replace、Desaturate
  - 注意：劃之前要讓觀眾先讀到
  - 範例：`catalog-components/strikethrough-replace` `herk-vox-explainer/t1-section-correction` `catalog-components/hw-underline`

## 光與聚焦

- **聚光壓暗 (Spotlight / Feather Dim)** `spotlight` — 整個畫面變暗，只有一個羽化的圓形或區塊保持亮。
  - 感受：聚焦、戲劇性、專業教學
  - 適合：截圖、介面、程式碼裡的某一處
  - 搭配：Zoom-follow、Callout
  - 注意：亮區要比目標大一圈
  - 範例：`catalog-components/yt-feather-highlight` `catalog/code-highlight` `herk-vox-explainer/t2-lb-spotlight`
- **放大鏡 (Magnifier)** `magnify` — 一個放大鏡圈移到某處，圈裡的東西放大。
  - 感受：細看、偵探、發現
  - 適合：小字、細節、圖表裡的一個點
  - 搭配：Spotlight
  - 注意：放大鏡裡的內容要真的是放大的同一區
  - 範例：`herk-vox-explainer/t2-lb-magnify` `herk-vox-explainer/t1-stat-magnifier`
- **掃光 (Shine Sweep)** `shine` — 一道斜的白光從左掃到右，掃過卡片、圖片或字。
  - 感受：高級、新、閃亮
  - 適合：產品圖、新功能、結果揭曉
  - 搭配：Gloss Sweep、Spring Pop
  - 注意：只掃一次或隔很久掃一次
  - 範例：`remotion-inspired/shine` `catalog-components/light-sweep-pass` `catalog-components/gloss-sweep`
- **外框描繪 (Outline Draw)** `outlinedraw` — 一條線沿著目標的外框順時針畫一圈，把它框起來。
  - 感受：精準、證明、「這一區」
  - 適合：介面的一塊、表格的一欄、卡片
  - 搭配：Label Chip、Tracing Beam
  - 注意：框要比目標留一點空隙
  - 範例：`catalog-components/outline-draw` `catalog-components/svg-stroke-trace` `herk-kallaway/t2-lb-highlightbox`

## 標籤與印記

- **標註小卡 (Label Chip)** `labelchip` — 一個小標籤出現在畫面某處：主字＋小字，旁邊一條強調色細線。
  - 感受：清楚、資訊、不打擾
  - 適合：疊在講者畫面上提示名詞、操作步驟、數值
  - 搭配：Arrow、Callout、Clip Wipe
  - 注意：避開講者的臉；停留到講完再退場
  - 範例：`kit/label-chip` `herk-kallaway/t2-lb-tag` `herk-kallaway/t2-lb-iconchip` `herk-vox-explainer/t2-lb-sticky`
- **引線標註 (Callout Leader)** `callout` — 一條線從畫面上的點拉出去，線尾接一個說明。
  - 感受：圖解、技術、說明書
  - 適合：產品部位、圖表的某個點、架構圖
  - 搭配：Exploded Stack、Spotlight
  - 注意：引線不要互相交叉
  - 範例：`herk-kallaway/t2-lb-callout` `herk-kallaway/t2-lb-leader` `catalog-components/arc-motion-path`
- **蓋章 (Stamp)** `stamp` — 一個印章「砰」地蓋上去，略歪、有磨損感。
  - 感受：定案、官方、警告、Vox 風
  - 適合：「已完成」「機密」「NO」、章節標題
  - 搭配：Impact、Paper、Redact
  - 注意：有一點晃動和放大縮回才像真的蓋
  - 範例：`herk-vox-explainer/t1-section-stamp` `herk-vox-explainer/t1-stat-stamp` `remocn/caption-stamp`
- **放射爆線 (Burst Lines)** `burst` — 從一點向外迸出幾道短線，像漫畫的「叮！」。
  - 感受：靈光一閃、驚喜、注意
  - 適合：想法出現、按鈕被按、關鍵詞旁
  - 搭配：Spring Pop、Icon
  - 注意：很短（< 0.3s）
  - 範例：`remocn/trim-burst` `catalog-components/confetti`
- **選取框 (Selection Snap)** `selection` — 像設計軟體或滑鼠選取：一個框（或反白）拉過文字，吸附到正確的範圍。
  - 感受：精準、工具感、「這段」
  - 適合：答案裡的重點句、文件裡的一段
  - 搭配：Cursor、Marker
  - 注意：選取速度要像人手
  - 範例：`remocn/selection-snap` `snapcn/answer-highlight` `catalog-components/cursor-text-select`
- **晃動提醒 (Nudge)** `nudge` — 一個標籤或徽章停在那裡，每隔一段時間晃一下或跳一下提醒你。
  - 感受：俏皮、促銷、別忘了
  - 適合：折扣、新功能、CTA
  - 搭配：Spring、Badge
  - 注意：間隔要夠長（3s 以上），不然很煩
  - 範例：`remotion-inspired/discount-callout` `catalog-components/badge-pop`
- **環繞標籤 (Radial Surround)** `radial` — 一個主體在中間，幾個標籤繞成一圈出現在周圍。
  - 感受：屬性、面向、全方位
  - 適合：「它有這些特點」、一個概念的多個面向
  - 搭配：Hub、Orbit
  - 注意：標籤 4–8 個
  - 範例：`catalog-components/radial-surround` `catalog-components/locked-nucleus-orbit`
