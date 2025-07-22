import matplotlib.pyplot as plt
import os

def plot_returns(df, ticker, short_window, long_window, start, end, metrics, strategy_name="MA", extra_param=None):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Cum_Buy_Hold'], label='Buy & Hold', color='blue', linewidth=2)
    plt.plot(df.index, df['Cum_Strategy'], label='Strategy', color='orange', linewidth=2)

    # Buy and Sell Signals
    plt.scatter(df[df['buy_signal']].index, df.loc[df['buy_signal'], 'Cum_Strategy'],
                marker='^', color='green', label='Buy Signal', s=100, alpha=0.8)
    plt.scatter(df[df['sell_signal']].index, df.loc[df['sell_signal'], 'Cum_Strategy'],
                marker='v', color='red', label='Sell Signal', s=100, alpha=0.8)

    # Chart title
    plt.title(f'{ticker} - {strategy_name} Strategy vs Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Metrics Box
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

    # Save file
    folder = os.path.join("assets", ticker)
    os.makedirs(folder, exist_ok=True)

    # Smart naming
    if strategy_name == "MA":
        file_name = f"MA{short_window}-{long_window}_{ticker}_{start}_{end}.png"
    elif strategy_name == "RSI":
        file_name = f"RSI{extra_param}_{ticker}_{start}_{end}.png"
    else:
        file_name = f"{strategy_name}_{ticker}_{start}_{end}.png"

    file_path = os.path.join(folder, file_name)
    plt.savefig(file_path)
    print(f"Plot saved as {file_path}")
