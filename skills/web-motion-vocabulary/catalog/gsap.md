# GSAP

GSAP 本身與所有外掛目前都免費（授權不是一般的開源授權，商用前看 https://gsap.com/licensing/ ）。與框架無關；React 用 `@gsap/react` 的 `useGSAP()`，元件卸載時會自動清理。外掛要先 `gsap.registerPlugin()`。

格式：`**名稱** — 中文說明 → 對應效果 id · 官方文件`。手動維護，不由腳本同步。

## 核心

- **Tween／Timeline** — 補間動畫與時間軸，把多段動畫排在同一條時間線上；固定畫面敘事的骨架 → `pinned`、`scrollzoom` · https://gsap.com/docs/v3/GSAP/Timeline/
- **gsap.context()** — 把一個元件裡建立的動畫收在一起，一次 `revert()` 全部清掉（含 ScrollTrigger） · https://gsap.com/docs/v3/GSAP/gsap.context()/
- **gsap.matchMedia()** — 依螢幕寬度或 `prefers-reduced-motion` 建立不同動畫，條件不成立時自動清理 · https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/
- **gsap.quickTo()** — 為反覆更新的數值（如游標位置）建立高效能的補間 → `magnet` · https://gsap.com/docs/v3/GSAP/gsap.quickTo()/
- **React 整合（useGSAP）** — React 裡使用 GSAP 的官方方式與清理規則 · https://gsap.com/resources/React/

## 捲動

- **ScrollTrigger** — 用捲動位置觸發或驅動（scrub）動畫，也能把元素釘住（pin） → `parallax`、`pinned`、`hscroll`、`scrollzoom`、`linedraw` · https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- **ScrollSmoother** — GSAP 自己的平滑捲動，與 ScrollTrigger 深度整合；和 Lenis 二擇一 → `smooth` · https://gsap.com/docs/v3/Plugins/ScrollSmoother/
- **ScrollToPlugin** — 平滑捲動到指定位置或元素（錨點導覽） · https://gsap.com/docs/v3/Plugins/ScrollToPlugin/
- **Observer** — 統一偵測滾輪、觸控、指標的手勢與方向，用來做「捲一下切一頁」 · https://gsap.com/docs/v3/Plugins/Observer/

## 文字

- **SplitText** — 把文字拆成行、詞、字，可以加遮罩，做逐行或逐字進場 → `splitreveal` · https://gsap.com/docs/v3/Plugins/SplitText/
- **ScrambleTextPlugin** — 文字先變亂碼再解出正確內容 → `scramble` · https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin/
- **TextPlugin** — 逐字替換文字內容，可做打字機效果 · https://gsap.com/docs/v3/Plugins/TextPlugin/

## SVG 與路徑

- **DrawSVGPlugin** — 讓 SVG 線條像被畫出來 → `linedraw` · https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/
- **MorphSVGPlugin** — 一個 SVG 形狀變形成另一個 · https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
- **MotionPathPlugin** — 讓元素沿著路徑移動 · https://gsap.com/docs/v3/Plugins/MotionPathPlugin/

## 版面與互動

- **Flip** — 記下版面變化前後的位置，再平滑過渡（篩選、展開、排序） · https://gsap.com/docs/v3/Plugins/Flip/
- **Draggable** — 讓元素可以拖曳、旋轉，可加邊界與吸附 · https://gsap.com/docs/v3/Plugins/Draggable/
- **InertiaPlugin** — 放手後依速度慣性滑行，常搭配 Draggable · https://gsap.com/docs/v3/Plugins/InertiaPlugin/
- **Physics2DPlugin** — 依速度、角度、重力做拋物運動（彩帶、碎片） · https://gsap.com/docs/v3/Plugins/Physics2DPlugin/

## 緩動與工具

- **Eases** — 內建緩動曲線一覽，決定動畫「怎麼加速減速」 · https://gsap.com/docs/v3/Eases/
- **CustomEase** — 自己畫緩動曲線 · https://gsap.com/docs/v3/Eases/CustomEase/
- **CustomBounce** — 自訂彈跳，含落地壓扁效果 · https://gsap.com/docs/v3/Eases/CustomBounce/
- **CustomWiggle** — 自訂搖晃抖動 · https://gsap.com/docs/v3/Eases/CustomWiggle/
- **GSDevTools** — 開發時用的時間軸控制面板，可以逐格檢查動畫 · https://gsap.com/docs/v3/Plugins/GSDevTools/
