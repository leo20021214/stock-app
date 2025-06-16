import streamlit as st
import yfinance as yf

st.set_page_config(page_title="股票查詢與智能推薦", layout="wide")
st.title("📈 股票查詢與智能推薦系統")

# 使用者輸入區
code = st.text_input("輸入股票代號（如 2330.TW、2303.TW、2350.HK）")
cost = st.number_input("輸入買入成本（元）", min_value=0.0, step=1.0)
shares = st.number_input("輸入持有股數", min_value=1, step=1)
mode = st.radio("選擇操作策略", ["短期", "長期"])
submitted = st.button("🔍 查詢")

if submitted and code:
    stock = yf.Ticker(code)

    try:
        price = stock.info["regularMarketPrice"]
        name = stock.info.get("longName", code)
        market_cap = stock.info.get("marketCap", 0)
        volume = stock.info.get("volume", 0)

        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        st.markdown("---")
        st.subheader(f"📌 {name} ({code})")
        st.write(f"💵 現價：{price} 元")
        st.write(f"📉 報酬率：{percent}%")
        st.write(f"💰 總盈虧：{profit} 元")

        # 投資建議邏輯
        suggestion = ""
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
                suggestion = "📌 建議繼續持有"

        st.success(f"📊 系統建議： {suggestion}")

        # Google 新聞搜尋連結（使用公司名稱）
        company_name = name.split()[0] if " " in name else name
        search_url = f"https://www.google.com/search?q={company_name}+股票+新聞&tbm=nws"

        st.markdown("---")
        st.subheader("📰 最新新聞：")
        st.markdown(f"🔗 [點我查看「{company_name}」的 Google 財經新聞]({search_url})")

    except Exception as e:
        st.error("❌ 查詢失敗")
