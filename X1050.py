import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

## Load stock data
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

## print(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))

## Actual backtest
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
## backtest(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))

## Plotting
def plot_returns(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Cum_Buy_Hold'], label='Buy & Hold')
    plt.plot(df['Cum_Strategy'], label='Strategy')
    plt.title(f'{ticker} - Strategy vs Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    folder = "assets"
    os.makedirs(folder, exist_ok=True)
    file_name = f"X1050 vs buy_hold - {ticker}.png"
    file_path = os.path.join(folder, file_name)
    plt.savefig(file_path)
    print(f"Plot saved as X1050 vs buy_hold - {ticker}.png")


## Main execution
def main():
    while True:
        try:
            ticker = input("Enter a stock ticker: ").strip().upper() #the strip and upper makes input cleaner btw
            if not ticker.isalpha():
                raise ValueError("Ticker needs to be letter!")
            start = input("Enter a start date (YYYY-MM-DD):").strip() #Don't need upper, it's date
            end = input("Enter a end date (YYYY-MM-DD):").strip() #You too
            break
        except ValueError:
            print("Invalid input! Try again!") #Lowk might not need this
    df = download_data(ticker, start, end)
    if df.empty:
        print("No data have found for the given ticker.")
        return
    df = add_signals(df)
    df = backtest(df)   
    plot_returns(df, ticker)

if __name__ == "__main__":
    main()
