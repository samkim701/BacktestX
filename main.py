from core.data_loader import download_data
from core.backtester import backtest
from core.plotter import plot_returns
from core.utils import validate_date
from strategies.ma_crossover import add_signals as ma_add_signals
from strategies.rsi_strategy import add_signals as rsi_add_signals

def main():
    print("\nSelect a strategy:")
    print("1. Moving Average Crossover")
    print("2. RSI Strategy")

    # Choose strategy
    while True:
        try:
            strategy_choice = int(input("Enter your choice (1 or 2): ").strip())
            if strategy_choice not in [1, 2]:
                raise ValueError("Choice must be 1 or 2.")
            break
        except ValueError as e:
            print(f"Invalid input! {e}")

    # Common inputs
    while True:
        try:
            ticker = input("\nEnter a stock ticker: ").strip().upper()
            if not ticker.isalpha():
                raise ValueError("Ticker must contain only letters.")

            start = input("Enter a start date (YYYY-MM-DD): ").strip()
            end = input("Enter an end date (YYYY-MM-DD): ").strip()
            if not validate_date(start) or not validate_date(end):
                raise ValueError("Dates must be in YYYY-MM-DD format.")
            break
        except ValueError as e:
            print(f"Invalid input! {e}")

    # Strategy-specific inputs
    short_window, long_window, rsi_period = None, None, None

    if strategy_choice == 1:
        # Moving Average Crossover
        while True:
            try:
                short_window = int(input("Enter short moving average window: ").strip())
                long_window = int(input("Enter long moving average window: ").strip())
                if short_window <= 0 or long_window <= 0:
                    raise ValueError("Windows must be positive integers.")
                if short_window >= long_window:
                    raise ValueError("Long window must be greater than short window.")
                break
            except ValueError as e:
                print(f"Invalid input! {e}")

    elif strategy_choice == 2:
        # RSI Strategy
        while True:
            try:
                rsi_input = input("Enter RSI period (default = 14): ").strip()
                rsi_period = 14 if rsi_input == "" else int(rsi_input)
                if rsi_period <= 0:
                    raise ValueError("RSI period must be a positive integer.")
                break
            except ValueError as e:
                print(f"Invalid input! {e}")

    # Download stock data
    print("\nDownloading data...")
    df = download_data(ticker, start, end)
    if df.empty:
        print("No data found for the given ticker and date range.")
        return

    # Apply selected strategy
    print("Applying strategy...")
    if strategy_choice == 1:
        df = ma_add_signals(df, short_window, long_window)
    elif strategy_choice == 2:
        df = rsi_add_signals(df, rsi_period)

    # Backtest and plot
    print("Running backtest...")
    metrics = backtest(df)

    # For plot naming consistency
    short = short_window if short_window else 'NA'
    long = long_window if long_window else 'NA'

    print("Saving plot...")
    if strategy_choice == 1:
        plot_returns(df, ticker, short, long, start, end, metrics, strategy_name="MA")
    elif strategy_choice == 2:
        plot_returns(df, ticker, 'NA', 'NA', start, end, metrics, strategy_name="RSI", extra_param=rsi_period)

if __name__ == "__main__":
    main()
