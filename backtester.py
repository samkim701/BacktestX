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

##print(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))

##Actual backtest
def backtest(df):
    df['Strategy_Return'] = df['Position'] * df['Return'] # Remember, the return could be negative when we have position
    df['Cum_Strategy'] = (1 + df['Strategy_Return']).cumprod() #cumprod is cumulative product. Ex: [1,2,3,4] = [1,2,6,24] 
    df['Cum_Buy_Hold'] = (1 + df['Return']).cumprod()
    total_strategy_return = df['Cum_Strategy'].iloc[-1] - 1
    total_buy_hold_return = df['Cum_Buy_Hold'].iloc[-1] - 1
    cagr = (df['Cum_Strategy'].iloc[-1]) ** (252 / len(df)) - 1 #I can only trade 252 days a year
    sharpe = (df['Strategy_Return'].mean() / df['Strategy_Return'].std()) * np.sqrt(252) #Sharpe Ratio (Standard version of the risk-return ratio)
    max_drawdown = (df['Cum_Strategy'] / df['Cum_Strategy'].cummax() - 1).min() #Shows the worst pain an investor would experience, cummax() : gives the running maximum value 
    print(f"Total Strategy Return: {total_strategy_return:.2%}")
    print(f"Total Buy Hold Return: {total_buy_hold_return:.2%}")
    print(f"CAGR: {cagr:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    
    return df

backtest(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))


