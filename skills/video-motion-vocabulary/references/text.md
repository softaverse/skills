# 文字動畫

文字怎麼進場、怎麼變、怎麼離開。字幕（跟著講話時間）在 `captions.md`；指向某個詞的
強調在 `emphasis.md`。

## 進場

- **上浮淡入 (Rise / Fade-up)** `rise` — 字從下方一小段距離往上移、同時淡入，落定後停住。可以整句、逐詞或逐字。
  - 感受：俐落、乾淨、專業，最不會出錯
  - 適合：標題、章節字卡、金句的預設進場
  - 搭配：Stagger、Ease-out、Eyebrow Rule
  - 注意：位移 20–40px 就夠，移太遠會像在飄；全片都用它會沒有記憶點
  - 範例：`recipes/headline-rise` `recipes/char-rise` `catalog-components/per-word-rise` `catalog-components/staggered-fade-up`
- **模糊浮現 (Blur-in / Focus Resolve)** `blurin` — 字從失焦的模糊慢慢變清楚，像鏡頭對焦。
  - 感受：柔和、高級、電影感、有呼吸
  - 適合：開場標題、安靜的金句、品牌字
  - 搭配：Push-in、Tracking-in、Calm Pacing
  - 注意：模糊量大的話要 0.6s 以上才不會糊成一團；不適合要快速讀的資訊
  - 範例：`catalog-components/blur-in` `catalog-components/focus-blur-resolve` `catalog-components/soft-blur-in` `catalog/yt-prism-title`
- **遮罩揭露 (Mask Reveal)** `maskline` — 字從一條看不見的線下方升上來，超出線的部分被裁掉，像從縫裡冒出。
  - 感受：精準、編輯感、有設計
  - 適合：標題、換句、名牌名字
  - 搭配：Stagger、Line Swap
  - 注意：遮罩邊緣要對齊行高，不然字的下緣會被切到
  - 範例：`catalog-components/line-swap` `catalog-components/bottom-up-letters` `catalog/lt-mask-reveal` `remocn/caption-rise`
- **擦除揭露 (Clip Wipe)** `clipwipe` — 一道看不見的邊從左往右推，推過的地方字才出現。
  - 感受：有方向、像在寫出來、俐落
  - 適合：名牌、副標、一行說明
  - 搭配：Accent Rule 同步畫出、Ease-out
  - 注意：方向要跟閱讀方向一致（左→右）
  - 範例：`catalog-components/caption-clip-wipe` `catalog-components/colorama-wipe` `catalog/lt-clean-bar`
- **字距收攏 (Tracking-in)** `trackingin` — 字母一開始散得很開，慢慢收攏到正常字距。
  - 感受：高級、精品、電影片頭
  - 適合：英文標題、品牌名、短詞
  - 搭配：Blur-in、Fade、Calm Pacing
  - 注意：中文效果弱很多；只用在短字串
  - 範例：`catalog-components/tracking-in`
- **階梯字母 (Letter Staircase)** `letterdrop` — 字母一個接一個從上方（或下方）落進位置，排成明顯的階梯。
  - 感受：俏皮、有節奏、看得到「一個一個」
  - 適合：短標題、單字、英文 logo 字
  - 搭配：Spring、Stagger
  - 注意：字一多就太慢
  - 範例：`catalog-components/top-down-letters` `catalog-components/bottom-up-letters`
- **中心推擠 (Kinetic Center Build)** `centerbuild` — 詞從右邊一個個加入，把已經在的詞往左推，最後整句剛好置中鎖住。
  - 感受：動能、講話的節奏感、短影音
  - 適合：一句口號、片頭標語
  - 搭配：Word Pop、Beat Sync
  - 注意：句子長於 6–7 個詞就看不完
  - 範例：`catalog-components/kinetic-center-build`

## 重擊與能量

- **字砸下來 (Headline Slam)** `slam` — 大字從放大狀態快速縮到定位、「咚」一聲落地，常帶幾格畫面晃動。
  - 感受：衝擊、肯定、重點就是這個
  - 適合：一個關鍵詞、數字揭曉、轉折句
  - 搭配：Impact、Camera Shake、Beat Sync、Flash
  - 注意：一支片用一兩次才有力；連續砸會疲乏；疊畫面時會蓋到講者
  - 範例：`catalog-components/headline-slam` `catalog-components/caption-kinetic-slam` `catalog-components/shutter-slam` `catalog-components/char-slam-explode`
