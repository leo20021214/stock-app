import streamlit as st
import yfinance as yf

st.set_page_config(page_title="股票查詢與智能推薦系統", layout="wide")

st.title("📈 股票查詢與智能推薦系統")

# 使用者輸入
code = st.text_input("輸入股票代號（如 2330.TW）", value="2330.TW")
cost = st.number_input("輸入買入成本（元）", min_value=0.0, step=1.0)
shares = st.number_input("輸入持有股數", min_value=1, step=1)
mode = st.radio("選擇策略", ["短期", "長期"])
clicked = st.button("查詢")

if clicked and code:
    stock = yf.Ticker(code)
    try:
        price = stock.info['regularMarketPrice']
        name = stock.info.get('longName', code)
        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        st.markdown(f"### 📌 {name} ({code})")
        st.write(f"💵 現價：{price} 元")
        st.write(f"📉 報酬率：{percent}%")
        st.write(f"💰 總盈虧：{profit} 元")

        # 推薦策略
        suggestion = ""
        if mode == "短期":
            if percent >= 5:
                suggestion = "✅ 建議賣出"
            elif percent <= -5:
                suggestion = "⚠️ 建議停損"
            else:
                suggestion = "🔄 建議持有觀望"
        elif mode == "長期":
            if percent >= 10:
                suggestion = "✅ 長期獲利可考慮分批賣出"
            elif percent <= -10:
                suggestion = "💡 可考慮加碼攤平"
            else:
                suggestion = "📌 建議繼續長期持有"

        st.success(f"📊 系統建議：{suggestion}")

        st.divider()

        # 🔍 顯示 Google 新聞連結
        st.subheader("📰 最新新聞：")
        query_name = name.split()[0] if " " in name else name
        search_url = f"https://www.google.com/search?q={query_name}+site:news.google.com&tbm=nws"
        st.markdown(f"🔗 [點我查看 Google 財經新聞 →]({search_url})")

    except Exception as e:
        st.error("❌ 查詢失敗")
