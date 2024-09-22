
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Función para obtener datos de Yahoo Finance
def get_data(ticker1, ticker2, start, end):
    data1 = yf.download(ticker1, start=start, end=end)
    data2 = yf.download(ticker2, start=start, end=end)
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
st.title("Pair Trading Bot - Last 6 Months")

ticker1 = st.text_input('Enter first stock ticker', 'TSLA')
ticker2 = st.text_input('Enter second stock ticker', 'RIVN')

if st.button('Run Pair Trading Analysis'):

    # Obtener fechas de los últimos 6 meses
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(months=6)

    # Obtener datos de los últimos 6 meses
    stock1, stock2 = get_data(ticker1, ticker2, start_date, end_date)

    # Asegurarnos de que no haya valores NaN en los datos
    stock1 = stock1.dropna()
    stock2 = stock2.dropna()

    # Alinear las series por fecha para evitar errores
    stock1, stock2 = stock1.align(stock2, join='inner')

    # Generar señales de compra
    buy_stock1_signals, buy_stock2_signals, zscore = pair_trading_with_zscore(stock1, stock2)

    # Plotear los resultados
    st.subheader(f"Z-score and Buy Signals for {ticker1} and {ticker2} (Last 6 Months)")

    plt.figure(figsize=(10, 6))
    plt.plot(stock1.index, zscore, label=f'Z-score {ticker1}-{ticker2}')
    plt.plot(stock1.index, np.where(buy_stock1_signals, zscore, np.nan), '^', markersize=10, color='g', lw=0, label=f'Buy {ticker1}')
    plt.plot(stock1.index, np.where(buy_stock2_signals, zscore, np.nan), 'v', markersize=10, color='b', lw=0, label=f'Buy {ticker2}')
    plt.axhline(1, color='gray', linestyle='--', label='Upper Threshold (1)')
    plt.axhline(-1, color='gray', linestyle='--', label='Lower Threshold (-1)')
    plt.axhline(0, color='black', linestyle='-', label='Mean (0)')
    plt.legend(loc='best')
    plt.title(f'Pair Trading {ticker1} vs {ticker2} (Z-score) - Last 6 Months')
    plt.xticks(rotation=45)  # Rotar las etiquetas de las fechas en el eje X
    plt.tight_layout()  # Asegurarnos de que no se corten las etiquetas
    st.pyplot(plt)
