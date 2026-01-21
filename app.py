import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os

st.set_page_config(page_title="539 AI 智能研發系統", layout="centered")

# --- 核心爬蟲功能 ---
def get_geggg_data():
    url = "https://539.geggg.com/page2.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 針對 geggg.com 的結構精準抓取
        all_rows = []
        # 抓取表格中所有的行
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # geggg 的結構通常是：日期在第1欄，號碼在第2欄
            if len(cols) >= 2:
                raw_date = cols[0].get_text(strip=True)
                raw_nums = cols[1].get_text(strip=True)
                
                # 簡單格式化日期
                date = raw_date[:10].replace("-", "/")
                # 提取出5個數字 (例如 01 05 33 36 38)
                nums = [n for n in raw_nums.split() if n.isdigit() and len(n) == 2]
                
                if len(nums) == 5:
                    all_rows.append([date] + nums)
        
        if all_rows:
            df = pd.DataFrame(all_rows, columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5'])
            df.to_csv('history539.csv', index=False, encoding='utf-8-sig')
            return df
        return None
    except Exception as e:
        st.error(f"抓取發生錯誤: {e}")
        return None

# --- UI 介面 ---
st.markdown("<h1 style='text-align: center;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)

# 同步按鈕
if st.button("🔄 點擊同步最新開獎數據 (從 geggg.com)"):
    with st.spinner("正在抓取中..."):
        df = get_geggg_data()
        if df is not None:
            st.success("✅ 數據更新成功！")
            st.rerun() # 重新整理頁面以顯示新數據
        else:
            st.error("❌ 無法取得數據，請確認網站是否正常。")

st.divider()

# --- 讀取與邏輯分析 (加入空檔案保護) ---
if os.path.exists('history539.csv'):
    try:
        df_display = pd.read_csv('history539.csv')
        if not df_display.empty:
            st.write(f"📊 目前分析期數：{len(df_display)} 期")
            latest = df_display.iloc[0]
            st.info(f"📅 最新開獎：{latest['date']} \n\n 🎰 獎號：{latest['n1']:02}, {latest['n2']:02}, {latest['n3']:02}, {latest['n4']:02}, {latest['n5']:02}")
            
            # AI 推薦邏輯
            all_nums = df_display.iloc[:, 1:6].values.flatten().astype(int)
            counts = Counter(all_nums)
            # 取得最常出現的號碼作為示範
            recommend = [n for n, c in counts.most_common(7)]
            
            st.subheader("💎 今日 AI 推薦【專車】")
            st.markdown(f"### <font color='#ff4b4b'>{recommend[0]:02d} , {recommend[1]:02d}</font>", unsafe_allow_html=True)
            
            st.subheader("🔥 今日 AI 推薦【連碰】")
            st.markdown(f"### {' , '.join([f'{x:02d}' for x in recommend[2:7]])}")
        else:
            st.warning("⚠️ 檔案內容為空，請點擊上方按鈕同步數據。")
    except:
        st.warning("⚠️ 檔案讀取失敗，請重新點擊同步按鈕。")
else:
    st.warning("👋 歡迎！請先點擊上方按鈕同步『樂透預言家』的歷史數據。")
