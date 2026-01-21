import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os

st.set_page_config(page_title="539 AI 智能研發系統", layout="centered")

def get_geggg_data():
    url = "https://539.geggg.com/page2.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_rows = []
    try:
        # 嘗試抓取前 20 頁 (約 600 期)
        for p in range(1, 21):
            p_url = f"{url}?page={p}"
            res = requests.get(p_url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = soup.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    date_text = cols[0].get_text(strip=True)
                    nums_text = cols[1].get_text(strip=True)
                    # 只要日期格式對 (YYYY-MM-DD)，就抓取
                    if len(date_text) >= 10 and "-" in date_text:
                        date = date_text[:10].replace("-", "/")
                        nums = [n for n in nums_text.split() if n.isdigit() and len(n) == 2]
                        if len(nums) == 5:
                            all_rows.append([date] + nums)
        
        if all_rows:
            df = pd.DataFrame(all_rows, columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5'])
            # 刪除重複項並存檔
            df.drop_duplicates(subset=['date'], keep='first', inplace=True)
            df.to_csv('history539.csv', index=False, encoding='utf-8-sig')
            return df
        return None
    except:
        return None

st.markdown("<h1 style='text-align: center;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)

if st.button("🔄 啟動深度數據同步 (抓取 600 期)"):
    with st.spinner("正在逐頁掃描『樂透預言家』數據，請稍候..."):
        df = get_geggg_data()
        if df is not None:
            st.success(f"✅ 同步完成！已儲存 {len(df)} 期精準數據。")
            st.rerun()
        else:
            st.error("同步中斷，但可能已保留部分數據。")

st.divider()

if os.path.exists('history539.csv'):
    df_display = pd.read_csv('history539.csv')
    if not df_display.empty:
        st.write(f"📊 目前分析期數：**{len(df_display)}** 期")
        latest = df_display.iloc[0]
        st.info(f"📅 最新開獎：{latest['date']} \n\n 🎰 獎號：{latest['n1']:02d}, {latest['n2']:02d}, {latest['n3']:02d}, {latest['n4']:02d}, {latest['n5']:02d}")
        
        # --- 權重演算法 ---
        all_nums = df_display.iloc[:, 1:6].values.flatten().astype(int)
        counts = Counter(all_nums)
        scores = {i: counts.get(i, 0) * 10 for i in range(1, 40)}
        
        # 增加尾數 2, 8, 9 權重
        for i in range(1, 40):
            if i % 10 in [2, 8, 9]: scores[i] += 50
            
        sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommend = [x[0] for x in sorted_res]

        st.subheader("💎 今日 AI 推薦【專車】")
        st.markdown(f"## <font color='#ff4b4b'>{recommend[0]:02d} , {recommend[1]:02d}</font>", unsafe_allow_html=True)
        
        st.subheader("🔥 今日 AI 推薦【連碰】")
        st.markdown(f"### {' , '.join([f'{x:02d}' for x in recommend[2:7]])}")
    else:
        st.warning("請點擊上方按鈕同步數據。")
else:
    st.warning("請點擊上方按鈕同步數據。")
