import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Page Title
st.title("📈 Real-Time Stock Market Dashboard")

# Auto Refresh Every 60 Seconds
st_autorefresh(
    interval=60000,
    key="refresh"
)

# Stock Comparison Section
st.subheader("📊 Compare Stocks")

stocks = st.multiselect(
    "Select Stocks",
    ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "AMZN"],
    default=["AAPL"]
)

comparison = pd.DataFrame()

for stock_symbol in stocks:
    temp = yf.download(
        stock_symbol,
        period="1mo"
    )

    comparison[stock_symbol] = temp["Close"]

if not comparison.empty:
    st.line_chart(comparison)

# Single Stock Analysis
st.subheader("📈 Stock Analysis")

ticker = st.text_input(
    "Enter Stock Symbol",
    "AAPL"
)

stock = yf.Ticker(ticker)

# Stock Information
try:
    info = stock.info

    current_price = info.get("currentPrice")
    market_cap = info.get("marketCap")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Price",
            current_price
        )

    with col2:
        st.metric(
            "Market Cap",
            f"{market_cap:,}" if market_cap else "N/A"
        )

except:
    st.warning("Unable to fetch stock information.")

# Time Period Selection
period = st.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"]
)

# Historical Data
data = stock.history(period=period)

if not data.empty:

    # Moving Average
    data["MA20"] = data["Close"].rolling(20).mean()

    # Display Data
    st.subheader("📋 Stock Data")
    st.write(data.tail())

    # Price Chart
    fig = px.line(
        data,
        x=data.index,
        y=["Close", "MA20"],
        title=f"{ticker} Closing Price vs Moving Average"
    )

    st.plotly_chart(fig)

    # Volume Chart
    fig2 = px.bar(
        data,
        x=data.index,
        y="Volume",
        title=f"{ticker} Trading Volume"
    )

    st.plotly_chart(fig2)

else:
    st.error("No data available for this stock symbol.")