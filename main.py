from core.data_loader import download_data
from core.backtester import backtest
from core.plotter import plot_returns
from core.utils import validate_date
from strategies.ma_crossover import add_signals

def main():
    while True:
        try:
            ticker = input("Enter a stock ticker: ").strip().upper()
            if not ticker.isalpha():
                raise ValueError("Ticker must contain only letters.")
            start = input("Enter a start date (YYYY-MM-DD):").strip()
            end = input("Enter an end date (YYYY-MM-DD):").strip()
            if not validate_date(start) or not validate_date(end):
                raise ValueError("Dates must be in YYYY-MM-DD format.")

            short_window = int(input("Enter short moving average window:"))
            long_window = int(input("Enter long moving average window:"))
            if short_window <= 0 or long_window <= 0:
                raise ValueError("Window must be positive integers.")
            if short_window >= long_window:
                raise ValueError("Long window must be greater than short window.")
            break
        except ValueError as e:
            print(f"Invalid input! {e}")

    df = download_data(ticker, start, end)
    if df.empty:
        print("No data found for the given ticker.")
        return

    df = add_signals(df, short_window, long_window)
    metrics = backtest(df)
    plot_returns(df, ticker, short_window, long_window, start, end, metrics)

if __name__ == "__main__":
    main()