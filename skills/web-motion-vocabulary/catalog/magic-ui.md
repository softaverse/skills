# Magic UI

官方元件清單，由 `scripts/sync_catalog.py` 從 https://magicui.design/llms.txt 產生，2026-10-27 同步，共 78 個。只收名稱、說明與連結，不含程式碼。

React 專用，需要 Tailwind CSS；用 shadcn CLI 把元件原始碼加進專案。授權 MIT。

格式：`**名稱** — 中文說明 → 對應效果 id · 官方頁面`。沒有中文說明的是新元件，暫列英文。

## 元件（Components）

- **Android** — Android 手機外框樣機 · https://magicui.design/docs/components/android
- **Animated Beam** — 光束沿路徑在元素之間流動，常用來展示整合 → `linedraw` · https://magicui.design/docs/components/animated-beam
- **Animated Circular Progress Bar** — 環形百分比進度表 · https://magicui.design/docs/components/animated-circular-progress-bar
- **Animated Gradient Text** — 文字裡的漸層顏色持續變換 · https://magicui.design/docs/components/animated-gradient-text
- **Animated Grid Pattern** — 動態 SVG 網格背景 · https://magicui.design/docs/components/animated-grid-pattern
- **Animated List** — 清單項目依序延遲出現，適合通知或事件 → `stagger` · https://magicui.design/docs/components/animated-list
- **Animated Shiny Text** — 一道光掃過文字的流光效果 → `shimmer` · https://magicui.design/docs/components/animated-shiny-text
- **Theme Toggler** — 用 View Transitions 與遮罩動畫切換深淺色 · https://magicui.design/docs/components/animated-theme-toggler
- **Aurora Text** — 文字內有極光色彩流動 → `aurora` · https://magicui.design/docs/components/aurora-text
- **Avatar Circles** — 重疊排列的頭像 · https://magicui.design/docs/components/avatar-circles
- **Backlight** — 影片、圖片或 SVG 後方的背光光暈 · https://magicui.design/docs/components/backlight
- **Bento Grid** — 便當格版面，展示產品功能 · https://magicui.design/docs/components/bento-grid
- **Blur Fade** — 模糊淡入淡出 → `reveal` · https://magicui.design/docs/components/blur-fade
- **Border Beam** — 一道光沿容器邊框繞行 → `borderbeam` · https://magicui.design/docs/components/border-beam
- **Client Tweet Card** — 客戶端渲染的推文卡片 · https://magicui.design/docs/components/client-tweet-card
- **Code Comparison** — 左右比較兩段程式碼 · https://magicui.design/docs/components/code-comparison
- **Comic Text** — 漫畫風文字動畫 · https://magicui.design/docs/components/comic-text
- **Confetti** — 特別時刻灑出彩帶 · https://magicui.design/docs/components/confetti
- **Cool Mode** — 點擊按鈕或連結時噴出小圖案 · https://magicui.design/docs/components/cool-mode
- **Dia Text Reveal** — 一道色帶掃過文字，留下漸層光澤後定色 · https://magicui.design/docs/components/dia-text-reveal
- **Dock** — macOS Dock 實作 · https://magicui.design/docs/components/dock
- **Dot Pattern** — SVG 點陣背景 · https://magicui.design/docs/components/dot-pattern
- **Dotted Map** — 點陣地圖 · https://magicui.design/docs/components/dotted-map
- **File Tree** — 資料夾與檔案樹狀結構 · https://magicui.design/docs/components/file-tree
- **Flickering Grid** — 閃爍的 SVG 網格背景 · https://magicui.design/docs/components/flickering-grid
- **Floating 3D Particles** — 帶透視、旋轉與漂浮的偽 3D 粒子場 · https://magicui.design/docs/components/floating-3d-particles
- **Glare Hover** — hover 時斜向光澤掃過 → `tilt` · https://magicui.design/docs/components/glare-hover
- **Globe** — 自動旋轉、可互動的 WebGL 地球 → `hero3d` · https://magicui.design/docs/components/globe
- **Glyph Matrix** — 字元網格緩慢變換、淡出 · https://magicui.design/docs/components/glyph-matrix
- **Grid Pattern** — SVG 網格背景 · https://magicui.design/docs/components/grid-pattern
- **Hero Video Dialog** — Hero 區的影片彈窗 · https://magicui.design/docs/components/hero-video-dialog
- **Hexagon Pattern** — SVG 六角形背景 · https://magicui.design/docs/components/hexagon-pattern
- **Highlighter** — 模仿手繪螢光筆劃過文字 → `linedraw` · https://magicui.design/docs/components/highlighter
- **Hyper Text** — 字母先亂跳再顯示最終文字 → `scramble` · https://magicui.design/docs/components/hyper-text
- **Icon Cloud** — 可互動的 3D 圖示雲 · https://magicui.design/docs/components/icon-cloud
- **Interactive Grid Pattern** — 可互動的 SVG 網格背景 · https://magicui.design/docs/components/interactive-grid-pattern
- **interactive-hover-button** — hover 時有互動變化的按鈕 · https://magicui.design/docs/components/interactive-hover-button
- **iPhone** — iPhone 外框樣機 · https://magicui.design/docs/components/iphone
- **Kinetic Text** — hover 時字元的字重變化 · https://magicui.design/docs/components/kinetic-text
- **Lens** — 可以放大圖片或影片局部的放大鏡 · https://magicui.design/docs/components/lens
- **Light Rays** — 從上方灑下的動態光線 · https://magicui.design/docs/components/light-rays
- **Line Shadow Text** — 帶移動線條陰影的文字 · https://magicui.design/docs/components/line-shadow-text
- **Magic Card** — 聚光燈跟著游標並照亮邊框 → `spot` · https://magicui.design/docs/components/magic-card
- **Marquee** — 無限捲動的跑馬燈，可放文字、圖片、影片 · https://magicui.design/docs/components/marquee
- **Meteors** — 流星雨效果 · https://magicui.design/docs/components/meteors
- **Morphing Text** — 文字在詞與詞之間變形切換 · https://magicui.design/docs/components/morphing-text
- **Neon Gradient Card** — 霓虹漸層卡片 · https://magicui.design/docs/components/neon-gradient-card
- **Noise Texture** — SVG 雜訊質感疊加層 · https://magicui.design/docs/components/noise-texture
- **Number Ticker** — 數字往上或往下跳到目標值 → `countup` · https://magicui.design/docs/components/number-ticker
- **Orbiting Circles** — 沿圓形軌道運行的圓圈 · https://magicui.design/docs/components/orbiting-circles
- **Particles** — 增加景深與動感的粒子 · https://magicui.design/docs/components/particles
- **Pixel Image** — 像素化的復古圖片 · https://magicui.design/docs/components/pixel-image
- **Pointer** — hover 時顯示的自訂指標 · https://magicui.design/docs/components/pointer
- **Progressive Blur** — 捲動內容邊緣的漸進模糊，提示上下還有內容 · https://magicui.design/docs/components/progressive-blur
- **Pulsating Button** — 吸引注意的脈動按鈕 · https://magicui.design/docs/components/pulsating-button
- **Rainbow Button** — 彩虹流動按鈕 · https://magicui.design/docs/components/rainbow-button
- **Retro Grid** — 復古捲動網格 · https://magicui.design/docs/components/retro-grid
- **Ripple** — 元素後方的漣漪，用來強調 · https://magicui.design/docs/components/ripple
- **Ripple Button** — 點擊產生漣漪的按鈕 · https://magicui.design/docs/components/ripple-button
- **Safari** — Safari 瀏覽器樣機 · https://magicui.design/docs/components/safari
- **Scroll Based Velocity** — 速度隨捲動快慢改變的跑馬燈文字 · https://magicui.design/docs/components/scroll-based-velocity
- **Scroll Progress** — 頁面捲動進度條 · https://magicui.design/docs/components/scroll-progress
- **Shimmer Button** — 光沿按鈕外圍繞行的按鈕 → `borderbeam` · https://magicui.design/docs/components/shimmer-button
- **Shine Border** — 動態光澤邊框 → `borderbeam` · https://magicui.design/docs/components/shine-border
- **Shiny Button** — 深淺色都有光澤的按鈕 · https://magicui.design/docs/components/shiny-button
- **smooth-cursor** — 帶彈簧物理與旋轉的平滑游標 · https://magicui.design/docs/components/smooth-cursor
- **Sparkles Text** — 文字周圍不斷冒出星星 · https://magicui.design/docs/components/sparkles-text
- **Spinning Text** — 文字沿圓形旋轉 · https://magicui.design/docs/components/spinning-text
- **Striped Pattern** — SVG 條紋背景 · https://magicui.design/docs/components/striped-pattern
- **Terminal** — 終端機視窗 · https://magicui.design/docs/components/terminal
- **Text 3D Flip** — hover 時每個字母交錯 3D 翻轉 · https://magicui.design/docs/components/text-3d-flip
- **Text Animate** — 多種文字進場動畫 → `splitreveal` · https://magicui.design/docs/components/text-animate
- **Text Reveal** — 往下捲時文字逐字亮起 → `reveal` · https://magicui.design/docs/components/text-reveal
- **Tweet Card** — 推文卡片 · https://magicui.design/docs/components/tweet-card
- **Typing Animation** — 打字機逐字出現 · https://magicui.design/docs/components/typing-animation
- **Video Text** — 文字裡播放影片 · https://magicui.design/docs/components/video-text
- **Warp Background** — 時空扭曲背景卡片 · https://magicui.design/docs/components/warp-background
- **Word Rotate** — 詞語垂直輪替 · https://magicui.design/docs/components/word-rotate
