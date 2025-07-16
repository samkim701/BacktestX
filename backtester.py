import yfinance as yf 
import pandas as pd

stock_appl = yf.download("AAPL")
print(stock_appl)