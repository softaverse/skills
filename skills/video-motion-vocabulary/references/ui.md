# 介面模擬

用動畫重做一個「看起來像真的在操作」的畫面，而不是螢幕錄影。比錄影好的地方：乾淨、可控、
能放大、能改字。先決定**要多像真的**：品牌原樣（ChatGPT、Claude、終端機）、還是通用樣式。
用真實產品的外觀時，注意不要讓人誤以為是官方畫面。

## AI 與輸入

- **輸入框打字 (Typed Prompt)** `prompt` — 一個 AI 對話輸入框，提示詞照人手的節奏打出來，最後按下送出。
  - 感受：真實、「我就是這樣問的」
  - 適合：展示提示詞、AI 工具教學
  - 搭配：Typewriter、Push-in、Punch-in、AI Stream
  - 注意：長提示詞要加速或只打關鍵部分
  - 範例：`kit/chat-prompt` `catalog-components/typed-prompt` `snapcn/prompt-send` `remocn/claude-chat`
- **AI 串流回答 (AI Streaming Answer)** `aistream` — AI 的回答一段段不均勻地冒出來，像真的在生成，可能先有思考點點、搜尋步驟。
  - 感受：AI、即時、正在思考
  - 適合：展示 AI 回答、對比好壞回答
  - 搭配：Typed Prompt、Selection、Marker
  - 注意：回答太長就快轉，只停在重點句
  - 範例：`catalog-components/streaming-text` `snapcn/answer-stream` `catalog/claude-exchange` `catalog/chatgpt-exchange`
- **AI 代理步驟 (Agent Steps)** `agentsteps` — AI 代理的工作紀錄：一步步列出「讀檔、搜尋、執行、完成」，有勾勾和狀態。
  - 感受：自動化、可靠、看得到過程
  - 適合：Claude Code、AI Agent 的展示
  - 搭配：Terminal、Progress Fill
  - 注意：步驟名要短
  - 範例：`snapcn/agent-steps` `remocn/agent-run` `catalog-components/agent-cursor`
- **對話泡泡 (Chat Bubbles)** `chat` — 訊息一則則彈出，對方輸入中先出現三個點點。
  - 感受：對話、生活、社群
  - 適合：簡訊、Slack、Discord、客服
  - 搭配：Typing Indicator、Notification
  - 注意：每則訊息要給閱讀時間
  - 範例：`catalog-components/chat-thread` `remotion-inspired/chat-messages` `catalog/message-thread-reveal` `snapcn/channel-thread`
- **筆記打字 (Notes Typing)** `notes` — 筆記 App 裡逐字打出一段文字，頁面跟著往上捲。
  - 感受：私密、真心話、日記
  - 適合：自白、清單、想法
  - 搭配：Typewriter
  - 注意：中文輸入沒有注音過程就好
  - 範例：`catalog-components/notes-typing` `catalog/notes-reveal`
- **搜尋框 (Search Bar)** `searchbar` — 一條大搜尋框撐開，搜尋字打進去，下面跳出結果。
  - 感受：好奇、研究、「有沒有……」
  - 適合：章節開場的問題、找工具、研究
  - 搭配：Push-in、Typewriter
  - 注意：搜尋框可以很大，當成標題用
  - 範例：`snapcn/search-typing` `remocn/search-reveal` `herk-kallaway/t1-section-searchbar` `find-existing-tools`

## 開發者畫面

- **終端機 (Terminal)** `terminal` — 終端機視窗：指令一個字一個字打出來，按 Enter 後輸出一行行出現。
  - 感受：開發者、真實、專業
  - 適合：CLI 工具、安裝步驟、Claude Code
  - 搭配：Zoom-follow、Agent Steps
  - 注意：輸出太長就捲動或截斷；字要夠大
  - 範例：`kit/terminal-type` `catalog-components/terminal-simulator` `claude-code-terminal` `remocn/claude-code`
- **程式碼打字 (Code Typing)** `codetype` — 編輯器裡程式碼逐字打出、有語法上色，旁邊可以同步出現預覽。
  - 感受：開發中、透明、可以學
  - 適合：程式教學、「AI 寫出來的 code」
  - 搭配：Highlight Band、Scroll Camera
  - 注意：不要逐字打完一整個檔案——觀眾讀不完
  - 範例：`catalog/code-typing` `catalog/code-snippet-dark-modern` `remocn/live-code-compilation` `remocn/glass-code-block`
- **程式碼變化 (Code Diff / Morph)** `codediff` — 一段程式碼變成另一段：刪除的行紅色收起、新增的綠色長出，或 token 滑到新位置。
  - 感受：重構、修正、改了什麼一目了然
  - 適合：前後版本、修 bug、重構
  - 搭配：Highlight Band
  - 注意：一次只改幾行
  - 範例：`catalog/code-diff` `catalog/code-morph`
- **立體程式碼 (Code FX)** `codefx` — 程式碼浮在 3D 板子上翻轉、或從雜訊溶解出現。
  - 感受：炫、片頭、開發者品牌
  - 適合：片頭、章節開場
  - 搭配：Type 3D、Orbit
  - 注意：好看但讀不清——不要放要讀的 code
  - 範例：`catalog/code-3d-extrude` `code-3d-extrude` `catalog/code-shader-dissolve`

## 游標與手勢

