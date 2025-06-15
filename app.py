import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="📈 股票查詢與推薦系統", layout="centered")

# ✅ 使用公司名稱查新聞（避免用 ticker 找不到新聞）
def fetch_news(company_name, limit=5):
    search_url = f"https://news.google.com/search?q={company_name}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article h3 a")[:limit]

    news = []
    for a in articles:
        title = a.text.strip()
        link = a["href"]
        if not link.startswith("http"):
            link = "https://news.google.com" + link[1:]
        news.append((title, link))
    return news

# 🖥️ UI 介面開始
st.title("📈 股票查詢與智能推薦系統")

code = st.text_input("輸入股票代號（如 2330.TW, AAPL, 2350.HK）")
cost = st.number_input("輸入買入成本（元）", step=1.0, format="%.2f")
shares = st.number_input("輸入持有股數", step=1, min_value=1)
mode = st.radio("選擇操作策略", ["🔴 短期", "⚪ 長期"])
clicked = st.button("查詢")

if clicked and code:
    stock = yf.Ticker(code)
    try:
        price = stock.info['regularMarketPrice']
        name = stock.info.get('longName', code)
        percent = round((price - cost) / cost * 100, 2)
        profit = round((price - cost) * shares, 2)

        st.markdown("----")
        st.subheader(f"📌 {name} ({code})")
        st.write(f"💵 **現價**：{price} 元")
        st.write(f"📈 **報酬率**：{percent}%")
        st.write(f"💰 **總盈虧**：{profit} 元")

        # 🧠 系統建議
        suggestion = ""
        if mode == "🔴 短期":
            if percent >= 5:
                suggestion = "✅ 建議賣出（已達獲利目標）"
            elif percent <= -5:
                suggestion = "⚠️ 建議停損"
            else:
                suggestion = "🔄 建議持有觀望"
        elif mode == "⚪ 長期":
            if percent >= 10:
                suggestion = "✅ 長期獲利可考慮分批賣出"
            elif percent <= -10:
                suggestion = "💡 可考慮加碼攤平"
            else:
                suggestion = "📌 建議繼續長期持有"

        st.success(f"📊 系統建議：{suggestion}")

        # 📰 顯示最新新聞
        st.markdown("----")
        st.subheader("📰 最新新聞：")
        try:
            news_list = fetch_news(name)  # ← 用公司名稱搜尋
            if news_list:
                for title, link in news_list:
                    st.markdown(f"- [{title}]({link})")
            else:
                st.warning("目前查無新聞資料")
        except:
            st.error("❌ 查詢失敗，請檢查代號是否正確或稍後再試")

    except Exception as e:
        st.error("❌ 查詢失敗，請檢查股票代號是否正確或稍後再試")

    except Exception as e:
        st.error("❌ 查詢失敗，請檢查股票代號是否正確或稍後再試")





https://news.google.com/search?q=台積電&hl=zh-TW&gl=TW&ceid=TW:zh-Hant