- **故障字 (RGB Glitch Text)** `glitchtext` — 紅藍綠三色分離、短暫抖動跳格，再恢復成正常字。
  - 感受：科技、駭客、出錯、不穩定
  - 適合：「壞掉了」「警告」、科技主題的轉折
  - 搭配：Scramble、CRT、Glitch Transition
  - 注意：時間要短（< 0.5s）；長時間抖動很難讀
  - 範例：`catalog-components/rgb-glitch-text` `catalog-components/scan-band` `catalog-components/caption-glitch-rgb`
- **立體字 (3D Type)** `type3d` — 有厚度、會反光的 3D 字在空間裡翻轉、組合後定住。
  - 感受：大製作、片頭、電影感
  - 適合：開場片名、品牌定版
  - 搭配：Orbit、Light Leak、Particles
  - 注意：製作和 render 成本高；和平面簡報風格放在一起會突兀
  - 範例：`catalog/extruded-logo` `catalog/glass-shard-title` `catalog/wireframe-portal-title` `catalog/canopy-part-title`
- **粒子組字 (Particle Text)** `particletext` — 一大片粒子飛過來聚成字（或字散成粒子）。
  - 感受：魔法、科技、生成感
  - 適合：AI 相關的揭曉、片頭
  - 搭配：Space / Particles 背景、Blur-in
  - 注意：要夠暗的背景才看得到；成本高
  - 範例：`catalog-components/particle-text-dissolve` `catalog/code-particle-assemble`

## 打字與解碼

- **打字機 (Typewriter / Type-on)** `typewriter` — 字一個一個打出來，後面跟著閃爍的游標。
  - 感受：真實、正在發生、像在輸入
  - 適合：提示詞、指令、搜尋字、引用一句話
  - 搭配：Typed Prompt、Terminal、Push-in
  - 注意：長句要加速或分段；中文一秒 8–12 字比較自然
  - 範例：`recipes/type-on` `catalog-components/typewriter` `catalog-components/typed-prompt` `kit/terminal-type`
- **亂碼解碼 (Scramble Decode)** `scramble` — 字先是一串亂跳的符號，再從左到右一個個定成正確的字。
  - 感受：駭客、解密、揭曉
  - 適合：揭曉答案、科技名詞、密碼、數據
  - 搭配：Glitch Text、Terminal、CRT
  - 注意：中文可以用，但亂碼字元集要選好看的；別在嚴肅主題用
  - 範例：`catalog-components/scramble-reveal` `catalog-components/matrix-decode` `catalog-components/caption-matrix-decode` `remocn/caption-scramble`
- **翻牌看板 (Split-flap)** `splitflap` — 機場翻牌：每格一塊翻牌，嘩啦啦翻過幾個字後停在目標。
  - 感受：復古、機械、出發、期待
  - 適合：目的地、日期、倒數、揭曉名稱
  - 搭配：Slot Roll、Ticker
  - 注意：有「喀啦」音效效果加倍；字數太多太吵
  - 範例：`catalog/split-flap-board` `remocn/caption-split-flap`
- **拉霸滾動 (Slot Roll)** `slotroll` — 字或數字像拉霸機一樣垂直滾動，最後停在目標值。
  - 感受：期待、揭曉、遊戲感
  - 適合：價格、排名、選項揭曉
  - 搭配：Odometer、Impact
  - 注意：停下前減速要明顯，不然像跳針
  - 範例：`catalog-components/slot-machine-roll` `catalog-components/ticker-takeover` `remocn/caption-slot`

## 變化與替換

- **換字輪播 (Word Swap)** `wordswap` — 句子其他部分不動，只有一個詞的位置一直換成別的詞。
  - 感受：可能性很多、輕快、有梗
  - 適合：「做給 ___ 的工具」「正在 ___」這種句型
  - 搭配：Mask Reveal、Caret
  - 注意：換的詞長度差太多，整句會跳動；最好預留最寬的位置
  - 範例：`catalog-components/kinetic-type-swap` `snapcn/status-cycle` `remotion-inspired/text-wheel` `catalog-components/text-state-swap`
