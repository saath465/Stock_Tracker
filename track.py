#import modules
import pandas as pd
import yfinance as yf
import yahoofinancials as YahooFinancials

#retrieve the basic data for a stock

st_data = yf.Ticker("MSFT")
stock_data = yf.download('AAPL', start='2022-04-01', end='2022-04-13', progress=False)

#print the data found
print(stock_data.tail())
print(st_data.get_dividends())