# 區塊 × 效果

逐個區塊討論時，從這裡挑 2–3 個候選。「首選」是多數網站都適合的安全選項；「加強」是強度「中」以上才考慮；「大招」會用掉預算額度，要先確認。

| 區塊 | 首選 | 加強 | 大招（用掉額度） |
|---|---|---|---|
| 導覽列 | `stagger`（選單展開） | `magnet`（聯絡按鈕） | — |
| Hero 主標題 | `splitreveal` | `scramble` | — |
| Hero 背景／主視覺 | 靜態不動 | `parallax` | `aurora` 或 `hero3d`（3D 額度） |
| Hero 到第一段的過場 | `reveal` | `scrollzoom` | — |
| 特色／功能卡片 | `stagger` | `spot`、`tilt` | — |
| 功能逐步說明 | `reveal` | `linedraw` | `pinned`（固定畫面額度） |
| 數據／成果 | `countup` | `stagger` | — |
| 作品集／案例列表 | `reveal` | `tilt` | `hscroll`（固定畫面額度） |
| 品牌故事 | `reveal`、`splitreveal` | `parallax`、`linedraw` | `pinned`（固定畫面額度） |
| 產品主圖／影片 | `reveal` | `parallax` | `scrollzoom` |
| 價格方案 | `stagger` | `spring` | `borderbeam`（視覺特效額度，給推薦方案） |
| 公告／標籤 | 靜態 | — | `shimmer`（持續動畫額度） |
| CTA 按鈕 | `spring` | `magnet` | `borderbeam`（視覺特效額度） |
| 表單送出／成功提示 | `spring` | `lottie` | — |
| Footer | 靜態不動 | `reveal` | — |
| 整站 | — | `smooth` | — |

## 判斷原則

- **一個區塊一種主效果。** 同一區塊同時有進場、游標、持續動畫，訪客不知道該看哪裡。
- **越往下越安靜。** Hero 可以有記憶點，內文區塊以 `reveal` 為主，Footer 通常不需要動。
- **滾動敘事整頁只講一個故事。** `pinned` 和 `hscroll` 只能選一段，放在最值得講的地方。
- **Hero 只放一個大招。** 標題特效＋3D 背景＋視差同時出現，就沒有重點。
