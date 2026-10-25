# 疊加元件

疊在口播畫面上的固定元件：名牌、社群卡、訂閱、片尾、Logo、進度條。
共同規則：避開講者的臉、進場快、停留時不亂動、退場乾淨。

## 名牌（Lower Third）

- **極簡名牌 (Minimal Lower Third)** `ltclean` — 沒有底卡或只有細卡：名字升起、一條強調色細線畫出、職稱淡入。
  - 感受：乾淨、專業、Podcast / 訪談
  - 適合：大部分訪談、知識型頻道
  - 搭配：Rise、Clip Wipe
  - 注意：亮背景要有文字陰影
  - 範例：`catalog/lt-accent-underline` `catalog/lt-clean-bar` `catalog/lt-side-rule` `catalog/lt-soft-pill`
- **大膽色塊名牌 (Bold Block Lower Third)** `ltbold` — 實心色塊從側邊擦進來（帶過衝），大寫粗字名字砸上去。
  - 感受：高能、運動、YouTuber
  - 適合：高能量節目、遊戲、運動
  - 搭配：Spring、Slam
  - 注意：色塊面積大，會搶畫面
  - 範例：`catalog/lt-bold-block` `catalog/lt-color-block` `catalog/lt-stack-bars` `catalog/lt-kicker-name`
- **新聞名牌 (Broadcast Lower Third)** `ltnews` — 新聞台式：白底標題條、紅色副標、跑馬燈。
  - 感受：新聞、可信、正式、即時
  - 適合：新聞評論、時事、「快訊」梗
  - 搭配：Ticker、News Headline
  - 注意：太像真新聞台時要小心誤導
  - 範例：`catalog/lower-third-bild` `catalog/news-ticker`
- **玻璃名牌 (Glass Lower Third)** `ltglass` — 毛玻璃卡片彈上來，邊緣一道細光，名字和職稱滑入。
  - 感受：科技、精緻、深色系
  - 適合：科技頻道、Kallaway 風格
  - 搭配：Glass、Aurora、Spring
  - 注意：背景太亂時玻璃看不出來
  - 範例：`herk-kallaway/t2-lt-glasscard` `herk-kallaway/t2-lt-capsule` `herk-kallaway/t2-lt-minimal`
- **霓虹名牌 (Neon Lower Third)** `ltneon` — 兩道光沿著名牌框邊緣跑，在角落接上，帶柔光。
  - 感受：夜晚、遊戲、電競
  - 適合：遊戲、直播、音樂
  - 搭配：Neon Caption
  - 注意：亮背景失效
  - 範例：`catalog/lt-neon-border` `herk-kallaway/t2-lt-neonframe` `herk-kallaway/t2-lt-neonpill`
- **紙質名牌 (Paper Lower Third)** `ltpaper` — 便利貼、印章、膠帶、打字卡片風格的名牌。
  - 感受：手作、Vox、溫暖
  - 適合：Vox 風格的解說、手作類
  - 搭配：Stamp、Scrapbook
  - 注意：要配紙質的整體風格
  - 範例：`herk-vox-explainer/t2-lt-sticky` `herk-vox-explainer/t2-lt-stamp` `herk-vox-explainer/t2-lt-typecard` `herk-vox-explainer/t2-lt-clapper`
- **地點名牌 (Location Lower Third)** `ltlocation` — 圖釘掉下來、壓扁回彈，地名和副標擦出來。
  - 感受：旅行、紀錄片、到了某地
  - 適合：Vlog、旅遊、場景切換
  - 搭配：Map Zoom、Spring
  - 注意：圖釘的彈跳是記憶點，其他要收斂
  - 範例：`remotion-inspired/location-lower-third` `herk-kallaway/t2-lt-geopin` `herk-kallaway/t2-lt-location`

## 社群與行動呼籲

- **社群貼文卡 (Social Post Card)** `socialcard` — X、Reddit、YouTube 留言的卡片彈出來，讚數跳上去。
  - 感受：社會證明、真實、網路聲量
  - 適合：引用網友、留言回應、輿論
  - 搭配：Count-up、Spring
  - 注意：真實帳號要去識別化
  - 範例：`catalog/x-post` `catalog/reddit-post` `catalog/yt-comment-card` `remotion-inspired/youtube-comment`
