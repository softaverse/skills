# 工具

用戶選的是效果，工具由你填。只有當工具會影響用戶在乎的事（成本、手機、效能、要不要換框架）時才主動提。

## 一張表選工具

| 想做的效果 | 工具 | 一句話 |
|---|---|---|
| 文字、卡片進場、Hover、按鈕回饋 | **Motion** | 一般介面互動與簡單動畫 |
| 滾動敘事、視差、縮放、固定畫面 | **GSAP + ScrollTrigger** | 控制動畫時間軸與捲動進度 |
| 發光卡片、光束、動態文字、動態背景 | **Magic UI / React Bits** | 重用現成的視覺元件 |
| 3D 物件、粒子、互動場景 | **Three.js / React Three Fiber** | 用程式寫 3D |
| 快速做 3D 視覺 | **Spline** | 用視覺化編輯器做 3D 場景，再嵌入網站 |
| 互動插畫、角色、動態圖示 | **Rive / Lottie** | Rive 偏互動狀態；Lottie 適合播放預製動畫 |
| 捲動手感 | **Lenis** | 可選的平滑捲動輔助工具 |

## 各工具

### Motion（前身 Framer Motion）
- 擅長：元件進場、hover／按下回饋、彈簧手感、版面切換動畫、數字動畫。
- 不擅長：長段的滾動時間軸、固定畫面敘事。
- 框架：React（`motion/react`）、Vue（Motion for Vue），也有原生 JS 版（`motion`），任何網站都能用。
- 注意：Next.js App Router 裡使用要放在 Client Component（`"use client"`）。
- 官方：https://motion.dev

### GSAP + ScrollTrigger
- 擅長：精準的時間軸、捲動綁定（`scrub`）、固定畫面（`pin`）、視差、文字拆分（SplitText）、亂碼（ScrambleText）、線條描繪（DrawSVG）。
- 不擅長：React 狀態驅動的小互動（用 Motion 比較順手）。
- 框架：任何框架，與框架無關。React 用 `@gsap/react` 的 `useGSAP()`，元件卸載時會自動清理 ScrollTrigger。
- 注意：GSAP 與所有外掛（含 SplitText、ScrambleText、DrawSVG）目前全部免費；授權不是一般開源授權，商用前看一下條款。
- 官方：https://gsap.com ・授權 https://gsap.com/licensing/ ・React https://gsap.com/resources/React/

### Lenis
- 擅長：整頁慣性平滑捲動，可以和 ScrollTrigger 同步。
- 不擅長：它不做任何動畫，只改捲動手感。
- 框架：任何框架。
- 注意：要把 Lenis 的捲動事件接到 `ScrollTrigger.update`，否則捲動動畫會對不上。
- 官方：https://github.com/darkroomengineering/lenis

### Magic UI
- 擅長：AI SaaS、產品特色、價格方案、科技品牌——光束邊框、Shimmer 文字、聚光燈卡片、數字跳動、進場淡入。
- 框架：**只有 React**，需要 Tailwind CSS，用 shadcn CLI 把元件原始碼加進專案（不是 npm 套件）。
- 授權：MIT。
- 非 React 專案：效果本身多半可以用 CSS 或 Motion 原生版重做。
- 官方：https://magicui.design

### React Bits
- 擅長：Hero、CTA、作品集、科技感背景——文字特效、動態背景、磁吸按鈕、游標互動、卡片效果，數量很多（400+ 變體）。
- 框架：**只有 React**；每個元件有 JS／TS、CSS／Tailwind 四種版本；用 shadcn 或 jsrepo CLI 加進專案。
- 授權：MIT + Commons Clause——可以用在任何網站或產品（含商用），但**不能轉賣或轉散布元件本身**（包含改寫版本）。
- 官方：https://reactbits.dev

### Three.js／React Three Fiber
- 擅長：程式化 3D、粒子、shader、可互動的 3D 場景。
- 不擅長：讓設計師不寫程式就調整場景（用 Spline）。
- 框架：Three.js 任何框架；React Three Fiber 是 React 版。
- 注意：首頁載入成本高；手機要準備靜態替代。
- 官方：https://threejs.org

### Spline
- 擅長：在瀏覽器編輯器裡拖拉出 3D 場景，匯出後嵌入網站，不必寫 3D 程式。
- 框架：任何框架（`@splinetool/runtime`），React 有 `@splinetool/react-spline`。
- 注意：執行檔不小，延遲載入；場景太複雜會拖慢手機。
- 官方：https://docs.spline.design

### Rive
- 擅長：會依使用者操作改變狀態的動畫（state machine）——hover 時角色看過來、點擊切換表情、產品引導。
- 框架：任何框架，React 有官方套件。
- 注意：需要在 Rive 編輯器做動畫檔。
- 官方：https://rive.app/docs

### Lottie
- 擅長：播放設計師做好的向量動畫——Loading、成功提示、空狀態、插畫。
- 不擅長：依使用者操作改變狀態（用 Rive）。
- 框架：任何框架（`lottie-web`），React 有 `lottie-react`。
- 注意：素材來源（如 LottieFiles）各有授權，使用前確認。
- 官方：https://airbnb.io/lottie/

## 安裝原則

- 只裝規劃表用到的套件；不要「先全部裝起來再說」。
- 能用一個工具做完就不要用兩個：只有進場和 hover 的網站不需要 GSAP；只有滾動動畫的網站不需要 Motion。
- 專案已經裝了某個動畫套件，優先沿用。
