import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os

# 網頁設定
st.set_page_config(page_title="539 AI 自動更新系統", layout="centered")

# --- 爬蟲功能：從您提供的網頁抓取數據 ---
def update_data():
    url = "https://539.geggg.com/page2.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找數據表格 (假設是網頁中的 table 結構)
        rows = soup.find_all('tr')
        new_data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)[:10] # 抓取日期 YYYY-MM-DD
                nums_text = cols[1].get_text(strip=True)
                # 提取號碼 (排除期號)
                nums = [n for n in nums_text.split() if len(n) == 2 and n.isdigit()]
                if len(nums) == 5:
                    new_data.append([date_str.replace("-", "/")] + nums)
        
        df = pd.DataFrame(new_data, columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5'])
        df.to_csv('history539.csv', index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        return False

# --- UI 介面 ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)

if st.button("🔄 點擊同步最新開獎數據"):
    with st.spinner("正在連線至 geggg.com 抓取最新號碼..."):
        if update_data():
            st.success("數據更新成功！")
        else:
            st.error("同步失敗，請確認網路連線。")

# --- 讀取與分析 ---
if os.path.exists('history539.csv'):
    df = pd.read_csv('history539.csv')
    st.write(f"📊 目前分析期數：{len(df)} 期")
    st.write("📅 最新開獎日期：", df.iloc[0]['date'])
    st.write("🎰 最新獎號：", ", ".join(df.iloc[0, 1:6].astype(str)))

    # AI 演算法 (簡化版)
    all_nums = df.iloc[:, 1:6].values.flatten().astype(int)
    counts = Counter(all_nums)
    # 這裡可以加入您更複雜的邏輯...
    top_nums = [f"{n:02d}" for n, count in counts.most_common(7)]
    
    st.divider()
    st.subheader("💎 今日 AI 推薦【專車】")
    st.info(f"建議：{top_nums[0]} , {top_nums[1]}")
    
    st.subheader("🔥 今日 AI 推薦【連碰】")
    st.warning(f"號碼：{' , '.join(top_nums[2:])}")
else:
    st.warning("尚未偵測到 history539.csv，請點擊上方按鈕同步。")
