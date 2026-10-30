# 素材來源與授權

這個 skill 只收**免費、可商用**的素材。授權白名單寫在 `scripts/sources.py`，搜尋時過濾一次，下載前再檢查一次，不在白名單上的不會出現、也下載不了。

## 白名單

| 來源 | 收錄 | 網站上要標註嗎 | 使用方式 |
|---|---|---|---|
| Pexels | 全部（Pexels License） | 不用（建議在 CREDITS 留紀錄） | 下載到專案 |
| Unsplash | 全部，但排除付費的 Unsplash+ | **要**：授權本身不需要，但 API 規範要求顯示時標作者與 Unsplash | **用 CDN 連結**，不下載 |
| Pixabay | 全部（Pixabay Content License） | 不用 | 下載到專案 |
| Openverse | 只收 CC0、Public Domain Mark、CC BY | CC BY 要標註 | 下載到專案 |
| Iconify | 只收 MIT、ISC、Apache-2.0、BSD-3-Clause、Unlicense、OFL-1.1、CC0、CC BY 的圖示集 | CC BY 的圖示集要標註 | 下載 SVG |

**一律排除**：
- NC（非商業）：不能商用。
- ND（禁止改作）：網站幾乎一定會裁切、調色、壓縮。
- SA（相同方式分享）：改作要用同樣授權釋出，網站做不到。
- GPL、MPL 圖示集：copyleft 條款，不適合直接放進網站。
- 付費或混合授權的圖庫：Freepik、Shutterstock、Adobe Stock、Unsplash+、iStock。免費區常常要標註或有額外限制，而且和付費素材混在一起，容易誤用。
- Wikimedia Commons：大量是 CC BY-SA，第一版不收。

## 「可商用」也不包含的事

圖庫授權處理的是**著作權**。下面這些是別的權利，授權不保證：

| 風險 | 說明 | skill 怎麼處理 |
|---|---|---|
| 肖像權 | 圖庫大多沒有保證有模特兒授權書。可辨識的人用在「暗示代言」「假裝是客戶或員工」「敏感主題（疾病、債務、犯罪）」都有風險 | 照片的描述裡有人物字眼的，比較頁標 ⚠️ 可能含人像（插畫不標） |
| 商標 | 畫面裡的 Logo、產品外觀、招牌屬於別人 | 有品牌關鍵字的標 ⚠️ 可能含商標 |
| 原樣轉售 | 把素材原封不動當商品賣（桌布、印刷品、模板、素材包） | 在 SKILL.md 的規則裡說明 |
| 誤導 | 圖庫人像當成「我們的團隊」「客戶見證」 | 一律不行，見 `slots.md` |

⚠️ 標記是用關鍵字猜的，不是辨識結果：沒有標記不代表沒有人或商標，挑的時候仍要用眼睛看一次。

## 各來源

### Pexels
- 內容：照片、影片。影片是背景影片的主要來源。
- Key：`PEXELS_API_KEY`，到 https://www.pexels.com/api/ 免費申請。2026 年 10 月時 Pexels 暫停受理新的 API 申請；沒有 key 時，照片靠 Unsplash 與 Pixabay，背景影片只剩 Pixabay。
- 限流：預設每小時 200 次、每月 20,000 次（以申請時的官方頁面為準）。
- 授權：Pexels License，可商用、免標註；不能原樣轉售，不能用來暗示人物代言。https://www.pexels.com/license/
- API 規範：要顯示 Pexels 連結，盡量標註攝影師。比較頁有顯示；網站本身不強制。
- 尺寸：可以下載原圖，`fetch.py` 會用 Pexels CDN 縮到版位需要的寬度（`?w=`），不會下載 6000px 的原檔。
- 顏色篩選：支援顏色名稱或 hex（`--color "#e8d5c4"`），可以直接用品牌色搜。

### Unsplash
- 內容：照片。整體質感最高、最有「攝影作品感」。
- Key：`UNSPLASH_ACCESS_KEY`，到 https://unsplash.com/developers 建立應用程式，用 Access Key。
- 限流：Demo 模式每小時 50 次；申請上線（Production）後每小時 5,000 次。
- 授權：Unsplash License，可商用、免標註。https://unsplash.com/license
- **API 規範（重要）**：
  1. 必須使用 API 回傳的 hotlink 圖片網址（`photo.urls`），所以 `fetch.py` 不下載，而是產生 `<img srcset>` 程式碼。好處是 Unsplash 的 CDN 會自動依寬度縮圖、轉 WebP/AVIF。
  2. 使用者選定圖片時，必須呼叫 `download_location`，`fetch.py` 會自動做。
  3. 顯示時要標註攝影師與 Unsplash，並連回他們的頁面（連結帶 `utm_source`）。`fetch.py` 會印出標註文字。
- 排除：`premium` 或 `plus` 為 true 的 Unsplash+ 付費圖片。

### Pixabay
- 內容：照片、插畫、向量、影片。插畫的主要來源。
- Key：`PIXABAY_API_KEY`，到 https://pixabay.com/api/docs/ 登入後就會看到。
- 限流：每 60 秒 100 次。官方要求搜尋結果**快取 24 小時**：同一組關鍵字不要重複搜，session 檔就是快取。
- 授權：Pixabay Content License，可商用、免標註；不能原樣轉售，不能用在誤導或違法的用途，可辨識的人物或品牌可能需要另外取得同意。https://pixabay.com/service/license-summary/
- API 規範：搜尋結果要顯示來自 Pixabay（比較頁有）；**不能永久 hotlink**，要下載到自己的伺服器（`fetch.py` 會下載）。
- 尺寸限制：一般帳號透過 API 最大只拿得到 1280px；原圖與向量 SVG 要申請 full API access，或到網站手動下載。Hero 需要 1920px 以上時，比較頁會標出「下載上限 1280px」。
- 圖片網址 24 小時後失效，`fetch.py` 下載前會用 id 重新查一次。

### Openverse
- 內容：彙整 Flickr、博物館等來源的 CC 授權圖片。量大、品質參差，適合找特定主題（歷史、科學、自然）。
- Key：不用。匿名使用的限流比較嚴，連續大量查詢會被擋。
- 授權：每張不同，只收 CC0、PDM、CC BY。CC BY 一定要標註，API 會回傳標註文字，`fetch.py` 照抄。
- 注意：原圖放在各個來源網站，偶爾會失效；不是每張都有寬高資訊。

### Iconify
- 內容：200 多套開源圖示集的 SVG。
- Key：不用。
- 授權：每套不同，依 SPDX 代碼過濾，詳見 `icons.md`。
- 不收「Archive / Unmaintained」分類的圖示集。

## 沒有 key 的時候

`search.py` 會跳過沒有 key 的來源，並在輸出裡寫 `skipped: set PEXELS_API_KEY`。看到這行時告訴使用者：哪個來源沒用到、申請連結在哪、申請只要幾分鐘。只有 Openverse 和 Iconify 也能跑，但照片數量和品質會差很多。

key 放在 shell 設定檔（例如 `~/.zshrc`）：

```bash
export PEXELS_API_KEY="..."
export UNSPLASH_ACCESS_KEY="..."
export PIXABAY_API_KEY="..."
```

不要把 key 寫進專案檔案或 commit。值是 `...`、`your-key` 這類佔位文字時，會當作沒有 key。

改了 `~/.zshrc` 之後，已經開著的 shell 讀不到新的值；開新的終端機，或用 `zsh -ic 'python3 …'` 跑腳本。
