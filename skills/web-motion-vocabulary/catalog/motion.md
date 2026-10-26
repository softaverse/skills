# Motion

Motion（前身 Framer Motion），授權 MIT。有原生 JS 版（`motion`）與 React 版（`motion/react`），也有 Vue 版。Next.js App Router 裡要放在 Client Component（`"use client"`）。

格式：`**名稱** — 中文說明 → 對應效果 id · 官方文件`。手動維護，不由腳本同步。

## 原生 JS（任何網站都能用）

- **animate()** — 對元素或數值做動畫，支援彈簧與時間軸序列 → `stagger`、`countup` · https://motion.dev/docs/animate
- **inView()** — 元素進入畫面時觸發，離開時可執行收尾 → `reveal`、`countup` · https://motion.dev/docs/inview
- **scroll()** — 把動畫綁在捲動進度上，可用瀏覽器原生的 ScrollTimeline · https://motion.dev/docs/scroll
- **hover()** — 處理滑鼠懸停，自動排除觸控造成的假 hover → `spring` · https://motion.dev/docs/hover
- **press()** — 處理按下與放開，含鍵盤操作 → `spring` · https://motion.dev/docs/press
- **stagger()** — 讓一組元素依序延遲 → `stagger` · https://motion.dev/docs/stagger
- **spring** — 彈簧物理，讓動作有重量與回彈 → `spring` · https://motion.dev/docs/spring

## React

- **motion 元件** — `<motion.div>` 用屬性宣告動畫，是 React 版的核心 · https://motion.dev/docs/react-motion-component
- **動畫基礎** — `initial`、`animate`、`transition`、variants 的用法 · https://motion.dev/docs/react-animation
- **AnimatePresence** — 讓元件被移除時也能播放離場動畫 · https://motion.dev/docs/react-animate-presence
- **Layout animations** — 版面改變（展開、排序、換位置）時自動補間，加 `layout` 屬性即可 · https://motion.dev/docs/react-layout-animations
- **Scroll animations** — React 裡的捲動觸發與捲動連動動畫 → `reveal`、`parallax` · https://motion.dev/docs/react-scroll-animations
- **useScroll** — 取得捲動進度，搭配 useTransform 做視差或進度條 → `parallax` · https://motion.dev/docs/react-use-scroll
- **useTransform** — 把一個數值（如捲動進度）換算成另一個（位移、透明度） → `parallax`、`scrollzoom` · https://motion.dev/docs/react-use-transform
- **useSpring** — 讓數值帶彈簧慣性地跟隨 → `magnet` · https://motion.dev/docs/react-use-spring
- **useInView** — 元素是否在畫面中 → `reveal` · https://motion.dev/docs/react-use-in-view
- **useAnimate** — 在 React 裡用命令式方式控制動畫序列 · https://motion.dev/docs/react-use-animate
- **Gestures** — `whileHover`、`whileTap`、`whileFocus` 等手勢狀態 → `spring` · https://motion.dev/docs/react-gestures
- **Drag** — 拖曳，可加邊界、慣性與吸附 · https://motion.dev/docs/react-drag
- **Reorder** — 可拖曳排序的清單 · https://motion.dev/docs/react-reorder
