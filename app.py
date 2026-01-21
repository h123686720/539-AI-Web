import streamlit as st
import urllib.request
import re
import pandas as pd
from collections import Counter
from datetime import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="539 AI 自動更新中心", page_icon="🔮", layout="centered")

# --- 自動抓取數據函數 (爬取發財網) ---
@st.cache_data(ttl=3600)  # 每小時自動更新一次
def fetch_lto_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_rows = []
    try:
        # 抓取前 3 頁數據以供分析
        for p in range(1, 4):
            url = f"https://www.pilio.idv.tw/lto539/list.asp?indexpage={p}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                html = res.read().decode('utf-8')
            
            # 正則表達式匹配日期與號碼
            matches = re.findall(r'(\d{2}/\d{2}).*?(\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2})', html, re.S)
            for m in matches:
                date = f"2026/{m[0]}"
                nums = [int(n.strip()) for n in m[1].split(',')]
                all_rows.append([date] + nums)
        return all_rows
    except Exception as e:
        return None

# --- 網頁介面設計 ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center;'>數據狀態：🟢 自動同步發財網最新開獎</div>", unsafe_allow_html=True)
st.divider()

data = fetch_lto_data()

if data:
    # 顯示最新一期資訊
    latest = data[0]
    st.info(f"📅 **官方最新開獎日期**：{latest[0]} \n\n 🎰 **最新開獎號碼**：{', '.join([f'{x:02d}' for x in latest[1:]])}")

    # --- AI 核心演算法 ---
    df = pd.DataFrame(data, columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5'])
    all_history = df.iloc[:, 1:6].values.flatten()
    counts = Counter(all_history)
    
    # 計算積分
    scores = {i: counts.get(i, 0) * 12 for i in range(1, 40)}
    
    # 推薦尾數權重 (2, 8, 9 尾)
    for i in range(1, 40):
        if i % 10 in [2, 8, 9]: scores[i] += 50
    
    # 關聯推算 (依據最新一期)
    for n in latest[1:]:
        if n+1 <= 39: scores[n+1] += 35
        if n-1 >= 1: scores[n-1] += 35

    # 產出推薦號碼
    sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    cars = sorted([x[0] for x in sorted_res[:2]])
    combos = sorted([x[0] for x in sorted_res[2:7]])

    # 顯示結果
    st.divider()
    st.subheader("💎 今日 AI 推薦【專車】")
    col1, col2 = st.columns(2)
    col1.metric("推薦一", f"{cars[0]:02d}")
    col2.metric("推薦二", f"{cars[1]:02d}")

    st.divider()
    st.subheader("🔥 今日 AI 推薦【連碰】")
    st.markdown(f"### ` {' , '.join([f'{x:02d}' for x in combos])} `")

    st.divider()
    st.caption(f"系統自動更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("本系統基於歷史大數據規律分析，僅供參考。")

else:
    st.error("❌ 目前無法連線至發財網抓取數據。請檢查雲端伺服器網路狀態。")
