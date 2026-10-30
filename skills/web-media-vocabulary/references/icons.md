# 圖示

圖示從 Iconify 找：它收錄 200 多套開源圖示集，不用 key，可以直接下載 SVG。要選的是**一整套**，不是一個個挑：同一個網站的圖示要出自同一套，線條粗細、圓角、視覺重量才會一致。

`search.py --slot icons` 一次搜網站需要的所有概念，比較頁每一列是一套圖示集，看它把這些概念畫成什麼樣、缺了哪幾個。

## 搜尋要點

- `--q` 放網站實際要用的概念，逗號分隔：`"home, user, settings, chart, mail, lock"`。
- 不同圖示集對同一個東西的命名不同，用 `|` 寫同義詞：`home|house`、`settings|gear|cog`、`mail|envelope`、`delete|trash`、`search|magnifying-glass`。
- `--prefixes` 限定要比較的圖示集（下表的「圖示集」欄）；不限定的話會搜全部，結果比較雜。
- `--variant` 選同一套裡的變體：`base`＝沒有後綴的預設版；`fill`、`filled`、`solid`、`duotone`、`bold`、`light`、`thin`、`linear`… 依圖示集而定（看下表）。

授權已在搜尋時過濾：只留 MIT、ISC、Apache-2.0、BSD、Unlicense、OFL、CC0，以及要標註的 CC BY。GPL、MPL、CC BY-SA、CC BY-NC 的圖示集不會出現。

## 圖示風格

- **線性圖示 (Outline Icons)** `iconline` — 統一粗細的描邊圖示。
  - 感受：輕盈、現代、乾淨
  - 適合：SaaS、工具、內容多的介面，最萬用
  - 搭配：highkey、minimal、swiss
  - 圖示集：`lucide`（ISC）、`tabler`（MIT）、`iconoir`（MIT）、`hugeicons`（MIT）、`ph`（MIT，Phosphor）、`solar` 的 `linear`（CC BY 4.0，需標註）
  - 篩選：`--prefixes lucide tabler iconoir ph --variant base`
  - 注意：Lucide 與 Tabler 數量多、風格穩，是最安全的起點
- **面性圖示 (Filled Icons)** `iconfill` — 實心填色的圖示。
  - 感受：明確、有份量、好辨識
  - 適合：底部導覽列、行動版、小尺寸圖示、兒童與大眾服務
  - 搭配：flat、colorblock
  - 圖示集：`ph` 的 `fill`、`tabler` 的 `filled`、`heroicons` 的 `solid`、`ri` 的 `fill`（Apache）、`mdi`（Apache，預設就是實心）
  - 篩選：`--prefixes ph --variant fill`（一次只比一種後綴）
  - 注意：常見作法是「未選取＝線性、選取中＝實心」，這時要挑同時有兩種版本的圖示集（Phosphor、Tabler、Heroicons、Remix）
- **雙色圖示 (Duotone Icons)** `iconduo` — 主色加一層淡色的圖示。
  - 感受：友善、豐富、有層次
  - 適合：功能介紹區、行銷頁、儀表板
  - 搭配：iconline、pastelphoto
  - 圖示集：`ph` 的 `duotone`（MIT）、`solar` 的 `bold-duotone`（CC BY 4.0，需標註）
  - 篩選：`--prefixes ph solar --variant duotone`
  - 注意：雙色圖示的淡色層用 `currentColor` 加透明度，顏色跟著文字色走；要自訂兩種顏色，要改 SVG
- **3D 圖示 (3D Icons)** `icon3d` — 有光影與立體感的圖示，常見於登陸頁。
  - 感受：活潑、新穎、吸睛
  - 適合：行銷頁的功能區、空狀態、引導流程
  - 搭配：render3d、clay、pastelphoto
  - 圖示集：Iconify 沒有真正的 3D 圖示；最接近的是 `fluent-emoji`（MIT，彩色立體感）
  - 現成來源（只給連結）：3dicons https://3dicons.co （CC0，可商用、免標註；授權以官網為準）
  - 注意：3D 圖示通常是 PNG，檔案比 SVG 大很多，一頁不要放太多
- **表情符號風 (Emoji Style)** `emoji` — 用 emoji 當作圖示或視覺重點。
  - 感受：親切、輕鬆、有個性
  - 適合：社群、內部工具、Notion 風格網站
  - 搭配：doodle、minimal
  - 圖示集：`fluent-emoji-flat`（MIT）、`noto`（Apache）、`twemoji`（CC BY 4.0，需標註）
  - 篩選：`--prefixes fluent-emoji-flat noto`
  - 注意：直接打 emoji 字元，每個作業系統顯示的樣子都不同；下載成 SVG 才會一致。OpenMoji 是 CC BY-SA，已排除
- **手繪圖示 (Hand-drawn Icons)** `iconhand` — 線條不規則、帶筆觸感的圖示。
  - 感受：親切、手作、有溫度
  - 適合：教育、兒童、創作者、手作品牌
  - 搭配：doodle、papertex、film
  - 圖示集：`doodle-icons`（MIT）、`streamline-freehand`（CC BY 4.0，需標註）
  - 篩選：`--prefixes doodle-icons streamline-freehand`
  - 注意：手繪圖示數量通常比較少，先確認需要的概念都有
- **漸層圖示 (Gradient Icons)** `icongrad` — 填入漸層色的圖示。
  - 感受：科技、活力、現代
  - 適合：科技新創、App 介紹頁
  - 搭配：gtext、aurora
  - 圖示集：沒有現成的漸層圖示集；用任一套 `iconline` 或 `iconfill`，在網站上用 CSS 遮罩填入漸層
  - 注意：CSS 作法是 `background: linear-gradient(…); mask: url(icon.svg) center/contain no-repeat;`
- **像素圖示 (Pixel Icons)** `iconpixel` — 點陣格繪製的復古圖示。
  - 感受：復古、遊戲、玩心
  - 適合：遊戲、開發者工具、復古風網站
  - 搭配：pixel、y2k、terminal
  - 圖示集：`pixelarticons`（MIT）、`streamline-pixel`（CC BY 4.0，需標註）
  - 篩選：`--prefixes pixelarticons streamline-pixel`
  - 注意：要以 24px 的整數倍顯示，不然像素會糊

## 品牌 Logo

整合列表、「用 Google 登入」、社群連結需要別家的 Logo 時，用 `simple-icons`（CC0，單色）或 `logos`（CC0，彩色）。

- 圖檔授權是 CC0，但 **Logo 本身是對方的商標**：只能用來指稱那個品牌（例如「支援 Slack 整合」），要遵守對方的品牌規範，不能改形狀。
- **不能**用來做「合作客戶／媒體報導」Logo 牆，除非對方真的是客戶、也同意你使用。

## 使用規則

- 一個網站只用**一套**圖示集（品牌 Logo 另計）。缺的概念，優先在同一套裡找替代名稱，不要從另一套借。
- 下載的 SVG 都是 `currentColor`，顏色跟著文字色走；大小用 CSS 控制。
- MIT、ISC、Apache：網站上不用標註，`CREDITS.md` 會留下授權連結。CC BY：網站上要放標註（`fetch.py` 會印出標註文字）。