- **劃掉改寫 (Strikethrough Replace)** `strikereplace` — 舊的字被一條線劃掉，旁邊或原地換上新的字。
  - 感受：修正、反轉、「其實不是這樣」
  - 適合：迷思 vs 事實、改名、前後對照
  - 搭配：Strike、Hand Underline
  - 注意：舊字要留夠久讓人讀完再劃
  - 範例：`catalog-components/strikethrough-replace` `catalog-components/caret-swap` `herk-vox-explainer/t1-section-correction`
- **文字匹配剪接 (Text Match Cut)** `textmatch` — 一行字在移動中途瞬間換成另一行，速度和位置連續，像同一個東西變了。
  - 感受：巧妙、俐落、剪接感
  - 適合：A 變成 B 的轉折、兩個概念的對應
  - 搭配：Match Cut、Whip Pan
  - 注意：兩行字要在同一位置、差不多寬
  - 範例：`catalog-components/text-match-cut` `catalog-components/type-match-cut`
- **字重變化 (Variable Weight)** `varweight` — 字的粗細（或寬窄）在原地流動變化，從細到粗、或一道粗細的浪掃過去。
  - 感受：優雅、有設計感、強調但不吵
  - 適合：一個關鍵詞的強調、品牌字
  - 搭配：Calm Pacing、Tracking-in
  - 注意：需要可變字型；中文可變字型選擇少
  - 範例：`catalog-components/variable-font-flex` `catalog-components/variable-axis-type` `catalog/weight-wave` `remocn/caption-weight`
- **黏液變形字 (Gooey Morph Text)** `gooeytext` — 一個詞像液體一樣融化、流成下一個詞。
  - 感受：流動、有趣、有機
  - 適合：一系列詞的輪播、品牌形容詞
  - 搭配：Blob、Liquid 背景
  - 注意：細字體和中文容易糊掉
  - 範例：`catalog-components/morph-text`
- **掃光字 (Text Shimmer)** `shimmer` — 一道亮光從字的左邊掃到右邊，掃完回到普通樣子。
  - 感受：精緻、高級、AI 產品感
  - 適合：產品名、「AI」、重點詞的收尾
  - 搭配：Dark 背景、Gloss Sweep
  - 注意：只掃一次最高級；循環掃像載入中
  - 範例：`catalog-components/text-shimmer` `catalog-components/shimmer-sweep`

## 手寫與材質

- **手寫寫出 (Write-on)** `writeon` — 字照筆畫順序一筆一筆寫出來，像有人正在寫。
  - 感受：溫度、親切、手作、筆記感
  - 適合：標註、標題的一部分、溫暖的結語
  - 搭配：Hand Underline、Boil、Whiteboard
  - 注意：真正照筆順需要描邊字型；中文多用遮罩往右推來模擬
  - 範例：`catalog/hw-write-title` `remocn/handwrite` `catalog-components/stitched-text-draw` `catalog/hw-path-text`
- **材質字 (Texture Fill Text)** `texturetext` — 大字裡面填的是流動的材質或影像（大理石、岩漿、影片）。
  - 感受：大膽、海報感、有質地
  - 適合：一兩個英文大字、片名
  - 搭配：Big Type、Full-bleed
  - 注意：字要夠粗夠大，材質才看得到
  - 範例：`catalog-components/texture-mask-text` `catalog-components/caption-texture` `catalog-components/svg-mask-reveal`
- **堆疊大字 (Stacked Type)** `stacktype` — 一句話拆成幾行大字往下疊，關鍵詞最大。
  - 感受：海報、張力、強勢
  - 適合：章節標題、口號
  - 搭配：Slam、Stagger
  - 注意：中文斷行要手動決定
  - 範例：`herk-kallaway/t1-section-stacked-words` `herk-kallaway/t1-section-type-scale` `remocn/caption-stack`
- **浮水印大字 (Ghost Word)** `ghostword` — 背景放一個超大、很淡的字，慢慢平移，當成紋理。
  - 感受：有層次、雜誌感、不空
  - 適合：章節字卡、步驟字卡的背景
  - 搭配：Rise、Calm Pacing
  - 注意：透明度要夠低（< 10%），不然會跟主標搶
  - 範例：`recipes/ghost-drift` `catalog-components/mk-emphasis-type` `kit/step-card`
