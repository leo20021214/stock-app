import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup

def fetch_news(ticker, limit=5):
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("h3 a[href^='/news/']")[:limit]
    
    news = []
    for tag in articles:
        title = tag.get_text().strip()
        link = tag["href"]
        if not link.startswith("http"):
            link = "https://finance.yahoo.com" + link
        news.append((title, link))
    return news


st.title("📈 股票查詢與智能推薦系統")
code = st.text_input("輸入股票代號（如 2330.TW）")
cost = st.number_input("輸入買入成本（元）", step=1.0)
shares = st.number_input("輸入持有股數", step=1)
mode = st.radio("選擇策略", ["短期", "長期"])

if st.button("查詢") and code:
    stock = yf.Ticker(code)
    try:
        price = stock.info['regularMarketPrice']
        name = stock.info['longName']
        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        st.subheader(f"📌 {name} ({code})")
        st.write(f"💵 現價：{price} 元")
        st.write(f"📈 報酬率：{percent}%")
        st.write(f"💰 總盈虧：{profit} 元")

        if mode == "短期":
            if percent >= 5:
                suggestion = "✅ 建議賣出"
            elif percent <= -5:
                suggestion = "⚠️ 建議停損"
            else:
                suggestion = "🔄 建議觀望"
        elif mode == "長期":
            if percent >= 10:
                suggestion = "✅ 長期獲利可考慮分批賣出"
            elif percent <= -10:
                suggestion = "💡 可考慮加碼攤平"
            else:
                suggestion = "📌 建議繼續長期持有"

        st.success(f"📊 系統建議：{suggestion}")

        st.divider()
        st.subheader("📰 最新新聞：")
        news_list = fetch_news(code.replace(".TW", ""))
        for t, l in news_list:
            st.markdown(f"- [{t}]({l})")

    except Exception as e:
        st.error("查詢失敗，請檢查代號是否正確或稍後再試")
