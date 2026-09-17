import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Smart Expense Analyzer", page_icon="💰", layout="wide")

st.title("💰 Smart Expense & Cashflow Analyzer 智慧個人財務與現金流剖析器")
st.markdown("結合資料清洗、預算控管、時間序列趨勢分析與匯出功能的個人化財務決策系統。")

# --- 初始化 Session State ---
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"日期": "2026-09-01", "項目": "便當", "類別": "伙食餐飲", "金額": 120},
        {"日期": "2026-09-03", "項目": "捷運", "類別": "交通通勤", "金額": 50},
        {"日期": "2026-09-05", "項目": "電影票", "類別": "休閒娛樂", "金額": 350},
        {"日期": "2026-09-10", "項目": "咖啡", "類別": "伙食餐飲", "金額": 80},
        {"日期": "2026-09-15", "項目": "超級市場", "類別": "生活日用", "金額": 680},
    ])

# --- 側邊欄：功能選單與控制面板 ---
st.sidebar.header("⚙️ 財務控制面板")
menu = st.sidebar.selectbox("選擇操作功能", ["📝 手動新增消費", "📂 批量上傳 CSV 帳單", "🎯 設定每月預算", "📥 匯出財務報表"])

if menu == "📝 手動新增消費":
    st.sidebar.subheader("新增單筆消費")
    item_date = st.sidebar.date_input("消費日期")
    item_name = st.sidebar.text_input("消費項目名稱", "晚餐")
    item_category = st.sidebar.selectbox("消費類別", ["伙食餐飲", "交通通勤", "休閒娛樂", "生活日用", "投資理財", "其他"])
    item_amount = st.sidebar.number_input("金額 (元)", value=100, step=10)

    if st.sidebar.button("➕ 確認新增"):
        new_row = pd.DataFrame([{
            "日期": str(item_date), 
            "項目": item_name, 
            "類別": item_category, 
            "金額": item_amount
        }])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_row], ignore_index=True)
        st.sidebar.success("新增成功！")

elif menu == "📂 批量上傳 CSV 帳單":
    st.sidebar.subheader("上傳你的記帳 CSV 檔案")
    uploaded_file = st.sidebar.file_uploader("選擇 CSV 檔 (需包含 日期, 項目, 類別, 金額 欄位)", type=["csv"])
    if uploaded_file is not None:
        user_df = pd.read_csv(uploaded_file)
        if all(col in user_df.columns for col in ["項目", "類別", "金額"]):
            if "日期" not in user_df.columns:
                user_df["日期"] = "2026-09-15"
            st.session_state.expenses = pd.concat([st.session_state.expenses, user_df], ignore_index=True)
            st.sidebar.success("CSV 數據成功匯入！")
        else:
            st.sidebar.error("CSV 格式有誤，請確保至少包含「項目」、「類別」、「金額」欄位！")

elif menu == "🎯 設定每月預算":
    st.sidebar.subheader("設定你的財務目標")
    monthly_budget = st.sidebar.number_input("每月總預算上限 (元)", value=15000, step=1000)
    st.session_state.monthly_budget = monthly_budget

elif menu == "📥 匯出財務報表":
    st.sidebar.subheader("下載最新財務資料")
    df_export = st.session_state.expenses
    csv_data = df_export.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 下載完整記帳 CSV",
        data=csv_data,
        file_name="my_expenses_report.csv",
        mime="text/csv",
    )

# --- 主畫面：動態數據儀表板 ---
df = st.session_state.expenses

if not df.empty:
    total_spent = df["金額"].sum()
    budget = st.session_state.get("monthly_budget", 15000)
    remaining_budget = budget - total_spent
    budget_usage_pct = total_spent / budget if budget > 0 else 0

    # 頂部關鍵指標
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💸 本月累積總支出", value=f"$ {total_spent:,}")
    with col2:
        st.metric(label="🎯 本月預算剩餘", value=f"$ {remaining_budget:,}", delta=f"{-budget_usage_pct*100:.1f}% 已使用")
    with col3:
        st.metric(label="📋 記帳總筆數", value=f"{len(df)} 筆")

    # 預算進度條警告
    st.subheader("⚠️ 預算控制健康度")
    st.progress(min(budget_usage_pct, 1.0))
    if budget_usage_pct > 0.85:
        st.error("🚨 警告：您的本月支出已接近或超過預算上限，請注意開銷！")
    else:
        st.success("✅ 目前財務狀況在安全範圍內！")

    st.markdown("---")

    # 圖表區：圓餅圖 (佔比) + 折線圖 (時間序列趨勢)
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🥧 各類別開銷佔比分析")
        category_df = df.groupby("類別")["金額"].sum().reset_index()
        fig_pie = px.pie(
            category_df, 
            values='金額', 
            names='類別', 
            hole=0.4, 
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("📈 每日消費金額趨勢")
        if "日期" in df.columns:
            trend_df = df.groupby("日期")["金額"].sum().reset_index()
            fig_line = px.line(
                trend_df, 
                x='日期', 
                y='金額', 
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["#FF4B4B"]
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("尚無日期資料可供繪製趨勢圖。")

    st.markdown("---")

    # 數據篩選與表格區
    st.subheader("🔍 詳細消費紀錄與智慧篩選")
    
    # 智慧篩選工具列
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_category = st.selectbox("依類別篩選檢視", ["全部顯示"] + list(df["類別"].unique()))
    with filter_col2:
        search_keyword = st.text_input("關鍵字搜尋項目名稱", "")

    # 套用篩選條件
    filtered_df = df.copy()
    if selected_category != "全部顯示":
        filtered_df = filtered_df[filtered_df["類別"] == selected_category]
    if search_keyword:
        filtered_df = filtered_df[filtered_df["項目"].str.contains(search_keyword, case=False, na=False)]

    st.dataframe(filtered_df, use_container_width=True, height=300)

else:
    st.info("目前尚無記帳資料，請從左側新增或上傳！")
