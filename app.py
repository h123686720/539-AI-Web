import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os

st.set_page_config(page_title="539 AI 智能系統", layout="centered")

# --- 強化版爬蟲功能 ---
def get_data_from_web(pages=5):
    url = "https://539.geggg.com/page2.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    rows_list = []
    try:
        for p in range(1, pages + 1):
            p_url = f"{url}?page={p}"
            res = requests.get(p_url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    dt = cols[0].get_text(strip=True)[:10].replace("-", "/")
                    nums = [n for n in cols[1].get_text(strip=True).split() if n.isdigit() and len(n)==2]
                    if len(nums) == 5:
                        rows_list.append([dt] + nums)
        return rows_list
    except:
        return None

st.markdown("<h1 style='text-align: center;'>🔮 539 AI 智能研發系統</h1>", unsafe_allow_html=True)

# --- 功能區塊：同步與手動補號 ---
with st.expander("🛠️ 數據管理工具 (網站沒更新時點此)"):
    c1, c2 = st.columns(2)
    if c1.button("🔄 同步最新數據"):
        with st.spinner("同步中..."):
            new_rows = get_data_from_web(5)
            if new_rows:
                new_df = pd.DataFrame(new_rows, columns=['date','n1','n2','n3','n4','n5'])
                if os.path.exists('history539.csv'):
                    old_df = pd.read_csv('history539.csv')
                    new_df = pd.concat([new_df, old_df]).drop_duplicates(subset=['date'])
                new_df.to_csv('history539.csv', index=False, encoding='utf-8-sig')
                st.success("同步完成！")
                st.rerun()

    st.write("---")
    st.write("📝 手動新增昨天號碼 (如網站尚未更新)")
    in_date = st.text_input("日期", value="2026/01/21")
    in_nums = st.text_input("號碼 (空格隔開)", placeholder="例如: 05 12 18 24 37")
    if st.button("➕ 確認手動新增"):
        nums_list = in_nums.split()
        if len(nums_list) == 5:
            new_entry = pd.DataFrame([[in_date] + nums_list], columns=['date','n1','n2','n3','n4','n5'])
            if os.path.exists('history539.csv'):
                old_df = pd.read_csv('history539.csv')
                final_df = pd.concat([new_entry, old_df]).drop_duplicates(subset=['date'])
            else:
                final_df = new_entry
            final_df.to_csv('history539.csv', index=False, encoding='utf-8-sig')
            st.success("手動補號成功！")
            st.rerun()
        else:
            st.error("請輸入正確的5個號碼")

st.divider()

# --- 顯示與分析 ---
if os.path.exists('history539.csv'):
    df = pd.read_csv('history539.csv').sort_values(by='date', ascending=False)
    st.write(f"📊 目前分析期數：**{len(df)}** 期")
    l = df.iloc[0]
    st.info(f"📅 最新獎號 ({l['date']})：{l['n1']:02d}, {l['n2']:02d}, {l['n3']:02d}, {l['n4']:02d}, {l['n5']:02d}")
    
    # 權重分析邏輯
    all_n = df.iloc[:, 1:6].values.flatten().astype(int)
    counts = Counter(all_n)
    scores = {i: counts.get(i,0)*5 for i in range(1,40)}
    # 增加您偏好的尾數加權
    for i in range(1,40):
        if i % 10 in [2, 8, 9]: scores[i] += 15
    
    rec = [x[0] for x in sorted(scores.items(), key=lambda x:x[1], reverse=True)]
    
    st.subheader("💎 今日 AI 推薦【專車】")
    st.markdown(f"## <font color='#ff4b4b'>{rec[0]:02d} , {rec[1]:02d}</font>", unsafe_allow_html=True)
    st.subheader("🔥 今日 AI 推薦【連碰】")
    st.markdown(f"### {' , '.join([f'{x:02d}' for x in rec[2:7]])}")
else:
    st.warning("請先使用上方工具同步數據。")
