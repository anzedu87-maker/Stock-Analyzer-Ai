import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.set_page_config(page_title="Stock Analyzer AI", layout="wide")

st.title("📈 Stock Analyzer AI Indonesia")

kode = st.text_input("Masukkan Kode Saham BEI", "BBCA")

if st.button("Analisa"):
   ticker = kode.upper().strip() + ".JK"

data = yf.download(ticker, period="6mo", auto_adjust=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if data.empty:
                    st.error("Kode saham tidak ditemukan.")
else:

                                data["EMA20"] = EMAIndicator(
                                            close=data["Close"].squeeze(),
                                                        window=20
                                                                ).ema_indicator()

data["EMA50"] = EMAIndicator(
                                                                                    close=data["Close"].squeeze(),
                                                                                                window=50
                                                                                                        ).ema_indicator()

data["RSI"] = RSIIndicator(
                                                                                                                            close=data["Close"].squeeze(),
                                                                                                                                        window=14
                                                                                                                                                ).rsi()

harga = float(data["Close"].iloc[-1])
ema20 = float(data["EMA20"].iloc[-1])

ema50 = float(data["EMA50"].iloc[-1])
rsi = float(data["RSI"].iloc[-1])

support = float(data["Low"].tail(20).min())
resistance = float(data["High"].tail(20).max())

entry = harga
stop_loss = support
take_profit = resistance

st.success(f"Data {ticker} berhasil diambil.")

st.subheader("Data Terakhir")
st.write(data.tail())

fig = px.line(
                                                                                                                                                                                                                                                                    x=data.index,
                                                                                                                                                                                                                                                                                y=data["Close"].squeeze(),
                                                                                                                                                                                                                                                                                            title=f"Harga Saham {ticker}"
                                                                                                                                                                                                                                                                                                    )

st.plotly_chart(fig, use_container_width=True)
st.subheader("📊 Hasil Analisa")

col1, col2, col3 = st.columns(3)

with col1:
                                                                                                                                                                                                                                                                                                                                                st.metric("Harga", f"Rp {harga:,.0f}")
st.metric("EMA20", f"{ema20:.2f}")
st.metric("EMA50", f"{ema50:.2f}")

with col2:
                                                                                                                                                                                                                                                                                                                                                                                            st.metric("RSI", f"{rsi:.2f}")
st.metric("Support", f"Rp {support:,.0f}")
st.metric("Resistance", f"Rp {resistance:,.0f}")

with col3:
                                                                                                                                                                                                                                                                                                                                                                                                                                        st.metric("Entry", f"Rp {entry:,.0f}")
st.metric("Stop Loss", f"Rp {stop_loss:,.0f}")

                                                                                                                                                                                                                                                                                                                                                
st.metric("Take Profit", f"Rp {take_profit:,.0f}")