import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# 標題
st.title("📈 股票查詢與智能建議系統")

# 輸入區塊
symbol = st.text_input("請輸入台股股票代號（例如：2330）")
strategy = st.radio("操作策略", ("短期", "長期"))
cost = st.number_input("買入成本價", min_value=0.0)
shares = st.number_input("持有股數", min_value=1, step=1)
target = st.number_input("目標賣出價", min_value=0.0)

if st.button("開始查詢"):
    try:
        stock = yf.Ticker(f"{symbol}.TW")
        info = stock.info
        price = info['regularMarketPrice']
        change = info['regularMarketChange']
        change_percent = info['regularMarketChangePercent']
        market_cap = info.get("marketCap", 0)

        # 報酬率與盈虧
        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        # 顯示基本資訊
        st.subheader("📊 查詢結果")
        st.write(f"現價：{price} 元")
        st.write(f"漲跌：{change} 元（{round(change_percent, 2)}%）")
        st.write(f"報酬率：{percent}%")
        st.write(f"總盈虧金額：{profit} 元")

        # 系統建議邏輯
        suggestion = ""
        if strategy == "短期":
            if percent >= 5:
                suggestion = "✅ 建議賣出"
            elif percent <= -5:
                suggestion = "⚠️ 建議停損"
            else:
                suggestion = "🔄 建議觀望"
        else:
            if percent < -3:
                suggestion = "📉 可考慮加碼攤平"
            elif percent > 3:
                suggestion = "📈 可分批獲利了結"
            else:
                suggestion = "🔒 建議長期持有"

        st.success(f"系統建議：{suggestion}")

        # 目標價提醒
        if price >= target:
            st.info("🎯 目前已達目標價，建議可考慮賣出！")

        # 市值 + 跌幅風險提示
        if market_cap < 100_000_000_000 and change_percent < -3:
            st.warning("⚠️ 小型股跌幅大，波動較高，請留意風險。")

        # 畫股價圖表
        hist = stock.history(period="7d")
        st.subheader("📈 近七日收盤價走勢圖")
        fig, ax = plt.subplots()
        hist['Close'].plot(ax=ax)
        ax.set_title(f"{symbol} 收盤價走勢")
        ax.set_xlabel("日期")
        ax.set_ylabel("收盤價")
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error("❌ 查詢失敗，請確認代號是否正確或稍後再試。")