- **游標點擊 (Cursor Click)** `cursorclick` — 一個游標移到按鈕上、停一下、按下去，有一圈波紋。
  - 感受：操作示範、清楚
  - 適合：UI 教學、「按這裡」
  - 搭配：Zoom-follow、Ripple
  - 注意：游標要放大（2–3 倍）才看得到
  - 範例：`remocn/simulated-cursor` `snapcn/cursor-track` `catalog-components/press-ripple` `catalog-components/oversized-cursor`
- **游標操作 (Cursor Drag / Select)** `cursorop` — 游標拖曳卡片、框選一群東西、選取文字、右鍵開選單。
  - 感受：真實操作、流暢
  - 適合：拖拉式工具、檔案管理、設計工具
  - 搭配：Physics、Spring
  - 注意：被拖的東西要有一點傾斜和陰影，才有拿起來的感覺
  - 範例：`catalog-components/cursor-drag-drop` `catalog-components/cursor-marquee-select` `catalog-components/cursor-text-select` `catalog-components/cursor-context-menu`
- **磁吸游標 (Magnetic Cursor)** `magnetcursor` — 游標靠近按鈕時被吸過去，變形成按鈕的懸停框。
  - 感受：精緻、高級 UI、Apple 感
  - 適合：產品宣傳、設計工具
  - 搭配：Micro UI、Spring
  - 注意：只在少數重點按鈕上
  - 範例：`catalog-components/magnetic-cursor` `catalog-components/multiplayer-cursors`
- **觸控手勢 (Touch Gesture)** `touch` — 半透明的圓點代表手指：點擊、滑動、下拉重新整理。
  - 感受：手機、直覺
  - 適合：App 示範
  - 搭配：Device Frame、Sheet
  - 注意：手勢的速度要像真的手指
  - 範例：`catalog-components/touch-indicator` `catalog-components/gesture-tap` `catalog-components/swipe-rail` `catalog-components/pull-to-refresh`

## 裝置與介面片段

- **裝置框 (Device Mockup)** `device` — 手機、平板、筆電、瀏覽器的外框，裡面放介面；可以浮動、旋轉、展開成多台。
  - 感受：產品、真實、專業
  - 適合：App 宣傳、網站展示
  - 搭配：Orbit、Dive、Shine
  - 注意：外框越寫實越重，簡單的瀏覽器框常常就夠
  - 範例：`catalog-components/device-frame-stage` `catalog-components/browser-device-stage` `catalog-components/multi-device-splay` `catalog/app-showcase`
- **通知轟炸 (Notification Stack)** `notifstack` — 手機通知一則接一則掉下來疊起來，越來越快。
  - 感受：忙碌、壓力、熱門
  - 適合：痛點、「大家都在找你」、熱度
  - 搭配：Escalation、Shake
  - 注意：結尾要有釋放
  - 範例：`catalog/notification-cascade` `catalog-components/notification-pileup` `catalog-components/notification-stack` `catalog-components/native-notification-pop`
- **介面微轉場 (Micro UI)** `microui` — 開關切換、分頁指示滑動、成功打勾、輸入錯誤抖動、選單變形。
  - 感受：精緻、真實、好用
  - 適合：產品介面展示、狀態變化
  - 搭配：Spring、Cursor Click
  - 注意：每個都很短（0.2–0.4s）
  - 範例：`catalog-components/micro-transitions` `catalog-components/toggle-flip` `catalog-components/success-check` `catalog-components/tabs-slide-indicator`
- **表單流程 (Form Flow)** `formflow` — 註冊、引導、設定頁的完整流程：欄位填入、按鈕按下、下一步。
  - 感受：簡單、上手很快
  - 適合：「三步就完成」、新手引導
  - 搭配：Cursor Click、Stepper
  - 注意：只演關鍵步驟
  - 範例：`catalog-components/signup-flow` `catalog-components/onboarding-stepper-flow` `catalog-components/settings-toggle-flow`
- **底部面板 (Bottom Sheet)** `sheet` — 手機底部的面板彈簧般衝上來，裡面的內容輪播。
  - 感受：App、原生、流暢
  - 適合：分享、選項、App 示範
  - 搭配：Spring、Device Frame
  - 注意：彈簧的手感是重點
  - 範例：`catalog-components/sheet-spring-up` `catalog/share-sheet-carousel`
- **骨架載入 (Skeleton)** `skeleton` — 先出現灰色的內容輪廓脈動，再換成真正的內容。
  - 感受：載入中、真實 App
  - 適合：「資料進來了」、動態牆
  - 搭配：Fade、Stagger
  - 注意：骨架要接近真實排版
  - 範例：`catalog-components/skeleton-reveal` `catalog-components/scroll-feed`
- **貼文牆 (Post Wall)** `postwall` — 社群貼文一則則彈出、互相疊壓，堆成一面牆。
  - 感受：熱鬧、真實需求、很多人在說
  - 適合：證明一個需求、輿論、社群觀察
  - 搭配：Escalation、Stamp
  - 注意：去識別化
  - 範例：`social-posts-wall` `catalog-components/scroll-feed`
- **設計軟體 (Vector Editor)** `vectoredit` — 設計軟體的畫面：鋼筆工具畫出路徑、錨點、控制把手。
  - 感受：設計過程、專業工具
  - 適合：設計教學、logo 製作過程
  - 搭配：Cursor、Outline Draw
  - 注意：路徑要畫得像人在畫
  - 範例：`catalog-components/vector-editor-rig`
