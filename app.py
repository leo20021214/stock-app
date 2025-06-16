import streamlit as st
import yfinance as yf

# 介面設定
st.set_page_config(page_title="股票查詢與智能建議", layout="centered")
st.title("📈 股票查詢與智能建議系統")

# 使用者輸入
code = st.text_input("輸入股票代號（如 2330.TW）", value="2330.TW")
cost = st.number_input("輸入買入成本（元）", step=1.0)
shares = st.number_input("輸入持有股數", step=1, min_value=1)
mode = st.radio("選擇策略", ["短期", "長期"])
query = st.button("🔍 查詢")

# 當使用者點擊查詢按鈕
if query and code:
    stock = yf.Ticker(code)
    try:
        # 擷取資訊
        price = stock.info['regularMarketPrice']
        name = stock.info.get('longName', code)
        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        # 顯示資料
        st.subheader(f"📌 {name} ({code})")
        st.write(f"💵 現價：{price} 元")
        st.write(f"📉 報酬率：{percent}%")
        st.write(f"💰 總盈虧：{profit} 元")

        # 系統建議邏輯
        suggestion = ""
        if mode == "短期":
            if percent >= 5:
                suggestion = "✅ 建議賣出"
            elif percent <= -5:
                suggestion = "⚠️ 建議停損"
            else:
                suggestion = "🔄 建議持有觀望"
        else:  # 長期
            if percent >= 10:
                suggestion = "✅ 長期獲利可考慮分批賣出"
            elif percent <= -10:
                suggestion = "💡 可考慮加碼攤平"
            else:
                suggestion = "📌 建議繼續長期持有"

        st.success(f"📊 系統建議：{suggestion}")

        # 顯示 Google 財經新聞搜尋結果畫面
        st.divider()
        st.subheader("📰 最新新聞：")
        google_news_url = f"https://www.google.com/search?q={name}+site:news.google.com&tbm=nws"
        st.markdown(f"[📌 點我前往 Google 新聞查看 >>]({google_news_url})")
        st.components.v1.iframe(google_news_url, height=600, scrolling=True)

    except Exception as e:
        st.error("❌ 查詢失敗，請確認代號是否正確或稍後再試")

