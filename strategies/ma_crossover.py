import pandas as pd

def add_signals(df, short_window, long_window):
    df['MA_Short'] = df['Close'].rolling(short_window).mean()
    df['MA_Long'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = 0
    df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1
    df['Position'] = df['Signal'].shift(1)
    df['buy_signal'] = ((df['Signal'] == 1) & (df['Position'] == 0))
    df['sell_signal'] = ((df['Signal'] == 0) & (df['Position'] == 1))
    return df