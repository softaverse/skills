# B｜游標互動

高級手感的來源，但只在有滑鼠的裝置上有效。手機與平板上這一類效果等於不存在，所以重要資訊絕不能只靠它傳達。預算上限：全站最多 3 個重點元素。

- **磁吸按鈕 (Magnetic Button)** `magnet` — 游標靠近按鈕時，按鈕會被「吸」向游標偏移一點，游標離開後再彈回原位。
  - 感受：精緻、好玩、高級手感
  - 適合：主要 CTA、導覽列、作品集的「聯絡我」
  - 搭配：spring
  - 注意：只給最重要的 1–2 個按鈕；偏移量太大會讓人點不到
  - 工具：GSAP（`quickTo`）或 Motion；React 有 React Bits Magnet
  - 成本：複雜度 低｜效能 低｜持續動畫 否
  - 手機：無效，按鈕維持靜止
  - 減少動態：關閉偏移
  - 來源：GSAP quickTo https://gsap.com/docs/v3/GSAP/gsap.quickTo() ；React Bits Magnet（MIT + Commons Clause）https://reactbits.dev/animations/magnet
  - Demo：`demos/magnet.js`（把游標移到按鈕附近，慢慢繞一圈）
- **3D 傾斜卡片 (Tilt Card)** `tilt` — 卡片隨游標位置往不同方向傾斜，表面帶一道跟著移動的反光，像手裡拿著一張實體卡片。
  - 感受：立體、可觸摸、精品感
  - 適合：作品集縮圖、產品卡、會員卡、名片
  - 搭配：spot
  - 注意：傾斜角度 10° 以內；卡片內文字多時會難讀
  - 工具：原生 JS + CSS `transform`（不需要套件）；React 有 React Bits Tilted Card
  - 成本：複雜度 低｜效能 低｜持續動畫 否
  - 手機：無效，卡片維持平放
  - 減少動態：關閉傾斜，保留 hover 陰影
  - 來源：React Bits Tilted Card（MIT + Commons Clause）https://reactbits.dev/components/tilted-card
  - Demo：`demos/tilt.js`（把游標移到卡片上畫圈）
- **聚光燈卡片 (Spotlight Card)** `spot` — 游標劃過卡片時，一圈柔和的光暈跟著游標走，連卡片邊框都被照亮。
  - 感受：科技感、探索感、精緻
  - 適合：功能特色卡片、AI / SaaS 產品、深色主題
  - 搭配：borderbeam、tilt
  - 注意：深色背景效果最明顯，淺色背景幾乎看不出來；同一區塊用一種光暈色
  - 工具：React 用 Magic UI Magic Card 或 React Bits Spotlight Card；非 React 用 CSS 變數 + `radial-gradient`
  - 成本：複雜度 低｜效能 低｜持續動畫 否
  - 手機：無效，可改成靜態的淡淡邊框光
  - 減少動態：保留，因為只跟著游標、不自己動
  - 來源：Magic UI Magic Card（MIT）https://magicui.design/docs/components/magic-card ；React Bits Spotlight Card（MIT + Commons Clause）https://reactbits.dev/components/spotlight-card
  - Demo：`demos/spot.js`（把游標在卡片之間移動）
