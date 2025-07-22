import pandas as pd

def compute_rsi(df, period):
    delta = df['Close'].diff() #Difference between Close each day
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def add_signals(df, rsi_period):
    df = compute_rsi(df, rsi_period)
    df['Signal'] = 0
    df.loc[df['RSI'] < 30, 'Signal'] = 1  # Buy when RSI < 30
    df.loc[df['RSI'] > 70, 'Signal'] = 0  # Sell when RSI > 70
    df['Position'] = df['Signal'].shift(1)
    df['buy_signal'] = ((df['Signal'] == 1) & (df['Position'] == 0))
    df['sell_signal'] = ((df['Signal'] == 0) & (df['Position'] == 1))
    return df