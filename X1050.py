import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

## Load stock data
def download_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end) #open, high, low, close, adj close, volume
    df['Return'] = df['Close'].pct_change()
    return df
## print(download_data("AAPL","2019-01-01", "2024-01-01")) 

def add_signals(df, short_window, long_window): 
    df['MA_Short'] = df['Close'].rolling(short_window).mean()
    df['MA_Long'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = 0
    df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1 # buy signal
    df['Position'] = df['Signal'].shift(1) #Realistic buy, you won't be able to buy right away
    df['buy_signal'] = ((df['Signal'] == 1) & (df['Position'] == 0))
    df['sell_signal'] = ((df['Signal'] == 0) & (df['Position'] == 1))
    return df

## print(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))

## Actual backtest & matrics
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
    
    return {
        'total_strategy_return': total_strategy_return,
        'total_buy_hold_return': total_buy_hold_return,
        'cagr': cagr,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown
    }
## backtest(add_signals(download_data("AAPL", "2018-01-01", "2024-01-01")))

## Plotting
def plot_returns(df, ticker, short_window, long_window, start, end, metrics):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Cum_Buy_Hold'], label='Buy & Hold', color='blue', linewidth=2)
    plt.plot(df.index, df['Cum_Strategy'], label='Strategy', color='orange', linewidth=2)
    # Buy signals
    plt.scatter(df[df['buy_signal']].index, df.loc[df['buy_signal'], 'Cum_Strategy'],
        marker='^', color='green', label='Buy Signal', s=100, alpha=0.8)
    # Sell signals 
    plt.scatter(df[df['sell_signal']].index, df.loc[df['sell_signal'], 'Cum_Strategy'],
        marker='v', color='red', label='Sell Signal', s=100, alpha=0.8)
    #Title and labels
    plt.title(f'{ticker} - Strategy vs Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #Add Annotation with metrics
    metrics_text = "\n".join([
        f"Strategy Return: {metrics['total_strategy_return']:.2%}",
        f"Buy & Hold: {metrics['total_buy_hold_return']:.2%}",
        f"CAGR: {metrics['cagr']:.2%}",
        f"Sharpe Ratio: {metrics['sharpe']:.2f}",
        f"Max Drawdown: {metrics['max_drawdown']:.2%}"
    ])
    plt.gca().text(0.02, 0.98, metrics_text, transform=plt.gca().transAxes,
                   fontsize=10, verticalalignment='top',
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
    #Save File
    folder = "assets"
    os.makedirs(folder, exist_ok=True)
    file_name = f"{ticker}_X{short_window}-{long_window}_vs_BuyHold_{start}_{end}.png"
    file_path = os.path.join(folder, file_name)
    plt.savefig(file_path)
    print(f"Plot saved as {ticker}_X{short_window}-{long_window}_vs_BuyHold_{start}_{end}.png")


## Main execution
def main():
    while True:
        try:
            ticker = input("Enter a stock ticker: ").strip().upper() #the strip and upper makes input cleaner btw
            if not ticker.isalpha():
                raise ValueError("Ticker needs to be letter!")
            start = input("Enter a start date (YYYY-MM-DD):").strip() #Don't need upper, it's date
            end = input("Enter a end date (YYYY-MM-DD):").strip() #You too
            short_window = int(input("Enter short moving average window:"))
            long_window = int(input("Enter long moving average window:"))
            if short_window <= 0 or long_window <= 0: 
                raise ValueError("Window must be positive integer")
            if short_window >= long_window:
                raise ValueError("Long window must be bigger than Short window")
            break
        except ValueError:
            print("Invalid input! Try again!") #Lowk might not need this
    df = download_data(ticker, start, end)
    if df.empty:
        print("No data have found for the given ticker.")
        return
    df = add_signals(df, short_window, long_window)
    metrics = backtest(df)
    plot_returns(df, ticker, short_window, long_window, start, end, metrics)

if __name__ == "__main__":
    main()
