# 白話感受 → 候選詞

使用者說的是感受，不是術語。先在這裡找到最接近的說法，拿到候選詞的 `id`，
再到對應的分類檔讀完整定義。候選詞是討論的起點，不是答案——依網站目的挑 2–3 個。

每組的「分辨」是用來縮小範圍的問題：選一個最能改變方向的問，不要全部問。

## 整體感受

### 高級、有質感、有品牌感
- 雜誌式品牌觀點：`editorial` `serif` `bigtype` `asym`
- 安靜克制的精品感：`minimal` `gray1` `morandi` `greige` `hairline` `tracking`
- 奢華、尊貴：`blackgold` `deco` `marble`
- 分辨：要「有觀點、有個性」（Editorial），還是「安靜、低調」（Minimalism），還是「奢華」（Black & Gold）？

### 高級但不要太制式
- `editorial` `asym` `broken` `serif` `grain`
- 分辨：「不制式」是指版面要打破格子（Broken Grid / Asymmetric），還是質感要有溫度（Grain / Serif Revival）？

### 乾淨、簡潔、專業
- `swiss` `minimal` `gray1` `singlecol` `contrast`
- 分辨：要理性、資訊清楚（Swiss），還是留白多、聚焦單一重點（Minimalism）？

### 科技感、未來感
- 精緻現代：`darksaas` `aurora` `glass` `gborder` `beams` `gridbg`
- 硬派科幻：`cyber` `hud` `glitch` `neon` `glow`
- 冷冽未來：`y3k` `chrome` `liquid` `space`
- 分辨：要像「現在的 AI 新創」（Dark SaaS），還是「科幻電影」（Cyberpunk / HUD）？

### 活潑、有趣、年輕
- 大膽撞色：`neob` `memphis` `dopamine` `colorblock`
- 可愛柔軟：`clay` `kawaii` `macaron` `spring`
- 手作隨性：`doodle` `sticker` `annot` `collage`
- 分辨：要「大膽有態度」、「可愛療癒」，還是「手作親切」？

### 溫暖、自然、療癒
- `japandi` `earth` `grain` `morandi` `wood` `lofi`
- 分辨：偏東方寧靜（Japandi），還是偏生活風格的溫度（Earth Tones + Grain）？

### 有個性、前衛、藝術感
- `brutal` `neob` `broken` `collage` `zine` `riso` `bigtype`
- 分辨：要「刻意粗糙的態度」（Brutalist），還是「有設計感的張力」（Broken Grid / Editorial）？

### 復古、懷舊
- 80s：`retro` `memphis` `vapor`
- 千禧年：`y2k` `aero` `chrome`
- 印刷與報刊：`riso` `halftone` `news` `zine`
- 早期電腦與網路：`pixel` `dither` `oldweb` `terminal`
- 分辨：懷念的是哪個年代？

### 東方、文化感
- `inkwash` `japandi` `guochao` `vertical` `ukiyoe` `folk`
- 分辨：要寧靜留白（水墨／侘寂），還是熱鬧自信（國潮）？

### 可信、穩重（金融、醫療、政府、B2B）
- `swiss` `contrast` `mono` `gray1` `singlecol` `social`
- 分辨：通常不需要問風格；優先討論資訊層級與信任元素（Social Proof）。

### 開發者感、工程師氣質
- `terminal` `monofont` `gridbg` `darksaas` `cmdk` `wire`
- 分辨：要「硬派命令列」（Terminal），還是「精緻開發者工具」（Dark SaaS + Grid Background）？

## 「像某某網站」

這些是常被拿來當參考的網站類型與它們常見的語彙。說明時用「這類網站常見…」，
不要宣稱某網站目前一定長這樣。

- **像 Apple 官網**：`bigtype` `minimal` `floatprod` `scrolly` `pinned` `scrollzoom` `sticky`
- **像 Linear／新一代 SaaS**：`darksaas` `gborder` `gridbg` `glow` `cmdk` `bento`
- **像 Stripe**：`aurora` `diagonal` `gtext` `iso`
- **像 Notion**：`doodle` `minimal` `singlecol` `gray1`
- **像時尚雜誌／精品**：`editorial` `serif` `tracking` `fullbleed` `hairline`
- **像 Pinterest**：`masonry` `card` `infinite`
- **像遊戲官網**：`gameui` `cyber` `pixel` `cel` `ptrans`
- **像 Awwwards 得獎作品**：`kinetic` `magnet` `ptrans` `maskrev` `broken` `scrolly`

