# 白話感受 → 候選詞

使用者說的是感受，不是術語。先在這裡找到最接近的說法，拿到候選詞的 `id`，
再到對應的分類檔讀完整定義和範例。候選詞是討論的起點，不是答案——依這一幕的角色和用途挑 2–3 個。

每組的「分辨」是用來縮小範圍的問題：選一個最能改變方向的問，不要全部問。

## 整體手感

### 俐落、專業、不要花俏
- `easeout` `rise` `clipwipe` `stagger` `hardcut` `onething`
- 分辨：俐落是指「快」（進場 0.3s、硬切多），還是「乾淨」（動作少、每個都很準）？

### 高級、有質感、電影感
- 安靜的高級：`blurin` `trackingin` `calm` `creep` `film` `kenburns`
- 鏡頭語言的電影感：`pushin` `rackfocus` `dollyzoom` `lightleak`
- 大製作：`type3d` `cinematic3d` `orbit` `object3d`
- 分辨：要「安靜、慢、留白」，還是「鏡頭在說故事」，還是「片頭很有規模」？

### 活潑、可愛、有趣
- `spring` `letterdrop` `stopmotion` `stopmotionpaper` `nudge` `burst` `physics`
- 分辨：要「彈來彈去的 App 感」（Spring），還是「手作的可愛」（Stop-motion / 紙感）？

### 有衝擊、這句要很有力
- `slam` `impact` `shake` `flash` `punchin` `dollyzoom`
- 分辨：是「一個詞砸下來」（Slam），還是「整個畫面震一下」（Flash / Shake），還是「鏡頭突然靠近」（Punch-in）？
- 注意：衝擊靠對比——前面要夠安靜

### 高能、短影音感、停不下來
- `shortform` `wordpop` `punchy` `beat` `hardcut` `whippan` `keywordcap`
- 分辨：整支都這樣，還是只有開場 5 秒？

### 安靜、沉穩、可信
- `calm` `fade` `blurin` `subtitle` `breathe` `ltclean`
- 分辨：可信是要「像新聞」（Broadcast），還是「像紀錄片」（Calm + Film）？

### 科技感、未來感
- 精緻的 AI / SaaS：`kallaway` `aurorabg` `glass` `shimmer` `gridbg` `aistream`
- 駭客、系統：`scramble` `glitchtext` `terminal` `crt` `machinevision`
- 科幻大片：`orb` `particletext` `tunnel` `halftone`
- 分辨：要像「現在的 AI 新創」，還是「駭客電影」，還是「科幻片頭」？

### 手作、溫度、親切
- `handdrawn` `writeon` `handunderline` `circle` `arrow` `boil` `whiteboard` `scrapbook`
- 分辨：要「白板上邊畫邊講」（Whiteboard），還是「筆記上的重點」（Marker / Underline），還是「剪貼簿」（Scrapbook）？

### 像在講故事、紀錄片
- `kenburns` `pushin` `film` `cinemagraph` `cameracap` `oner` `lightleak`
- 分辨：故事是「人的回憶」（Light Leak、Film），還是「一個過程」（Oner、Pan）？

## 參考對象

### 像 Vox / 解說新聞
- `vox` `mapzoom` `marker` `stamp` `scrapbook` `callout` `strike`
### 像 MrBeast / 短影音
- `shortform` `wordpop` `slam` `punchin` `beat` `outlinecap`
### 像 Apple 發表會 / 產品片
- `applepromo` `spring` `device` `countup` `shine` `magnetcursor`
### 像新聞台
- `broadcast` `ltnews` `subtitle`
### 像 Kallaway 那種深色科技口播
- `kallaway` `ltglass` `aurorabg` `stagger`
### 像螢幕錄影教學（但更乾淨）
- `zoomfollow` `cursorclick` `keystroke` `spotlight` `pip`
### 像這個頻道之前的影片
- `softaverse` `onething` `sharedelement` `connector` `handunderline` — 先讀 `<hf-studio>/compositions/DESIGN.md`

## 問題描述（「怪怪的」該怎麼改）