- **訂閱提示 (Subscribe Nudge)** `subscribe` — 頻道卡片彈出，游標按下訂閱鈕，變成「已訂閱」＋小鈴鐺。
  - 感受：友善提醒、標準 YouTube
  - 適合：開場後、高潮前、片尾
  - 搭配：Cursor Click、Spring
  - 注意：一支片 1–2 次；不要蓋到重要內容
  - 範例：`remotion-inspired/youtube-subscribe-nudge` `catalog/yt-lower-third` `catalog/instagram-follow` `catalog-components/x-follow-card`
- **資訊欄提示 (Description CTA)** `desccta` — 角落一個膠囊：往下箭頭＋「資訊欄免費下載」＋資源名稱。
  - 感受：貼心、實用
  - 適合：提到可下載資源、連結的時候
  - 搭配：Label Chip
  - 注意：頻道 kit 元件，位置固定在右下
  - 範例：`kit/description-cta` `EP3-stitch/seg_15-o1`
- **片尾卡 (End Card)** `endcard` — 片尾畫面：「謝謝收看」、下一支影片框、訂閱鈕、一句話收尾。
  - 感受：完整、有始有終
  - 適合：每集最後 10–20 秒
  - 搭配：Subscribe、Logo Sting
  - 注意：YouTube 片尾元素的位置要預留
  - 範例：`remotion-inspired/youtube-end-card` `kit/subscribe-outro` `catalog-components/cta-lockup` `catalog-components/cta-close`
- **評價卡 (Testimonial)** `testimonial` — 一則使用者評價依閱讀速度出現，再放上頭像、名字、星等。
  - 感受：可信、口碑
  - 適合：產品推薦、案例
  - 搭配：Rating、Logo Wall
  - 注意：字要讀得完
  - 範例：`catalog-components/testimonial-card` `catalog-components/testimonial-proof-card` `catalog-components/social-proof-card`
- **信任牆 (Logo Wall)** `logowall` — 一排或一牆的品牌 logo 依序淡入。
  - 感受：規模、可信、被採用
  - 適合：「這些公司都在用」、合作夥伴
  - 搭配：Stagger
  - 注意：logo 統一成單色比較整齊
  - 範例：`catalog-components/logo-wall` `catalog-components/trust-strip` `herk-kallaway/t1-overview-logowall`

## 品牌與資訊列

- **Logo 定版 (Logo Sting)** `logosting` — Logo 砸進定位（或一片片組合起來），一道光或衝擊，然後完全靜止。
  - 感受：品牌、完成、正式
  - 適合：片頭最後一拍、片尾
  - 搭配：Impact、Flash、Shine
  - 注意：1.5–3 秒；完成後一定要停住
  - 範例：`catalog-components/logo-sting` `catalog-components/logo-brand-close` `catalog/logo-outro` `catalog/yt-logo-intro`
- **章節進度條 (Chapter Progress Bar)** `chapterbar` — 畫面邊緣一條細細的進度條，分成章節，跟著影片進度前進。
  - 感受：清楚、不迷路
  - 適合：長的教學、多章節影片
  - 搭配：Section Card
  - 注意：要細、要淡，全程存在不能搶戲
  - 範例：`youtube-progress-bar` `herk-kallaway/t2-lt-chapterbar`
- **快捷鍵提示 (Keystroke)** `keystroke` — 畫面下方浮出立體鍵帽，依序按下快捷鍵。
  - 感受：教學、具體、可以照做
  - 適合：軟體教學、操作示範
  - 搭配：Cursor Click、Zoom-follow
  - 注意：按鍵順序和時間要跟口白一致
  - 範例：`remocn/keystroke` `herk-kallaway/t2-lb-keycap`
- **錄影介面 (Camcorder HUD)** `camhud` — REC 紅點、電池、時間碼、角框——像透過攝影機在看。
  - 感受：紀錄、真實、復古 DV、監視
  - 適合：Vlog、幕後花絮、「現場」感
  - 搭配：Film Grain、Shake
  - 注意：是畫面處理，不是資訊——內容要另外放
  - 範例：`catalog/camcorder-hud` `catalog-components/telemetry-hud`