## 動態與互動

### 網站要「很有動態」
- 敘事型：`scrolly` `pinned` `scrollzoom` `parallax`
- 精緻細節：`reveal` `stagger` `micro` `magnet`
- 文字動態：`kinetic` `typewriter` `marquee`
- 分辨：要「捲動時講故事」（Scrollytelling），還是「整體很順、有細節」（Reveal + Micro-interactions）？還是只有標題要動？

### 動態要「低調、精緻」
- `reveal` `stagger` `easing` `micro` `stateful`

### 滑鼠移過去要有反應
- `magnet` `tilt` `hoverrev` `spot` `trail`
- 分辨：只有按鈕（Magnetic），還是卡片（Tilt / Hover Reveal），還是整個背景（Spotlight / Cursor Trail）？

### 載入、等待不要很無聊
- `skeleton` `loading` `stream` `optim`

## 特定效果的白話描述

使用者常描述效果、卻不知道名字。直接對應：

- 透明、漂浮在背景上的卡片 → `glass`（若要更像 Apple 新版：`liquid`）
- 像黏土、軟軟膨膨的 → `clay`
- 背景是會流動的彩色霧 → `aurora`
- 底片顆粒、有點粗糙的漸層 → `grain`
- 黑底配發光的線 → `glow` `rim` `beams`
- 按鈕會跟著游標吸過去 → `magnet`
- 往下捲時畫面卡住、內容在裡面換 → `pinned`
- 捲動時背景跟前景速度不同 → `parallax`
- 一直橫向跑的文字帶 → `marquee`
- 字很大、字本身就是主視覺 → `bigtype`
- 文字裡面有影片或照片 → `tmask`
- 卡片隨滑鼠傾斜、有反光 → `tilt`
- 首頁被切成格子、大小不一的方塊 → `bento`
- 圖文故意疊在一起、超出格線 → `broken`
- 粗黑框加偏移的實心陰影 → `neob`
- 按 ⌘K 跳出搜尋框 → `cmdk`
- 膠囊形、懸浮、背景模糊的導覽列 → `floatnav`
- 數字從 0 跑到目標值 → `countup`

## 頁面區塊

### Hero／首屏要有特色
- 布局：`hero` `split` `fullbleed` `asym` `broken`
- 主角：`bigtype` `videobg` `render3d` `floatprod` `kinetic`
- 背景：`aurora` `beams` `gridbg` `particles`

### 作品集
- `masonry` `editorial` `hscroll` `hoverrev` `ptrans` `magnet` `asym`

### 功能介紹
- `bento` `stacked` `pinned` `sidebyside` `iso`

### 定價方案
- `sidebyside` `card` `gborder` `social` `prog`

### 部落格、文章、文件
- `singlecol` `serif` `dropcap` `readprog` `scrollspy`

### 數據、後台
- `dash` `statcard` `sparkline` `tabnum` `cmdk` `facets`

## 模糊詞要拆開

這些詞每個人想的不一樣。使用者用到時，用具體的視覺特徵說明你理解的意思，
或給兩個具體方向讓對方選：

- **現代**：Dark SaaS 式的精緻？Swiss 式的理性？還是 Neo-Brutalism 式的大膽？
- **簡潔**：元素少（Minimalism）？還是資訊排得整齊（Swiss）？
- **大氣**：大圖滿版（Full-bleed）？大字（Big Type）？還是大量留白？
- **有設計感**：版面有張力（Broken Grid / Asymmetric）？還是字體講究（Serif Revival / Font Pairing）？
- **酷**：暗色科技（Dark SaaS / Cyberpunk）？還是有態度（Brutalist）？
- **專業**：Swiss 的秩序感，加上高對比可讀性
