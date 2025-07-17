import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Load stock data
def download_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end) #open, high, low, close, adj close, volume
    df['Return'] = df['Close'].pct_change()
    return df
## print(download_data("AAPL","2019-01-01", "2024-01-01")) 

def add_signals(df, short_window=10, long_window=50):
    df['MA_Short'] = df['Close'].rolling(short_window).mean()
    df['MA_Long'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = 0
    df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1 # buy signal
    df['Position'] = df['Signal'].shift(1) #Realistic buy, you won't be able to buy right away
    return df

## print(add_signals(download_data("AAPL", "1985-05-19", "1992-04-09")))