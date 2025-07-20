import numpy as np

def backtest(df):
    df['Strategy_Return'] = df['Position'] * df['Return']
    df['Cum_Strategy'] = (1 + df['Strategy_Return']).cumprod()
    df['Cum_Buy_Hold'] = (1 + df['Return']).cumprod()

    total_strategy_return = df['Cum_Strategy'].iloc[-1] - 1
    total_buy_hold_return = df['Cum_Buy_Hold'].iloc[-1] - 1
    cagr = (df['Cum_Strategy'].iloc[-1]) ** (252 / len(df)) - 1
    sharpe = (df['Strategy_Return'].mean() / df['Strategy_Return'].std()) * np.sqrt(252)
    max_drawdown = (df['Cum_Strategy'] / df['Cum_Strategy'].cummax() - 1).min()

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
