import streamlit as st
import urllib.request
import re
import pandas as pd
from collections import Counter
from datetime import datetime

# 網頁基本設定
st.set_page_config(page_title="539 AI 智能研發中心", layout="centered")

# --- 強大的自動抓取功能 (直接從發財網抓取 500 期) ---
@st.cache_data(ttl=3600)  # 每小時自動更新
def get_pilio_data():
    all_rows = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # 抓取前 10 頁，每頁約 50 期，總計約 500 期
        for p in range(1, 11):
            url = f"https://www.pilio.idv.tw/lto539/list.asp?indexpage={p}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                html = res.read().decode('utf-8')
            
            # 使用正則表達式精準抓取表格中的日期與號碼
            # 格式：MM/DD 與 n1,n2,n3,n4,n5
            matches = re.findall(r'(\d{2}/\d{2}).*?(\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2}\s*,\s*\d{1,2})', html, re.S)
            for m in matches:
                date = m[0]
                nums = [int(n.strip()) for n in m[1].split(',')]
                all_rows.append([date] + nums)
        return all_rows
    except Exception as e:
        return f"連線失敗: {e}"

# --- 執行抓取 ---
raw_data = get_pilio_data()

st.title("🔮 539 AI 雲端大數據系統")

if isinstance(raw_data, list) and len(raw_data) > 0:
    # 建立 DataFrame
    df = pd.DataFrame(raw_data, columns=['日期', 'n1', 'n2', 'n3', 'n4', 'n5'])
    
    # 顯示狀態
    latest = df.iloc[0]
    st.success(f"✅ 數據同步成功：已自動抓取發財網最新 **{len(df)}** 期紀錄")
    st.info(f"📅 **最新開獎**：{latest['日期']} 🎰 **號碼**：{latest['n1']:02d}, {latest['n2']:02d}, {latest['n3']:02d}, {latest['n4']:02d}, {latest['n5']:02d}")

    # --- AI 核心演算法 (基於真實 500 期) ---
    all_nums = df.iloc[:, 1:6].values.flatten()
    counts = Counter(all_nums)
    scores = {i: counts.get(i, 0) * 15 for i in range(1, 40)}
    
    # 1. 尾數權重 (2, 8, 9 尾)
    for i in range(1, 40):
        if i % 10 in [2, 8, 9]: scores[i] += 50
    
    # 2. 拖牌邏輯 (根據最新一期)
    for n in [latest['n1'], latest['n2'], latest['n3'], latest['n4'], latest['n5']]:
        if n+1 <= 39: scores[n+1] += 30
        if n-1 >= 1: scores[n-1] += 30

    # 排序產出
    sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    cars = sorted([x[0] for x in sorted_res[:2]])
    combos = sorted([x[0] for x in sorted_res[2:7]])

    # --- 顯示推薦結果 ---
    st.divider()
    st.subheader("💎 今日 AI 推薦【專車】")
    st.markdown(f"## <font color='#ff4b4b'>{cars[0]:02d} , {cars[1]:02d}</font>", unsafe_allow_html=True)
    
    st.subheader("🔥 今日 AI 推薦【連碰】")
    st.markdown(f"### {', '.join([f'{x:02d}' for x in combos])}")
    
    st.divider()
    st.caption("備註：本系統直接對接發財網原始碼，數據每小時自動校對更新。")

else:
    st.error("❌ 抓取失敗。請確認發財網 (pilio.idv.tw) 是否正常開啟，或檢查 Streamlit 伺服器權限。")
