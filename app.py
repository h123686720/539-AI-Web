import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="539 AI 智能研發系統", page_icon="🔮", layout="centered")

st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)
st.divider()

# 讀取資料檔案
try:
    df = pd.read_csv('history539.csv', encoding='utf-8-sig')
    
    # 取得最新一期資訊
    latest_date = df.iloc[0, 0]
    latest_nums = [str(x).zfill(2) for x in df.iloc[0, 1:6].values]
    
    st.info(f"📅 **官方最新開獎日期**：{latest_date} \n\n 🎰 **最新開獎號碼**：{', '.join(latest_nums)}")

    # AI 演算邏輯 (基於 CSV 內的歷史紀錄)
    all_history = df.iloc[:, 1:6].values.flatten()
    counts = Counter(all_history)
    scores = {i: counts.get(i, 0) * 10 for i in range(1, 40)}
    for i in range(1, 40):
        if i % 10 in [2, 8, 9]: scores[i] += 45
    
    latest_int_nums = [int(x) for x in latest_nums]
    for n in latest_int_nums:
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
    st.error("⚠️ 讀取 history539.csv 失敗，請確認檔案已正確上傳至 GitHub。")
