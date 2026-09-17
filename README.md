# 💰 Smart Expense & Cashflow Analyzer (智慧個人財務與現金流剖析器)

> 一個結合資料清洗、動態預算控管、多維度視覺化（甜甜圈圖與時間序列趨勢）及完整資料閉環的現代化個人財務決策管理系統。

## 🎯 專案動機 (Project Motivation)
本專案旨在透過 Python 與資料科學工具，打造一個能解決日常記帳痛點的互動式網頁應用程式。跳脫傳統記帳軟體的單調介面，本系統強調「資料洞察（Data Insights）」與「即時風險預警（Budget Tracking）」，協助使用者精準掌握個人現金流與消費習慣。

---

## 🛠️ 技術架構 (Tech Stack)
* **核心語言**：Python
* **網頁框架**：Streamlit (打造高效互動式前端儀表板)
* **數據處理與分析**：`pandas`, `numpy` (進行高效資料清洗、樞紐分析與條件篩選)
* **互動式資料視覺化**：`plotly` (支援動態甜甜圈佔比圖、時間序列趨勢折線圖)
* **版本控制與部署**：Git / GitHub, Google Colab, `pyngrok`

---

## ✨ 核心功能亮點 (Key Features)

### 1. 靈活的資料輸入與匯出 (Data Ingestion & Export)
* **手動新增**：支援自訂日期、項目名稱、消費類別與金額。
* **批次匯入**：支援上傳自訂的 CSV 格式記帳清單，自動進行資料驗證與整合。
* **資料匯出 (閉環設計)**：支援一鍵將最新財務報表打包下載回傳為 CSV 格式。

### 2. 動態預算控管與智慧警報 (Budget Control & Alerts)
* 自訂每月總預算上限，系統即時計算剩餘額度與已使用比例。
* 內建動態進度條與「財務健康度紅綠燈警告」，當花費超過 85% 時自動發出警示。

### 3. 多維度互動式視覺化分析 (Advanced Analytics & Visualization)
* **各類別開銷佔比**：採用 Plotly 製作的精美甜甜圈圓餅圖，讓開銷分佈一目了然。
* **每日消費趨勢圖**：結合時間序列折線圖，追蹤每日花費波動。

### 4. 智慧篩選與關鍵字搜尋 (Smart Filtering & Search)
* 提供類別下拉選單與關鍵字即時搜尋列，方便快速檢索與分析特定消費紀錄。

---

## 🚀 專案收穫與工程思維 (Takeaways)
* **Product-Oriented Mindset**：完整實現了從「資料輸入 (Input) -> 數據清洗與運算 (Process) -> 視覺化與匯出 (Output)」的完整產品生命週期。
* **User Experience (UX)**：透過 Streamlit 的狀態管理（Session State）與互動組件，打造流暢且直覺的使用者操作體驗。