### 太平了、太無聊、像 PPT
- 加鏡頭：`pushin` `kenburns` `pullback`
- 加層次：`ghostword` `depthstack` `meshbg`
- 給一個重點：`marker` `handunderline` `slam`（只給一個）
- 分辨：是「畫面停太久沒變化」（加鏡頭／呼吸），還是「每個東西都一樣重」（給一個重點）？

### 太亂了、太吵
- `onething` `calm` `stagger`（降低同時動的數量）
- 檢查：是不是背景動得比主角多？是不是三種轉場混用？是不是每個元素都在彈？

### 太慢、拖
- 進場改 0.3–0.5s、`easeout`、`hardcut` 取代 `fade`、`stagger` 間隔縮短

### 太快、看不完
- 數字落定後停 1 秒以上（`impact` 而不是一直動）、清單改成跟著口白出現、`calm`

### 太廉價
- 常見原因：每個元素都彈（`spring` 只給小東西）、線性移動（改 `easeout` / `creep`）、
  轉場太多種（收斂成 `hardcut` + 一種）、閃光和故障用在不對的情緒
- 補質感：`film` `blurin` `breathe` `shine`（一次）

### 擋到講者 / 疊畫面太搶
- 改成角落的小元件：`labelchip` `ltclean` `desccta`；字幕改 `subtitle`；或改成切畫面

## 效果描述 → 名稱

| 使用者說 | 候選 |
|---|---|
| 字一個一個打出來 | `typewriter` `prompt` `typecap` |
| 亂碼跳一跳才變成字 | `scramble` |
| 像機場那種翻牌 | `splitflap` |
| 字從模糊變清楚 | `blurin` |
| 字從一條線下面冒出來 | `maskline` |
| 字很大砸下來 | `slam` `impact` |
| 一句話裡有一個詞一直換 | `wordswap` |
| 字粗細在變 | `varweight` `weightcap` |
| 字幕講到哪亮到哪 | `karaoke` `dimprogress` `highlightbox` `underlinefollow` |
| 字幕一次跳一個詞 | `wordpop` |
| 字在人後面 | `behindcap` |
| 數字一直跳上去 | `countup` `odometer` |
| 長條互相超車 | `barrace` |
| 線從左畫到右的圖 | `linedraw` |
| 地圖拉近畫圈 | `mapzoom` `circle` |
| 飛機飛過地圖 | `flight` |
| 線一段段把方塊連起來 | `connector` `steps` |
| 一張卡放大講完再縮回去 | `sharedelement` `onething` |
| 一個東西變成另一個 | `morph` `matchcut` `textmatch` |
| 畫面閃白切過去 | `flash` |
| 圓形打開 | `iris` |
| 鏡頭甩過去 | `whippan` |
| 鏡頭衝進去下一幕 | `zoomthrough` `dive` |
| 鏡頭慢慢靠近 | `pushin` `kenburns` |
| 先特寫再拉遠看全部 | `pullback` |
| 鏡頭跟著滑鼠放大 | `zoomfollow` |
| 前面清楚後面模糊，再換過來 | `rackfocus` |
| 畫面震一下 | `shake` `impact` |
| 講者縮到角落 | `pip` |
| 螢光筆劃過 | `marker` |
| 手畫一條底線 / 圈起來 / 箭頭 | `handunderline` `circle` `arrow` |
| 其他變暗只有一塊亮 | `spotlight` |
| 一道光掃過去 | `shine` `shimmer` |
| 背景一直慢慢在動的顏色 | `meshbg` `aurorabg` `noisebg` |
| 很淡的大字在背景 | `ghostword` |
| 老電視掃描線 | `crt` |
| 底片顆粒感 | `film` |
| 彩帶噴出來 | `confetti` |
| 通知一直跳出來 | `notifstack` `escalate` |
| 游標點來點去 | `cursorclick` `cursorop` |
| AI 一段段吐出回答 | `aistream` |
| 東西彈一下才停 | `spring` |
| 一個接一個出現 | `stagger` |
| 像黏土動畫一頓一頓的 | `stopmotion` |
| 手繪線一直在抖 | `boil` |
| 跟著音樂節拍 | `beat` |
| 一直轉的圖片圈 | `carousel` |
