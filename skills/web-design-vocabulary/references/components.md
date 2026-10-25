# 介面元件與導覽

## 介面元件語彙 (Component Patterns)

- **藥丸按鈕 (Pill Button)** `pill` — 全圓角的膠囊形按鈕。
- **浮動操作按鈕 (FAB)** `fab` — 懸浮在畫面角落的主要操作按鈕。
- **抽屜／底部彈出面板 (Drawer / Bottom Sheet)** `sheet` — 從側邊或底部滑出的面板。
- **指令面板 (Command Palette)** `cmdk` — 按 ⌘K 叫出的搜尋與指令框（Linear、Raycast 式）。
- **空狀態設計 (Empty State)** `empty` — 沒有資料時，用插圖加引導文案代替一片空白。
- **吐司通知 (Toast)** `toast` — 從角落短暫浮出、自動消失的訊息。
- **對話框 (Modal / Dialog)** `modal` — 蓋在頁面上、需要使用者回應的視窗。
- **工具提示 (Tooltip)** `tooltip` — 滑過時出現的小說明框。
- **分段控制 (Segmented Control)** `seg` — 幾個並排按鈕的單選切換。
- **標籤／徽章 (Chip / Badge)** `chips` — 小型圓角標籤，用來分類或顯示數量。
- **步驟條 (Stepper)** `stepper` — 顯示多步驟流程進度。
- **麵包屑 (Breadcrumb)** `breadcrumb` — 「首頁 › 分類 › 頁面」的路徑導覽。
- **頭像疊放 (Avatar Stack)** `avatars` — 多個頭像重疊排列，表示成員或協作者。
- **定價表 (Pricing Table)** `pricing` — 並排的方案卡，中間那張通常被強調。
- **看板 (Kanban Board)** `kanban` — 分欄的任務卡片（Trello 式）。
- **手風琴 (Accordion)** `accordion` — 點標題才展開內容的摺疊列表。
- **輪播 (Carousel)** `carousel` — 左右切換的圖片或卡片，帶指示點。
- **分頁標籤 (Tabs)** `tabs` — 同一區塊用標籤切換不同內容。
- **開關 (Toggle Switch)** `toggle` — 二選一的滑動開關。
- **滑桿 (Slider)** `slider` — 拖曳把手調整數值。
- **日期選擇器 (Date Picker)** `datepicker` — 月曆格狀的日期選取元件。
- **評分星等 (Rating)** `rating` — 一到五顆星的評分。
- **進度條 (Progress Bar)** `progress` — 顯示完成百分比的長條。
- **時間軸 (Timeline)** `timeline` — 沿一條線排列的事件節點。
- **即時驗證 (Inline Validation)** `valid` — 輸入時就在欄位旁顯示對錯。
- **下拉選單 (Dropdown / Select)** `dropdown` — 點開後列出選項。
- **搜尋列 (Search Bar)** `search` — 帶放大鏡圖示的輸入框。
- **檔案上傳區 (Dropzone)** `dropzone` — 虛線框的拖放上傳區。
- **資料表格 (Data Table)** `table` — 可排序、篩選的表格。
- **通知中心 (Notification Center)** `notif` — 集中顯示通知的面板。
- **前後對比滑桿 (Before / After Slider)** `ba` — 拖動分隔線比較兩張圖。
- **驗證碼輸入 (OTP Input)** `otp` — 一格一個數字的驗證碼欄位。
- **Cookie 橫幅 (Cookie Banner)** `cookie` — 底部的隱私同意提示。
- **懸浮卡 (Popover / Hover Card)** `popover` — 滑過或點擊時浮出的小資訊卡。
- **標籤輸入 (Tag Input)** `taginput` — 輸入後變成可刪除的標籤。
- **影片播放器 (Video Player)** `player` — 播放鍵、進度條、音量與全螢幕控制。
- **地圖標記 (Map Pin)** `mappin` — 地圖上的定位針與資訊氣泡。
- **留言串 (Comment Thread)** `comments` — 頭像、留言和縮排回覆。
- **個人資料卡 (Profile Card)** `profile` — 頭像、名稱、簡介和追蹤按鈕。
- **大型頁尾 (Fat Footer)** `footer` — 多欄連結、訂閱表單與社群圖示。
- **燈箱 (Lightbox)** `lightbox` — 點圖後放大、背景變暗的檢視模式。

## 導覽模式 (Navigation)

- **漢堡選單 (Hamburger Menu)** `hamburger` — 三條線圖示，點開展開選單。
- **底部分頁列 (Tab Bar)** `tabbar` — 手機底部固定的 3 到 5 個主要入口。
- **巨型選單 (Mega Menu)** `megamenu` — 滑過後展開大面板，分欄列出所有連結。
- **浮動導覽列 (Floating Nav)** `floatnav` — 膠囊形、懸浮且帶模糊背景的導覽列。
- **目錄跟隨 (Scrollspy / TOC)** `scrollspy` — 側邊目錄隨捲動標示目前章節。
- **分頁器 (Pagination)** `pagination` — 「‹ 1 2 3 … 10 ›」的頁碼導覽。
