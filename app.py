import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="股票查詢與智能推薦", layout="centered")
st.title("📈 股票查詢與智能推薦系統")

# 熱門股快速選擇
st.subheader("📌 熱門台股快速選擇")
popular_stocks = {
    "台積電 (2330.TW)": "2330.TW",
    "聯發科 (2454.TW)": "2454.TW",
    "鴻海 (2317.TW)": "2317.TW",
    "長榮 (2603.TW)": "2603.TW",
    "陽明 (2609.TW)": "2609.TW",
    "中鋼 (2002.TW)": "2002.TW",
    "大立光 (3008.TW)": "3008.TW",
    "自行輸入": ""
}
selected_label = st.selectbox("選擇熱門股票（或選擇『自行輸入』）", list(popular_stocks.keys()))
code = popular_stocks[selected_label]

if selected_label == "自行輸入":
    code = st.text_input("輸入股票代號（如 2330.TW）")

cost = st.number_input("輸入買入成本（元）", step=1.0)
shares = st.number_input("輸入持有股數", step=1)
mode = st.radio("選擇策略", ["短期", "長期"])

def plot_stock_history(ticker_code):
    stock = yf.Ticker(ticker_code)
    hist = stock.history(period="1mo")
    if not hist.empty:
        plt.figure(figsize=(8, 3))
        plt.plot(hist.index, hist['Close'], marker='o')
        plt.title("近一個月收盤價走勢")
        plt.xlabel("日期")
        plt.ylabel("收盤價")
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.warning("⚠️ 找不到歷史股價資料")

if st.button("查詢"):
    if not code:
        st.warning("⚠️ 請輸入股票代號")
    elif cost == 0.0:
        st.warning("⚠️ 請輸入買入成本價格（不可為 0）")
    elif shares == 0:
        st.warning("⚠️ 請輸入持有股數（不可為 0）")
    else:
        try:
            stock = yf.Ticker(code)
            info = stock.info
            name = info.get("longName", "未知公司")
            price = info.get("regularMarketPrice", None)

            if price is None:
                st.error("❌ 查詢失敗，請檢查代號是否正確。")
            else:
                percent = round((price - cost) / cost * 100, 2)
                profit = round((price - cost) * shares, 2)

                st.subheader(f"📌 {name} ({code})")
                st.write(f"💵 現價：{price} 元")
                st.write(f"📈 報酬率：{percent}%")
                st.write(f"💰 總盈虧金額：{profit} 元")

                if mode == "短期":
                    if percent >= 5:
                        suggestion = "✅ 建議賣出"
                    elif percent <= -5:
                        suggestion = "⚠️ 建議停損"
                    else:
                        suggestion = "🔄 建議觀望"
                else:
                    if percent >= 10:
                        suggestion = "✅ 長期獲利可考慮分批賣出"
                    elif percent <= -10:
                        suggestion = "💡 可考慮加碼攤平"
                    else:
                        suggestion = "📌 建議繼續長期持有"

                st.success(f"📊 系統建議：{suggestion}")

                # Google 財經新聞搜尋
                company_name = name.split()[0] if " " in name else name
                search_url = f"https://www.google.com/search?q={company_name}+股票+新聞&tbm=nws"
                st.markdown("---")
                st.subheader("📰 最新新聞")
                st.markdown(f"🔗 [點我查看「{company_name}」的 Google 財經新聞]({search_url})")

                # 股價走勢圖
                st.markdown("---")
                st.subheader("📉 近一個月股價走勢圖")
                plot_stock_history(code)

        except Exception as e:
            st.error(f"⚠️ 發生錯誤：{e}")
