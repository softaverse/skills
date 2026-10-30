# 插畫

插畫用在照片表達不了、或不適合用照片的地方：抽象概念、流程、空狀態（`empty`）、錯誤頁（`e404`）、引導流程。一個網站的插畫要同一種風格，最好出自同一個來源。

可搜尋的來源只有 Pixabay（插畫、向量）與 Openverse（CC 授權插畫）：`search.py --slot illustration`。風格最一致、最好用的免費插畫庫多半沒有 API，下面列在「現成來源」，只給連結，讓使用者自己去挑。

> Pixabay 的向量圖透過 API 只拿得到 1280px 的 PNG，要 SVG 原檔得到它的網站手動下載。

## 插畫風格

- **扁平插畫 (Flat Illustration)** `flat` — 純色塊、沒有陰影漸層的插畫。
  - 感受：清楚、友善、現代
  - 適合：SaaS 功能說明、流程圖、空狀態
  - 搭配：iconfill、colorblock
  - 搜尋：`flat illustration`、`flat design people`、`vector illustration minimal`
  - 現成來源：unDraw（可在網站上直接換成品牌色）
  - 注意：最常見也最容易撞圖；用品牌色重新上色會好很多
- **線條插畫 (Line Art)** `lineart` — 單一粗細的線條描繪，簡潔俐落。
  - 感受：優雅、輕盈、有設計感
  - 適合：精品、顧問、作品集、極簡網站
  - 搭配：iconline、highkey、serif
  - 搜尋：`line art`、`one line drawing`、`continuous line illustration`
  - 現成來源：Open Doodles（部分是線稿）
  - 注意：線條粗細要和圖示的描邊粗細接近，放在一起才和諧
- **手繪塗鴉 (Hand-drawn / Doodle)** `doodle` — 手繪線條、塗鴉和不規則邊緣。
  - 感受：親切、隨性、有人味
  - 適合：教育、創作者、Notion 風格的網站、社群
  - 搭配：iconhand、papertex、emoji
  - 搜尋：`doodle illustration`、`hand drawn illustration`、`sketch`
  - 現成來源：Open Peeps、Open Doodles
  - 注意：手繪風會讓整站看起來比較不正式；B2B 網站要斟酌
- **等距插畫 (Isometric)** `iso` — 2.5D 等角投影的場景與物件。
  - 感受：系統化、科技、有結構
  - 適合：架構說明、雲端服務、資料流程
  - 搭配：iconduo、render3d
  - 搜尋：`isometric illustration`、`isometric server`、`isometric city`
  - 現成來源：沒有好的免費整套；Pixabay 搜得到零散的
  - 注意：不同作者的等距角度和光源方向不一樣，混用會很明顯
- **漸層插畫 (Gradient Illustration)** `gradillus` — 插畫用柔和漸層代替平塗。
  - 感受：現代、柔和、科技
  - 適合：App 介紹、金融科技、行銷頁
  - 搭配：aurora、blurgrad、icongrad
  - 搜尋：`gradient illustration`、`abstract gradient shapes`
  - 現成來源：無；多半要自己用 CSS 或設計工具做
  - 注意：漸層插畫和照片放在同一頁時容易風格衝突
- **3D 插畫 (3D Render)** `render3d` — Blender 式的柔光 3D 物件。
  - 感受：新穎、吸睛、精緻
  - 適合：Hero 主視覺、功能卡片、空狀態
  - 搭配：icon3d、clay、pastelphoto
  - 搜尋：`3d render illustration`、`3d object pastel`
  - 現成來源：3dicons（CC0）
  - 注意：PNG 檔案大，一定要壓縮；同一頁的 3D 物件光源方向要一致
- **黏土風 (Claymorphism)** `clay` — 柔軟、澎潤的 3D 立體造型。
  - 感受：可愛、親切、玩心
  - 適合：兒童、遊戲化、消費 App
  - 搭配：render3d、pastelphoto、kawaii
  - 搜尋：`clay 3d illustration`、`cute 3d character`
  - 現成來源：無穩定的免費整套
  - 注意：免費素材很少，多半要另外製作
- **抽象幾何 (Geometric Abstract)** `geo` — 用圓、方、線組成的抽象構圖。
  - 感受：理性、現代、有設計感
  - 適合：裝飾性的區塊背景、文章封面、OG 圖
  - 搭配：swiss、bauhaus、colorblock
  - 搜尋：`geometric abstract`、`bauhaus shapes`、`geometric pattern`
  - 現成來源：無；簡單的幾何直接用 SVG 或 CSS 畫，比找圖更好控制
  - 注意：如果是純裝飾，先考慮用程式畫
- **有機流體 (Organic / Blob)** `blob` — 不規則的柔軟色塊和液態形狀。
  - 感受：柔和、親切、活潑
  - 適合：區塊背景裝飾、頭像底圖
  - 搭配：pastelphoto、flat
  - 搜尋：`organic shapes`、`blob abstract`
  - 現成來源：無；用 SVG 產生器或 CSS 做
  - 注意：同上，純裝飾就不必找圖

## 現成來源（只給連結）

這些網站沒有公開 API。授權都可以免費商用；細節以官網為準，使用前再看一次。

| 來源 | 風格 | 授權 | 標註 | 連結 |
|---|---|---|---|---|
| unDraw | 扁平人物與情境，可換成任意主色 | unDraw License（可商用；不能拿插畫本身轉賣、重新打包成素材庫或訓練 AI） | 免 | https://undraw.co |
| Open Peeps | 手繪人物，可組合表情與姿勢 | CC0 | 免 | https://www.openpeeps.com |
| Open Doodles | 手繪塗鴉人物 | 免費商用，官網註明不需標註 | 免 | https://www.opendoodles.com |
| 3dicons | 3D 圖示與物件 | CC0 | 免 | https://3dicons.co |

使用者從這些網站自己下載後，請他告訴你檔名和來源，手動補一列到 `CREDITS.md`，格式和 `fetch.py` 寫的一樣。
