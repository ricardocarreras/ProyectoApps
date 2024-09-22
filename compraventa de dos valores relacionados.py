import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Función para obtener datos de Yahoo Finance
def get_data(ticker1, ticker2):
    start_date = st.date_input('Start Date', value=pd.to_datetime('2022-01-01'))
    end_date = st.date_input('End Date', value=pd.to_datetime('today'))
    
    data1 = yf.download(ticker1, start=start_date, end=end_date)
    data2 = yf.download(ticker2, start=start_date, end=end_date)
    
    return data1['Close'], data2['Close']

# Función para calcular el Z-score del spread
def calculate_zscore(spread, window=30):
    mean_spread = spread.rolling(window=window).mean()
    std_spread = spread.rolling(window=window).std()
    zscore = (spread - mean_spread) / std_spread
    return zscore

# Función para generar las señales de compra
def pair_trading_with_zscore(stock1, stock2):
    spread = stock1 - stock2
    zscore = calculate_zscore(spread)

    buy_stock1_signals = zscore < -1  # Comprar cuando el Z-score es menor a -1
    buy_stock2_signals = zscore > 1   # Comprar cuando el Z-score es mayor a 1

    return buy_stock1_signals, buy_stock2_signals, zscore

# Interfaz de usuario de Streamlit
st.title("Pair Trading Bot")

ticker1 = st.text_input('Enter first stock ticker', 'TSLA')
ticker2 = st.text_input('Enter second stock ticker', 'RIVN')

if st.button('Run Pair Trading Analysis'):
    stock1, stock2 = get_data(ticker1, ticker2)
    
    buy_stock1_signals, buy_stock2_signals, zscore = pair_trading_with_zscore(stock1, stock2)
    
    # Mostrar gráfico
    st.subheader(f"Z-score between {ticker1} and {ticker2}")
    plt.figure(figsize=(10, 6))
    plt.plot(zscore, label=f'Z-score {ticker1}-{ticker2}')
    plt.plot(zscore[buy_stock1_signals], '^', markersize=10, color='g', lw=0, label=f'Buy {ticker1}')
    plt.plot(zscore[buy_stock2_signals], 'v', markersize=10, color='b', lw=0, label=f'Buy {ticker2}')
    plt.axhline(1, color='gray', linestyle='--', label='Upper Threshold (1)')
    plt.axhline(-1, color='gray', linestyle='--', label='Lower Threshold (-1)')
    plt.axhline(0, color='black', linestyle='-', label='Mean (0)')
    plt.legend(loc='best')
    plt.title(f'Pair Trading {ticker1} vs {ticker2} (Z-score)')
    st.pyplot(plt)
    
    # Simulación de compra
    cash = 100000  # Monto inicial en USD
    stock1_shares = 0
    stock2_shares = 0
    for i in range(len(zscore)):
        if buy_stock1_signals[i] and cash > 0:  # Comprar primera acción
            stock1_shares += cash / stock1[i]
            cash = 0
        elif buy_stock2_signals[i] and cash > 0:  # Comprar segunda acción
            stock2_shares += cash / stock2[i]
            cash = 0
    
    st.write(f"Final result: ${cash:.2f} in cash, {stock1_shares:.2f} shares of {ticker1}, and {stock2_shares:.2f} shares of {ticker2}")
