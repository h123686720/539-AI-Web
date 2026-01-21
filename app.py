import streamlit as st
import pandas as pd
from collections import Counter

# 網頁設定
st.set_page_config(page_title="539 AI 智能研發系統", layout="centered")

st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)
st.divider()

# 核心邏輯：讀取您親手校對的 CSV
try:
    # 讀取 CSV，確保編碼正確
    df = pd.read_csv('history539.csv', encoding='utf-8-sig')
    
    # 顯示分析期數，讓您確認數據量
    total_records = len(df)
    latest_date = df.iloc[0, 0]
    latest_nums = [str(x).zfill(2) for x in df.iloc[0, 1:6].values]
    
    st.success(f"✅ 數據載入成功！目前分析期數：**{total_records}** 期")
    st.info(f"📅 **最新一期日期**：{latest_date} \n\n 🎰 **開出號碼**：{', '.join(latest_nums)}")

    # AI 演算法
    all_history = df.iloc[:, 1:6].values.flatten()
    counts = Counter(all_history)
    scores = {i: counts.get(i, 0) * 10 for i in range(1, 40)}
    
    # 1. 尾數加權 (2, 8, 9 尾)
    for i in range(1, 40):
        if i % 10 in [2, 8, 9]: scores[i] += 45
    
    # 2. 拖牌邏輯 (根據 CSV 第一行最新號碼)
    current_latest = [int(x) for x in latest_nums]
    for n in current_latest:
        if n + 1 <= 39: scores[n+1] += 30
        if n - 1 >= 1: scores[n-1] += 30

    sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    cars = sorted([x[0] for x in sorted_res[:2]])
    combos = sorted([x[0] for x in sorted_res[2:7]])

    st.divider()
    st.subheader("💎 今日 AI 推薦【專車】")
    c1, c2 = st.columns(2)
    c1.metric("推薦一", f"{cars[0]:02d}")
    c2.metric("推薦二", f"{cars[1]:02d}")

    st.subheader("🔥 今日 AI 推薦【連碰】")
    st.markdown(f"### ` {' , '.join([f'{x:02d}' for x in combos])} `")

except Exception as e:
    st.error(f"⚠️ CSV 讀取失敗，請確認 GitHub 內有 history539.csv 檔案。錯誤訊息: {e}")
