# 畫面角色與用途

「這一幕是什麼」用 hf-studio 自己的詞：`<hf-studio>/kinds.json`。每個 composition 的
`manifest.json` 有 `kind: { layer, purpose: [...] }`，Gallery 也能用它篩選。這裡不另外發明詞，
只補上每一種對動態的意義。kinds.json 改了，以它為準。

## 畫面角色（layer）

| layer | 名稱 | 是什麼 | 對動態的意義 |
|---|---|---|---|
| `cutaway` | 切畫面 | 講者不在畫面上，不透明背景，取代口播 | 整個畫面都是你的：可以用鏡頭運動、背景氛圍、大字。長度通常跟一段口白一樣，所以要有「進場 → 停留 → 下一個重點」的節奏，而不是一次全部出現 |
| `overlay` | 疊畫面 | 疊在口播畫面上，透明背景 | 講者的臉才是主角：動作要小、位置避開臉（player 的「參考線」可以看安全區）、進場快、停留時不要一直動。Herk 的 tier2 卡、所有字幕、名牌都屬於這類 |
| `transition` | 轉場 | 夾在兩幕之間 | 時間很短（多半 < 1s），要和前後兩幕的節奏一致；同一支片的轉場種類越少越好 |

## 用途（purpose）

| purpose | 名稱 | 動態上通常要的 | 常見詞彙 |
|---|---|---|---|
| `section` | 章節字卡 | 有「開新的一段」的分量，進場可以大一點，然後安靜停住 | `rise` `slam` `sectioncard` `ghostword` `flash` |
| `statement` | 金句 | 一句話是唯一主角；強調只給一個關鍵詞 | `statementcard` `blurin` `marker` `handunderline` `pushin` |
| `problem` | 痛點 | 帶一點不安：劃掉、變灰、紅色、卡住 | `strike` `spotcard` `shake` `escalate` |
| `list` | 清單 | 一項一項跟著口白出現，不要一次全上 | `stagger` `numlist` `gridlist` `checklist` `onething` |
| `flow` | 流程 | 方向感：連線一段段長出、節點依序亮 | `steps` `connector` `cycle` `progressfill` |
| `compare` | 比較 | 兩邊同時存在才能比；差異點要被強調 | `beforeafter` `bawipe` `versus` `table` |
| `diagram` | 架構圖 | 先全貌、再逐塊講細節 | `hub` `exploded` `connector` `sharedelement` `pullback` |
| `stat` | 數字 | 數字本身要「動」起來，落定後停住讓人讀 | `countup` `odometer` `bars` `gauge` |
| `demo` | 畫面示範 | 像真的在操作：打字、游標、串流 | `prompt` `terminal` `cursorclick` `zoomfollow` |
| `label` | 標註 | 小、快、指向明確 | `labelchip` `callout` `arrow` `circle` |
| `lower-third` | 名牌 | 進場 < 0.6s、停留、乾淨退場 | `ltclean` `ltbold` `ltglass` |
| `caption` | 字幕 | 跟著講話時間，讀得到比好看重要 | `karaoke` `wordpop` `subtitle` |
| `cta` | 行動呼籲 | 一個明確的動作（按鈕、訂閱），最後要定住 | `subscribe` `endcard` `desccta` `logosting` |
| `progress` | 進度條 | 全程存在、幾乎不搶戲 | `chapterbar` |
| `background` | 背景 | 慢、循環、低對比 | `meshbg` `aurorabg` `patternbg` |
| `audio` | 音訊 | 跟著聲音動 | `waveform` `beat` |
