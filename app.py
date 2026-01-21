import streamlit as st
import pandas as pd
from collections import Counter
import os

# 1. 網頁基本設定
st.set_page_config(page_title="539 AI 智能預測", page_icon="🔮", layout="centered")

# 自定義標題樣式
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔮 539 AI 數據研究中心</h1>", unsafe_allow_html=True)
st.write(f"<div style='text-align: center;'>數據對接：發財網 (pilio.idv.tw) 500期大數據</div>", unsafe_allow_html=True)
st.divider()

# 2. 核心邏輯：讀取資料並分析
def run_prediction():
    if not os.path.exists('history539.csv'):
        st.error("⚠️ 找不到 history539.csv 檔案，請確認已上傳至 GitHub 儲存庫。")
        return None

    try:
        # 讀取 CSV
        df = pd.read_csv('history539.csv', encoding='utf-8-sig')
        
        # 取得最新一期資訊用於網頁顯示驗證
        latest_date = str(df.iloc[0, 0])
        latest_nums = [str(x).zfill(2) for x in df.iloc[0, 1:6].values]
        
        # --- AI 演算法：計算 500 期規律 ---
        # 提取所有歷史號碼進行頻率統計
        all_history = df.iloc[:, 1:6].values.flatten()
        counts = Counter(all_history)
        
        scores = {i: counts.get(i, 0) * 10 for i in range(1, 40)}
        
        # 尾數加權邏輯 (根據 2, 8, 9 尾進行強化)
        for i in range(1, 40):
            if i % 10 in [2, 8, 9]: scores[i] += 45
            
        # 拖牌關聯分析 (根據最新一期)
        current_latest = [int(x) for x in latest_nums]
        for n in current_latest:
            if n + 1 <= 39: scores[n+1] += 30
            if n - 1 >= 1: scores[n-1] += 30

        # 排序選出最高分的號碼
        sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        cars = sorted([x[0] for x in sorted_res[:2]])
        combos = sorted([x[0] for x in sorted_res[2:7]])

        return {
            "date": latest_date,
            "nums": latest_nums,
            "cars": cars,
            "combos": combos
        }
    except Exception as e:
        st.error(f"❌ 數據讀取出錯: {e}")
        return None

# 3. 執行分析並渲染網頁
result = run_prediction()

if result:
    # 顯示目前校正的號碼 (讓朋友確認數據沒錯)
    st.info(f"📅 **資料庫最新日期**：{result['date']} \n\n 🎰 **開出號碼**：{', '.join(result['nums'])}")
    
    st.divider()
    
    # 顯示專車
    st.subheader("💎 今日 AI 推薦【專車】")
    c1, c2 = st.columns(2)
    c1.metric("第一支", f"{result['cars'][0]:02d}")
    c2.metric("第二支", f"{result['cars'][1]:02d}")
    
    st.divider()
    
    # 顯示連碰
    st.subheader("🔥 今日 AI 推薦【連碰】")
    combo_str = " , ".join([f"{x:02d}" for x in result['combos']])
    st.markdown(f"## {combo_str}")
    
    st.divider()
    st.caption("💡 免責聲明：本工具僅供大數據研究參考，不保證獲利，請理性對待。")
