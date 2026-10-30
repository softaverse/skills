# 背景影片

網站上的影片幾乎都是 **Hero 背景循環**（`videobg`）：靜音、自動播放、無限循環，上面疊標題。它不是要人「看」的影片，是會動的氛圍。來源只有 Pexels 與 Pixabay（`search.py --slot herovideo`）。

## 先決定要不要用影片

背景影片是網站最重的素材之一，用之前先問三件事：

1. **動態有沒有在說話？** 影片要傳達照片給不了的東西（流動、節奏、規模）。只是「比較酷」的話，一張好照片通常更好。
2. **標題讀得到嗎？** 會動的背景比照片更搶眼，文字幾乎一定要加深色遮罩。
3. **能接受手機上只看到靜態圖嗎？** 很多網站在手機上改顯示 poster，以節省流量與電量。

和 `web-motion-vocabulary` 的預算一起算：背景影片是一個「持續動畫」，同一個畫面裡就不要再放其他持續播放的效果。

## 影片風格

- **慢速空拍 (Slow Aerial Loop)** `aerialloop` — 空拍機緩慢飛過海岸、森林、城市。
  - 感受：宏觀、平靜、有規模
  - 適合：旅遊、地產、永續、品牌開場
  - 搭配：aerial、landscape
  - 搜尋：`aerial slow`、`drone ocean`、`drone forest`
  - 篩選：`--orientation landscape`
  - 注意：細節很多，壓縮後最容易糊，碼率不能壓太低
- **環境氛圍 (Ambient Nature)** `ambient` — 幾乎不動的畫面：葉子晃、水波、雲在飄、窗簾飄動。
  - 感受：安靜、療癒、高級
  - 適合：保養品、身心健康、精品、旅宿
  - 搭配：natlight、negspace
  - 搜尋：`leaves wind slow`、`calm water surface`、`curtain wind`
  - 篩選：無
  - 注意：**最適合當背景的類型**：動得少、檔案小、循環接縫不明顯
- **縮時攝影 (Timelapse)** `timelapse` — 城市車流、雲層、日夜變化被快轉。
  - 感受：節奏、時間、規模、都市
  - 適合：新創、物流、媒體、科技
  - 搭配：urban、mblur
  - 搜尋：`city timelapse`、`clouds timelapse`、`traffic timelapse night`
  - 篩選：無
  - 注意：畫面動得快，壓縮後檔案大；要確認循環的頭尾接得起來
- **抽象流體 (Abstract Flow)** `inkflow` — 墨水在水裡擴散、液體、煙霧、光粒子。
  - 感受：創意、科技、神秘
  - 適合：AI、創意工作室、科技品牌、深色網站
  - 搭配：abstract、lowkey、blurgrad
  - 搜尋：`ink in water`、`abstract liquid`、`smoke black background`、`particles`
  - 篩選：`--color` 品牌色（可能被忽略）
  - 注意：純黑背景的流體可以用 CSS `mix-blend-mode: screen` 疊在深色網站上，邊緣會消失
- **光暈漏光 (Light Leak)** `lightleak` — 底片漏光、彩色光暈緩緩飄過。
  - 感受：溫暖、懷舊、夢幻
  - 適合：攝影師、婚禮、音樂、作品集
  - 搭配：film、goldenhour
  - 搜尋：`light leak`、`lens flare overlay`
  - 篩選：無
  - 注意：通常拿來疊在照片上（`mix-blend-mode: screen`），不是單獨當背景
- **手部工作 (Hands at Work)** `handsvideo` — 手在做事的近拍：打字、手作、沖咖啡。
  - 感受：專注、手作、真實
  - 適合：工作室、工藝、課程、服務流程
  - 搭配：hands、shallowdof
  - 搜尋：`hands crafting close up`、`barista pouring coffee slow motion`、`hands typing keyboard`
  - 篩選：無
  - 注意：有人味又不露臉；要挑沒有明顯剪接的單一鏡頭
- **慢動作 (Slow Motion)** `slowmo` — 水花、粉末、布料、頭髮在慢動作下飄動。
  - 感受：優雅、感官、高級
  - 適合：飲料、美妝、時尚、運動
  - 搭配：lowkey、macro
  - 搜尋：`slow motion splash`、`powder explosion slow motion`、`fabric flowing slow motion`
  - 篩選：無
  - 注意：慢動作片段通常很短，循環接縫明顯；挑長一點的，或做成來回播放（boomerang）
- **辦公情境 (Office B-roll)** `officebroll` — 辦公室裡的人走動、討論、打字。
  - 感受：專業、團隊、日常
  - 適合：招募、企業服務
  - 搭配：teamwork、workspace
  - 搜尋：`office people working candid`、`startup office`
  - 篩選：無
  - 注意：⚠️ 人像與圖庫感最重；不能當作你們的辦公室或員工。能用 `handsvideo` 或 `ambient` 取代就取代

## 規格

| 項目 | 建議 |
|---|---|
| 長度 | 6–15 秒，可以無縫循環 |
| 解析度 | 寬 1280–1920px；1920 以上通常只是浪費流量 |
| 檔案大小 | **≤ 3 MB**（`fetch.py` 超過會提醒） |
| 音軌 | 刪掉（`-an`） |
| 格式 | MP4（H.264）一定要有；可另外加 WebM（VP9）給支援的瀏覽器 |
| HTML | `<video autoplay muted loop playsinline poster="…">`，四個屬性缺一不可 |
| poster | 一定要有；它是影片載入前、手機省流量模式和減少動態時看到的畫面 |
| 減少動態 | `prefers-reduced-motion: reduce` 時只顯示 poster |
| 文字對比 | 影片上的文字加深色遮罩，對比至少 4.5:1 |

## 壓縮與 poster（交給實作端）

```bash
# 縮成 1280 寬、24fps、去掉音軌，適合網頁的 MP4
ffmpeg -i in.mp4 -an -vf "scale=1280:-2,fps=24" -c:v libx264 -crf 28 -preset slow \
  -pix_fmt yuv420p -movflags +faststart hero.mp4

# 給支援的瀏覽器用的 WebM（通常更小）
ffmpeg -i in.mp4 -an -vf "scale=1280:-2,fps=24" -c:v libvpx-vp9 -crf 38 -b:v 0 hero.webm

# 取第 1 秒當 poster
ffmpeg -ss 1 -i in.mp4 -frames:v 1 -q:v 3 hero-poster.jpg
```

圖庫影片常有 20–30 秒，先剪到 10 秒左右（在 `-i` 前加 `-ss <起點秒數> -t 10`，挑一段頭尾接得起來的），檔案大小通常就跟著減少一半以上。還是超過 3 MB，再試 `-crf 30`，最後才縮到 960 寬。poster 再交給 `optimize-images` 轉 WebP。
