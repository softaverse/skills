# 搜尋配方

把「風格」變成「圖庫搜得到的字」。

## 關鍵字怎麼寫

1. **用英文。** 所有來源的英文標籤最多，中文的結果少很多，也不準。
2. **主題名詞 1–2 個，加光線或氛圍 1 個，總共不超過 3–4 個字。** Unsplash 要求每個字都要符合，`minimal desk copy space natural light` 只找得到 1 張，`minimal desk` 有上千張。 `workspace natural light` 比 `beautiful modern professional workspace with natural light and plants` 好；字越多，每個字的權重越低。
3. **寫看得到的東西，不寫抽象概念。** `success`、`innovation`、`teamwork` 會得到握手和燈泡；`hands typing laptop`、`whiteboard sticky notes` 會得到真實場景。
4. **排除用換詞，不用減號。** 圖庫 API 不支援 `-people`。不要人就搜沒有人的東西（`empty office`、`desk setup`），或在 Unsplash、Pexels 加 `no people`，效果只有部分。
5. **一個方向一次搜尋。** 想比較 A、B 兩個方向，就搜兩次、用兩個 `--label`，比較頁才會分成兩列。

## 中文說法 → 搜尋字

| 使用者說 | 搜尋字 |
|---|---|
| 辦公室、上班 | `office candid`、`modern office interior` |
| 在家工作 | `home office`、`working from home natural light` |
| 開會 | `team meeting candid`、`whiteboard discussion` |
| 咖啡廳 | `cafe interior`、`coffee shop natural light` |
| 城市 | `city street`、`urban architecture` |
| 夜景 | `city night`、`night skyline` |
| 大自然 | `nature landscape`、`forest light` |
| 海 | `ocean calm`、`sea aerial` |
| 天空 | `clear sky`、`sky clouds minimal` |
| 科技 | `circuit macro`、`abstract light`、`server room` |
| 健康、運動 | `running outdoor`、`yoga natural light` |
| 學習、教育 | `studying notebook`、`library interior` |
| 醫療 | `clinic interior bright`、`doctor hands` |
| 金融 | `architecture glass building`、`calculator desk minimal` |
| 背景、底圖 | `minimal background`、`texture`、`copy space` |

## 各來源的參數

`search.py` 會把共用參數轉成各家的寫法；不支援的就略過。

| 共用參數 | Pexels | Unsplash | Pixabay | Openverse |
|---|---|---|---|---|
| `--orientation landscape` | landscape | landscape | horizontal | wide |
| `--orientation portrait` | portrait | portrait | vertical | tall |
| `--orientation square` | square | squarish | （不支援） | square |
| `--color` | 名稱或 hex | 名稱 | 名稱 | （不支援） |
| `--min-width` | 搜尋後過濾 | 搜尋後過濾 | 原生支援 | 搜尋後過濾 |

**顏色名稱**

| 來源 | 支援的值 |
|---|---|
| Pexels | `red` `orange` `yellow` `green` `turquoise` `blue` `violet` `pink` `brown` `black` `gray` `white`，或任何 hex（`#ffffff`） |
| Unsplash | `black_and_white` `black` `white` `yellow` `orange` `red` `purple` `magenta` `green` `teal` `blue` |
| Pixabay | `grayscale` `transparent` `red` `orange` `yellow` `green` `turquoise` `blue` `lilac` `pink` `white` `gray` `black` `brown` |

黑白一律寫 `--color bw`，`search.py` 會轉成 Unsplash 的 `black_and_white` 與 Pixabay 的 `grayscale`；Pexels 沒有黑白篩選，會略過。

常見的別名會自動對應（`purple` → Pexels 的 `violet`、Pixabay 的 `lilac`；`teal` → `turquoise`）。某個來源對應不到的顏色只會在那個來源被略過，其他來源照用。要針對某一家，加 `--sources`。

## 結果不好時

| 狀況 | 試試 |
|---|---|
| 太多人 | 換成物件或環境的名詞；加 `empty`、`interior`、`detail` |
| 太擺拍 | 加 `candid`、`documentary`、`natural light` |
| 太飽和、太亮 | 加 `muted`、`soft`、`film` |
| 主體在正中間，沒地方放標題 | 加 `copy space`、`negative space`，用 `--orientation landscape` |
| 太少結果 | 減少關鍵字；拿掉 `--color` 和 `--min-width` |
| 各張色調不一致 | 用 `--color` 鎖顏色；或接受不一致，實作時統一處理（`bw`、`overlay`） |
| 都是 AI 生成感的圖 | 加 `photography`、`35mm`；改看 Unsplash |

## 讓整組一致

- 同一個版位的幾張圖（例如三張功能卡片），從**同一次搜尋**裡挑。
- 在比較頁點作者名字，看同一位攝影師有沒有同系列的其他照片。這是讓整組一致最有效的辦法。
- 最後一招：實作時統一處理（全部黑白、全部疊同一層品牌色、全部同樣的圓角與比例）。
