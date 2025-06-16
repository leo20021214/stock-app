import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="股票查詢與智能推薦系統", layout="centered")
st.title("📈 股票查詢與智能推薦系統")

# --- 熱門股清單 ---
hot_stocks = {
    "台積電 (2330.TW)": "2330.TW",
    "聯發科 (2454.TW)": "2454.TW",
    "鴻海 (2317.TW)": "2317.TW",
    "台塑 (1301.TW)": "1301.TW",
    "中鋼 (2002.TW)": "2002.TW"
}
selected = st.selectbox("快速選擇熱門股", ["請選擇"] + list(hot_stocks.keys()))
default_code = hot_stocks[selected] if selected != "請選擇" else ""

# --- 使用者輸入 ---
symbol = st.text_input("輸入股票代號 (例如 2330.TW)", value=default_code)
cost = st.number_input("輸入買入成本（元）", min_value=0.0, step=1.0)
shares = st.number_input("輸入持有股數", min_value=1, step=1, value=1)
mode = st.radio("選擇操作策略", ["短期", "長期"])

# --- 查詢按鈕 ---
if st.button("查詢"):
    if cost == 0.0:
        st.warning("❗請輸入有效的買入成本價格")
    else:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            name = info.get("longName", "未知公司")
            price = info.get("regularMarketPrice", 0.0)

            # 基本資訊
            profit = round((price - cost) * shares, 2)
            percent = round((price - cost) / cost * 100, 2)

            st.markdown("---")
            st.subheader(f"📌 {name} ({symbol})")
            st.write(f"💹 現價：{price} 元")
            st.write(f"📈 報酬率：{percent}%")
            st.write(f"💰 總盈虧：{profit} 元")

            # 智能建議
            if mode == "短期":
                if percent >= 5:
                    suggestion = "✅ 建議賣出"
                elif percent <= -5:
                    suggestion = "⚠️ 建議停損"
                else:
                    suggestion = "👀 建議持有觀望"
            else:
                if percent < -3:
                    suggestion = "📉 可考慮加碼攤平"
                elif abs(percent) <= 3:
                    suggestion = "⏳ 建議長期持有"
                else:
                    suggestion = "✅ 長期獲利可考慮分批賣出"
            st.success(f"🧠 系統建議：{suggestion}")

            # 走勢圖
            st.markdown("---")
            st.subheader("📊 歷史股價走勢")
            today = datetime.datetime.today()
            past = today - datetime.timedelta(days=180)
            hist = stock.history(start=past, end=today)
            fig, ax = plt.subplots()
            ax.plot(hist.index, hist["Close"])
            ax.set_title(f"{name} 收盤價走勢")
            ax.set_xlabel("日期")
            ax.set_ylabel("收盤價")
            st.pyplot(fig)

            # 新聞連結
            st.markdown("---")
            st.subheader("📰 最新新聞：")
            if symbol in hot_stocks.values():
                st.markdown(f"🔗 [Yahoo 財經新聞 - {symbol}](https://tw.stock.yahoo.com/q/h?s={symbol})")
            else:
                st.markdown("🔗 [前往 Google 財經新聞首頁](https://news.google.com/topics/CAAqBwgKMN2Flwsw6qvYAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant)")

        except Exception as e:
            st.error(f"查詢失敗：{e}")
